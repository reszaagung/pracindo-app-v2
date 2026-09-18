from rest_framework import serializers
from .models import Batch, Tangki

class TangkiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tangki
        fields = ['id', 'kode', 'nama', 'aktif', 'kapasitas_kg']

class BatchSerializer(serializers.ModelSerializer):
    tangki_kode = serializers.CharField(source="tangki.kode", read_only=True)
    tangki_tujuan_nama = serializers.CharField(source="tangki.nama", read_only=True)
    batch = serializers.CharField(source="nomor", read_only=True)
    harga_per_kg = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = [
            "id", "batch", "nomor", "jenis", "nama_hasil", 
            "tangki", "tangki_kode", "tangki_tujuan_nama", 
            "qty_hasil", "harga_per_kg", "tanggal", "waktu"
        ]

    def get_harga_per_kg(self, obj):
        return str(obj.harga_per_kg) if obj.harga_per_kg else "0.00"