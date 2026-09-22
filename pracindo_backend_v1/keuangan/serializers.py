from rest_framework import serializers

from .models import PengeluaranKas


class PengeluaranKasSerializer(serializers.ModelSerializer):
    entitas_kode = serializers.CharField(
        source="entitas.kode",
        read_only=True,
    )
    mutasi_id = serializers.IntegerField(
        source="mutasi.id",
        read_only=True,
    )

    class Meta:
        model = PengeluaranKas
        fields = [
            "id",
            "entitas",
            "entitas_kode",
            "kategori",
            "keterangan",
            "pemohon",
            "nominal",
            "bukti_nota",
            "mutasi",
            "mutasi_id",
            "dibuat_pada",
            "diubah_pada",
        ]
        read_only_fields = [
            "id",
            "entitas_kode",
            "mutasi",
            "mutasi_id",
            "dibuat_pada",
            "diubah_pada",
        ]


class InputPengeluaranSerializer(serializers.Serializer):
    entitas = serializers.CharField(
        max_length=32,
    )
    kategori = serializers.CharField(
        max_length=50,
    )
    keterangan = serializers.CharField(
        max_length=255,
    )
    pemohon = serializers.CharField(
        max_length=120,
    )
    nominal = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
    )
    bukti_nota = serializers.FileField(
        required=False,
        allow_null=True,
    )

    def validate_nominal(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Nominal harus lebih besar dari nol."
            )
        return value

    def validate_entitas(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Entitas wajib diisi."
            )

        return value

    def validate_kategori(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Kategori wajib diisi."
            )

        return value

    def validate_keterangan(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Keterangan wajib diisi."
            )

        return value

    def validate_pemohon(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Pemohon wajib diisi."
            )

        return value