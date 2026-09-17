"""
Posisi aset lancar, hak antar-grup, dan rasio likuiditas.

Dihitung saat diminta, tidak menyimpan apa pun.

MODEL POOL PATUNGAN
    Bahan yang dibeli entitas manapun langsung masuk pool bersama tanpa
    pemilik. Kepemilikan baru dihitung saat klaim (packing): entitas yang
    menarik lebih banyak dari setorannya jadi berhutang kepada yang
    menarik lebih sedikit.

    SaldoEntitas.saldo positif = punya klaim atas pool.
    SaldoEntitas.saldo negatif = berhutang ke entitas/grup lain.

    Hutang antar-grup ini TIDAK ada di ledger akunting — tidak masuk
    FakturPembelian maupun akun 2100. Dia hidup hanya di SaldoEntitas,
    jadi harus dilaporkan terpisah supaya tidak tak terlihat.

BATAS
    Barang jadi tidak punya nilai rupiah di sistem ini. StokBarangJadi
    hanya menyimpan qty_unit dan qty_kg, dan tidak ada jalur yang
    menguranginya saat barang terjual. Jadi dilaporkan sebagai kuantitas
    saja, TIDAK masuk aset lancar dan TIDAK masuk rasio.

    Pool dan tanki tidak punya dimensi grup — memang begitu desainnya.
    Jadi "nilai fisik milik grup X" tidak ada; yang ada adalah hak grup X
    atas pool bersama.
"""
from decimal import Decimal

from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce

F_RP = DecimalField(max_digits=20, decimal_places=2)
F_QTY = DecimalField(max_digits=18, decimal_places=3)
D0 = Decimal('0')
TOL_RP = Decimal('0.01')

# Dari akunting/posting_rules.py hanya ada KAS 1100. Tambahkan kode akun
# bank di sini kalau nanti ada akun terpisah.
KODE_KAS = ['1100']
KODE_BANK = []


def _sum_rp(qs, field):
    return qs.aggregate(t=Coalesce(Sum(field), Value(D0), output_field=F_RP))['t']


# =========================================================
# POS-POS DARI LEDGER DAN FAKTUR
# =========================================================

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
    """Hutang ke supplier dari faktur pembelian. Tidak termasuk hutang
    antar-grup atas pool — itu ada di hitung_hak_per_grup()."""
    from akunting.models import FakturPembelian

    qs = FakturPembelian.objects.all()
    if entitas is not None:
        qs = qs.filter(entitas_id=entitas)
    return _sum_rp(qs, 'sisa_hutang')


# =========================================================
# NILAI FISIK (GLOBAL, TANPA GRUP)
# =========================================================

def hitung_persediaan():
    """Pool bahan, pool kemasan, dan WIP di tanki.

    Selalu global: pool dan tanki milik bersama tanpa dimensi entitas
    maupun grup. Pembagian haknya ada di hitung_hak_per_grup()."""
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


# =========================================================
# HAK DAN HUTANG ANTAR-GRUP
# =========================================================

def _status(saldo):
    if saldo > 0:
        return 'KLAIM'
    if saldo < 0:
        return 'HUTANG'
    return 'IMPAS'


def hitung_hak_per_grup(grup=None):
    """Hak dan hutang per grup bahan atas pool bersama.

    Saldo positif berarti grup itu menyetor lebih banyak daripada yang
    ditarik, jadi punya klaim. Saldo negatif berarti sudah menarik
    melebihi setoran, jadi berhutang ke grup lain.

    Total klaim dikurangi total hutang harus sama dengan nilai fisik
    (pool + WIP). Itu invarian inti sistem ini."""
    from inventory.models import SaldoEntitas

    qs = SaldoEntitas.objects.select_related('entitas', 'entitas__grup_bahan')
    if grup is not None:
        qs = qs.filter(entitas__grup_bahan_id=grup)

    per_grup = {}
    for s in qs:
        g = s.entitas.grup_bahan
        baris = per_grup.setdefault(g.id, {
            'grup_id': g.id,
            'grup_kode': g.kode,
            'grup_nama': g.nama,
            'saldo': D0,
            'klaim': D0,
            'hutang': D0,
            'entitas': [],
        })
        baris['saldo'] += s.saldo
        if s.saldo > 0:
            baris['klaim'] += s.saldo
        elif s.saldo < 0:
            baris['hutang'] += -s.saldo
        baris['entitas'].append({
            'entitas_id': s.entitas_id,
            'entitas_kode': s.entitas.kode,
            'saldo': s.saldo,
            'status': _status(s.saldo),
        })

    rincian = sorted(per_grup.values(), key=lambda b: b['grup_kode'])
    for b in rincian:
        b['status'] = _status(b['saldo'])
        b['entitas'].sort(key=lambda e: e['entitas_kode'])

    return {
        'rincian': rincian,
        'total_saldo': sum((b['saldo'] for b in rincian), D0),
        'total_klaim': sum((b['klaim'] for b in rincian), D0),
        'total_hutang': sum((b['hutang'] for b in rincian), D0),
    }


