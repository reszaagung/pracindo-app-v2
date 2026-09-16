from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseFinanceModel
from .period import PeriodeFinance


class RevenueTarget(BaseFinanceModel):
    periode = models.ForeignKey(
        PeriodeFinance, on_delete=models.PROTECT, related_name="revenue_targets"
    )
    kategori = models.CharField(max_length=100, default="OVERALL")
    nominal_target = models.DecimalField(max_digits=18, decimal_places=2)
    catatan = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["periode", "kategori"], name="uq_revenuetarget_periode_kategori"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.periode.nama_periode} — {self.kategori}"


class COGSTarget(BaseFinanceModel):
    periode = models.ForeignKey(
        PeriodeFinance, on_delete=models.PROTECT, related_name="cogs_targets"
    )
    kategori = models.CharField(max_length=100, default="OVERALL")
    nominal_target = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    persentase_target = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    catatan = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["periode", "kategori"], name="uq_cogstarget_periode_kategori"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.periode.nama_periode} — {self.kategori}"

    def clean(self):
        if self.nominal_target is None and self.persentase_target is None:
            raise ValidationError(
                "Minimal salah satu dari nominal_target atau persentase_target harus diisi."
            )