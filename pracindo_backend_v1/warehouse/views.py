from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.db import transaction

from akunting.models import PurchaseOrder, PurchaseOrderItem
from staff_user.permissions import AksesModul
from . import services
from .models import (
    LaporanSelisih,
    PenerimaanBarang,
    Distribusi,
    ItemDistribusi,
    StatusDistribusi 
)
from .serializers import (
    LaporanManualSerializer,
    LaporanSelisihAkuntingSerializer,
    LaporanSelisihGudangSerializer,
    PenerimaanBarangSerializer,
    PenerimaanListSerializer,
    POGudangSerializer,
    SelesaikanSelisihSerializer,
    TerimaBarangSerializer,
    TutupSelisihSerializer,
    DistribusiSerializer,
    BuatDistribusiSerializer,
)

def _galat(e):
    isi = e.message_dict if hasattr(e, 'message_dict') else {'detail': e.messages}
    return Response(isi, status=status.HTTP_400_BAD_REQUEST)


class POSiapTerimaViewSet(viewsets.ReadOnlyModelViewSet):
    modul = 'warehouse'
    permission_classes = [AksesModul]
    serializer_class = POGudangSerializer
    filterset_fields = ['suplier', 'entitas']
    search_fields = ['no_po', 'suplier__nama']

    def get_queryset(self):
        return (PurchaseOrder.objects.terbuka()
                .select_related('suplier', 'entitas')
                .prefetch_related(
                    Prefetch('item',
                             queryset=PurchaseOrderItem.objects.select_related('produk')))
                .order_by('tanggal'))


