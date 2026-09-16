from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import (
    Budget, BudgetLine,
    FixedCost,
    RevenueTarget, COGSTarget,
    Forecast,
)
from .serializers import (
    BudgetSerializer, BudgetLineSerializer,
    FixedCostSerializer,
    RevenueTargetSerializer, COGSTargetSerializer,
    ForecastSerializer,
)


class DiauditCreateMixin:
    """dibuat_oleh editable=False → tidak datang dari body request."""

    def perform_create(self, serializer):
        serializer.save(dibuat_oleh=self.request.user)


class SoftDeleteMixin:
    """DELETE = arsip (is_active=False), bukan hapus baris."""

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
        return _filter_params(qs, self.request, {
            'entitas': 'entitas_id', 'tahun': 'tahun', 'status': 'status',
        })


class BudgetDetailAPIView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Budget.objects.select_related('entitas').prefetch_related('lines__akun')
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.terkunci:
            raise ValidationError('Budget DITUTUP/BATAL — tidak bisa diarsipkan.')
        super().perform_destroy(instance)


class BudgetLineListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BudgetLineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (BudgetLine.objects
                .filter(budget_id=self.kwargs['budget_pk'], is_active=True)
                .select_related('akun'))

    def perform_create(self, serializer):
        budget = get_object_or_404(Budget, pk=self.kwargs['budget_pk'])
        if budget.terkunci:
            raise ValidationError('Budget DITUTUP/BATAL — tidak bisa menambah baris.')
        serializer.save(budget=budget, dibuat_oleh=self.request.user)


class BudgetLineDetailAPIView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetLineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BudgetLine.objects.filter(budget_id=self.kwargs['budget_pk']).select_related('akun')

    def perform_destroy(self, instance):
        if instance.budget.terkunci:
            raise ValidationError('Budget DITUTUP/BATAL — baris tidak bisa dihapus.')
        super().perform_destroy(instance)


class FixedCostListCreateAPIView(DiauditCreateMixin, generics.ListCreateAPIView):
    serializer_class = FixedCostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (FixedCost.objects.filter(is_active=True)
              .select_related('entitas', 'akun_beban'))
        qs = _filter_params(qs, self.request, {'entitas': 'entitas_id'})
        aktif = self.request.query_params.get('aktif')
        if aktif is not None:
            qs = qs.filter(aktif=aktif.lower() in ('1', 'true', 'ya'))
        return qs


class FixedCostDetailAPIView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = FixedCost.objects.select_related('entitas', 'akun_beban')
    serializer_class = FixedCostSerializer
    permission_classes = [IsAuthenticated]


class RevenueTargetListCreateAPIView(DiauditCreateMixin, generics.ListCreateAPIView):
    serializer_class = RevenueTargetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (RevenueTarget.objects.filter(is_active=True)
              .select_related('entitas', 'akun_pendapatan'))
        return _filter_params(qs, self.request, {
            'entitas': 'entitas_id', 'tahun': 'tahun', 'bulan': 'bulan',
        })


class RevenueTargetDetailAPIView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = RevenueTarget.objects.select_related('entitas', 'akun_pendapatan')
    serializer_class = RevenueTargetSerializer
    permission_classes = [IsAuthenticated]


class COGSTargetListCreateAPIView(DiauditCreateMixin, generics.ListCreateAPIView):
    serializer_class = COGSTargetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (COGSTarget.objects.filter(is_active=True)
              .select_related('entitas', 'akun_cogs'))
        return _filter_params(qs, self.request, {
            'entitas': 'entitas_id', 'tahun': 'tahun', 'bulan': 'bulan',
        })


class COGSTargetDetailAPIView(SoftDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = COGSTarget.objects.select_related('entitas', 'akun_cogs')
    serializer_class = COGSTargetSerializer
    permission_classes = [IsAuthenticated]


class ForecastListCreateAPIView(DiauditCreateMixin, generics.ListCreateAPIView):
    """List + Create saja. Forecast append-only, jadi tidak ada
    endpoint update/delete sama sekali."""
    serializer_class = ForecastSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = (Forecast.objects.filter(is_active=True)
              .select_related('periode', 'periode__entitas', 'dibuat_oleh')
              .order_by('-dibuat_pada'))
        # entitas hanya bisa difilter lewat periode — bukan field di Forecast.
        return _filter_params(qs, self.request, {
            'periode': 'periode_id',
            'entitas': 'periode__entitas_id',
            'tahun': 'periode__tahun',
            'bulan': 'periode__bulan',
        })


class ForecastDetailAPIView(generics.RetrieveAPIView):
    queryset = Forecast.objects.select_related('periode', 'periode__entitas')
    serializer_class = ForecastSerializer
    permission_classes = [IsAuthenticated]