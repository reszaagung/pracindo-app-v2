# admin.py
from django.contrib import admin
from .models import StikerBesar, GenerateStikerBesar, ItemCetak


@admin.register(StikerBesar)
class StikerBesarAdmin(admin.ModelAdmin):
    list_display = ("nama_file", "aktif")
    list_filter = ("aktif",)
    search_fields = ("nama_file",)


class ItemCetakInline(admin.TabularInline):
    model = ItemCetak
    extra = 1


@admin.register(GenerateStikerBesar)
class GenerateStikerBesarAdmin(admin.ModelAdmin):
    list_display = ("id", "pola_terdeteksi", "alamat_file", "total_unit", "dibuat_pada")
    list_filter = ("pola_terdeteksi",)
    readonly_fields = ("pola_terdeteksi", "alamat_file")
    inlines = [ItemCetakInline]