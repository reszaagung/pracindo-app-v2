from django.db import models
from .cabang import CabangToko

class PenerimaanBarang(models.Model):
    nomor_penerimaan = models.CharField(max_length=50, unique=True)
    cabang = models.ForeignKey(CabangToko, on_delete=models.CASCADE, related_name='riwayat_penerimaan')
    referensi_logistik = models.CharField(max_length=100, blank=True, null=True)
    tanggal_kirim = models.DateTimeField(null=True, blank=True)
    tanggal_terima = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[('DIKIRIM', 'DIKIRIM'), ('DITERIMA SEBAGIAN', 'DITERIMA SEBAGIAN'), ('SELESAI', 'SELESAI')],
        default='DIKIRIM'
    )
    keterangan = models.TextField(blank=True)

    class Meta:
        db_table = 'retail_penerimaan_barang'
        ordering = ['-tanggal_terima']

    def __str__(self):
        return f"{self.nomor_penerimaan} - {self.cabang.kode}"

class ItemPenerimaan(models.Model):
    penerimaan = models.ForeignKey(PenerimaanBarang, on_delete=models.CASCADE, related_name='items')
    produk = models.ForeignKey('master.MasterProduk', on_delete=models.PROTECT)
    entitas = models.ForeignKey(
        'core.Entitas', on_delete=models.PROTECT, null=True, blank=True,
        related_name='item_penerimaan_retail',
        help_text='Pemilik barang, dibawa dari ItemDistribusi.',
    )
    kemasan = models.CharField(max_length=50)
    unit_dikirim = models.IntegerField(default=0)
    unit_diterima = models.IntegerField(default=0)

    class Meta:
        db_table = 'retail_item_penerimaan'