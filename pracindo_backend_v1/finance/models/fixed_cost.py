from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from .base import BaseFinanceModel


class FixedCost(BaseFinanceModel):
    """
    Biaya tetap/berulang sebagai input planning.

    FixedCost != actual expense. Baris di sini tidak pernah memposting
    jurnal; actual tetap datang dari transaksi yang di-posting akunting.
    Dicocokkan ke satu bulan lewat overlap tanggal, bukan FK ke periode.
    """

    entitas = models.ForeignKey(
        'core.Entitas', on_delete=models.PROTECT, related_name='fixed_costs',
    )
    akun_beban = models.ForeignKey(
        'akunting.Akun', on_delete=models.PROTECT, related_name='fixed_costs',
    )
    nama = models.CharField(max_length=150)
    nominal_bulanan = models.DecimalField(max_digits=18, decimal_places=2)
    tanggal_mulai   = models.DateField()
    tanggal_selesai = models.DateField(null=True, blank=True)
    aktif = models.BooleanField(default=True, db_index=True)
    auto_masuk_budget = models.BooleanField(
        default=False,
        help_text='Hanya memengaruhi baseline budget/planning. '
                  'Tidak pernah membuat expense actual.',
    )
    keterangan = models.TextField(blank=True)

    class Meta:
        db_table = 'finance_fixed_cost'
        ordering = ['-tanggal_mulai', 'nama']
        verbose_name_plural = 'Fixed cost'
        constraints = [
            models.CheckConstraint(
                condition=Q(nominal_bulanan__gte=0),
                name='ck_fixedcost_nominal_non_negatif',
            ),
            models.CheckConstraint(
                condition=Q(tanggal_selesai__isnull=True)
                          | Q(tanggal_selesai__gte=models.F('tanggal_mulai')),
                name='ck_fixedcost_tanggal_valid',
            ),
        ]
        indexes = [
            models.Index(
                fields=['aktif', 'tanggal_mulai', 'tanggal_selesai'],
                name='ix_fixedcost_periode_aktif',
            ),
        ]

    def __str__(self):
        return self.nama

    def clean(self):
        # TODO: akun_beban wajib bertipe BEBAN — nunggu nama field tipe
        # di akunting.Akun.
        if self.tanggal_selesai and self.tanggal_mulai:
            if self.tanggal_selesai < self.tanggal_mulai:
                raise ValidationError(
                    {'tanggal_selesai': 'Tanggal selesai tidak boleh sebelum tanggal mulai.'}
                )

    def berlaku_pada(self, tahun, bulan):
        """Helper untuk forecast/budget service — overlap tanggal, bukan FK."""
        import calendar
        from datetime import date

        awal = date(tahun, bulan, 1)
        akhir = date(tahun, bulan, calendar.monthrange(tahun, bulan)[1])
        return (
            self.aktif
            and self.tanggal_mulai <= akhir
            and (self.tanggal_selesai is None or self.tanggal_selesai >= awal)
        )