# models.py
from django.db import models


class StikerBesar(models.Model):
    """Master data template. Satu baris per kombinasi jenis+pola,
    misal: stiker_polos_besar_AABB"""

    nama_file = models.CharField(max_length=100, unique=True)
    file_template = models.FileField(upload_to="template_stiker_besar/")
    aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ["nama_file"]
        verbose_name = "Template Stiker Besar"
        verbose_name_plural = "Template Stiker Besar"

    def __str__(self):
        return self.nama_file


class GenerateStikerBesar(models.Model):
    """Satu baris = satu batch cetak (satu lembar/set stiker)."""

    total_unit = models.PositiveIntegerField(default=0)
    pola_terdeteksi = models.CharField(max_length=10, blank=True, null=True)
    alamat_file = models.ForeignKey(
        StikerBesar, on_delete=models.SET_NULL, null=True, blank=True
    )
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    file_hasil = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        ordering = ["-dibuat_pada"]
        verbose_name = "Generate Stiker Besar"
        verbose_name_plural = "Generate Stiker Besar"

    def __str__(self):
        return f"GenerateStikerBesar #{self.pk} ({self.pola_terdeteksi or '-'})"


class ItemCetak(models.Model):
    """Satu baris = satu 'nilai' milik satu huruf/grup dalam pola.
    Untuk pola AABB akan ada 2 baris (grup A dan grup B)."""

    generate = models.ForeignKey(
        GenerateStikerBesar, on_delete=models.CASCADE, related_name="item_set"
    )
    grup = models.CharField(
        max_length=1,
        verbose_name="Grup Pola",
        help_text="Posisi dalam pola, mis. huruf 'A' pada AABB — bukan tipe barang.",
    )
    nama_item = models.CharField(max_length=255, verbose_name="Nama Barang")
    tipe = models.CharField(
        max_length=100,
        verbose_name="Tipe Barang",
        help_text="Klasifikasi barang, independen dari grup pola.",
    )
    lot = models.DateField(verbose_name="Tanggal Lot")
    net = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Net (KGS)")

    class Meta:
        unique_together = [("generate", "grup")]
        ordering = ["grup"]
        verbose_name = "Item Cetak"
        verbose_name_plural = "Item Cetak"

    def __str__(self):
        return f"{self.grup} - {self.nama_item}"