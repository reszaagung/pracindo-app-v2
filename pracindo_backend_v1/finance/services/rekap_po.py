"""
Rekap nilai purchase order per entitas per bulan.

Sumber: akunting.PurchaseOrderItem. Ini angka KOMITMEN pembelian, bukan
actual akuntansi — actual masuk ledger lewat faktur pembelian
(akunting.services.terbitkan_faktur), bukan lewat PO.

nilai_pesan memakai kolom `amount` yang sudah tersimpan di item, sama
dengan PurchaseOrderQuerySet.dengan_total(), supaya angka rekap tidak
pernah berbeda dari angka di halaman PO.
"""
import calendar
from datetime import date
from decimal import Decimal

from django.db import transaction
from django.db.models import Sum, F, Count, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce

from akunting.models import PurchaseOrderItem, StatusPO

from finance.models import RekapPurchaseOrder

# PO mati bukan komitmen. Sisanya (DRAFT, PENDING, APPROVED, TERKIRIM,
# SEBAGIAN, SELESAI) ikut dihitung.
STATUS_DIKECUALIKAN = [StatusPO.BATAL, StatusPO.DITOLAK]

_NILAI_DITERIMA = ExpressionWrapper(
    F('qty_diterima') * F('harga_per_kg'),
    output_field=DecimalField(max_digits=20, decimal_places=2),
)


def _rentang(tahun, bulan):
    return (date(tahun, bulan, 1),
            date(tahun, bulan, calendar.monthrange(tahun, bulan)[1]))


def _item_qs(tahun, bulan, entitas=None):
    awal, akhir = _rentang(tahun, bulan)
    qs = (PurchaseOrderItem.objects
          .filter(purchase_order__tanggal__gte=awal,
                  purchase_order__tanggal__lte=akhir)
          .exclude(purchase_order__status__in=STATUS_DIKECUALIKAN))
    if entitas is not None:
        qs = qs.filter(purchase_order__entitas=entitas)
    return qs


def hitung_rekap_po(tahun, bulan, entitas=None):
    """Hitung tanpa menyimpan — dipakai endpoint real-time dan oleh
    generate_rekap_po()."""
    qs = _item_qs(tahun, bulan, entitas)

    agregat = (qs.values('purchase_order__entitas_id')
                 .annotate(jumlah_po=Count('purchase_order_id', distinct=True),
                           jumlah_item=Count('id'),
                           nilai_pesan=Coalesce(Sum('amount'), Decimal('0')),
                           nilai_diterima=Coalesce(Sum(_NILAI_DITERIMA), Decimal('0')))
                 .order_by('purchase_order__entitas__kode'))

    ppn = _ppn_per_entitas(qs)
    return [{
        'entitas_id': b['purchase_order__entitas_id'],
        'jumlah_po': b['jumlah_po'],
        'jumlah_item': b['jumlah_item'],
        'nilai_pesan': b['nilai_pesan'],
        'nilai_diterima': b['nilai_diterima'],
        'nilai_ppn': ppn.get(b['purchase_order__entitas_id'], Decimal('0')),
    } for b in agregat]


def _ppn_per_entitas(qs):
    """PPN dihitung per-PO karena ppn_persen ada di header dan berbeda
    antar-PO (0 untuk suplier non-PKP)."""
    per_po = (qs.values('purchase_order_id',
                        'purchase_order__entitas_id',
                        'purchase_order__ppn_persen')
                .annotate(dpp=Coalesce(Sum('amount'), Decimal('0'))))
    total = {}
    for row in per_po:
        persen = row['purchase_order__ppn_persen'] or Decimal('0')
        eid = row['purchase_order__entitas_id']
        total[eid] = total.get(eid, Decimal('0')) + row['dpp'] * persen / Decimal('100')
    return {k: v.quantize(Decimal('0.01')) for k, v in total.items()}


@transaction.atomic
def generate_rekap_po(tahun, bulan, user, entitas=None):
    """
    Simpan/perbarui baris RekapPurchaseOrder. Baris yang sudah dibekukan
    dilewati, tidak ditimpa.

    `user` wajib: dibuat_oleh di DiauditModel non-null dan PROTECT. Kalau
    nanti dipanggil dari cron, siapkan user sistem khusus.
    """
    if user is None:
        raise ValueError('generate_rekap_po butuh user — dibuat_oleh tidak boleh kosong.')

    hasil = []
    for data in hitung_rekap_po(tahun, bulan, entitas):
        entitas_id = data.pop('entitas_id')
        rekap = RekapPurchaseOrder.objects.filter(
            entitas_id=entitas_id, tahun=tahun, bulan=bulan,
        ).first()

        if rekap and rekap.dibekukan:
            continue

        if rekap:
            for k, v in data.items():
                setattr(rekap, k, v)
            rekap.save()
        else:
            rekap = RekapPurchaseOrder.objects.create(
                entitas_id=entitas_id, tahun=tahun, bulan=bulan,
                dibuat_oleh=user, **data,
            )
        hasil.append(rekap)
    return hasil