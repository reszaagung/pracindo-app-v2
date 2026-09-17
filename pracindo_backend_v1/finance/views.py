from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Budget, BudgetLine,
    FixedCost,
    RevenueTarget, COGSTarget,
    Forecast,
    RekapPurchaseOrder, RekapMutasiProduksi, RekapMutasiKlaim,
)
from .serializers import (
    BudgetSerializer, BudgetLineSerializer,
    FixedCostSerializer,
    RevenueTargetSerializer, COGSTargetSerializer,
    ForecastSerializer,
    RekapPurchaseOrderSerializer, GenerateRekapSerializer,
    RekapMutasiProduksiSerializer, RekapMutasiKlaimSerializer,
    GenerateRekapProduksiSerializer,
)
from .services import (
    hitung_rekap_po, generate_rekap_po,
    hitung_rekap_produksi, generate_rekap_produksi,
    hitung_rekap_klaim, generate_rekap_klaim,
    CountRealtime,
)


def batasi_entitas(qs, request, field='entitas'):
    """Pola sama dengan akunting/views.py: staff hanya melihat entitas
    yang diizinkan untuknya."""
    u = getattr(request, 'user', None)
    if not (u and u.is_authenticated):
        return qs.none()
    if u.is_superuser:
        return qs
    rel = getattr(u, 'entitas_diizinkan', None)
    if rel is None:
        return qs.none()
    ids = list(rel.values_list('id', flat=True))
    if not ids:
        return qs.none()
    return qs.filter(**{f'{field}_id__in': ids})


class DiauditCreateMixin:
    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)


class SoftDeleteMixin:
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])


def _filter_params(qs, request, mapping):
    for param, field in mapping.items():
        value = request.query_params.get(param)
        if value:
            qs = qs.filter(**{field: value})
    return qs


class BudgetListCreateAPIView(DiauditCreateMixin, generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (Budget.objects.filter(is_active=True)
              .select_related('entitas', 'dibuat_oleh')
              .prefetch_related('lines__akun'))
        qs = batasi_entitas(qs, self.request)
        return _filter_params(qs, self.request, {
            'entitas': 'entitas_id', 'tahun': 'tahun', 'status': 'status',
        })


class BudgetDetailAPIView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Budget.objects.select_related('entitas').prefetch_related('lines__akun')
        return batasi_entitas(qs, self.request)

    def perform_destroy(self, instance):
        if instance.terkunci:
            raise ValidationError('Budget DITUTUP/BATAL, tidak bisa diarsipkan.')
        super().perform_destroy(instance)


class BudgetLineListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BudgetLineSerializer
    permission_classes = [IsAuthenticated]

    def get_budget(self):
        qs = batasi_entitas(Budget.objects.all(), self.request)
        return get_object_or_404(qs, pk=self.kwargs['budget_pk'])

    def get_queryset(self):
        self.get_budget()
        return (BudgetLine.objects
                .filter(budget_id=self.kwargs['budget_pk'], is_active=True)
                .select_related('akun'))

    def perform_create(self, serializer):
        budget = self.get_budget()
        if budget.terkunci:
            raise ValidationError('Budget DITUTUP/BATAL, tidak bisa menambah baris.')
        serializer.save(budget=budget, dibuat_oleh=self.request.user)


class BudgetLineDetailAPIView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetLineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        budget_qs = batasi_entitas(Budget.objects.all(), self.request)
        return (BudgetLine.objects
                .filter(budget_id=self.kwargs['budget_pk'], budget__in=budget_qs)
                .select_related('akun', 'budget'))

    def perform_destroy(self, instance):
        if instance.budget.terkunci:
            raise ValidationError('Budget DITUTUP/BATAL, baris tidak bisa dihapus.')
        super().perform_destroy(instance)


class FixedCostListCreateAPIView(DiauditCreateMixin, generics.ListCreateAPIView):
    serializer_class = FixedCostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (FixedCost.objects.filter(is_active=True)
              .select_related('entitas', 'akun_beban'))
        qs = batasi_entitas(qs, self.request)
        qs = _filter_params(qs, self.request, {'entitas': 'entitas_id'})
        aktif = self.request.query_params.get('aktif')
        if aktif is not None:
            qs = qs.filter(aktif=aktif.lower() in ('1', 'true', 'ya'))
        return qs


class FixedCostDetailAPIView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FixedCostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = FixedCost.objects.select_related('entitas', 'akun_beban')
        return batasi_entitas(qs, self.request)


class RevenueTargetListCreateAPIView(DiauditCreateMixin, generics.ListCreateAPIView):
    serializer_class = RevenueTargetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (RevenueTarget.objects.filter(is_active=True)
              .select_related('entitas', 'akun_pendapatan'))
        qs = batasi_entitas(qs, self.request)
        return _filter_params(qs, self.request, {
            'entitas': 'entitas_id', 'tahun': 'tahun', 'bulan': 'bulan',
        })


class RevenueTargetDetailAPIView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RevenueTargetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = RevenueTarget.objects.select_related('entitas', 'akun_pendapatan')
        return batasi_entitas(qs, self.request)


class COGSTargetListCreateAPIView(DiauditCreateMixin, generics.ListCreateAPIView):
    serializer_class = COGSTargetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (COGSTarget.objects.filter(is_active=True)
              .select_related('entitas', 'akun_cogs'))
        qs = batasi_entitas(qs, self.request)
        return _filter_params(qs, self.request, {
            'entitas': 'entitas_id', 'tahun': 'tahun', 'bulan': 'bulan',
        })


class COGSTargetDetailAPIView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = COGSTargetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = COGSTarget.objects.select_related('entitas', 'akun_cogs')
        return batasi_entitas(qs, self.request)


class ForecastListCreateAPIView(DiauditCreateMixin, generics.ListCreateAPIView):
    """Append-only: tidak ada endpoint update/delete."""
    serializer_class = ForecastSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (Forecast.objects.filter(is_active=True)
              .select_related('periode', 'periode__entitas', 'dibuat_oleh')
              .order_by('-dibuat_pada'))
        qs = batasi_entitas(qs, self.request, field='periode__entitas')
        return _filter_params(qs, self.request, {
            'periode': 'periode_id',
            'entitas': 'periode__entitas_id',
            'tahun': 'periode__tahun',
            'bulan': 'periode__bulan',
        })


class ForecastDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ForecastSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Forecast.objects.select_related('periode', 'periode__entitas')
        return batasi_entitas(qs, self.request, field='periode__entitas')


class RekapPurchaseOrderListAPIView(generics.ListAPIView):
    serializer_class = RekapPurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (RekapPurchaseOrder.objects.filter(is_active=True)
              .select_related('entitas'))
        qs = batasi_entitas(qs, self.request)
        return _filter_params(qs, self.request, {
            'entitas': 'entitas_id', 'tahun': 'tahun', 'bulan': 'bulan',
        })


class RekapPurchaseOrderDetailAPIView(generics.RetrieveUpdateAPIView):
    """Update hanya untuk membekukan/membuka. Field angka read-only."""
    serializer_class = RekapPurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = RekapPurchaseOrder.objects.select_related('entitas')
        return batasi_entitas(qs, self.request)


class RekapPurchaseOrderLiveAPIView(APIView):
    """Hitung langsung dari PO tanpa menyimpan, untuk bulan berjalan."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        s = GenerateRekapSerializer(data=request.query_params)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        return Response(hitung_rekap_po(
            tahun=d['tahun'], bulan=d['bulan'], entitas=d.get('entitas'),
        ))


class RekapPurchaseOrderGenerateAPIView(APIView):
    """Hitung dan simpan. Baris yang sudah dibekukan dilewati."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        s = GenerateRekapSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        hasil = generate_rekap_po(
            tahun=d['tahun'], bulan=d['bulan'],
            entitas=d.get('entitas'), user=request.user,
        )
        return Response(
            RekapPurchaseOrderSerializer(hasil, many=True).data,
            status=status.HTTP_200_OK,
        )


