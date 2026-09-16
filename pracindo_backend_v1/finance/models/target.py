from django.db import models
from django.db.models import Q

from .base import BaseFinanceModel


class TargetBulanan(BaseFinanceModel):
    """Bentuk bersama RevenueTarget & COGSTarget: satu angka per
    (entitas, akun, tahun, bulan). Actual-nya selalu dari ledger."""

    entitas = models.ForeignKey('core.Entitas', on_delete=models.PROTECT, related_name='+')
    tahun = models.PositiveSmallIntegerField()
    bulan = models.PositiveSmallIntegerField()
    nominal_target = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        abstract = True
        ordering = ['-tahun', '-bulan']


class RevenueTarget(TargetBulanan):
    entitas = models.ForeignKey(
        'core.Entitas', on_delete=models.PROTECT, related_name='revenue_targets',
    )
    akun_pendapatan = models.ForeignKey(
        'akunting.Akun', on_delete=models.PROTECT, related_name='revenue_targets',
    )

    class Meta(TargetBulanan.Meta):
        abstract = False
        db_table = 'finance_revenue_target'
        verbose_name_plural = 'Revenue target'
        constraints = [
            models.UniqueConstraint(
                fields=['entitas', 'akun_pendapatan', 'tahun', 'bulan'],
                name='uq_revenuetarget_entitas_akun_tahun_bulan',
            ),
            models.CheckConstraint(
                condition=Q(bulan__gte=1) & Q(bulan__lte=12),
                name='ck_revenuetarget_bulan_valid',
            ),
        ]

    def __str__(self):
        return f"{self.akun_pendapatan} — {self.bulan:02d}/{self.tahun}"

    def clean(self):
        # TODO: akun_pendapatan wajib bertipe PENDAPATAN.
        pass


class COGSTarget(TargetBulanan):
    entitas = models.ForeignKey(
        'core.Entitas', on_delete=models.PROTECT, related_name='cogs_targets',
    )
    akun_cogs = models.ForeignKey(
        'akunting.Akun', on_delete=models.PROTECT, related_name='cogs_targets',
    )

    class Meta(TargetBulanan.Meta):
        abstract = False
        db_table = 'finance_cogs_target'
        verbose_name_plural = 'COGS target'
        constraints = [
            models.UniqueConstraint(
                fields=['entitas', 'akun_cogs', 'tahun', 'bulan'],
                name='uq_cogstarget_entitas_akun_tahun_bulan',
            ),
            models.CheckConstraint(
                condition=Q(bulan__gte=1) & Q(bulan__lte=12),
                name='ck_cogstarget_bulan_valid',
            ),
        ]

    def __str__(self):
        return f"{self.akun_cogs} — {self.bulan:02d}/{self.tahun}"

    def clean(self):
        # TODO: akun_cogs wajib bertipe COGS/HPP.
        pass