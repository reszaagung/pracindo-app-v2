"""
Financial movement — daftar mutasi keuangan dari ledger.

Bukan tabel. Dibaca langsung dari akunting.JurnalDetail setiap kali
diminta, jadi transaksi yang baru diposting langsung terlihat tanpa
proses apa pun di antaranya.

Satu baris di sini adalah satu baris jurnal: akun apa, bergerak ke arah
mana, berapa. Kepala dokumennya (nomor, tanggal, entitas, kejadian)
ikut dibawa supaya bisa ditelusuri ke sumbernya.
"""
import calendar
from datetime import date
from decimal import Decimal

from django.db.models import Sum, Value, DecimalField, Q
from django.db.models.functions import Coalesce

F_RP = DecimalField(max_digits=20, decimal_places=2)
D0 = Decimal('0')

BATAS_DEFAULT = 100
BATAS_MAKS = 1000


def _rentang(tahun, bulan=None):
    if bulan:
        return (date(tahun, bulan, 1),
                date(tahun, bulan, calendar.monthrange(tahun, bulan)[1]))
    return date(tahun, 1, 1), date(tahun, 12, 31)


def _queryset(entitas=None, tahun=None, bulan=None, akun=None,
              tipe_akun=None, kejadian=None, dari=None, sampai=None):
    from akunting.models import JurnalDetail

    qs = (JurnalDetail.objects
          .select_related('jurnal', 'jurnal__entitas', 'akun')
          .order_by('-jurnal__tanggal', '-jurnal__id', 'id'))

    if entitas:
        qs = qs.filter(jurnal__entitas_id=entitas)
    if akun:
        qs = qs.filter(akun_id=akun)
    if tipe_akun:
        qs = qs.filter(akun__tipe=tipe_akun)
    if kejadian:
        qs = qs.filter(jurnal__kejadian=kejadian)

    # Rentang eksplisit menang atas tahun/bulan.
    if dari:
        qs = qs.filter(jurnal__tanggal__gte=dari)
    if sampai:
        qs = qs.filter(jurnal__tanggal__lte=sampai)
    if not dari and not sampai and tahun:
        awal, akhir = _rentang(tahun, bulan)
        qs = qs.filter(jurnal__tanggal__gte=awal, jurnal__tanggal__lte=akhir)

    return qs


def financial_movement(entitas=None, tahun=None, bulan=None, akun=None,
                       tipe_akun=None, kejadian=None, dari=None, sampai=None,
                       batas=BATAS_DEFAULT):
    """
    Daftar mutasi terbaru lebih dulu.

    Tanpa filter tanggal sama sekali, yang dikembalikan adalah mutasi
    terakhir sebanyak `batas` — cocok untuk panel "aktivitas terkini" di
    dashboard.
    """
    batas = min(int(batas or BATAS_DEFAULT), BATAS_MAKS)
    qs = _queryset(entitas, tahun, bulan, akun, tipe_akun, kejadian, dari, sampai)

    total = qs.aggregate(
        debit=Coalesce(Sum('debit'), Value(D0), output_field=F_RP),
        kredit=Coalesce(Sum('kredit'), Value(D0), output_field=F_RP),
    )

    baris = [{
        'id': b.id,
        'tanggal': b.jurnal.tanggal,
        'nomor': b.jurnal.nomor,
        'kejadian': b.jurnal.kejadian,
        'referensi': b.jurnal.referensi,
        'entitas_id': b.jurnal.entitas_id,
        'entitas_kode': b.jurnal.entitas.kode,
        'akun_id': b.akun_id,
        'akun_kode': b.akun.kode,
        'akun_nama': b.akun.nama,
        'akun_tipe': b.akun.tipe,
        'debit': b.debit,
        'kredit': b.kredit,
        'keterangan': b.keterangan or b.jurnal.keterangan,
    } for b in qs[:batas]]

    return {
        'rincian': baris,
        'jumlah_ditampilkan': len(baris),
        'total_baris': qs.count(),
        'total': {
            'debit': total['debit'],
            'kredit': total['kredit'],
            # Selisih harus nol: setiap jurnal seimbang, dijaga trigger
            # database. Kalau tidak nol, ada yang salah di luar dugaan.
            'selisih': total['debit'] - total['kredit'],
        },
        'batas': batas,
    }


def ringkasan_per_akun(entitas=None, tahun=None, bulan=None, tipe_akun=None):
    """
    Mutasi dijumlahkan per akun, bukan per baris. Untuk melihat akun mana
    yang paling banyak bergerak dalam satu periode.

    Nilai bersih dihitung sesuai saldo normal: akun ASET dan BEBAN
    bersaldo debit, sisanya kredit.
    """
    from akunting.models import TipeAkun

    qs = _queryset(entitas, tahun, bulan, tipe_akun=tipe_akun)

    agregat = (qs.values('akun_id', 'akun__kode', 'akun__nama', 'akun__tipe')
                 .annotate(
                     debit=Coalesce(Sum('debit'), Value(D0), output_field=F_RP),
                     kredit=Coalesce(Sum('kredit'), Value(D0), output_field=F_RP),
                 )
                 .order_by('akun__kode'))

    saldo_debit = (TipeAkun.ASET, TipeAkun.BEBAN)
    rincian = []
    for a in agregat:
        if a['akun__tipe'] in saldo_debit:
            bersih = a['debit'] - a['kredit']
        else:
            bersih = a['kredit'] - a['debit']
        rincian.append({
            'akun_id': a['akun_id'],
            'akun_kode': a['akun__kode'],
            'akun_nama': a['akun__nama'],
            'akun_tipe': a['akun__tipe'],
            'debit': a['debit'],
            'kredit': a['kredit'],
            'bersih': bersih,
        })

    return {
        'rincian': rincian,
        'total': {
            'debit': sum((r['debit'] for r in rincian), D0),
            'kredit': sum((r['kredit'] for r in rincian), D0),
        },
    }