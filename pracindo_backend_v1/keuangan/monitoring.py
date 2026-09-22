from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from akunting.models.hutang import FakturPembelian, StatusFaktur

from .models import JenisRekening, RekeningBank


HARI_PERINGATAN_DEFAULT = 7
TERMIN_DEFAULT = 30


def klasifikasi_tempo(
    tanggal_jatuh_tempo,
    hari_peringatan=HARI_PERINGATAN_DEFAULT,
):
    hari_ini = timezone.localdate()
    hari_tersisa = (tanggal_jatuh_tempo - hari_ini).days

    if hari_tersisa < 0:
        return "TERLAMBAT", hari_tersisa

    if hari_tersisa == 0:
        return "JATUH_TEMPO", 0

    if hari_tersisa <= hari_peringatan:
        return "PERINGATAN", hari_tersisa

    return "NORMAL", hari_tersisa


def saldo_kas(entitas_id=None):
    qs = RekeningBank.objects.filter(
        aktif=True,
        jenis__in=[
            JenisRekening.BANK,
            JenisRekening.KAS,
            JenisRekening.KAS_KECIL,
        ],
    )

    if entitas_id:
        qs = qs.filter(entitas_id=entitas_id)

    total = (
        qs.aggregate(total=Sum("saldo"))["total"]
        or Decimal("0")
    )

    rekening = list(
        qs.select_related("entitas")
        .order_by("entitas__kode", "jenis", "nama_bank", "id")
        .values(
            "id",
            "entitas__kode",
            "jenis",
            "nama_bank",
            "nomor_rekening",
            "nama_pemilik",
            "saldo",
            "aktif",
        )
    )

    return {
        "saldo_kas": total,
        "rekening": rekening,
    }


def queryset_tagihan_supplier(entitas_id=None):
    qs = (
        FakturPembelian.objects.filter(
            jenis="BARANG",
            status__in=[
                StatusFaktur.BELUM_BAYAR,
                StatusFaktur.SEBAGIAN,
            ],
            sisa_hutang__gt=0,
            penerimaan__isnull=False,
        )
        .select_related(
            "entitas",
            "suplier",
            "penerimaan",
            "penerimaan__purchase_order",
        )
        .order_by(
            "tanggal_jatuh_tempo",
            "id",
        )
    )

    if entitas_id:
        qs = qs.filter(entitas_id=entitas_id)

    return qs


def monitoring_tagihan_supplier(
    entitas_id=None,
    hari_peringatan=HARI_PERINGATAN_DEFAULT,
):
    data = []

    for faktur in queryset_tagihan_supplier(entitas_id):
        status_tempo, hari_tersisa = klasifikasi_tempo(
            faktur.tanggal_jatuh_tempo,
            hari_peringatan,
        )

        data.append(
            {
                "id": faktur.id,
                "entitas_id": faktur.entitas_id,
                "entitas": faktur.entitas.kode,
                "supplier_id": faktur.suplier_id,
                "supplier": faktur.suplier.nama,
                "no_po": faktur.penerimaan.purchase_order.no_po,
                "nomor_penerimaan": faktur.penerimaan.nomor,
                "nomor_faktur": faktur.nomor_faktur,
                "no_internal": faktur.no_internal,
                "tanggal_penerimaan": faktur.penerimaan.tanggal,
                "tanggal_faktur": faktur.tanggal_faktur,
                "termin_hari": faktur.termin_hari,
                "tanggal_jatuh_tempo": faktur.tanggal_jatuh_tempo,
                "total_tagihan": faktur.total_tagihan,
                "total_dibayar": faktur.total_dibayar,
                "sisa_hutang": faktur.sisa_hutang,
                "status_faktur": faktur.status,
                "status_tempo": status_tempo,
                "hari_tersisa": hari_tersisa,
            }
        )

    return data


def ringkasan_tagihan_supplier(
    entitas_id=None,
    hari_peringatan=HARI_PERINGATAN_DEFAULT,
):
    data = monitoring_tagihan_supplier(
        entitas_id=entitas_id,
        hari_peringatan=hari_peringatan,
    )

    ringkasan = {
        "jumlah_tagihan": len(data),
        "terlambat": 0,
        "jatuh_tempo": 0,
        "peringatan": 0,
        "normal": 0,
        "total_outstanding": Decimal("0"),
    }

    for item in data:
        status = item["status_tempo"]

        if status == "TERLAMBAT":
            ringkasan["terlambat"] += 1
        elif status == "JATUH_TEMPO":
            ringkasan["jatuh_tempo"] += 1
        elif status == "PERINGATAN":
            ringkasan["peringatan"] += 1
        else:
            ringkasan["normal"] += 1

        ringkasan["total_outstanding"] += item["sisa_hutang"]

    return ringkasan, data


def monitoring_summary(
    entitas_id=None,
    hari_peringatan=HARI_PERINGATAN_DEFAULT,
):
    kas = saldo_kas(entitas_id=entitas_id)

    ringkasan_tagihan, tagihan = ringkasan_tagihan_supplier(
        entitas_id=entitas_id,
        hari_peringatan=hari_peringatan,
    )

    return {
        "tanggal": timezone.localdate(),
        "termin_default": TERMIN_DEFAULT,
        "peringatan_hari": hari_peringatan,
        "kas": kas,
        "tagihan": {
            "ringkasan": ringkasan_tagihan,
            "data": tagihan,
        },
    }