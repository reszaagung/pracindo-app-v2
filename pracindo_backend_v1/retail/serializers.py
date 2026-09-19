from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db import transaction
from .models import (
    StokRetail, TransaksiPOS, SesiKasir, ItemTransaksi,
    KategoriAkun, AkunBukuBesar, TransaksiJurnal, DetailJurnal,
    SalesRetail, PelangganRetail,
    BukuPiutangRetail, RiwayatBayarPiutang,
    PenerimaanBarang, ItemPenerimaan, CabangToko ,StokRetail
)

User = get_user_model()

class KatalogPOSSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='produk.id', read_only=True)
    nama = serializers.CharField(source='produk.nama_item', read_only=True)
    kemasan = serializers.CharField(read_only=True)
    stok = serializers.IntegerField(source='total_unit', read_only=True)
    harga = serializers.DecimalField(source='harga_jual', max_digits=12,
                                     decimal_places=2, read_only=True)

    class Meta:
        model = StokRetail
        fields = ['id', 'nama', 'kemasan', 'stok', 'harga']


class StokRetailSerializer(serializers.ModelSerializer):
    kode_produk = serializers.CharField(source='produk.id', read_only=True)
    nama_produk = serializers.CharField(source='produk.nama_item', read_only=True)
    satuan = serializers.CharField(source='kemasan', read_only=True)
    qty = serializers.IntegerField(source='total_unit', read_only=True)
    entitas_kode = serializers.CharField(source='entitas.kode', read_only=True, default=None)
    grup_kode = serializers.CharField(source='entitas.grup_bahan.kode', read_only=True, default=None)

    class Meta:
        model = StokRetail
        fields = ['id', 'kode_produk', 'nama_produk', 'kemasan', 'satuan',
                  'qty', 'harga_jual', 'entitas', 'entitas_kode', 'grup_kode']

class ItemTransaksiSerializer(serializers.ModelSerializer):
    produk_nama = serializers.CharField(source='produk.nama_item', read_only=True)

    class Meta:
        model = ItemTransaksi
        fields = ['id', 'produk', 'produk_nama', 'kemasan', 'qty_unit', 'harga_satuan', 'subtotal']

class RiwayatTransaksiSerializer(serializers.ModelSerializer):
    produk_nama = serializers.CharField(source='produk.nama_item', read_only=True)
    pelanggan_nama = serializers.CharField(source='pelanggan.nama', read_only=True, allow_null=True)
    sales_nama = serializers.CharField(source='sales.nama', read_only=True, allow_null=True)

    class Meta:
        model = TransaksiPOS
        fields = [
            'id', 'nomor_struk', 'waktu_transaksi', 
            'pelanggan', 'pelanggan_nama', 'sales', 'sales_nama',
            'subtotal', 'pajak', 'grand_total', 
            'metode_bayar', 'status', 'items'
        ]

class SesiKasirSerializer(serializers.ModelSerializer):
    kasir_nama = serializers.CharField(source='kasir.username', read_only=True)
    cabang_nama = serializers.CharField(source='cabang.nama', read_only=True)

    class Meta:
        model = SesiKasir
        fields = [
            'id', 'cabang_nama', 'kasir_nama', 'waktu_buka', 
            'waktu_tutup', 'saldo_awal', 'total_penjualan', 'status'
        ]

class KategoriAkunSerializer(serializers.ModelSerializer):
    class Meta:
        model = KategoriAkun
        fields = '__all__'

class AkunBukuBesarSerializer(serializers.ModelSerializer):
    kategori_nama = serializers.CharField(source='kategori.nama', read_only=True)
    tipe_saldo = serializers.CharField(source='kategori.tipe_saldo', read_only=True)

    class Meta:
        model = AkunBukuBesar
        fields = ['id', 'kode', 'nama', 'kategori', 'kategori_nama', 'tipe_saldo', 'cabang', 'aktif']

