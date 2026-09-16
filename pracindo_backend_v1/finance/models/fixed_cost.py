from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseFinanceModel


class FrekuensiFixedCost(models.TextChoices):
    BULANAN = "BULANAN", "Bulanan"
    TRIWULAN = "TRIWULAN", "Triwulan"
    TAHUNAN = "TAHUNAN", "Tahunan"


class StatusFixedCost(models.TextChoices):
    AKTIF = "AKTIF", "Aktif"
    NONAKTIF = "NONAKTIF", "Nonaktif"


class FixedCost(BaseFinanceModel):
    nama_biaya = models.CharField(max_length=150)
    akun = models.ForeignKey(
        "akunting.Akun",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="fixed_costs",
    )
    nominal = models.DecimalField(max_digits=18, decimal_places=2)
    frekuensi = models.CharField(
        max_length=10, choices=FrekuensiFixedCost.choices, default=FrekuensiFixedCost.BULANAN
    )
    tanggal_mulai = models.DateField()
    tanggal_berakhir = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=StatusFixedCost.choices, default=StatusFixedCost.AKTIF
    )
    catatan = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-tanggal_mulai", "nama_biaya"]
        indexes = [models.Index(fields=["status", "tanggal_mulai", "tanggal_berakhir"])]

    def __str__(self):
        return self.nama_biaya

    def clean(self):
        if self.tanggal_berakhir and self.tanggal_mulai:
            if self.tanggal_berakhir <= self.tanggal_mulai:
                raise ValidationError(
                    {"tanggal_berakhir": "Tanggal berakhir harus setelah tanggal mulai."}
                )

    def overlaps_periode(self, periode):
        """Helper buat forecast service nanti — cocokkan FixedCost ke
        PeriodeFinance via overlap tanggal, bukan FK langsung (PRD §6.4)."""
        akhir = self.tanggal_berakhir or periode.tanggal_selesai
        return self.tanggal_mulai <= periode.tanggal_selesai and akhir >= periode.tanggal_mulai