class PenerimaanViewSet(viewsets.ModelViewSet):
    modul = 'warehouse'
    permission_classes = [AksesModul]
    filterset_fields = ['purchase_order', 'ada_selisih', 'tanggal']
    search_fields = ['nomor', 'no_surat_jalan', 'purchase_order__no_po']

    def get_queryset(self):
        return (PenerimaanBarang.objects
                .select_related('purchase_order__suplier', 'dibuat_oleh')
                .prefetch_related('item__po_item', 'laporan_selisih')
                .order_by('-tanggal', '-id'))

    def get_serializer_class(self):
        if self.action == 'list':
            return PenerimaanListSerializer
        if self.action == 'create':
            return TerimaBarangSerializer
        return PenerimaanBarangSerializer

    @action(detail=True, methods=['get'])
    def ringkasan(self, request, pk=None):
        penerimaan = self.get_object()
        serializer = PenerimaanBarangSerializer(penerimaan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def create(self, request, *args, **kwargs):
        s = TerimaBarangSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                penerimaan, laporan, setoran = services.terima_barang(user=request.user, **s.validated_data)
        except DjangoValidationError as e:
            return _galat(e)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PenerimaanBarangSerializer(penerimaan).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Penerimaan barang tidak bisa diubah langsung. Gunakan modul Selisih.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    partial_update = update

    def destroy(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Penerimaan barang tidak boleh dihapus demi jejak audit.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class LaporanSelisihViewSet(viewsets.ModelViewSet):
    modul = 'warehouse'
    permission_classes = [AksesModul]
    filterset_fields = ['penerimaan', 'jenis', 'status', 'resolusi']
    search_fields = ['nomor', 'uraian', 'penerimaan__nomor']

    def get_queryset(self):
        return (LaporanSelisih.objects
                .select_related('penerimaan__purchase_order__suplier',
                                'penerimaan_item__po_item')
                .order_by('-tanggal', '-id'))

    def _sisi_akunting(self):
        return (self.request.query_params.get('sisi') == 'akunting'
                and self.request.user.bisa_akses_modul('akunting'))

    def get_serializer_class(self):
        if self._sisi_akunting():
            return LaporanSelisihAkuntingSerializer
        return LaporanSelisihGudangSerializer

    def create(self, request, *args, **kwargs):
        s = LaporanManualSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        try:
            lap = services.laporan_manual(user=request.user, **s.validated_data)
        except DjangoValidationError as e:
            return _galat(e)
            
        return Response(LaporanSelisihGudangSerializer(lap).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Laporan tidak bisa diubah langsung. Gunakan aksi '
                       'selesaikan atau tutup.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    partial_update = update

    def destroy(self, request, *args, **kwargs):
        return Response({'detail': 'Laporan tidak bisa dihapus. Tutup saja.'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get'])
    def terbuka(self, request):
        qs = services.klaim_belum_diselesaikan(
            suplier_id=request.query_params.get('suplier'),
            entitas_id=request.query_params.get('entitas'),
        )
        kelas = (LaporanSelisihAkuntingSerializer if self._sisi_akunting()
                 else LaporanSelisihGudangSerializer)
        return Response(kelas(qs, many=True).data)

    @action(detail=True, methods=['post'])
    def ajukan(self, request, pk=None):
        try:
            lap = services.ajukan_ke_suplier(laporan_id=pk, user=request.user)
        except DjangoValidationError as e:
            return _galat(e)
        return Response(LaporanSelisihGudangSerializer(lap).data)

    @action(detail=True, methods=['post'])
    def selesaikan(self, request, pk=None):
        if not request.user.bisa_akses_modul('akunting'):
            return Response(
                {'detail': 'Resolusi selisih ditetapkan modul akunting.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        s = SelesaikanSelisihSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        try:
            lap = services.selesaikan_laporan(
                laporan_id=pk, user=request.user, **s.validated_data,
            )
        except DjangoValidationError as e:
            return _galat(e)
        return Response(LaporanSelisihAkuntingSerializer(lap).data)

    @action(detail=True, methods=['post'])
    def tutup(self, request, pk=None):
        if not request.user.bisa_akses_modul('akunting'):
            return Response(
                {'detail': 'Penutupan selisih ditetapkan modul akunting.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        s = TutupSelisihSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        try:
            lap = services.tutup_laporan(laporan_id=pk, user=request.user,
                                         alasan=s.validated_data['alasan'])
        except DjangoValidationError as e:
            return _galat(e)
        return Response(LaporanSelisihAkuntingSerializer(lap).data)


class DistribusiViewSet(viewsets.ModelViewSet):
    modul = 'warehouse'
    permission_classes = [AksesModul]
    filterset_fields = ['status', 'jenis_tujuan']
    search_fields = ['nomor', 'pelanggan_nama', 'alamat']

    def get_queryset(self):
        return (Distribusi.objects
                .select_related('entitas', 'tujuan_cabang', 'diterima_oleh')
                .prefetch_related('item__produk', 'item__entitas')
                .order_by('-tanggal_dibuat', '-id'))

    def get_serializer_class(self):
        if self.action == 'create':
            return BuatDistribusiSerializer
        return DistribusiSerializer

    def _isi_baris(self, dist, baris):
        """Entitas per baris disimpan apa adanya. Baris yang kosong ikut
        entitas header saat stok dipotong — lihat ItemDistribusi.entitas_efektif."""
        for brs in baris:
            ItemDistribusi.objects.create(
                distribusi=dist,
                entitas_id=brs.get('entitas_id'),
                produk_id=brs['produk_id'],
                kemasan=brs['kemasan'],
                stiker=brs.get('stiker', ''),
                qty=brs['qty'],
            )

    def create(self, request, *args, **kwargs):
        s = BuatDistribusiSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data

        try:
            with transaction.atomic():
                dist = Distribusi.objects.create(
                    entitas_id=d['entitas_id'],
                    jenis_tujuan=d['jenis_tujuan'],
                    tujuan_cabang_id=d.get('tujuan_cabang_id'),
                    pelanggan_nama=d['pelanggan_nama'],
                    alamat=d['alamat'],
                    lat=d.get('lat'),
                    lng=d.get('lng'),
                    berat_total_kg=d.get('berat_total_kg', 0),
                    dibuat_oleh=request.user,
                )

                self._isi_baris(dist, d['baris'])

                dist = services.sahkan_distribusi(distribusi_id=dist.id, user=request.user)

                from logistik.services import rakit_pengiriman
                rakit_pengiriman(
                    entitas_id=dist.entitas_id,
                    distribusi_ids=[dist.id],
                    user=request.user,
                    catatan="Tugas otomatis dari pembuatan DO Gudang",
                )

        except DjangoValidationError as e:
            return _galat(e)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(DistribusiSerializer(dist).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        dist = self.get_object()

        if dist.status in [StatusDistribusi.DIKIRIM, StatusDistribusi.TERKIRIM]:
            return Response(
                {'detail': 'Dokumen yang sudah dibawa kurir atau selesai tidak bisa diubah.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        s = BuatDistribusiSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data

        try:
            with transaction.atomic():
                if dist.status == StatusDistribusi.SIAP_KIRIM:
                    services.kembalikan_potongan_stok(dist.id)
                    dist.status = StatusDistribusi.DRAFT
                    dist.save(update_fields=['status'])

                dist.entitas_id = d['entitas_id']
                dist.jenis_tujuan = d['jenis_tujuan']
                dist.tujuan_cabang_id = d.get('tujuan_cabang_id')
                dist.pelanggan_nama = d['pelanggan_nama']
                dist.alamat = d['alamat']
                dist.lat = d.get('lat')
                dist.lng = d.get('lng')
                dist.berat_total_kg = d.get('berat_total_kg', 0)
                dist.save()

                dist.item.all().delete()
                self._isi_baris(dist, d['baris'])

                dist = services.sahkan_distribusi(distribusi_id=dist.id, user=request.user)

        except DjangoValidationError as e:
            return _galat(e)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(DistribusiSerializer(dist).data, status=status.HTTP_200_OK)

    partial_update = update

    def destroy(self, request, *args, **kwargs):
        dist = self.get_object()

        if dist.status in [StatusDistribusi.DIKIRIM, StatusDistribusi.TERKIRIM]:
            return Response(
                {'detail': 'Dokumen yang sudah dibawa kurir atau selesai tidak bisa dihapus.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                if dist.status == StatusDistribusi.SIAP_KIRIM:
                    services.kembalikan_potongan_stok(dist.id)
                dist.delete()
        except DjangoValidationError as e:
            return _galat(e)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def sahkan(self, request, pk=None):
        try:
            dist = services.sahkan_distribusi(distribusi_id=pk, user=request.user)
        except DjangoValidationError as e:
            return _galat(e)

        return Response(DistribusiSerializer(dist).data, status=status.HTTP_200_OK)