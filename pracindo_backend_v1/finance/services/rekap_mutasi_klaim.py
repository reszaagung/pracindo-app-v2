"""
Rekap mutasi klaim per entitas per bulan.

Sumber: inventory.MutasiKlaim untuk pergerakan, inventory.SaldoEntitas
untuk saldo akhir. Arah +1 = setor, -1 = tarik.

saldo_akhir diambil dari SaldoEntitas saat ini, bukan direkonstruksi.
Untuk bulan berjalan itu benar; untuk bulan lampau hanya valid kalau
rekap digenerate di akhir bulan itu lalu dibekukan.
"""
import calendar
from datetime import date
from decimal import Decimal

from django.db import transaction
from django.db.models import Sum, Count, Q, Value, DecimalField
from django.db.models.functions import Coalesce

from inventory.models import MutasiKlaim, SaldoEntitas

from finance.models import RekapMutasiKlaim

F_RP = DecimalField(max_digits=20, decimal_places=2)
F_QTY = DecimalField(max_digits=18, decimal_places=3)
D0 = Decimal('0')


def _rentang(tahun, bulan):
    return (date(tahun, bulan, 1),
            date(tahun, bulan, calendar.monthrange(tahun, bulan)[1]))


def hitung_rekap_klaim(tahun, bulan, entitas=None):
    """Hitung tanpa menyimpan. Mengembalikan satu dict per entitas."""
    awal, akhir = _rentang(tahun, bulan)

    qs = MutasiKlaim.objects.filter(waktu__date__gte=awal, waktu__date__lte=akhir)
    if entitas is not None:
        qs = qs.filter(entitas_id=entitas)

    agregat = (qs.values('entitas_id')
                 .annotate(
                     jumlah_mutasi=Count('id'),
                     qty_setor=Coalesce(Sum('qty_kg', filter=Q(arah=1)),
                                        Value(D0), output_field=F_QTY),
                     nilai_setor=Coalesce(Sum('nilai', filter=Q(arah=1)),
                                          Value(D0), output_field=F_RP),
                     qty_tarik=Coalesce(Sum('qty_kg', filter=Q(arah=-1)),
                                        Value(D0), output_field=F_QTY),
                     nilai_tarik=Coalesce(Sum('nilai', filter=Q(arah=-1)),
                                          Value(D0), output_field=F_RP),
                 )
                 .order_by('entitas__kode'))

    saldo = {s.entitas_id: s for s in SaldoEntitas.objects.all()}

    hasil = []
    for b in agregat:
        se = saldo.get(b['entitas_id'])
        hasil.append({
            'entitas_id': b['entitas_id'],
            'jumlah_mutasi': b['jumlah_mutasi'],
            'qty_setor': b['qty_setor'],
            'nilai_setor': b['nilai_setor'],
            'qty_tarik': b['qty_tarik'],
            'nilai_tarik': b['nilai_tarik'],
            'saldo_akhir': se.saldo if se else D0,
            'qty_setor_kumulatif': se.qty_setor if se else D0,
            'qty_tarik_kumulatif': se.qty_tarik if se else D0,
        })
    return hasil


@transaction.atomic
def generate_rekap_klaim(tahun, bulan, user, entitas=None):
    """Simpan/perbarui baris rekap. Baris beku dilewati."""
    if user is None:
        raise ValueError('generate_rekap_klaim butuh user.')

    hasil = []
    for data in hitung_rekap_klaim(tahun, bulan, entitas):
        entitas_id = data.pop('entitas_id')
        rekap = RekapMutasiKlaim.objects.filter(
            entitas_id=entitas_id, tahun=tahun, bulan=bulan,
        ).first()

        if rekap and rekap.dibekukan:
            continue

        if rekap:
            for k, v in data.items():
                setattr(rekap, k, v)
            rekap.save()
        else:
            rekap = RekapMutasiKlaim.objects.create(
                entitas_id=entitas_id, tahun=tahun, bulan=bulan,
                dibuat_oleh=user, **data,
            )
        hasil.append(rekap)
    return hasil
