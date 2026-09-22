from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Entitas
from staff_user.models import Role
from staff_user.permissions import PunyaRole

from .models import PengeluaranKas
from .monitoring import (
    HARI_PERINGATAN_DEFAULT,
    monitoring_summary,
    ringkasan_tagihan_supplier,
    saldo_kas,
)
from .serializers import (
    InputPengeluaranSerializer,
    PengeluaranKasSerializer,
)


def get_entitas(request):
    kode = request.query_params.get("entitas")

    if not kode:
        return None

    return get_object_or_404(
        Entitas,
        kode=kode,
    )


# =========================================================
# MONITORING AKUNTING
# HANYA ROLE AKUNTING
# =========================================================

class MonitoringAkuntingPermission(PunyaRole):
    roles = (Role.AKUNTING,)
    message = 'Hanya staf Akunting yang boleh mengakses Monitoring Akunting.'


class MonitoringKeuanganAPIView(APIView):
    permission_classes = [MonitoringAkuntingPermission]

    def get(self, request):
        entitas = get_entitas(request)

        data = monitoring_summary(
            entitas_id=entitas.id if entitas else None,
            hari_peringatan=HARI_PERINGATAN_DEFAULT,
        )

        return Response(data)


class MonitoringTagihanAPIView(APIView):
    permission_classes = [MonitoringAkuntingPermission]

    def get(self, request):
        entitas = get_entitas(request)

        hari_peringatan = request.query_params.get(
            "hari_peringatan",
            HARI_PERINGATAN_DEFAULT,
        )

        try:
            hari_peringatan = int(hari_peringatan)
        except (TypeError, ValueError):
            return Response(
                {
                    "detail": "hari_peringatan harus berupa angka."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if hari_peringatan < 0:
            return Response(
                {
                    "detail": "hari_peringatan tidak boleh negatif."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ringkasan, data = ringkasan_tagihan_supplier(
            entitas_id=entitas.id if entitas else None,
            hari_peringatan=hari_peringatan,
        )

        return Response(
            {
                "peringatan_hari": hari_peringatan,
                "ringkasan": ringkasan,
                "data": data,
            }
        )


class MonitoringKasAPIView(APIView):
    permission_classes = [MonitoringAkuntingPermission]

    def get(self, request):
        entitas = get_entitas(request)

        data = saldo_kas(
            entitas_id=entitas.id if entitas else None,
        )

        return Response(data)


# =========================================================
# PENGELUARAN
# =========================================================

class PengeluaranViewSet(viewsets.ModelViewSet):
    queryset = (
        PengeluaranKas.objects
        .select_related("entitas", "mutasi")
        .order_by("-id")
    )

    serializer_class = PengeluaranKasSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = super().get_queryset()

        entitas_kode = self.request.query_params.get("entitas")

        if entitas_kode:
            qs = qs.filter(
                entitas__kode=entitas_kode
            )

        return qs

    def create(self, request, *args, **kwargs):
        serializer = InputPengeluaranSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        entitas = get_object_or_404(
            Entitas,
            kode=serializer.validated_data["entitas"],
        )

        with transaction.atomic():
            pengeluaran = PengeluaranKas.objects.create(
                entitas=entitas,
                kategori=serializer.validated_data["kategori"],
                keterangan=serializer.validated_data["keterangan"],
                pemohon=serializer.validated_data["pemohon"],
                nominal=serializer.validated_data["nominal"],
                bukti_nota=serializer.validated_data.get(
                    "bukti_nota"
                ),
            )

        return Response(
            PengeluaranKasSerializer(
                pengeluaran,
                context={"request": request},
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {
                "detail": (
                    "Pengeluaran yang sudah dicatat "
                    "tidak dapat diubah."
                )
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {
                "detail": (
                    "Pengeluaran yang sudah dicatat "
                    "tidak dapat diubah."
                )
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {
                "detail": (
                    "Pengeluaran yang sudah dicatat "
                    "tidak dapat dihapus."
                )
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="dashboard-summary",
    )
    def dashboard_summary(self, request):
        entitas = get_entitas(request)

        summary = monitoring_summary(
            entitas_id=entitas.id if entitas else None,
            hari_peringatan=HARI_PERINGATAN_DEFAULT,
        )

        return Response(
            {
                "tanggal": summary["tanggal"],
                "saldo_kas": summary["kas"]["saldo_kas"],
                "rekening": summary["kas"]["rekening"],
                "tagihan": summary["tagihan"]["ringkasan"],
            }
        )