from django.contrib import admin

from .models import (
    LaporanSelisih, PenerimaanBarang, PenerimaanItem,
    Distribusi, ItemDistribusi
)

class PenerimaanItemInline(admin.TabularInline):
    model = PenerimaanItem
    extra = 0
    autocomplete_fields = ('po_item',)
    readonly_fields = ('qty_deklarasi', 'selisih_berat')

    @admin.display(description='Selisih berat')
    def selisih_berat(self, obj):
        return obj.selisih_berat if obj.pk else '-'

class LaporanSelisihInline(admin.TabularInline):
    model = LaporanSelisih
    extra = 0
    fields = ('nomor', 'jenis', 'qty_selisih', 'nilai_selisih',
              'status', 'resolusi', 'nilai_klaim')
    readonly_fields = ('nomor', 'nilai_selisih')
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(PenerimaanBarang)
class PenerimaanBarangAdmin(admin.ModelAdmin):
    list_display = ('nomor', 'tanggal', 'purchase_order', 'no_surat_jalan',
                    'ada_selisih', 'dibuat_oleh')
    list_filter = ('ada_selisih', 'tanggal')
    search_fields = ('nomor', 'no_surat_jalan', 'purchase_order__no_po')
    list_select_related = ('purchase_order',)
    readonly_fields = ('nomor', 'ada_selisih', 'dibuat_oleh', 'dibuat_pada')
    inlines = [PenerimaanItemInline, LaporanSelisihInline]

    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(LaporanSelisih)
class LaporanSelisihAdmin(admin.ModelAdmin):
    list_display = ('nomor', 'tanggal', 'penerimaan', 'jenis',
                    'qty_selisih', 'nilai_selisih', 'status',
                    'resolusi', 'nilai_klaim', 'umur')
    list_filter = ('status', 'jenis', 'resolusi', 'tanggal')
    search_fields = ('nomor', 'penerimaan__nomor', 'uraian')
    list_select_related = ('penerimaan',)
    readonly_fields = ('nomor', 'nilai_selisih', 'diselesaikan_pada',
                       'diselesaikan_oleh', 'dibuat_oleh', 'dibuat_pada')

    @admin.display(description='Umur')
    def umur(self, obj):
        return f"{obj.umur_hari} hari"

    def has_delete_permission(self, request, obj=None):
        return False


# =========================================================
# ADMIN DISTRIBUSI (OUTBOUND)
# =========================================================

class ItemDistribusiInline(admin.TabularInline):
    model = ItemDistribusi
    extra = 0
    autocomplete_fields = ('produk',)

@admin.register(Distribusi)
class DistribusiAdmin(admin.ModelAdmin):
    list_display = ('nomor', 'tanggal_dibuat', 'pelanggan_nama', 'jenis_tujuan', 'berat_total_kg', 'status')
    list_filter = ('status', 'jenis_tujuan', 'tanggal_dibuat')
    search_fields = ('nomor', 'pelanggan_nama', 'alamat')
    list_select_related = ('entitas', 'tujuan_cabang')
    
    readonly_fields = ('nomor', 'tanggal_dibuat', 'waktu_terkirim', 'diterima_oleh')
    inlines = [ItemDistribusiInline]

    def has_delete_permission(self, request, obj=None):
        # Distribusi hanya boleh dihapus jika masih DRAFT (belum masuk ke logistik)
        if obj and obj.status != 'DRAFT':
            return False
        return super().has_delete_permission(request, obj)