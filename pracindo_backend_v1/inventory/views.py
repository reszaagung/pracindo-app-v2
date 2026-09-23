from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response

from core.models import CounterDokumen, Entitas
from core.serializers import EntitasSerializer as CoreEntitasSerializer
from master.models import MasterProduk, Produk

from . import serializers as ser
from . import services
from .models import (
    Kemasan,
    MutasiKlaim,
    Packing,
    Pembelian,
    PoolKemasan,
    PoolResource,
    StatusDokumen,
    StokBarangJadi,
    StokItemsPabrik,
)

from .permissions import (
    AksesInventory,
    SupervisorInventory,
)


MODUL = "inventory"


GALAT_TERTANGANI = (
    services.GalatInventory,
    DjangoValidationError,
)


def _galat(exc):
    kode = exc.__class__.__name__

    pesan = (
        getattr(exc, "message", None)
        or (
            exc.messages[0]
            if getattr(exc, "messages", None)
            else str(exc)
        )
    )

    return Response(
        {
            "detail": pesan,
            "kode": kode,
            "pesan": pesan,
        },
        status=getattr(
            exc,
            "http",
            status.HTTP_400_BAD_REQUEST,
        ),
    )


def _int_atau_none(nilai):
    try:
        return (
            int(nilai)
            if nilai not in (None, "")
            else None
        )
    except (TypeError, ValueError):
        return None


@api_view(["GET"])
@permission_classes([AksesInventory])
def entitas_list(request):
    qs = (
        Entitas.objects
        .select_related("grup_bahan")
        .order_by("kode")
    )

    aktif = request.query_params.get("aktif")

    if aktif in ("true", "1", "True"):
        qs = qs.filter(aktif=True)

    grup = request.query_params.get("grup")

    if grup:
        qs = qs.filter(
            grup_bahan_id=grup
        )

    return Response(
        CoreEntitasSerializer(
            qs,
            many=True,
        ).data
    )


# ============================================================
# PRODUK
# ============================================================

@api_view(["GET"])
@permission_classes([AksesInventory])
def produk_list(request):
    qs = Produk.objects.order_by("kode")

    q = request.query_params.get("q")
    jenis = request.query_params.get("jenis")

    if q:
        qs = qs.filter(
            nama__icontains=q
        )

    if jenis:
        qs = qs.filter(
            jenis=jenis.upper()
        )

    return Response(
        ser.ProdukRingkasSerializer(
            qs[:200],
            many=True,
        ).data
    )


# ============================================================
# MASTER KEMASAN
# ============================================================

class KemasanViewSet(viewsets.ModelViewSet):
    modul = MODUL
    queryset = (
        Kemasan.objects
        .all()
        .order_by("nama")
    )
    serializer_class = ser.KemasanSerializer
    permission_classes = [AksesInventory]

    def get_queryset(self):
        qs = super().get_queryset()

        aktif = self.request.query_params.get(
            "aktif"
        )

        if aktif in (
            "true",
            "1",
            "True",
        ):
            qs = qs.filter(
                aktif=True
            )

        return qs


# ============================================================
# PEMBELIAN
# ============================================================

