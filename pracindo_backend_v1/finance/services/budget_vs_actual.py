"""
Perbandingan anggaran dengan realisasi dari ledger.

Anggaran datang dari finance.BudgetLine, realisasi dari
akunting.JurnalDetail. Keduanya bertemu di akun_id — itulah sebabnya
BudgetLine mereferensikan akunting.Akun lewat FK sejak awal, bukan
menyimpan nama akun bebas.

ARAH SELISIH
    Selisih dibaca sesuai tipe akun, bukan dengan satu label seragam.
    Untuk BEBAN, realisasi melebihi anggaran berarti boros. Untuk
    PENDAPATAN, realisasi melebihi target berarti bagus. Memberi satu
    label favorable/unfavorable tanpa melihat tipe akun akan salah
    setengah waktu.

CATATAN
    JurnalDetail tidak menyimpan tanggal maupun entitas — keduanya ada di
    JurnalUmum. Jadi setiap agregasi periodik harus join ke header.
"""
import calendar
from datetime import date
from decimal import Decimal

from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce

F_RP = DecimalField(max_digits=20, decimal_places=2)
D0 = Decimal('0')


def _rentang_bulan(tahun, bulan):
    return (date(tahun, bulan, 1),
            date(tahun, bulan, calendar.monthrange(tahun, bulan)[1]))


def _rentang_tahun(tahun):
    return date(tahun, 1, 1), date(tahun, 12, 31)


def _mutasi_akun(entitas_id, tahun, bulan=None):
    """
    Mutasi bersih per akun dalam satu periode, dihitung sesuai saldo
    normalnya.

    Akun ASET dan BEBAN bersaldo normal debit, jadi mutasinya debit
    dikurangi kredit. Sisanya kebalikannya. Tanpa pembedaan ini,
    realisasi pendapatan akan keluar negatif.
    """
    from akunting.models import JurnalDetail, TipeAkun

    if bulan:
        awal, akhir = _rentang_bulan(tahun, bulan)
    else:
        awal, akhir = _rentang_tahun(tahun)

    baris = (JurnalDetail.objects
             .filter(jurnal__entitas_id=entitas_id,
                     jurnal__tanggal__gte=awal,
                     jurnal__tanggal__lte=akhir)
             .values('akun_id', 'akun__tipe')
             .annotate(
                 debit=Coalesce(Sum('debit'), Value(D0), output_field=F_RP),
                 kredit=Coalesce(Sum('kredit'), Value(D0), output_field=F_RP),
             ))

    saldo_debit = (TipeAkun.ASET, TipeAkun.BEBAN)
    hasil = {}
    for b in baris:
        if b['akun__tipe'] in saldo_debit:
            nilai = b['debit'] - b['kredit']
        else:
            nilai = b['kredit'] - b['debit']
        hasil[b['akun_id']] = nilai
    return hasil


def _arah(tipe, selisih):
    """
    selisih = anggaran - realisasi.

    BEBAN  : selisih positif berarti hemat.
    PENDAPATAN: selisih positif berarti target belum tercapai.
    """
    from akunting.models import TipeAkun

    if selisih == 0:
        return 'PAS'
    if tipe == TipeAkun.PENDAPATAN:
        return 'DI_BAWAH_TARGET' if selisih > 0 else 'DI_ATAS_TARGET'
    return 'HEMAT' if selisih > 0 else 'BOROS'


