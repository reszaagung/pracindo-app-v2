from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from .base import BaseFinanceModel


class RekapPurchaseOrder(BaseFinanceModel):
    """Rekap nilai PO per entitas per bulan. Komitmen pembelian, bukan
    actual akuntansi. Snapshot: boleh digenerate ulang selama belum
    dibekukan. Pemisahan PT/CV lewat entitas."""

    entitas = models.ForeignKey(
        'core.Entitas', on_delete=models.PROTECT, related_name='rekap_po',
    )
    tahun = models.PositiveSmallIntegerField()
    bulan = models.PositiveSmallIntegerField()
    jumlah_po = models.PositiveIntegerField(default=0)
    jumlah_item = models.PositiveIntegerField(default=0)
    nilai_pesan = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    nilai_diterima = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    nilai_ppn = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    dihitung_pada = models.DateTimeField(auto_now=True)
    dibekukan = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'finance_rekap_purchase_order'
        ordering = ['-tahun', '-bulan', 'entitas']
        verbose_name = 'Rekap purchase order'
        verbose_name_plural = 'Rekap purchase order'
        constraints = [
            models.UniqueConstraint(
                fields=['entitas', 'tahun', 'bulan'],
                name='uq_rekap_po_entitas_tahun_bulan',
            ),
            models.CheckConstraint(
                condition=Q(bulan__gte=1) & Q(bulan__lte=12),
                name='ck_rekap_po_bulan_valid',
            ),
        ]
        indexes = [models.Index(fields=['tahun', 'bulan'], name='ix_rekap_po_periode')]

    def __str__(self):
        return f"Rekap PO {self.entitas.kode} {self.bulan:02d}/{self.tahun}"

    @property
    def nilai_belum_diterima(self):
        return self.nilai_pesan - self.nilai_diterima

    @property
    def nilai_pesan_dengan_ppn(self):
        return self.nilai_pesan + self.nilai_ppn

    def save(self, *args, **kwargs):
        if self.pk:
            lama = RekapPurchaseOrder.objects.filter(pk=self.pk).only('dibekukan').first()
            if lama and lama.dibekukan:
                raise ValidationError('Rekap sudah dibekukan, tidak bisa diubah.')
        super().save(*args, **kwargs)


class RekapMutasiProduksi(BaseFinanceModel):
    """Snapshot mutasi produksi per bulan. Global, tanpa entitas: Tangki
    dan Batch resource bersama tanpa kepemilikan entitas."""

    tahun = models.PositiveSmallIntegerField()
    bulan = models.PositiveSmallIntegerField()

    batch_mixing = models.PositiveIntegerField(default=0)
    batch_blending = models.PositiveIntegerField(default=0)

    qty_hasil = models.DecimalField(max_digits=18, decimal_places=3, default=0)
    nilai_hasil = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    qty_susut = models.DecimalField(max_digits=18, decimal_places=3, default=0)
    nilai_susut = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    qty_packing = models.DecimalField(max_digits=18, decimal_places=3, default=0)
    nilai_packing = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    wip_akhir_kg = models.DecimalField(max_digits=18, decimal_places=3, default=0)
    wip_akhir_nilai = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pool_akhir_nilai = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pool_kemasan_akhir_nilai = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    dihitung_pada = models.DateTimeField(auto_now=True)
    dibekukan = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'finance_rekap_mutasi_produksi'
        ordering = ['-tahun', '-bulan']
        verbose_name = 'Rekap mutasi produksi'
        verbose_name_plural = 'Rekap mutasi produksi'
        constraints = [
            models.UniqueConstraint(
                fields=['tahun', 'bulan'], name='uq_rekap_produksi_tahun_bulan',
            ),
            models.CheckConstraint(
                condition=Q(bulan__gte=1) & Q(bulan__lte=12),
                name='ck_rekap_produksi_bulan_valid',
            ),
        ]

    def __str__(self):
        return f"Rekap produksi {self.bulan:02d}/{self.tahun}"

    @property
    def total_batch(self):
        return self.batch_mixing + self.batch_blending

    @property
    def persediaan_akhir(self):
        return (self.wip_akhir_nilai + self.pool_akhir_nilai
                + self.pool_kemasan_akhir_nilai)

    @property
    def rasio_susut(self):
        dasar = self.qty_hasil + self.qty_susut
        return (self.qty_susut / dasar) if dasar > 0 else 0

    def save(self, *args, **kwargs):
        if self.pk:
            lama = RekapMutasiProduksi.objects.filter(pk=self.pk).only('dibekukan').first()
            if lama and lama.dibekukan:
                raise ValidationError('Rekap sudah dibekukan, tidak bisa diubah.')
        super().save(*args, **kwargs)
