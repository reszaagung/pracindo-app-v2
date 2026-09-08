from django.db import models
from .cabang import CabangToko

class StokRetail(models.Model):
    cabang = models.ForeignKey(CabangToko, on_delete=models.CASCADE, related_name='stok')
    produk = models.ForeignKey('master.Produk', on_delete=models.CASCADE)
    kemasan = models.CharField(max_length=50, default='PCS')
    total_unit = models.IntegerField(default=0)
    harga_jual = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ('cabang', 'produk', 'kemasan')
        db_table = 'retail_stok'

    def __str__(self):
        return f"{self.produk.nama} ({self.kemasan}) - {self.total_unit} unit"

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