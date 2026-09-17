from datetime import datetime
from django.apps import apps
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from staff_user.permissions import SudahLogin, AdminAtauAkunting
from .models import SalesOrder, StatusSO
from .serializers import SalesOrderSerializer
from .utils import generate_nomor_so_dinamis

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.select_related('pelanggan', 'entitas').prefetch_related(
        'items__produk__satuan'
    ).order_by('-tanggal', '-nomor_so')
    
    serializer_class = SalesOrderSerializer
    filterset_fields = ['status', 'pelanggan', 'entitas']
    search_fields = ['nomor_so', 'pelanggan__nama']

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [SudahLogin()]
        return [AdminAtauAkunting()]

    def perform_destroy(self, instance):
        if instance.status != StatusSO.DRAFT:
            raise ValidationError("Hanya Sales Order berstatus DRAFT yang bisa dihapus.")
        instance.delete()

    @action(detail=False, methods=['get'], url_path='preview-nomor')
    def preview_nomor(self, request):
        entitas_id = request.query_params.get('entitas')
        tanggal_str = request.query_params.get('tanggal')
        
        try:
            tanggal_obj = datetime.strptime(tanggal_str, '%Y-%m-%d').date() if tanggal_str else datetime.today().date()
        except ValueError:
            tanggal_obj = datetime.today().date()
            
        entitas_obj = None
        if entitas_id:
            Entitas = apps.get_model('core', 'Entitas')
            entitas_obj = Entitas.objects.filter(id=entitas_id).first()
            
        nomor_preview = generate_nomor_so_dinamis(SalesOrder, entitas_obj, tanggal_obj)
        
        return Response({"nomor_so": nomor_preview})