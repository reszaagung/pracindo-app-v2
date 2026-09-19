from django.db import models
from .cabang import CabangToko


class StokRetail(models.Model):
    """
    Stok barang jadi di cabang.

    Punya `entitas` karena barang milik grup PT boleh dititipkan di gudang
    cabang tapi tidak dijual eceran — kasir menyaringnya lewat kolom ini.
    Uniknya ikut entitas supaya barang yang sama dari dua pemilik berbeda
    tidak saling menimpa.
    """
    cabang = models.ForeignKey(CabangToko, on_delete=models.CASCADE, related_name='stok')
    produk = models.ForeignKey('master.MasterProduk', on_delete=models.CASCADE)
    entitas = models.ForeignKey(
        'core.Entitas', on_delete=models.PROTECT, null=True, blank=True,
        related_name='stok_retail',
        help_text='Pemilik barang. Kosong untuk data lama sebelum kolom ini ada.',
    )
    kemasan = models.CharField(max_length=50, default='PCS')
    total_unit = models.IntegerField(default=0)
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ('cabang', 'produk', 'kemasan', 'entitas')
        db_table = 'retail_stok'

    def __str__(self):
        pemilik = self.entitas.kode if self.entitas_id else '-'
        return f"[{pemilik}] {self.produk.nama_item} ({self.kemasan}) - {self.total_unit} unit"
        
class MutasiStokRetail(models.Model):
    JENIS_MUTASI = [
        ('PENERIMAAN', 'Penerimaan Barang (Inbound)'),
        ('PENJUALAN', 'Penjualan Kasir (Outbound)'),
        ('RETUR', 'Retur Penjualan (Inbound)'),
        ('PENYESUAIAN', 'Penyesuaian Stok / Opname')
    ]

    stok = models.ForeignKey(StokRetail, on_delete=models.CASCADE, related_name='riwayat_mutasi')
    tanggal = models.DateTimeField(auto_now_add=True)
    jenis = models.CharField(max_length=20, choices=JENIS_MUTASI)
    referensi = models.CharField(max_length=100)
    unit_masuk = models.IntegerField(default=0)
    unit_keluar = models.IntegerField(default=0)
    saldo_akhir = models.IntegerField(default=0)
    keterangan = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'retail_mutasi_stok'
        ordering = ['-tanggal', '-id']