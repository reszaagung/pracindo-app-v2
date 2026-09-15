from django.contrib import admin
from .models import (
    CabangToko, StokRetail, MutasiStokRetail, SesiKasir, TransaksiPOS, ItemTransaksi,
    BukuHutangRetail, RiwayatBayarHutang, KategoriAkun, AkunBukuBesar, 
    TransaksiJurnal, DetailJurnal, SalesRetail, BonusSales, PelangganRetail,
    BukuPiutangRetail, RiwayatBayarPiutang, PenerimaanBarang, ItemPenerimaan,
    SelisihKasir, SelisihStok
)

@admin.register(CabangToko)
class CabangTokoAdmin(admin.ModelAdmin):
    # Ditambahkan 'user' untuk mempermudah identifikasi akun login cabang
    list_display = ('kode', 'nama', 'user', 'aktif')
    search_fields = ('kode', 'nama', 'user__username')

@admin.register(StokRetail)
class StokRetailAdmin(admin.ModelAdmin):
    list_display = ('cabang', 'produk', 'kemasan', 'total_unit', 'harga_jual')
    list_filter = ('cabang',)
    search_fields = ('produk__nama',)

@admin.register(SalesRetail)
class SalesRetailAdmin(admin.ModelAdmin):
    list_display = ('nama', 'cabang', 'persentase_bonus', 'aktif')
    list_filter = ('cabang', 'aktif')
    search_fields = ('nama',)

@admin.register(PenerimaanBarang)
class PenerimaanBarangAdmin(admin.ModelAdmin):
    list_display = ('nomor_penerimaan', 'cabang', 'referensi_logistik', 'status', 'tanggal_terima')
    list_filter = ('status', 'cabang')

@admin.register(TransaksiPOS)
class TransaksiPOSAdmin(admin.ModelAdmin):
    list_display = ('nomor_struk', 'sesi', 'waktu_transaksi', 'grand_total', 'metode_bayar', 'status')
    list_filter = ('status', 'metode_bayar')
    search_fields = ('nomor_struk',)

@admin.register(BukuPiutangRetail)
class BukuPiutangRetailAdmin(admin.ModelAdmin):
    list_display = ('pelanggan', 'transaksi', 'jatuh_tempo', 'total_piutang', 'total_dibayar', 'status')
    list_filter = ('status',)
    search_fields = ('pelanggan__nama',)

@admin.register(PelangganRetail)
class PelangganRetailAdmin(admin.ModelAdmin):
    list_display = ('nama', 'cabang', 'nomor_telepon', 'limit_piutang')
    list_filter = ('cabang',)
    search_fields = ('nama', 'nomor_telepon')

admin.site.register(MutasiStokRetail)
admin.site.register(SesiKasir)
admin.site.register(ItemTransaksi)
admin.site.register(BukuHutangRetail)
admin.site.register(RiwayatBayarHutang)
admin.site.register(KategoriAkun)
admin.site.register(AkunBukuBesar)
admin.site.register(TransaksiJurnal)
admin.site.register(DetailJurnal)
admin.site.register(BonusSales)
admin.site.register(RiwayatBayarPiutang)
admin.site.register(ItemPenerimaan)
admin.site.register(SelisihKasir)
admin.site.register(SelisihStok)