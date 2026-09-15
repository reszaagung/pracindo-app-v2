# serializers.py
from rest_framework import serializers
from .models import StikerBesar, GenerateStikerBesar, ItemCetak ,StikerKecil12, GenerateStikerKecil12, ItemCetakKecil12
import string

class StikerBesarSerializer(serializers.ModelSerializer):
    class Meta:
        model = StikerBesar
        fields = ["id", "nama_file", "aktif"]


class ItemCetakInputSerializer(serializers.ModelSerializer):
    """Input dari user — belum ada 'grup', itu baru ditentukan
    setelah algoritma chunking jalan."""

    class Meta:
        model = ItemCetak
        fields = ["nama_item", "tipe", "lot", "net"]


class ItemCetakSerializer(serializers.ModelSerializer):
    """Untuk menampilkan hasil, sudah termasuk 'grup'."""

    class Meta:
        model = ItemCetak
        fields = ["id", "grup", "nama_item", "tipe", "lot", "net"]


class GenerateStikerBesarInputSerializer(serializers.Serializer):
    jenis = serializers.ChoiceField(choices=["polos_besar", "cv_besar", "pt_besar"])
    pola = serializers.ChoiceField(choices=["AAAA", "AAAB", "AABB", "AABC", "ABCD"])
    items = ItemCetakInputSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Minimal harus ada 1 item.")
        if len(value) > 4:  
            raise serializers.ValidationError("Maksimal 4 item per lembar.")
        return value


class GenerateStikerBesarSerializer(serializers.ModelSerializer):
    item_set = ItemCetakSerializer(many=True, read_only=True)
    alamat_file = StikerBesarSerializer(read_only=True)

    class Meta:
        model = GenerateStikerBesar
        fields = ["id", "total_unit", "pola_terdeteksi", "alamat_file", "item_set", "dibuat_pada", "file_hasil"]
        read_only_fields = fields



JUMLAH_SLOT_KECIL12 = 12

def _validasi_pola_kontigu_kecil12(pola):
    huruf_unik = list(dict.fromkeys(pola))
    huruf_diharapkan = string.ascii_uppercase[:len(huruf_unik)]
    if list(huruf_unik) != list(huruf_diharapkan):
        raise serializers.ValidationError(
            f"Pola tidak valid: huruf harus dimulai dari A dan berurutan (dapat: {''.join(huruf_unik)})."
        )

class StikerKecil12Serializer(serializers.ModelSerializer):
    class Meta:
        model = StikerKecil12
        fields = ["id", "nama_file", "aktif"]

class ItemCetakKecil12InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCetakKecil12
        fields = ["nama_item", "tipe", "lot", "net"]

class ItemCetakKecil12Serializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCetakKecil12
        fields = ["id", "grup", "nama_item", "tipe", "lot", "net"]

class GenerateStikerKecil12InputSerializer(serializers.Serializer):
    jenis = serializers.ChoiceField(choices=["polos_kecil", "cv_kecil", "pt_kecil"])  # sesuaikan kalau beda
    pola = serializers.CharField(max_length=JUMLAH_SLOT_KECIL12, min_length=JUMLAH_SLOT_KECIL12)
    items = ItemCetakKecil12InputSerializer(many=True)

    def validate_pola(self, value):
        value = value.upper()
        if not value.isalpha():
            raise serializers.ValidationError("Pola hanya boleh berisi huruf.")
        _validasi_pola_kontigu_kecil12(value)
        return value

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Minimal harus ada 1 item.")
        if len(value) > JUMLAH_SLOT_KECIL12:
            raise serializers.ValidationError(f"Maksimal {JUMLAH_SLOT_KECIL12} item per lembar.")
        return value

    def validate(self, data):
        huruf_unik = list(dict.fromkeys(data["pola"]))
        if len(huruf_unik) != len(data["items"]):
            raise serializers.ValidationError(
                f"Pola '{data['pola']}' butuh {len(huruf_unik)} item unik, tapi {len(data['items'])} dikirim."
            )
        return data

class GenerateStikerKecil12Serializer(serializers.ModelSerializer):
    item_set = ItemCetakKecil12Serializer(many=True, read_only=True)
    alamat_file = StikerKecil12Serializer(read_only=True)

    class Meta:
        model = GenerateStikerKecil12
        fields = ["id", "total_unit", "pola_terdeteksi", "alamat_file", "item_set", "dibuat_pada", "file_hasil"]
        read_only_fields = fields