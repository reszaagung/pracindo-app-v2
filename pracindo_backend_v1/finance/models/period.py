from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseFinanceModel


class TipePeriode(models.TextChoices):
    BULANAN = "BULANAN", "Bulanan"
    TRIWULAN = "TRIWULAN", "Triwulan"
    SEMESTERAN = "SEMESTERAN", "Semesteran"
    TAHUNAN = "TAHUNAN", "Tahunan"


class StatusPeriode(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    AKTIF = "AKTIF", "Aktif"
    CLOSED = "CLOSED", "Closed"


class PeriodeFinance(BaseFinanceModel):
    nama_periode = models.CharField(max_length=100)
    tipe_periode = models.CharField(
        max_length=20, choices=TipePeriode.choices, default=TipePeriode.BULANAN
    )
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    tahun_fiskal = models.IntegerField()
    status = models.CharField(
        max_length=10, choices=StatusPeriode.choices, default=StatusPeriode.DRAFT
    )

    class Meta:
        ordering = ["-tanggal_mulai", "nama_periode"]
        indexes = [
            models.Index(fields=["tahun_fiskal"]),
            models.Index(fields=["tipe_periode", "status"]),
        ]
        verbose_name = "Periode Finance"
        verbose_name_plural = "Periode Finance"

    def __str__(self):
        return self.nama_periode

    def clean(self):
        # Overlap-check antar-periode dgn tipe_periode sama SENGAJA tidak di
        # sini — sesuai prinsip desain PRD (§3), itu tanggung jawab
        # service/serializer karena butuh query lintas-row.
        if self.tanggal_mulai and self.tanggal_selesai:
            if self.tanggal_selesai <= self.tanggal_mulai:
                raise ValidationError(
                    {"tanggal_selesai": "Tanggal selesai harus setelah tanggal mulai."}
                )

    @property
    def is_closed(self):
        return self.status == StatusPeriode.CLOSED