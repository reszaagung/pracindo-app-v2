from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from .base import BaseFinanceModel


class BasisPeriode(models.TextChoices):
    BULANAN = 'BULANAN', 'Bulanan'
    TAHUNAN = 'TAHUNAN', 'Tahunan'


class StatusBudget(models.TextChoices):
    DRAFT   = 'DRAFT',   'Draft'
    AKTIF   = 'AKTIF',   'Aktif'
    DITUTUP = 'DITUTUP', 'Ditutup'
    BATAL   = 'BATAL',   'Batal'


class Budget(BaseFinanceModel):
    """
    Header anggaran. Bukan transaksi akuntansi — tidak pernah membuat jurnal.

    Dikunci ke tahun, bukan ke PeriodeAkuntansi, karena satu budget
    membawahi 12 bulan sekaligus. Penguncian per bulan tetap dibaca dari
    core.PeriodeAkuntansi.ditutup oleh service, bukan dari sini.
    """

    entitas = models.ForeignKey(
        'core.Entitas', on_delete=models.PROTECT, related_name='budgets',
    )
    nama  = models.CharField(max_length=150)
    tahun = models.PositiveSmallIntegerField()
    basis_periode = models.CharField(
        max_length=10, choices=BasisPeriode.choices, default=BasisPeriode.BULANAN,
    )
    status = models.CharField(
        max_length=10, choices=StatusBudget.choices,
        default=StatusBudget.DRAFT, db_index=True,
    )
    versi = models.PositiveIntegerField(default=1)
    keterangan = models.TextField(blank=True)

    class Meta:
        db_table = 'finance_budget'
        ordering = ['-tahun', 'nama', '-versi']
        verbose_name_plural = 'Budget'
        constraints = [
            models.UniqueConstraint(
                fields=['entitas', 'nama', 'tahun', 'versi'],
                name='uq_budget_entitas_nama_tahun_versi',
            ),
        ]

    def __str__(self):
        return f"{self.nama} {self.tahun} v{self.versi}"

    @property
    def terkunci(self):
        return self.status in (StatusBudget.DITUTUP, StatusBudget.BATAL)

    @property
    def total_anggaran(self):
        """Dihitung on-the-fly. Sengaja bukan field tersimpan supaya tidak
        pernah out-of-sync dengan baris di bawahnya."""
        return self.lines.aggregate(t=models.Sum('nominal_anggaran'))['t'] or 0


class BudgetLine(BaseFinanceModel):
    """
    Rincian anggaran per akun COA. Titik sambung ke akunting: service
    budget-vs-actual join langsung lewat akun_id, tanpa mapping manual.
    """

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='lines')
    akun = models.ForeignKey(
        'akunting.Akun', on_delete=models.PROTECT, related_name='budget_lines',
    )
    bulan = models.PositiveSmallIntegerField(
        help_text='0 = seluruh tahun (basis TAHUNAN); 1–12 = bulan spesifik.',
    )
    nominal_anggaran = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    keterangan = models.TextField(blank=True)

    class Meta:
        db_table = 'finance_budget_line'
        ordering = ['budget', 'bulan', 'akun']
        verbose_name_plural = 'Budget line'
        constraints = [
            models.UniqueConstraint(
                fields=['budget', 'akun', 'bulan'],
                name='uq_budgetline_budget_akun_bulan',
            ),
            models.CheckConstraint(
                condition=Q(bulan__gte=0) & Q(bulan__lte=12),
                name='ck_budgetline_bulan_valid',
            ),
            models.CheckConstraint(
                condition=Q(nominal_anggaran__gte=0),
                name='ck_budgetline_nominal_non_negatif',
            ),
        ]
        indexes = [models.Index(fields=['budget', 'akun'], name='ix_budgetline_budget_akun')]

    def __str__(self):
        return f"{self.budget.nama} — {self.akun} ({self.bulan})"

    def clean(self):
        if self.akun_id and not self.akun.aktif:
            raise ValidationError({'akun': 'Akun yang dipilih tidak aktif.'})
        if self.budget_id and self.budget.terkunci:
            raise ValidationError('Budget DITUTUP/BATAL — baris tidak bisa diubah.')

    def save(self, *args, **kwargs):
        # Guard terakhir di level model: LOCKED harus ditolak lewat jalur
        # apa pun, bukan cuma lewat form/serializer.
        if self.budget_id and self.budget.terkunci:
            raise ValidationError('Budget DITUTUP/BATAL — baris tidak bisa diubah.')
        super().save(*args, **kwargs)