from django.db import models
from django.conf import settings
from .cabang import CabangToko
from .sales import SalesRetail

class PelangganRetail(models.Model):
    # Tambahkan baris ini
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    cabang = models.ForeignKey(CabangToko, on_delete=models.CASCADE, related_name='pelanggan')
    nama = models.CharField(max_length=100)
    nomor_telepon = models.CharField(max_length=20, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    limit_piutang = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    default_tempo_hari = models.IntegerField(default=30)
    sales = models.ForeignKey(SalesRetail, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'retail_pelanggan'

    def __str__(self):
        return self.nama