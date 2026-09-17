"""
Rekap mutasi produksi per bulan. Global, tanpa entitas.

wip_akhir/pool_akhir adalah saldo SAAT INI, bukan saldo akhir bulan yang
direkonstruksi. Untuk bulan berjalan itu benar; untuk bulan lampau hanya
valid kalau rekap digenerate di akhir bulan lalu dibekukan.
"""
import calendar
from datetime import date
from decimal import Decimal

from django.db import transaction
from django.db.models import Sum, Count, Q, Value, DecimalField
from django.db.models.functions import Coalesce

from produksi.models import Batch, Tangki, TipeProses
from inventory.models import Packing, PoolResource, PoolKemasan, StatusDokumen

from finance.models import RekapMutasiProduksi

F_RP = DecimalField(max_digits=20, decimal_places=2)
F_QTY = DecimalField(max_digits=18, decimal_places=3)
D0 = Decimal('0')


def _rentang(tahun, bulan):
    return (date(tahun, bulan, 1),
            date(tahun, bulan, calendar.monthrange(tahun, bulan)[1]))


def hitung_rekap_produksi(tahun, bulan):
    """Hitung tanpa menyimpan."""
    awal, akhir = _rentang(tahun, bulan)

    batch = Batch.objects.filter(
        tanggal__gte=awal, tanggal__lte=akhir, posted_at__isnull=False,
    ).aggregate(
        mixing=Count('id', filter=Q(jenis=TipeProses.MIXING)),
        blending=Count('id', filter=Q(jenis=TipeProses.BLENDING)),
        qty_hasil=Coalesce(Sum('qty_hasil'), Value(D0), output_field=F_QTY),
        nilai_hasil=Coalesce(Sum('nilai_hasil'), Value(D0), output_field=F_RP),
        qty_susut=Coalesce(Sum('susut_kg'), Value(D0), output_field=F_QTY),
        nilai_susut=Coalesce(Sum('nilai_susut'), Value(D0), output_field=F_RP),
    )

    packing = Packing.objects.filter(
        tanggal__gte=awal, tanggal__lte=akhir, status=StatusDokumen.POSTED,
    ).aggregate(
        qty=Coalesce(Sum('qty_kg'), Value(D0), output_field=F_QTY),
        nilai=Coalesce(Sum('cost_nom'), Value(D0), output_field=F_RP),
    )

    tangki = Tangki.objects.aggregate(
        kg=Coalesce(Sum('saldo_kg'), Value(D0), output_field=F_QTY),
        nilai=Coalesce(Sum('saldo_nilai'), Value(D0), output_field=F_RP),
    )
    pool = PoolResource.objects.aggregate(
        nilai=Coalesce(Sum('nilai'), Value(D0), output_field=F_RP))
    pool_kem = PoolKemasan.objects.aggregate(
        nilai=Coalesce(Sum('nilai'), Value(D0), output_field=F_RP))

    return {
        'batch_mixing': batch['mixing'],
        'batch_blending': batch['blending'],
        'qty_hasil': batch['qty_hasil'],
        'nilai_hasil': batch['nilai_hasil'],
        'qty_susut': batch['qty_susut'],
        'nilai_susut': batch['nilai_susut'],
        'qty_packing': packing['qty'],
        'nilai_packing': packing['nilai'],
        'wip_akhir_kg': tangki['kg'],
        'wip_akhir_nilai': tangki['nilai'],
        'pool_akhir_nilai': pool['nilai'],
        'pool_kemasan_akhir_nilai': pool_kem['nilai'],
    }


@transaction.atomic
def generate_rekap_produksi(tahun, bulan, user):
    """Simpan/perbarui satu baris rekap. Baris beku dilewati."""
    if user is None:
        raise ValueError('generate_rekap_produksi butuh user.')

    data = hitung_rekap_produksi(tahun, bulan)
    rekap = RekapMutasiProduksi.objects.filter(tahun=tahun, bulan=bulan).first()

    if rekap and rekap.dibekukan:
        return rekap

    if rekap:
        for k, v in data.items():
            setattr(rekap, k, v)
        rekap.save()
    else:
        rekap = RekapMutasiProduksi.objects.create(
            tahun=tahun, bulan=bulan, dibuat_oleh=user, **data,
        )
    return rekap
