"""
Posisi aset lancar dan rasio likuiditas, dihitung saat diminta.

Tidak menyimpan apa pun. Sebagian besar angka datang dari saldo berjalan
(PoolResource, PoolKemasan, Tangki, sisa_hutang, sisa_piutang) sehingga
biayanya satu query agregat per pos. Hanya kas yang diagregasi dari
ledger.

BATAS YANG PERLU DIKETAHUI
    Barang jadi tidak punya nilai rupiah di sistem ini. StokBarangJadi
    hanya menyimpan qty_unit dan qty_kg, dan tidak ada jalur yang
    menguranginya saat barang terjual. Jadi barang jadi dilaporkan
    sebagai kuantitas saja, TIDAK ikut dijumlahkan ke aset lancar dan
    TIDAK masuk perhitungan rasio. Menaksir nilainya akan membuat total
    aset terlihat lengkap padahal tidak.
"""
from decimal import Decimal

from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce

F_RP = DecimalField(max_digits=20, decimal_places=2)
F_QTY = DecimalField(max_digits=18, decimal_places=3)
D0 = Decimal('0')

# Dari akunting/posting_rules.py hanya ada KAS 1100. Tambahkan kode akun
# bank di sini kalau nanti ada akun terpisah.
KODE_KAS = ['1100']
KODE_BANK = []


def _sum_rp(qs, field):
    return qs.aggregate(t=Coalesce(Sum(field), Value(D0), output_field=F_RP))['t']


def hitung_kas(entitas=None):
    """Saldo kas dari ledger: debit dikurangi kredit pada akun kas/bank."""
    from akunting.models import JurnalDetail

    qs = JurnalDetail.objects.filter(akun__kode__in=KODE_KAS + KODE_BANK)
    if entitas is not None:
        qs = qs.filter(jurnal__entitas_id=entitas)

    agg = qs.aggregate(
        debit=Coalesce(Sum('debit'), Value(D0), output_field=F_RP),
        kredit=Coalesce(Sum('kredit'), Value(D0), output_field=F_RP),
    )
    return agg['debit'] - agg['kredit']


def hitung_piutang(entitas=None):
    from akunting.models import FakturPenjualan

    qs = FakturPenjualan.objects.all()
    if entitas is not None:
        qs = qs.filter(entitas_id=entitas)
    return _sum_rp(qs, 'sisa_piutang')


def hitung_hutang(entitas=None):
    from akunting.models import FakturPembelian

    qs = FakturPembelian.objects.all()
    if entitas is not None:
        qs = qs.filter(entitas_id=entitas)
    return _sum_rp(qs, 'sisa_hutang')


def hitung_persediaan():
    """Pool bahan, pool kemasan, dan WIP di tanki.

    Ketiganya milik bersama tanpa dimensi entitas, jadi tidak bisa
    dipecah per PT/CV. Hak masing-masing entitas atas nilai ini ada di
    SaldoEntitas, bukan di sini."""
    from inventory.models import PoolResource, PoolKemasan
    from produksi.models import Tangki

    pool = _sum_rp(PoolResource.objects.all(), 'nilai')
    kemasan = _sum_rp(PoolKemasan.objects.all(), 'nilai')
    wip = _sum_rp(Tangki.objects.all(), 'saldo_nilai')

    return {
        'pool_bahan': pool,
        'pool_kemasan': kemasan,
        'wip_tanki': wip,
        'total': pool + kemasan + wip,
    }


def hitung_barang_jadi(entitas=None):
    """Kuantitas saja. Nilai rupiahnya tidak dilacak sistem."""
    from inventory.models import StokBarangJadi

    qs = StokBarangJadi.objects.all()
    if entitas is not None:
        qs = qs.filter(entitas_id=entitas)

    agg = qs.aggregate(
        unit=Coalesce(Sum('qty_unit'), Value(0)),
        kg=Coalesce(Sum('qty_kg'), Value(D0), output_field=F_QTY),
    )
    return {
        'qty_unit': agg['unit'],
        'qty_kg': agg['kg'],
        'nilai': None,
        'catatan': 'Nilai barang jadi belum dilacak sistem.',
    }


def hitung_hak_entitas(entitas=None):
    """Hak entitas atas pool dan WIP, dari SaldoEntitas.

    Totalnya seharusnya sama dengan persediaan (pool + kemasan + WIP).
    Kalau berbeda, itu selisih yang assert_invarian() hitung tapi tidak
    pernah laporkan."""
    from inventory.models import SaldoEntitas

    qs = SaldoEntitas.objects.select_related('entitas')
    if entitas is not None:
        qs = qs.filter(entitas_id=entitas)

    rincian = [{
        'entitas_id': s.entitas_id,
        'entitas_kode': s.entitas.kode,
        'saldo': s.saldo,
    } for s in qs]

    return {'rincian': rincian, 'total': sum((s['saldo'] for s in rincian), D0)}


def _rasio(pembilang, penyebut):
    """None kalau tidak ada kewajiban: rasio tak hingga bukan angka yang
    berguna, dan lebih jujur daripada menampilkan 0."""
    if penyebut is None or penyebut == 0:
        return None
    return (pembilang / penyebut).quantize(Decimal('0.01'))


def posisi_likuiditas(entitas=None):
    """Satu payload untuk dashboard. entitas=None berarti konsolidasi.

    Catatan: persediaan selalu global (pool dan tanki milik bersama),
    jadi saat difilter per entitas, kas/piutang/hutang ikut terfilter
    tapi persediaan tidak."""
    kas = hitung_kas(entitas)
    piutang = hitung_piutang(entitas)
    hutang = hitung_hutang(entitas)
    persediaan = hitung_persediaan()

    aset_lancar = kas + piutang + persediaan['total']
    aset_cepat = kas + piutang

    return {
        'entitas': entitas,
        'kas': kas,
        'piutang': piutang,
        'persediaan': persediaan,
        'barang_jadi': hitung_barang_jadi(entitas),
        'hak_entitas': hitung_hak_entitas(entitas),
        'aset_lancar': aset_lancar,
        'kewajiban_lancar': hutang,
        'modal_kerja': aset_lancar - hutang,
        'rasio': {
            'current': _rasio(aset_lancar, hutang),
            'quick': _rasio(aset_cepat, hutang),
            'cash': _rasio(kas, hutang),
        },
        'catatan': [
            'Persediaan (pool, kemasan, WIP) global lintas entitas.',
            'Barang jadi tidak masuk aset lancar karena nilainya belum dilacak.',
        ],
    }