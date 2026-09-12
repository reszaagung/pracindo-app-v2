from rest_framework import serializers

from . import integrasi_warehouse as gudang
from .models import (
    BuktiTerima, Kendaraan, Pengiriman, Perhentian, Retur, 
)

class KendaraanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kendaraan
        fields = ['id', 'kode', 'nama', 'plat_nomor', 'kapasitas_kg', 'aktif']


class BuktiTerimaSerializer(serializers.ModelSerializer):
    diunggah_oleh_nama = serializers.SerializerMethodField()

    class Meta:
        model = BuktiTerima
        fields = ['id', 'foto', 'waktu', 'catatan', 'diunggah_oleh_nama']

    def get_diunggah_oleh_nama(self, obj):
        u = obj.diunggah_oleh
        return (u.get_full_name() or u.get_username()) if u else None

class ReturSerializer(serializers.ModelSerializer):
    dicatat_oleh_nama = serializers.SerializerMethodField()
    disetujui_oleh_nama = serializers.SerializerMethodField()
    pelanggan_nama = serializers.CharField(source='perhentian.pelanggan_nama', read_only=True)
    nomor_distribusi = serializers.CharField(source='perhentian.nomor_distribusi', read_only=True)
    menunggu_persetujuan = serializers.BooleanField(read_only=True)

    class Meta:
        model = Retur
        fields = ['id', 'perhentian', 'nomor_distribusi', 'pelanggan_nama',
                  'alasan', 'foto', 'dicatat_pada', 'dicatat_oleh_nama',
                  'disetujui_pada', 'disetujui_oleh_nama',
                  'stok_dikembalikan', 'menunggu_persetujuan']

    def get_dicatat_oleh_nama(self, obj):
        u = obj.dicatat_oleh
        return (u.get_full_name() or u.get_username()) if u else None

    def get_disetujui_oleh_nama(self, obj):
        u = obj.disetujui_oleh
        return (u.get_full_name() or u.get_username()) if u else None

class PerhentianSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source='get_status_display', read_only=True)
    bukti = BuktiTerimaSerializer(many=True, read_only=True)
    diretur = serializers.SerializerMethodField()
    baris = serializers.SerializerMethodField()

    class Meta:
        model = Perhentian
        fields = [
            'id', 'distribusi_id', 'nomor_distribusi', 'pelanggan_nama',
            'urutan', 'alamat', 'status', 'status_label', 'waktu_sampai', 
            'bukti', 'diretur', 'baris',
        ]

    def get_diretur(self, obj):
        return hasattr(obj, 'retur')

    def get_baris(self, obj):
        try:
            rincian = gudang.rincian_distribusi(obj.distribusi_id)
            return rincian.get('baris', [])
        except Exception:
            return []

class PengirimanSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source='get_status_display', read_only=True)
    entitas_kode = serializers.CharField(source='entitas.kode', read_only=True)
    kurir_nama = serializers.SerializerMethodField()
    kendaraan_kode = serializers.SerializerMethodField()
    jumlah_perhentian = serializers.IntegerField(read_only=True)
    
    dibuat_oleh_nama = serializers.SerializerMethodField()

    class Meta:
        model = Pengiriman
        fields = [
            'id', 'nomor', 'tanggal', 'entitas_kode', 'kurir', 'kurir_nama',
            'kendaraan', 'kendaraan_kode', 'status', 'status_label',
            'waktu_berangkat', 'waktu_selesai', 'jumlah_perhentian', 'catatan',
            'dibuat_oleh_nama',
        ]

    def get_kurir_nama(self, obj):
        u = obj.kurir
        return (u.get_full_name() or u.get_username()) if u else None

    def get_kendaraan_kode(self, obj):
        return obj.kendaraan.kode if obj.kendaraan_id else None

    def get_dibuat_oleh_nama(self, obj):
        u = obj.dibuat_oleh
        return (u.get_full_name() or u.get_username()) if u else None

class PengirimanDetailSerializer(PengirimanSerializer):
    perhentian = PerhentianSerializer(many=True, read_only=True)

    class Meta(PengirimanSerializer.Meta):
        fields = PengirimanSerializer.Meta.fields + ['perhentian']

class RakitPengirimanSerializer(serializers.Serializer):
    entitas_id = serializers.IntegerField()
    kurir_id = serializers.IntegerField(required=False, allow_null=True) 
    distribusi_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)
    tanggal = serializers.DateField(required=False, allow_null=True)
    kendaraan_id = serializers.IntegerField(required=False, allow_null=True)
    catatan = serializers.CharField(required=False, allow_blank=True, default='')

class UrutRuteSerializer(serializers.Serializer):
    urutan = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

class BuktiTerimaUploadSerializer(serializers.Serializer):
    foto = serializers.ImageField()
    catatan = serializers.CharField(required=False, allow_blank=True, default='')

class CatatReturSerializer(serializers.Serializer):
    alasan = serializers.CharField(allow_blank=False, max_length=1000)
    foto = serializers.ImageField(required=False, allow_null=True)

class BatalPengirimanSerializer(serializers.Serializer):
    alasan = serializers.CharField(allow_blank=False, max_length=500)