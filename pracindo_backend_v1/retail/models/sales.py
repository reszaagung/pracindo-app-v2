from django.db import models
from django.utils import timezone
from django.conf import settings
from .cabang import CabangToko

class SalesRetail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    cabang = models.ForeignKey(CabangToko, on_delete=models.CASCADE, related_name='sales')
    nama = models.CharField(max_length=100)
    persentase_bonus = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    aktif = models.BooleanField(default=True)

    class Meta:
        db_table = 'retail_sales'

    def __str__(self):
        return self.nama

class BonusSales(models.Model):
    sales = models.ForeignKey(SalesRetail, on_delete=models.CASCADE, related_name='bonus')
    transaksi = models.ForeignKey('TransaksiPOS', on_delete=models.CASCADE)
    tanggal = models.DateField(default=timezone.now)
    nominal_bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'retail_bonus_sales'

    def __str__(self):
        return f"{self.sales.nama} - {self.nominal_bonus}"