def budget_vs_actual(budget_id, bulan=None):
    """
    Bandingkan satu Budget dengan realisasi ledger.

    bulan=None membandingkan satu tahun penuh; baris anggaran bulanan
    dijumlahkan per akun. bulan=1..12 membandingkan satu bulan saja, dan
    hanya baris dengan bulan itu atau bulan=0 (anggaran seluruh tahun)
    yang diikutkan.
    """
    from finance.models import Budget

    budget = (Budget.objects.select_related('entitas')
              .prefetch_related('lines__akun')
              .get(pk=budget_id))

    mutasi = _mutasi_akun(budget.entitas_id, budget.tahun, bulan)

    lines = budget.lines.filter(is_active=True)
    if bulan:
        # bulan=0 berarti anggaran untuk seluruh tahun, tetap relevan
        # sebagai pembanding bulanan kalau dibagi rata. Di sini ikut
        # disertakan apa adanya, tidak dibagi dua belas.
        lines = lines.filter(bulan__in=[bulan, 0])

    # Satu akun bisa punya beberapa baris (per bulan), tapi realisasinya
    # satu angka per akun. Jadi anggarannya dijumlahkan dulu supaya
    # realisasi tidak terhitung berkali-kali.
    per_akun = {}
    for line in lines:
        slot = per_akun.setdefault(line.akun_id, {
            'akun_id': line.akun_id,
            'akun_kode': line.akun.kode,
            'akun_nama': line.akun.nama,
            'akun_tipe': line.akun.tipe,
            'anggaran': D0,
            'bulan': [],
        })
        slot['anggaran'] += line.nominal_anggaran
        slot['bulan'].append(line.bulan)

    rincian = []
    for slot in per_akun.values():
        realisasi = mutasi.get(slot['akun_id'], D0)
        selisih = slot['anggaran'] - realisasi
        serapan = ((realisasi / slot['anggaran'] * 100).quantize(Decimal('0.01'))
                   if slot['anggaran'] else None)

        slot['bulan'].sort()
        rincian.append({
            **slot,
            'realisasi': realisasi,
            'selisih': selisih,
            'serapan_persen': serapan,
            'arah': _arah(slot['akun_tipe'], selisih),
        })

    rincian.sort(key=lambda r: r['akun_kode'])

    total_anggaran = sum((r['anggaran'] for r in rincian), D0)
    total_realisasi = sum((r['realisasi'] for r in rincian), D0)

    return {
        'budget_id': budget.id,
        'budget_nama': budget.nama,
        'budget_status': budget.status,
        'entitas_id': budget.entitas_id,
        'entitas_kode': budget.entitas.kode,
        'tahun': budget.tahun,
        'bulan': bulan,
        'rincian': rincian,
        'total': {
            'anggaran': total_anggaran,
            'realisasi': total_realisasi,
            'selisih': total_anggaran - total_realisasi,
            'serapan_persen': ((total_realisasi / total_anggaran * 100)
                               .quantize(Decimal('0.01')) if total_anggaran else None),
        },
        'catatan': [
            'Realisasi dihitung dari jurnal terposting, bukan dari komitmen PO.',
            'Akun yang punya realisasi tapi tidak dianggarkan tidak muncul di sini.',
        ],
    }


def akun_tanpa_anggaran(budget_id, bulan=None):
    """
    Akun yang punya realisasi tapi tidak ada di BudgetLine.

    Berguna untuk menemukan pengeluaran yang lolos dari perencanaan —
    justru yang tidak dianggarkan itu yang sering perlu diperhatikan.
    """
    from akunting.models import Akun, TipeAkun
    from finance.models import Budget

    budget = Budget.objects.select_related('entitas').get(pk=budget_id)
    mutasi = _mutasi_akun(budget.entitas_id, budget.tahun, bulan)
    dianggarkan = set(budget.lines.filter(is_active=True)
                      .values_list('akun_id', flat=True))

    sisa_id = [aid for aid in mutasi if aid not in dianggarkan]
    if not sisa_id:
        return []

    akun = {a.id: a for a in Akun.objects.filter(
        id__in=sisa_id, tipe__in=[TipeAkun.PENDAPATAN, TipeAkun.BEBAN])}

    hasil = [{
        'akun_id': aid,
        'akun_kode': akun[aid].kode,
        'akun_nama': akun[aid].nama,
        'akun_tipe': akun[aid].tipe,
        'realisasi': mutasi[aid],
    } for aid in sisa_id if aid in akun]

    hasil.sort(key=lambda r: r['akun_kode'])
    return hasil