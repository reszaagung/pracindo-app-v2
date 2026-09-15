# retail/models.py
from django.db import models
from django.conf import settings

class CabangToko(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='cabang_toko'
    )
    kode = models.CharField(max_length=20, unique=True, blank=True)
    nama = models.CharField(max_length=100)
    alamat = models.TextField(blank=True, null=True)
    aktif = models.BooleanField(default=True)

    class Meta:
        db_table = 'retail_cabang_toko'
        verbose_name = "Cabang Toko"
        verbose_name_plural = "Cabang Tokos"

    def save(self, *args, **kwargs):
        if not self.kode:
            last_cabang = CabangToko.objects.filter(kode__startswith='pcjm-cbg-').order_by('id').last()
            
            if last_cabang:
                try:
                    last_number = int(last_cabang.kode.split('-')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1                
            
            self.kode = f"pcjm-cbg-{new_number:04d}"
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.kode} - {self.nama}"