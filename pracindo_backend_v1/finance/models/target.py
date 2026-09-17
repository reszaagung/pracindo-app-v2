from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from akunting.models import TipeAkun

from .base import BaseFinanceModel


class RevenueTarget(BaseFinanceModel):
    entitas = models.ForeignKey(
        'core.Entitas', on_delete=models.PROTECT, related_name='revenue_targets',
    )
    akun_pendapatan = models.ForeignKey(
        'akunting.Akun', on_delete=models.PROTECT, related_name='revenue_targets',
    )
    tahun = models.PositiveSmallIntegerField()
    bulan = models.PositiveSmallIntegerField()
    nominal_target = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'finance_revenue_target'
        ordering = ['-tahun', '-bulan']
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
        if self.akun_pendapatan_id and self.akun_pendapatan.tipe != TipeAkun.PENDAPATAN:
            raise ValidationError({'akun_pendapatan': 'Harus akun bertipe Pendapatan.'})


class COGSTarget(BaseFinanceModel):
    entitas = models.ForeignKey(
        'core.Entitas', on_delete=models.PROTECT, related_name='cogs_targets',
    )
    akun_cogs = models.ForeignKey(
        'akunting.Akun', on_delete=models.PROTECT, related_name='cogs_targets',
    )
    tahun = models.PositiveSmallIntegerField()
    bulan = models.PositiveSmallIntegerField()
    nominal_target = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'finance_cogs_target'
        ordering = ['-tahun', '-bulan']
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
        # Bagan akun ini tidak punya tipe khusus HPP — 5100 (HPP) dan 6100
        # (beban umum) sama-sama BEBAN. Validasi sengaja longgar; membedakan
        # HPP lewat prefix kode akun terlalu rapuh.
        if self.akun_cogs_id and self.akun_cogs.tipe != TipeAkun.BEBAN:
            raise ValidationError({'akun_cogs': 'Harus akun bertipe Beban (HPP).'})