from django.contrib import admin
from .models import BuktiTerima, Kendaraan, Pengiriman, Perhentian, Retur

class PerhentianInline(admin.TabularInline):
    model = Perhentian
    extra = 0
    readonly_fields = ('waktu_sampai',)

@admin.register(Pengiriman)
class PengirimanAdmin(admin.ModelAdmin):
    list_display = ('nomor', 'tanggal', 'kurir', 'kendaraan', 'status')
    list_filter = ('status', 'entitas', 'tanggal')
    search_fields = ('nomor', 'kurir__username', 'perhentian__pelanggan_nama')
    list_select_related = ('kurir', 'kendaraan', 'entitas')
    readonly_fields = ('nomor', 'waktu_berangkat', 'waktu_selesai', 'dibuat_oleh', 'dibuat_pada')
    inlines = [PerhentianInline]

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Kendaraan)
class KendaraanAdmin(admin.ModelAdmin):
    list_display = ('kode', 'nama', 'plat_nomor', 'kapasitas_kg', 'aktif')
    list_filter = ('aktif',)
    search_fields = ('kode', 'nama', 'plat_nomor')

@admin.register(BuktiTerima)
class BuktiTerimaAdmin(admin.ModelAdmin):
    list_display = ('perhentian', 'waktu', 'diunggah_oleh')
    readonly_fields = [f.name for f in BuktiTerima._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Retur)
class ReturAdmin(admin.ModelAdmin):
    list_display = ('perhentian', 'dicatat_pada', 'dicatat_oleh', 'stok_dikembalikan', 'disetujui_oleh')
    list_filter = ('stok_dikembalikan',)
    readonly_fields = ('dicatat_oleh', 'dicatat_pada', 'disetujui_oleh', 'disetujui_pada', 'stok_dikembalikan')