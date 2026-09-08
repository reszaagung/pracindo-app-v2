from django.db import models
from .cabang import CabangToko

class SelisihKasir(models.Model):
    sesi = models.ForeignKey('SesiKasir', on_delete=models.CASCADE, related_name='riwayat_selisih')
    waktu_lapor = models.DateTimeField(auto_now_add=True)
    saldo_sistem = models.DecimalField(max_digits=12, decimal_places=2)
    saldo_aktual = models.DecimalField(max_digits=12, decimal_places=2)
    selisih = models.DecimalField(max_digits=12, decimal_places=2)
    keterangan = models.TextField(blank=True, null=True)
    diselesaikan = models.BooleanField(default=False)

    class Meta:
        db_table = 'retail_selisih_kasir'

    def __str__(self):
        return f"Selisih {self.sesi} - {self.selisih}"

class SelisihStok(models.Model):
    cabang = models.ForeignKey(CabangToko, on_delete=models.CASCADE)
    produk = models.ForeignKey('master.Produk', on_delete=models.CASCADE)
    kemasan = models.CharField(max_length=50)
    waktu_lapor = models.DateTimeField(auto_now_add=True)
    stok_sistem = models.IntegerField()
    stok_aktual = models.IntegerField()
    selisih = models.IntegerField()
    keterangan = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=[('PENDING', 'PENDING'), ('DISETUJUI', 'DISETUJUI'), ('DITOLAK', 'DITOLAK')], 
        default='PENDING'
    )

    class Meta:
        db_table = 'retail_selisih_stok'

    def __str__(self):
        return f"Selisih {self.produk.nama} ({self.kemasan}) - {self.selisih} unit"