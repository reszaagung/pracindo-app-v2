from django.db import models

from .base import BaseFinanceModel
from .period import PeriodeFinance


class TipeForecast(models.TextChoices):
    REVENUE = "REVENUE", "Revenue"
    COGS = "COGS", "COGS"
    GROSS_PROFIT = "GROSS_PROFIT", "Gross Profit"
    OPEX = "OPEX", "OPEX"
    OPERATING_PROFIT = "OPERATING_PROFIT", "Operating Profit"
    OTHER_INCOME = "OTHER_INCOME", "Other Income"
    OTHER_EXPENSE = "OTHER_EXPENSE", "Other Expense"
    NET_PROFIT = "NET_PROFIT", "Net Profit"
    CASH = "CASH", "Cash"
    RECEIVABLE = "RECEIVABLE", "Receivable"
    PAYABLE = "PAYABLE", "Payable"
    INVENTORY = "INVENTORY", "Inventory"


class MetodeForecast(models.TextChoices):
    MANUAL = "MANUAL", "Manual"
    RUN_RATE = "RUN_RATE", "Run Rate"
    LINEAR_PROJECTION = "LINEAR_PROJECTION", "Linear Projection"
    WEIGHTED_AVERAGE = "WEIGHTED_AVERAGE", "Weighted Average"


class Forecast(BaseFinanceModel):
    periode = models.ForeignKey(
        PeriodeFinance, on_delete=models.PROTECT, related_name="forecasts"
    )
    tipe_forecast = models.CharField(max_length=20, choices=TipeForecast.choices)
    nominal_forecast = models.DecimalField(max_digits=18, decimal_places=2)
    metode = models.CharField(
        max_length=20, choices=MetodeForecast.choices, default=MetodeForecast.RUN_RATE
    )
    tanggal_snapshot = models.DateTimeField(auto_now_add=True)
    asumsi = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["periode", "tipe_forecast", "-tanggal_snapshot"],
                name="idx_forecast_latest",
            )
        ]
        ordering = ["-tanggal_snapshot"]

    def __str__(self):
        return f"{self.periode.nama_periode} — {self.tipe_forecast} @ {self.tanggal_snapshot:%Y-%m-%d}"

    def save(self, *args, **kwargs):
        # Append-only (PRD §6.7 & kriteria penerimaan §10): baris yang
        # udah punya pk nggak boleh di-save ulang. Service forecast harus
        # selalu .create() baris baru, nggak pernah .update().
        if self.pk is not None:
            raise ValueError("Forecast bersifat append-only — buat baris baru, jangan update yang lama.")
        super().save(*args, **kwargs)