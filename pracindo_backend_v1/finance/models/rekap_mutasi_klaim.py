from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from .base import BaseFinanceModel


class RekapMutasiKlaim(BaseFinanceModel):
    """Snapshot mutasi klaim per entitas per bulan.

    Sumber: inventory.MutasiKlaim (setor/tarik hak entitas atas pool) dan
    inventory.SaldoEntitas untuk saldo akhir.

    saldo_akhir WAJIB disnapshot: SaldoEntitas hanya menyimpan saldo
    berjalan tanpa histori, jadi bulan lampau tidak bisa direkonstruksi.

    Pemisahan PT/CV lewat entitas, satu baris per entitas per bulan."""

    entitas = models.ForeignKey(
        'core.Entitas', on_delete=models.PROTECT, related_name='rekap_klaim',
    )
    tahun = models.PositiveSmallIntegerField()
    bulan = models.PositiveSmallIntegerField()

    jumlah_mutasi = models.PositiveIntegerField(default=0)
    qty_setor = models.DecimalField(max_digits=18, decimal_places=3, default=0)
    nilai_setor = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    qty_tarik = models.DecimalField(max_digits=18, decimal_places=3, default=0)
    nilai_tarik = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    saldo_akhir = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    qty_setor_kumulatif = models.DecimalField(max_digits=18, decimal_places=3, default=0)
    qty_tarik_kumulatif = models.DecimalField(max_digits=18, decimal_places=3, default=0)

    dihitung_pada = models.DateTimeField(auto_now=True)
    dibekukan = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'finance_rekap_mutasi_klaim'
        ordering = ['-tahun', '-bulan', 'entitas']
        verbose_name = 'Rekap mutasi klaim'
        verbose_name_plural = 'Rekap mutasi klaim'
        constraints = [
            models.UniqueConstraint(
                fields=['entitas', 'tahun', 'bulan'],
                name='uq_rekap_klaim_entitas_tahun_bulan',
            ),
            models.CheckConstraint(
                condition=Q(bulan__gte=1) & Q(bulan__lte=12),
                name='ck_rekap_klaim_bulan_valid',
            ),
        ]
        indexes = [models.Index(fields=['tahun', 'bulan'], name='ix_rekap_klaim_periode')]

    def __str__(self):
        return f"Rekap klaim {self.entitas.kode} {self.bulan:02d}/{self.tahun}"

    @property
    def mutasi_bersih(self):
        """Setor dikurangi tarik dalam bulan ini."""
        return self.nilai_setor - self.nilai_tarik

    @property
    def qty_bersih(self):
        return self.qty_setor - self.qty_tarik

    def save(self, *args, **kwargs):
        if self.pk:
            lama = RekapMutasiKlaim.objects.filter(pk=self.pk).only('dibekukan').first()
            if lama and lama.dibekukan:
                raise ValidationError('Rekap sudah dibekukan, tidak bisa diubah.')
        super().save(*args, **kwargs)
