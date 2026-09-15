import uuid
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

from .models import (
    StokRetail, MutasiStokRetail, CabangToko, SesiKasir, TransaksiPOS, ItemTransaksi,
    AkunBukuBesar, TransaksiJurnal, DetailJurnal,
    PelangganRetail, SalesRetail, BukuPiutangRetail, BonusSales,
    RiwayatBayarPiutang, PenerimaanBarang, ItemPenerimaan
)

from .serializers import (
    KatalogPOSSerializer, RiwayatTransaksiSerializer, SesiKasirSerializer,
    AkunBukuBesarSerializer, TransaksiJurnalSerializer,
    PelangganRetailSerializer, SalesRetailSerializer,
    BukuPiutangRetailSerializer, PenerimaanBarangSerializer,
    MutasiBukuBesarSerializer, CabangTokoSerializer, RegistrasiCabangSerializer
)

class RetailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        cabang_data = None
        
        if hasattr(user, 'cabang_toko') and user.cabang_toko is not None:
            cabang = user.cabang_toko
            cabang_data = {
                'id': cabang.id,
                'kode': cabang.kode,
                'nama': cabang.nama
            }

        data['user'] = {
            'id': user.id,
            'username': user.username,
            'is_master': cabang_data is None,
            'cabang': cabang_data
        }
        return data

class RetailLoginView(TokenObtainPairView):
    serializer_class = RetailTokenObtainPairSerializer

def get_user_cabang(user):
    if hasattr(user, 'cabang_toko') and user.cabang_toko is not None:
        return user.cabang_toko
    return None

class KatalogPOSAPIView(generics.ListAPIView):
    serializer_class = KatalogPOSSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cabang = get_user_cabang(self.request.user)
        qs = StokRetail.objects.filter(total_unit__gt=0).select_related('produk', 'kemasan')
        if cabang:
            return qs.filter(cabang=cabang)
        return qs

class CheckoutPOSAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic 
    def post(self, request):
        user = request.user
        cabang = get_user_cabang(user)
        
        if not cabang:
            cabang_id = request.data.get('cabang_id')
            cabang = CabangToko.objects.filter(id=cabang_id).first()
            if not cabang:
                return Response({'status': 'gagal'}, status=status.HTTP_400_BAD_REQUEST)

        metode_bayar = request.data.get('metode_bayar', 'TUNAI')
        pelanggan_id = request.data.get('pelanggan_id')
        sales_id = request.data.get('sales_id')

        if hasattr(user, 'salesretail'):
            sales_id = user.salesretail.id
        if hasattr(user, 'pelangganretail'):
            pelanggan_id = user.pelangganretail.id

        if metode_bayar == 'TEMPO' and not pelanggan_id:
            return Response({'status': 'gagal'}, status=status.HTTP_400_BAD_REQUEST)

        sesi = SesiKasir.objects.filter(cabang=cabang, status='AKTIF').first()
        if not sesi:
            sesi = SesiKasir.objects.create(cabang=cabang, kasir=user, status='AKTIF')

        keranjang = request.data.get('keranjang', [])
        subtotal = Decimal(str(request.data.get('subtotal', 0)))
        
        transaksi = TransaksiPOS.objects.create(
            nomor_struk=f"TRX-{uuid.uuid4().hex[:8].upper()}",
            sesi=sesi,
            pelanggan_id=pelanggan_id,
            sales_id=sales_id,
            subtotal=subtotal,
            pajak=Decimal('0'),
            grand_total=subtotal,
            metode_bayar=metode_bayar
        )

        for item in keranjang:
            qty_beli = int(item['qty_unit'])
            harga_satuan = Decimal(str(item['harga']))

            stok = StokRetail.objects.select_for_update().get(
                cabang=cabang, 
                produk_id=item['produk_id'],
                kemasan_id=item['kemasan_id']
            )
            
            if stok.total_unit < qty_beli:
                transaction.set_rollback(True)
                return Response({'status': 'gagal'}, status=status.HTTP_400_BAD_REQUEST)

            ItemTransaksi.objects.create(
                transaksi=transaksi,
                produk_id=item['produk_id'],
                kemasan_id=item['kemasan_id'],
                qty_unit=qty_beli,
                harga_satuan=harga_satuan,
                subtotal=harga_satuan * Decimal(qty_beli)
            )
            
            stok.total_unit -= qty_beli
            stok.save()

            MutasiStokRetail.objects.create(
                stok=stok,
                jenis='PENJUALAN',
                referensi=transaksi.nomor_struk,
                unit_masuk=0,
                unit_keluar=qty_beli,
                saldo_akhir=stok.total_unit
            )

        if metode_bayar == 'TEMPO':
            pelanggan = PelangganRetail.objects.get(id=pelanggan_id)
            BukuPiutangRetail.objects.create(
                pelanggan=pelanggan,
                transaksi=transaksi,
                tanggal_piutang=timezone.now().date(),
                jatuh_tempo=timezone.now().date() + timedelta(days=pelanggan.default_tempo_hari),
                total_piutang=subtotal
            )

        if sales_id:
            sales = SalesRetail.objects.get(id=sales_id)
            nominal_bonus = subtotal * (sales.persentase_bonus / Decimal('100'))
            if nominal_bonus > 0:
                BonusSales.objects.create(
                    sales=sales,
                    transaksi=transaksi,
                    tanggal=timezone.now().date(),
                    nominal_bonus=nominal_bonus
                )

        sesi.total_penjualan = sesi.total_penjualan + subtotal
        sesi.save()

        return Response({'status': 'sukses', 'nomor_struk': transaksi.nomor_struk}, status=status.HTTP_201_CREATED)

