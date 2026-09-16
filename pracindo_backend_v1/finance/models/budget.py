from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseFinanceModel
from .period import PeriodeFinance


class KategoriBudget(models.TextChoices):
    OPEX = "OPEX", "OPEX"
    CAPEX = "CAPEX", "CAPEX"


class StatusBudget(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    SUBMITTED = "SUBMITTED", "Submitted"
    APPROVED = "APPROVED", "Approved"
    LOCKED = "LOCKED", "Locked"


class Budget(BaseFinanceModel):
    periode = models.ForeignKey(
        PeriodeFinance, on_delete=models.PROTECT, related_name="budgets"
    )
    nama_anggaran = models.CharField(max_length=150)
    kategori = models.CharField(
        max_length=10, choices=KategoriBudget.choices, default=KategoriBudget.OPEX
    )
    status = models.CharField(
        max_length=10, choices=StatusBudget.choices, default=StatusBudget.DRAFT
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="budget_approved",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    catatan = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["periode", "nama_anggaran"], name="uq_budget_periode_nama"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nama_anggaran} ({self.periode.nama_periode})"

    @property
    def total_budget(self):
        """Dihitung on-the-fly dari BudgetLine — sengaja tidak disimpan
        sbg field, biar nggak out-of-sync (PRD §6.2)."""
        return self.lines.aggregate(total=models.Sum("nominal_budget"))["total"] or 0

    @property
    def is_locked(self):
        return self.status == StatusBudget.LOCKED


class BudgetLine(BaseFinanceModel):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="lines")
    akun = models.ForeignKey(
        "akunting.Akun", on_delete=models.PROTECT, related_name="budget_lines"
    )
    nominal_budget = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    bulan = models.PositiveSmallIntegerField(null=True, blank=True)
    keterangan = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["budget", "bulan", "akun"]
        indexes = [models.Index(fields=["budget", "akun"])]

    def __str__(self):
        return f"{self.budget.nama_anggaran} — {self.akun}"

    def clean(self):
        if self.nominal_budget is not None and self.nominal_budget < 0:
            raise ValidationError({"nominal_budget": "Nominal budget tidak boleh negatif."})
        if self.bulan is not None and not (1 <= self.bulan <= 12):
            raise ValidationError({"bulan": "Bulan harus antara 1–12."})
        if self.akun_id and not self.akun.is_active:  # sesuaikan nama field kalau beda di akunting.Akun
            raise ValidationError({"akun": "Akun yang dipilih tidak aktif."})
        # Kombinasi (budget, akun, bulan) unik SENGAJA tidak jadi
        # UniqueConstraint DB — bulan nullable, NULL diperlakukan beda
        # antar-database di composite unique. Dicek di service/serializer.

    def save(self, *args, **kwargs):
        # Guard terakhir di level model spy status LOCKED beneran nggak
        # bisa ditembus lewat jalur manapun (bukan cuma UI) — kriteria
        # penerimaan PRD §10. Idealnya dicek juga di serializer.validate()
        # biar API balikin 400 yang rapi, bukan 500 dari sini.
        if self.budget_id and self.budget.status == StatusBudget.LOCKED:
            raise ValidationError("Budget berstatus LOCKED — BudgetLine tidak bisa diubah.")
        super().save(*args, **kwargs)