class PembelianViewSet(viewsets.ModelViewSet):
    modul = MODUL

    queryset = (
        Pembelian.objects
        .select_related(
            "entitas",
            "grup_bahan",
            "produk",
            "penerimaan_item",
        )
        .order_by(
            "-waktu",
            "-id",
        )
    )

    serializer_class = ser.PembelianSerializer
    permission_classes = [
        AksesInventory,
    ]

    def get_permissions(self):
        if self.action == "void":
            return [
                AksesInventory(),
                SupervisorInventory(),
            ]

        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        filters = (
            ("entitas", "entitas_id"),
            ("produk", "produk_id"),
            ("grup", "grup_bahan_id"),
            ("status", "status"),
            ("sumber", "sumber"),
        )

        for param, field in filters:
            value = params.get(param)

            if value:
                qs = qs.filter(
                    **{
                        field: value
                    }
                )

        if params.get("jenis"):
            qs = qs.filter(
                produk__jenis=params[
                    "jenis"
                ].upper()
            )

        if params.get("kategori_kemasan"):
            qs = qs.filter(
                kategori_kemasan=params[
                    "kategori_kemasan"
                ].upper()
            )

        if params.get("no_po"):
            qs = qs.filter(
                no_po__icontains=params[
                    "no_po"
                ]
            )

        if params.get("dari"):
            qs = qs.filter(
                tanggal__gte=params["dari"]
            )

        if params.get("sampai"):
            qs = qs.filter(
                tanggal__lte=params["sampai"]
            )

        return qs

    @transaction.atomic
    def perform_create(self, serializer):
        data = serializer.validated_data

        entitas = data["entitas"]
        tanggal = data["tanggal"]

        try:
            nomor = CounterDokumen.berikutnya(
                entitas,
                "PB",
                tanggal,
            )
        except DjangoValidationError as exc:
            raise DRFValidationError({
                "kode": "PENOMORAN_GAGAL",
                "pesan": str(exc),
            })

        qty_kg = data["qty_kg"]
        harga_per_kg = data["harga_per_kg"]

        serializer.save(
            nomor=nomor,
            grup_bahan=entitas.grup_bahan,
            nilai=services.rp(
                qty_kg * harga_per_kg
            ),
            dibuat_oleh=self.request.user,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        instance = serializer.instance
        data = serializer.validated_data

        qty_kg = data.get(
            "qty_kg",
            instance.qty_kg,
        )

        harga_per_kg = data.get(
            "harga_per_kg",
            instance.harga_per_kg,
        )

        entitas = data.get(
            "entitas",
            instance.entitas,
        )

        serializer.save(
            nilai=services.rp(
                qty_kg * harga_per_kg
            ),
            grup_bahan=entitas.grup_bahan,
        )

    def perform_destroy(self, instance):
        if instance.status != StatusDokumen.DRAFT:
            raise DRFValidationError({
                "kode": "DOKUMEN_TERKUNCI",
                "pesan": (
                    "Hanya pembelian DRAFT yang "
                    "bisa dihapus. Dokumen POSTED "
                    "dibatalkan lewat /void/."
                ),
            })

        instance.delete()

    @action(
        detail=True,
        methods=["post"],
        url_path="post",
    )
    def posting(self, request, pk=None):
        try:
            hasil = services.posting_pembelian(
                self.get_object(),
                user=request.user,
            )
        except GALAT_TERTANGANI as exc:
            return _galat(exc)

        return Response(
            ser.PembelianSerializer(
                hasil,
                context={
                    "request": request,
                },
            ).data
        )

    @action(
        detail=True,
        methods=["post"],
    )
    def void(self, request, pk=None):
        try:
            hasil = services.void_pembelian(
                self.get_object(),
                request.data.get(
                    "alasan",
                    "",
                ),
                user=request.user,
            )
        except GALAT_TERTANGANI as exc:
            return _galat(exc)

        return Response(
            ser.PembelianSerializer(
                hasil,
                context={
                    "request": request,
                },
            ).data
        )


# ============================================================
# PACKING
# ============================================================

class PackingViewSet(viewsets.ModelViewSet):
    modul = MODUL

    queryset = (
        Packing.objects
        .select_related(
            "entitas",
            "tangki",
            "nama_hasil",
            "kemasan_primer",
            "kemasan_primer__produk",
            "kemasan_sekunder",
            "kemasan_sekunder__produk",
        )
        .order_by(
            "-waktu",
            "-id",
        )
    )

    serializer_class = ser.PackingSerializer
    permission_classes = [
        AksesInventory,
    ]

    def get_permissions(self):
        if self.action in (
            "void_dokumen",
            "destroy",
        ):
            return [
                AksesInventory(),
                SupervisorInventory(),
            ]

        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        if params.get("entitas"):
            qs = qs.filter(
                entitas_id=params["entitas"]
            )

        if params.get("tangki"):
            qs = qs.filter(
                tangki_id=params["tangki"]
            )

        if params.get("status"):
            qs = qs.filter(
                status=params["status"].upper()
            )

        if params.get("produk"):
            qs = qs.filter(
                nama_hasil_id=params["produk"]
            )

        if params.get("dari"):
            qs = qs.filter(
                tanggal__gte=params["dari"]
            )

        if params.get("sampai"):
            qs = qs.filter(
                tanggal__lte=params["sampai"]
            )

        return qs

    @transaction.atomic
    def perform_create(self, serializer):
        data = serializer.validated_data

        entitas = data["entitas"]
        tanggal = (
            data.get("tanggal")
            or timezone.localdate()
        )

        try:
            nomor = CounterDokumen.berikutnya(
                entitas,
                "PKG",
                tanggal,
            )
        except DjangoValidationError as exc:
            raise DRFValidationError({
                "kode": "PENOMORAN_GAGAL",
                "pesan": str(exc),
            })

        packing = serializer.save(
            nomor=nomor,
            tanggal=tanggal,
            status=StatusDokumen.DRAFT,
            dibuat_oleh=self.request.user,
        )

        try:
            services.eksekusi_packing_langsung(
                packing,
                self.request.user,
            )
        except GALAT_TERTANGANI as exc:
            raise DRFValidationError({
                "kode": "GAGAL_POSTING",
                "pesan": str(exc),
            })

    @transaction.atomic
    def perform_update(self, serializer):
        instance = serializer.instance

        if instance.status != StatusDokumen.DRAFT:
            raise DRFValidationError({
                "kode": "PACKING_TERKUNCI",
                "pesan": (
                    f"Packing {instance.nomor} "
                    f"sudah {instance.get_status_display()} "
                    "dan tidak dapat diubah."
                ),
            })

        serializer.save()

    @transaction.atomic
    def perform_destroy(self, instance):
        try:
            services.rollback_hapus_packing(
                instance
            )
        except GALAT_TERTANGANI as exc:
            raise DRFValidationError({
                "kode": "GAGAL_ROLLBACK",
                "pesan": str(exc),
            })

        instance.delete()

    # --------------------------------------------------------
    # POST
    # --------------------------------------------------------

    @action(
        detail=True,
        methods=["post"],
        url_path="post",
    )
    def posting(self, request, pk=None):
        packing = self.get_object()

        if packing.status != StatusDokumen.DRAFT:
            return Response(
                {
                    "kode": "STATUS_TIDAK_VALID",
                    "pesan": (
                        f"Packing {packing.nomor} "
                        f"berstatus "
                        f"{packing.get_status_display()} "
                        "dan tidak dapat diposting."
                    ),
                },
                status=status.HTTP_409_CONFLICT,
            )

        try:
            hasil = services.eksekusi_packing_langsung(
                packing,
                request.user,
            )
        except GALAT_TERTANGANI as exc:
            return _galat(exc)

        return Response(
            ser.PackingSerializer(
                hasil,
                context={
                    "request": request,
                },
            ).data
        )

    # --------------------------------------------------------
    # PREVIEW
    # --------------------------------------------------------

    @action(
        detail=False,
        methods=["get"],
    )
    def pratinjau(self, request):
        tangki_id = request.query_params.get(
            "tangki"
        )

        qty_diminta = (
            request.query_params.get(
                "qty"
            )
            or 0
        )

        return Response(
            services.pratinjau_packing(
                tangki_id,
                qty_diminta,
            )
        )

    # --------------------------------------------------------
    # VOID
    # --------------------------------------------------------

    @action(
        detail=True,
        methods=["post"],
        url_path="void",
    )
    def void_dokumen(self, request, pk=None):
        packing = self.get_object()

        if packing.status != StatusDokumen.POSTED:
            return Response(
                {
                    "kode": "STATUS_TIDAK_VALID",
                    "pesan": (
                        f"Packing {packing.nomor} "
                        f"berstatus "
                        f"{packing.get_status_display()} "
                        "dan hanya Packing POSTED "
                        "yang dapat di-VOID."
                    ),
                },
                status=status.HTTP_409_CONFLICT,
            )

        alasan = request.data.get(
            "alasan",
            "",
        )

        try:
            hasil = services.void_packing(
                packing,
                alasan,
                user=request.user,
            )
        except GALAT_TERTANGANI as exc:
            return _galat(exc)

        return Response({
            "status": "sukses",
            "nomor": hasil.nomor,
            "status_packing": hasil.status,
            "pesan": (
                f"Packing {hasil.nomor} "
                "berhasil di-VOID dan seluruh "
                "nilai/stok dikembalikan."
            ),
        })


# ============================================================
# POOL RESOURCE
# ============================================================

@api_view(["GET"])
@permission_classes([AksesInventory])
def pool_list(request):
    return Response(
        services.get_pool_resource_all()
    )


# ============================================================
# POOL KEMASAN
# ============================================================

@api_view(["GET"])
@permission_classes([AksesInventory])
def pool_kemasan_list(request):
    qs = (
        PoolKemasan.objects
        .select_related("produk")
        .all()
    )

    kategori = request.query_params.get(
        "kategori"
    )

    tersedia = request.query_params.get(
        "tersedia"
    )

    if kategori:
        kategori = kategori.upper()

        if kategori == "PRIMER":
            qs = qs.filter(
                kategori__in=[
                    "PRIMER",
                    "PRIMER_SEKUNDER",
                ]
            )

        elif kategori == "SEKUNDER":
            qs = qs.filter(
                kategori__in=[
                    "SEKUNDER",
                    "PRIMER_SEKUNDER",
                ]
            )

        elif kategori == "PRIMER_SEKUNDER":
            qs = qs.filter(
                kategori="PRIMER_SEKUNDER"
            )

        else:
            return Response(
                {
                    "kode": "KATEGORI_TIDAK_VALID",
                    "pesan": (
                        "Kategori harus PRIMER, "
                        "SEKUNDER, atau PRIMER_SEKUNDER."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    if tersedia in (
        "true",
        "1",
        "True",
    ):
        qs = qs.filter(
            qty_unit__gt=0
        )

    return Response(
        ser.PoolKemasanSerializer(
            qs,
            many=True,
            context={
                "request": request,
            },
        ).data
    )


# ============================================================
# KARTU STOK
# ============================================================

@api_view(["GET"])
@permission_classes([AksesInventory])
def pool_kartu_stok(
    request,
    produk_id,
):
    try:
        return Response(
            services.get_kartu_stok(
                int(produk_id)
            )
        )
    except (
        PoolResource.DoesNotExist,
        PoolKemasan.DoesNotExist,
    ):
        return Response(
            {
                "kode": "POOL_BELUM_ADA",
                "detail": (
                    f"Produk {produk_id} "
                    "belum punya baris di Pool."
                ),
            },
            status=status.HTTP_404_NOT_FOUND,
        )


# ============================================================
# MUTASI
# ============================================================

@api_view(["GET"])
@permission_classes([AksesInventory])
def mutasi_list(request):
    qs = (
        MutasiKlaim.objects
        .select_related(
            "entitas",
            "grup_bahan",
        )
        .order_by(
            "-waktu",
            "-id",
        )
    )

    params = request.query_params

    if params.get("entitas"):
        qs = qs.filter(
            entitas_id=params["entitas"]
        )

    if params.get("grup"):
        qs = qs.filter(
            grup_bahan_id=params["grup"]
        )

    if params.get("tipe"):
        qs = qs.filter(
            tipe=params["tipe"].upper()
        )

    if params.get("dari"):
        qs = qs.filter(
            waktu__date__gte=params["dari"]
        )

    if params.get("sampai"):
        qs = qs.filter(
            waktu__date__lte=params["sampai"]
        )

    try:
        batas = min(
            int(
                params.get(
                    "limit",
                    200,
                )
            ),
            1000,
        )
    except (
        TypeError,
        ValueError,
    ):
        batas = 200

    return Response(
        ser.MutasiKlaimSerializer(
            qs[:batas],
            many=True,
        ).data
    )


@api_view(["GET"])
@permission_classes([AksesInventory])
def mutasi_rekap(request):
    return Response(
        services.get_rekap_klaim(
            _int_atau_none(
                request.query_params.get(
                    "grup"
                )
            )
        )
    )


@api_view(["GET"])
@permission_classes([AksesInventory])
def posisi_klaim(request):
    from decimal import Decimal

    grup_id = request.query_params.get("grup")

    if not grup_id:
        return Response([])

    try:
        grup_id = int(grup_id)
    except (TypeError, ValueError):
        return Response([])

    rows = (
        MutasiKlaim.objects
        .filter(grup_bahan_id=grup_id)
        .values(
            "entitas_id",
            "entitas__kode",
            "arah",
            "qty_kg",
            "nilai",
        )
        .order_by("entitas__kode", "entitas_id")
    )

    hasil = {}

    for row in rows:
        entitas_id = row["entitas_id"]

        if entitas_id not in hasil:
            hasil[entitas_id] = {
                "entitas": row["entitas__kode"],
                "setor": Decimal("0"),
                "ambil": Decimal("0"),
                "bersih": Decimal("0"),
                "qty_setor": Decimal("0"),
                "qty_ambil": Decimal("0"),
                "qty_bersih": Decimal("0"),
            }

        item = hasil[entitas_id]
        qty = row["qty_kg"] or Decimal("0")
        nilai = row["nilai"] or Decimal("0")

        if row["arah"] == 1:
            item["setor"] += nilai
            item["qty_setor"] += qty
        elif row["arah"] == -1:
            item["ambil"] += nilai
            item["qty_ambil"] += qty

        item["bersih"] = item["setor"] - item["ambil"]
        item["qty_bersih"] = item["qty_setor"] - item["qty_ambil"]

    return Response([
        {
            "entitas": item["entitas"],
            "setor": str(item["setor"]),
            "ambil": str(item["ambil"]),
            "bersih": str(item["bersih"]),
            "qty_setor": str(item["qty_setor"]),
            "qty_ambil": str(item["qty_ambil"]),
            "qty_bersih": str(item["qty_bersih"]),
            "berhutang": item["bersih"] < 0,
        }
        for item in hasil.values()
    ])


@api_view(["GET"])
@permission_classes([AksesInventory])
def saldo_entitas_list(request):
    saldo = (
        SaldoEntitas.objects
        .select_related("entitas")
        .order_by("entitas__kode")
    )

    hasil = []

    for item in saldo:
        hasil.append({
            "entitas_id": item.entitas_id,
            "entitas": item.entitas.kode,
            "total_setor": str(item.total_setor),
            "total_tarik": str(item.total_tarik),
            "total_rugi": str(item.total_rugi),
            "qty_setor": str(item.qty_setor),
            "qty_tarik": str(item.qty_tarik),
            "saldo": str(item.saldo),
            "terakhir_diperbarui": item.diperbarui_pada.isoformat()
            if hasattr(item, "diperbarui_pada") and item.diperbarui_pada
            else None,
        })

    return Response({
        "results": hasil,
        "total": len(hasil),
    })



@api_view(["GET"])
@permission_classes([AksesInventory])
def pemeriksaan_invarian(request):
    return Response(
        services.jalankan_pemeriksaan_invarian()
    )

@api_view(["GET"])
@permission_classes([AksesInventory])
def barang_jadi(request):
    return Response(
        services.get_barang_jadi(
            _int_atau_none(
                request.query_params.get(
                    "grup"
                )
            )
        )
    )

@api_view(["GET"])
@permission_classes([AksesInventory])
def stok_list(request):
    lapis = (
        request.query_params.get(
            "lapis"
        )
        or "POOL"
    ).upper()

    grup = _int_atau_none(
        request.query_params.get(
            "grup"
        )
    )

    if lapis == "POOL":
        data = (
            services.get_pool_resource_all()
        )

        return Response({
            "lapis": "POOL",
            "rincian": data["rincian"],
            "total_nilai": data[
                "total_nilai_pool"
            ],
        })

    if lapis == "KEMASAN":
        qs = (
            PoolKemasan.objects
            .select_related("produk")
            .all()
        )

        kategori = request.query_params.get(
            "kategori"
        )

        if kategori:
            kategori = kategori.upper()

            if kategori == "PRIMER":
                qs = qs.filter(
                    kategori__in=[
                        "PRIMER",
                        "PRIMER_SEKUNDER",
                    ]
                )

            elif kategori == "SEKUNDER":
                qs = qs.filter(
                    kategori__in=[
                        "SEKUNDER",
                        "PRIMER_SEKUNDER",
                    ]
                )

            elif kategori == "PRIMER_SEKUNDER":
                qs = qs.filter(
                    kategori="PRIMER_SEKUNDER"
                )

            else:
                return Response(
                    {
                        "kode": "KATEGORI_TIDAK_VALID",
                        "pesan": (
                            "Kategori harus PRIMER, "
                            "SEKUNDER, atau "
                            "PRIMER_SEKUNDER."
                        ),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        rincian = ser.PoolKemasanSerializer(
            qs,
            many=True,
        ).data

        total_nilai = sum(
            (
                pool.nilai
                for pool in qs
            ),
            services.D0_RP,
        )

        return Response({
            "lapis": "KEMASAN",
            "rincian": rincian,
            "total_nilai": str(
                services.rp(total_nilai)
            ),
        })

    # --------------------------------------------------------
    # BARANG JADI
    # --------------------------------------------------------

    if lapis == "JADI":
        data = services.get_barang_jadi(
            grup
        )

        return Response({
            "lapis": "JADI",
            "rincian": data["rincian"],
            "total_nilai": data[
                "total_nilai"
            ],
        })

    return Response(
        {
            "kode": "LAPIS_TIDAK_DIKENAL",
            "detail": (
                f"Lapis '{lapis}' tidak ada."
            ),
        },
        status=status.HTTP_400_BAD_REQUEST,
    )