class DetailJurnalSerializer(serializers.ModelSerializer):
    akun_kode = serializers.CharField(source='akun.kode', read_only=True)
    akun_nama = serializers.CharField(source='akun.nama', read_only=True)

    class Meta:
        model = DetailJurnal
        fields = ['id', 'akun', 'akun_kode', 'akun_nama', 'debit', 'kredit']

class TransaksiJurnalSerializer(serializers.ModelSerializer):
    item_jurnal = DetailJurnalSerializer(many=True, read_only=True)
    
    class Meta:
        model = TransaksiJurnal
        fields = ['id', 'nomor_jurnal', 'tanggal', 'referensi', 'keterangan', 'cabang', 'item_jurnal']

class SalesRetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesRetail
        fields = ['id', 'nama', 'persentase_bonus']

class PelangganRetailSerializer(serializers.ModelSerializer):
    sales_nama = serializers.CharField(source='sales.nama', read_only=True)

    class Meta:
        model = PelangganRetail
        fields = ['id', 'nama', 'nomor_telepon', 'alamat', 'limit_piutang', 'default_tempo_hari', 'sales', 'sales_nama']

class RiwayatBayarPiutangSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiwayatBayarPiutang
        fields = '__all__'

class BukuPiutangRetailSerializer(serializers.ModelSerializer):
    pelanggan_nama = serializers.CharField(source='pelanggan.nama', read_only=True)
    nomor_struk = serializers.CharField(source='transaksi.nomor_struk', read_only=True)
    sisa_piutang = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    umur_piutang_hari = serializers.IntegerField(read_only=True)
    sisa_hari_jatuh_tempo = serializers.IntegerField(read_only=True)
    riwayat_bayar = RiwayatBayarPiutangSerializer(many=True, read_only=True)

    class Meta:
        model = BukuPiutangRetail
        fields = [
            'id', 'pelanggan', 'pelanggan_nama', 'nomor_struk', 
            'tanggal_piutang', 'jatuh_tempo', 'total_piutang', 
            'total_dibayar', 'sisa_piutang', 'status', 
            'umur_piutang_hari', 'sisa_hari_jatuh_tempo', 'riwayat_bayar'
        ]

class ItemPenerimaanSerializer(serializers.ModelSerializer):
    produk_nama = serializers.CharField(source='produk.nama_item', read_only=True)

    class Meta:
        model = ItemPenerimaan
        fields = ['id', 'produk', 'produk_nama', 'kemasan', 'unit_dikirim', 'unit_diterima']

class PenerimaanBarangSerializer(serializers.ModelSerializer):
    items = ItemPenerimaanSerializer(many=True, read_only=True)

    class Meta:
        model = PenerimaanBarang
        fields = '__all__'

class MutasiBukuBesarSerializer(serializers.ModelSerializer):
    tanggal = serializers.DateTimeField(source='jurnal.tanggal', read_only=True)
    nomor_jurnal = serializers.CharField(source='jurnal.nomor_jurnal', read_only=True)
    keterangan = serializers.CharField(source='jurnal.keterangan', read_only=True)
    referensi = serializers.CharField(source='jurnal.referensi', read_only=True)

    class Meta:
        model = DetailJurnal
        fields = ['id', 'tanggal', 'nomor_jurnal', 'referensi', 'keterangan', 'debit', 'kredit']

class RegistrasiCabangSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    kode = serializers.CharField(read_only=True)

    class Meta:
        model = CabangToko
        fields = ['id', 'username', 'password', 'nama', 'alamat', 'kode', 'aktif']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username ini sudah digunakan.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        
        validated_data.pop('aktif', None)
        
        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False  
        )
        
        cabang = CabangToko.objects.create(
            user=user,
            aktif=False,     
            **validated_data
        )
        
        return cabang

class CabangTokoSerializer(serializers.ModelSerializer):
    username_kasir = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = CabangToko
        fields = ['id', 'kode', 'nama', 'alamat', 'aktif', 'username_kasir']

