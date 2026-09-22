from decimal import Decimal

from rest_framework import serializers

from .models import Batch, Tangki


class TangkiSerializer(serializers.ModelSerializer):
    nama_hasil = serializers.SerializerMethodField()
    harga_per_kg = serializers.SerializerMethodField()

    class Meta:
        model = Tangki
        fields = [
            "id",
            "kode",
            "nama",
            "aktif",
            "kapasitas_kg",
            "saldo_kg",
            "saldo_nilai",
            "harga_per_kg",
            "nama_hasil",
        ]

    def get_nama_hasil(self, obj):
        batch = (
            Batch.objects
            .filter(
                tangki=obj,
                posted_at__isnull=False,
            )
            .order_by(
                "-posted_at",
                "-waktu",
                "-id",
            )
            .first()
        )

        if not batch:
            return ""

        return batch.nama_hasil or ""

    def get_harga_per_kg(self, obj):
        saldo_kg = obj.saldo_kg or Decimal("0")
        saldo_nilai = obj.saldo_nilai or Decimal("0")

        if saldo_kg <= 0:
            return "0.000000"

        return str(
            saldo_nilai / saldo_kg
        )


class BatchSerializer(serializers.ModelSerializer):
    tangki_kode = serializers.CharField(
        source="tangki.kode",
        read_only=True,
    )

    tangki_tujuan_nama = serializers.CharField(
        source="tangki.nama",
        read_only=True,
    )

    batch = serializers.CharField(
        source="nomor",
        read_only=True,
    )

    harga_per_kg = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = [
            "id",
            "batch",
            "nomor",
            "jenis",
            "nama_hasil",
            "tangki",
            "tangki_kode",
            "tangki_tujuan_nama",
            "qty_hasil",
            "harga_per_kg",
            "tanggal",
            "waktu",
        ]

    def get_harga_per_kg(self, obj):
        return (
            str(obj.harga_per_kg)
            if obj.harga_per_kg
            else "0.00"
        )