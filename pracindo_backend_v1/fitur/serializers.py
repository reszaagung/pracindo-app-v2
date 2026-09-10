from rest_framework import serializers
from .models import StikerBesar, GenerateStikerBesar, ItemCetak

class StikerBesarSerializer(serializers.ModelSerializer):
    class Meta:
        model = StikerBesar
        fields = ["id", "nama_file", "aktif"]

class ItemCetakInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCetak
        fields = ["nama_item", "tipe", "lot", "net"]

class ItemCetakSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCetak
        fields = ["id", "grup", "nama_item", "tipe", "lot", "net"]

class GenerateStikerBesarInputSerializer(serializers.Serializer):
    jenis = serializers.ChoiceField(choices=["polos_besar", "cv_besar"])
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