def hitung_hak_entitas(entitas=None):
    """Daftar datar per entitas, tanpa pengelompokan grup."""
    from inventory.models import SaldoEntitas

    qs = SaldoEntitas.objects.select_related('entitas')
    if entitas is not None:
        qs = qs.filter(entitas_id=entitas)

    rincian = [{
        'entitas_id': s.entitas_id,
        'entitas_kode': s.entitas.kode,
        'saldo': s.saldo,
        'status': _status(s.saldo),
    } for s in qs]

    return {'rincian': rincian, 'total': sum((r['saldo'] for r in rincian), D0)}


def periksa_invarian():
    """Hak entitas harus sama dengan nilai fisik pool dan WIP.

    assert_invarian() di inventory menghitung selisih ini tapi tidak
    pernah memasukkannya ke daftar catatan, jadi tidak pernah gagal.
    Di sini selisihnya dilaporkan apa adanya."""
    from inventory.models import SaldoEntitas

    hak = _sum_rp(SaldoEntitas.objects.all(), 'saldo')
    fisik = hitung_persediaan()['total']
    selisih = hak - fisik

    return {
        'hak': hak,
        'fisik': fisik,
        'selisih': selisih,
        'cocok': abs(selisih) <= TOL_RP,
    }


# =========================================================
# RASIO DAN PAYLOAD DASHBOARD
# =========================================================

def _rasio(pembilang, penyebut):
    """None kalau tidak ada kewajiban: rasio tak hingga bukan angka yang
    berguna, dan lebih jujur daripada menampilkan 0."""
    if penyebut is None or penyebut == 0:
        return None
    return (pembilang / penyebut).quantize(Decimal('0.01'))


def posisi_likuiditas(entitas=None, grup=None):
    """Satu payload untuk dashboard.

    entitas=None dan grup=None berarti konsolidasi.

    Catatan: persediaan selalu global, jadi saat difilter per entitas,
    kas/piutang/hutang ikut terfilter tapi persediaan tidak."""
    kas = hitung_kas(entitas)
    piutang = hitung_piutang(entitas)
    hutang_supplier = hitung_hutang(entitas)
    persediaan = hitung_persediaan()
    hak = hitung_hak_per_grup(grup)

    # Hutang antar-grup adalah kewajiban nyata, tapi tidak pernah masuk
    # ledger. Dipisah supaya terlihat, bukan disembunyikan di total.
    hutang_antar_grup = hak['total_hutang']
    kewajiban = hutang_supplier + hutang_antar_grup

    aset_lancar = kas + piutang + persediaan['total']
    aset_cepat = kas + piutang

    return {
        'entitas': entitas,
        'grup': grup,
        'kas': kas,
        'piutang': piutang,
        'persediaan': persediaan,
        'barang_jadi': hitung_barang_jadi(entitas),
        'hak_per_grup': hak,
        'invarian': periksa_invarian(),
        'aset_lancar': aset_lancar,
        'kewajiban': {
            'supplier': hutang_supplier,
            'antar_grup': hutang_antar_grup,
            'total': kewajiban,
        },
        'modal_kerja': aset_lancar - kewajiban,
        'rasio': {
            'current': _rasio(aset_lancar, kewajiban),
            'quick': _rasio(aset_cepat, kewajiban),
            'cash': _rasio(kas, kewajiban),
        },
        'catatan': [
            'Pool dan WIP global lintas grup; yang dibagi adalah haknya, bukan barangnya.',
            'Hutang antar-grup tidak ada di ledger akunting, hanya di SaldoEntitas.',
            'Barang jadi tidak masuk aset lancar karena nilainya belum dilacak.',
        ],
    }