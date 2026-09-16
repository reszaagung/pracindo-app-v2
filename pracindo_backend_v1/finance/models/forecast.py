from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseFinanceModel


class Forecast(BaseFinanceModel):
    """
    Snapshot proyeksi per periode. Append-only: perhitungan ulang membuat
    baris baru, tidak menimpa yang lama, supaya tren revisi bisa dibaca.

    Nilai dashboard = baris terbaru per periode (ORDER BY dibuat_pada DESC).
    Tidak pernah mengubah General Ledger.
    """

    periode = models.ForeignKey(
        'core.PeriodeAkuntansi', on_delete=models.PROTECT, related_name='forecasts',
    )
    forecast_revenue       = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    forecast_cogs          = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    forecast_opex          = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    forecast_other_income  = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    forecast_other_expense = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    catatan = models.TextField(blank=True)

    class Meta:
        db_table = 'finance_forecast'
        ordering = ['-dibuat_pada']
        verbose_name_plural = 'Forecast'
        indexes = [
            models.Index(fields=['periode', '-dibuat_pada'], name='ix_forecast_terbaru'),
        ]

    def __str__(self):
        return f"Forecast {self.periode} @ {self.dibuat_pada:%Y-%m-%d}"

    @property
    def entitas(self):
        """Tidak disimpan ulang — periode sudah membawa entitas."""
        return self.periode.entitas

    @property
    def forecast_gross_profit(self):
        return self.forecast_revenue - self.forecast_cogs

    @property
    def forecast_operating_profit(self):
        return self.forecast_gross_profit - self.forecast_opex

    @property
    def forecast_net_profit(self):
        return (
            self.forecast_operating_profit
            + self.forecast_other_income
            - self.forecast_other_expense
        )

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError(
                'Forecast append-only — buat baris baru, jangan update yang lama.'
            )
        super().save(*args, **kwargs)