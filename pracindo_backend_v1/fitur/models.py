# models.py
from django.db import models


class StikerBesar(models.Model):
    """Master data template. Satu baris per kombinasi jenis+pola,
    misal: stiker_polos_besar_AABB"""

    nama_file = models.CharField(max_length=100, unique=True)
    file_template = models.FileField(upload_to="templates/stiker_besar/")
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
    generate = models.ForeignKey(
        GenerateStikerBesar, on_delete=models.CASCADE, related_name="item_set"
    )
    grup = models.CharField(
        max_length=1,
        verbose_name="Grup Pola",
        help_text="Posisi dalam pola, mis. huruf 'A' pada AABB — bukan tipe barang.",
    )
    nama_item = models.ForeignKey(
        "master.MasterProduk", on_delete=models.PROTECT, related_name="packing_hasil_besar"
    )
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

class StikerKecil12(models.Model):
    """Master data template untuk stiker kecil dengan 12 slot fisik.
    Sama prinsipnya dengan StikerBesar: satu baris per kombinasi
    jenis+pola, mis. stiker_polos_kecil_AABBCCDDEEFF."""

    nama_file = models.CharField(max_length=100, unique=True)
    file_template = models.FileField(upload_to="templates/stiker_kecil_12/")
    aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ["nama_file"]
        verbose_name = "Template Stiker Kecil (12 Slot)"
        verbose_name_plural = "Template Stiker Kecil (12 Slot)"

    def __str__(self):
        return self.nama_file


class GenerateStikerKecil12(models.Model):
    """Satu baris = satu batch cetak stiker kecil 12 slot."""

    total_unit = models.PositiveIntegerField(default=0)
    pola_terdeteksi = models.CharField(max_length=15, blank=True, null=True)
    alamat_file = models.ForeignKey(
        StikerKecil12, on_delete=models.SET_NULL, null=True, blank=True
    )
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    file_hasil = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-dibuat_pada"]
        verbose_name = "Generate Stiker Kecil (12 Slot)"
        verbose_name_plural = "Generate Stiker Kecil (12 Slot)"

    def __str__(self):
        return f"GenerateStikerKecil12 #{self.pk} ({self.pola_terdeteksi or '-'})"


class ItemCetakKecil12(models.Model):
    """Satu baris = satu 'nilai' milik satu huruf/grup dalam pola.
    Untuk pola AABBCCDDEEFF akan ada 6 baris (grup A sampai F)."""

    generate = models.ForeignKey(
        GenerateStikerKecil12, on_delete=models.CASCADE, related_name="item_set"
    )
    grup = models.CharField(
        max_length=1,
        verbose_name="Grup Pola",
        help_text="Posisi dalam pola, mis. huruf 'A' pada AABBCC... — bukan tipe barang.",
    )
    nama_item = models.ForeignKey(
        "master.MasterProduk", on_delete=models.PROTECT,
        related_name="packing_hasil_kecil12",
        null=True, blank=True,
    )
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
        verbose_name = "Item Cetak Kecil (12 Slot)"
        verbose_name_plural = "Item Cetak Kecil (12 Slot)"

    def __str__(self):
        return f"{self.grup} - {self.nama_item}"


        