class RekapMutasiProduksiListAPIView(generics.ListAPIView):
    """Global, tanpa entitas: Tangki dan Batch resource bersama."""
    serializer_class = RekapMutasiProduksiSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = RekapMutasiProduksi.objects.filter(is_active=True)
        return _filter_params(qs, self.request, {'tahun': 'tahun', 'bulan': 'bulan'})


class RekapMutasiProduksiDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = RekapMutasiProduksi.objects.all()
    serializer_class = RekapMutasiProduksiSerializer
    permission_classes = [IsAuthenticated]


class RekapMutasiProduksiLiveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        s = GenerateRekapProduksiSerializer(data=request.query_params)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        return Response(hitung_rekap_produksi(tahun=d['tahun'], bulan=d['bulan']))


class RekapMutasiProduksiGenerateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        s = GenerateRekapProduksiSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        rekap = generate_rekap_produksi(
            tahun=d['tahun'], bulan=d['bulan'], user=request.user,
        )
        return Response(RekapMutasiProduksiSerializer(rekap).data)


class RekapMutasiKlaimListAPIView(generics.ListAPIView):
    serializer_class = RekapMutasiKlaimSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (RekapMutasiKlaim.objects.filter(is_active=True)
              .select_related('entitas'))
        qs = batasi_entitas(qs, self.request)
        return _filter_params(qs, self.request, {
            'entitas': 'entitas_id', 'tahun': 'tahun', 'bulan': 'bulan',
        })


class RekapMutasiKlaimDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = RekapMutasiKlaimSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = RekapMutasiKlaim.objects.select_related('entitas')
        return batasi_entitas(qs, self.request)


class RekapMutasiKlaimLiveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        s = GenerateRekapSerializer(data=request.query_params)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        return Response(hitung_rekap_klaim(
            tahun=d['tahun'], bulan=d['bulan'], entitas=d.get('entitas'),
        ))


class RekapMutasiKlaimGenerateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        s = GenerateRekapSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data
        hasil = generate_rekap_klaim(
            tahun=d['tahun'], bulan=d['bulan'],
            entitas=d.get('entitas'), user=request.user,
        )
        return Response(RekapMutasiKlaimSerializer(hasil, many=True).data)


class VersiRealtimeAPIView(APIView):
    """Endpoint murah untuk polling. 304 kalau klien sudah punya versi
    terbaru, supaya tidak ada payload dikirim."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        versi = CountRealtime.stempel()
        if request.headers.get('If-None-Match') == versi:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
        resp = Response(CountRealtime.ringkas())
        resp['ETag'] = versi
        resp['Cache-Control'] = 'no-cache'
        return resp