class RiwayatTransaksiAPIView(generics.ListAPIView):
    serializer_class = RiwayatTransaksiSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        cabang = get_user_cabang(user)
        
        qs = TransaksiPOS.objects.all()
        if cabang:
            qs = qs.filter(sesi__cabang=cabang)
            
        if hasattr(user, 'salesretail'):
            qs = qs.filter(sales=user.salesretail)
        elif hasattr(user, 'pelangganretail'):
            qs = qs.filter(pelanggan=user.pelangganretail)
            
        return qs.order_by('-waktu_transaksi')[:50]

class SesiKasirAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cabang = get_user_cabang(request.user)
        qs = SesiKasir.objects.filter(status='AKTIF')
        if cabang:
            qs = qs.filter(cabang=cabang)
        
        sesi = qs.first()
        if sesi:
            return Response(SesiKasirSerializer(sesi).data)
        return Response({'status': 'TIDAK_ADA_SHIFT'}, status=status.HTTP_200_OK)
        
    def post(self, request):
        cabang = get_user_cabang(request.user)
        qs = SesiKasir.objects.filter(status='AKTIF')
        if cabang:
            qs = qs.filter(cabang=cabang)
        else:
            cabang_id = request.data.get('cabang_id')
            if cabang_id:
                qs = qs.filter(cabang_id=cabang_id)
                
        sesi = qs.first()
        if sesi:
            sesi.status = 'DITUTUP'
            sesi.waktu_tutup = timezone.now()
            sesi.save()
            return Response({'status': 'sukses'})
        return Response({'status': 'gagal'}, status=status.HTTP_400_BAD_REQUEST)

class AkunBukuBesarAPIView(generics.ListCreateAPIView):
    serializer_class = AkunBukuBesarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cabang = get_user_cabang(self.request.user)
        qs = AkunBukuBesar.objects.all()
        if cabang:
            return qs.filter(cabang=cabang)
        return qs

class JurnalUmumAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cabang = get_user_cabang(request.user)
        qs = TransaksiJurnal.objects.prefetch_related('item_jurnal__akun')
        if cabang:
            qs = qs.filter(cabang=cabang)
        return Response(TransaksiJurnalSerializer(qs, many=True).data)

    @transaction.atomic
    def post(self, request):
        cabang = get_user_cabang(request.user)
        if not cabang:
            cabang_id = request.data.get('cabang_id')
            cabang = CabangToko.objects.filter(id=cabang_id).first()
            if not cabang:
                return Response({'status': 'gagal'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        items = data.get('items', [])
        
        total_debit = sum(Decimal(str(i.get('debit', 0))) for i in items)
        total_kredit = sum(Decimal(str(i.get('kredit', 0))) for i in items)

        if total_debit != total_kredit:
            return Response({'status': 'gagal'}, status=status.HTTP_400_BAD_REQUEST)

        jurnal = TransaksiJurnal.objects.create(
            nomor_jurnal=f"JV-{uuid.uuid4().hex[:6].upper()}",
            referensi=data.get('referensi', ''),
            keterangan=data.get('keterangan', ''),
            cabang=cabang
        )

        for item in items:
            DetailJurnal.objects.create(
                jurnal=jurnal,
                akun_id=item['akun_id'],
                debit=Decimal(str(item.get('debit', 0))),
                kredit=Decimal(str(item.get('kredit', 0)))
            )

        return Response({'status': 'sukses', 'nomor_jurnal': jurnal.nomor_jurnal}, status=status.HTTP_201_CREATED)

class PelangganRetailAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cabang = get_user_cabang(self.request.user)
        qs = PelangganRetail.objects.select_related('sales')
        if cabang:
            return qs.filter(cabang=cabang)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            from .serializers import RegistrasiPelangganSerializer
            return RegistrasiPelangganSerializer
        return PelangganRetailSerializer

class SalesRetailAPIView(generics.ListAPIView):
    serializer_class = SalesRetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'salesretail'):
            return SalesRetail.objects.filter(id=user.salesretail.id, aktif=True)
            
        cabang = get_user_cabang(user)
        qs = SalesRetail.objects.filter(aktif=True)
        if cabang:
            return qs.filter(cabang=cabang)
        return qs

class DaftarPiutangAPIView(generics.ListAPIView):
    serializer_class = BukuPiutangRetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'pelangganretail'):
            return BukuPiutangRetail.objects.filter(pelanggan=user.pelangganretail).order_by('jatuh_tempo')
        if hasattr(user, 'salesretail'):
            return BukuPiutangRetail.objects.filter(pelanggan__sales=user.salesretail).order_by('jatuh_tempo')
            
        cabang = get_user_cabang(user)
        qs = BukuPiutangRetail.objects.all().order_by('jatuh_tempo')
        if cabang:
            return qs.filter(pelanggan__cabang=cabang)
        return qs

class BayarPiutangAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        try:
            piutang = BukuPiutangRetail.objects.get(id=pk)
        except BukuPiutangRetail.DoesNotExist:
            return Response({'status': 'gagal'}, status=status.HTTP_404_NOT_FOUND)

        nominal = Decimal(str(request.data.get('nominal', 0)))
        metode_bayar = request.data.get('metode_bayar', 'TUNAI')

        if nominal <= 0 or nominal > piutang.sisa_piutang:
            return Response({'status': 'gagal'}, status=status.HTTP_400_BAD_REQUEST)
        
        RiwayatBayarPiutang.objects.create(
            piutang=piutang,
            tanggal_bayar=timezone.now().date(),
            nominal=nominal,
            metode_bayar=metode_bayar
        )

        cabang = piutang.pelanggan.cabang
        sesi = SesiKasir.objects.filter(cabang=cabang, status='AKTIF').first()
        if sesi and metode_bayar == 'TUNAI':
            sesi.total_penjualan = sesi.total_penjualan + nominal
            sesi.save()

        return Response({'status': 'sukses'}, status=status.HTTP_200_OK)

class DaftarPenerimaanAPIView(generics.ListAPIView):
    serializer_class = PenerimaanBarangSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cabang = get_user_cabang(self.request.user)
        qs = PenerimaanBarang.objects.all().order_by('status', '-tanggal_terima')
        if cabang:
            return qs.filter(cabang=cabang)
        return qs

class ProsesPenerimaanAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        try:
            penerimaan = PenerimaanBarang.objects.get(id=pk)
        except PenerimaanBarang.DoesNotExist:
            return Response({'status': 'gagal'}, status=status.HTTP_404_NOT_FOUND)

        items = request.data.get('items', [])
        for item in items:
            item_obj = ItemPenerimaan.objects.get(id=item['id'])
            qty_terima = int(item.get('unit_diterima', 0))
            
            if qty_terima > 0:
                item_obj.unit_diterima = qty_terima
                item_obj.save()

                stok, created = StokRetail.objects.get_or_create(
                    cabang=penerimaan.cabang, 
                    produk=item_obj.produk,
                    kemasan=item_obj.kemasan,
                    defaults={'total_unit': 0, 'harga_jual': 0}
                )
                stok.total_unit += qty_terima
                stok.save()

                MutasiStokRetail.objects.create(
                    stok=stok,
                    jenis='PENERIMAAN',
                    referensi=penerimaan.nomor_penerimaan,
                    unit_masuk=qty_terima,
                    unit_keluar=0,
                    saldo_akhir=stok.total_unit
                )
            
        penerimaan.status = 'SELESAI'
        penerimaan.tanggal_terima = timezone.now()
        penerimaan.save()

        return Response({'status': 'sukses'})

class BukuBesarMutasiAPIView(generics.ListAPIView):
    serializer_class = MutasiBukuBesarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        akun_id = self.kwargs.get('pk')
        return DetailJurnal.objects.filter(akun_id=akun_id).select_related('jurnal').order_by('jurnal__tanggal', 'id')

class CabangTokoAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CabangToko.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegistrasiCabangSerializer
        return CabangTokoSerializer