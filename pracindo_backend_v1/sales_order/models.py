from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from core.models import TimeStampedModel
from master.models import Pelanggan, Produk
from .utils import generate_nomor_so_dinamis

class StatusSO(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    DISETUJUI = 'DISETUJUI', 'Disetujui'
    SELESAI = 'SELESAI', 'Selesai'
    BATAL = 'BATAL', 'Batal'

class SalesOrder(TimeStampedModel):
    nomor_so = models.CharField(max_length=50, unique=True, blank=True)
    tanggal = models.DateField()
    entitas = models.ForeignKey(
        'core.Entitas',
        on_delete=models.PROTECT,
        related_name='sales_orders',
        null=True,
        blank=True
    )
    pelanggan = models.ForeignKey(
        Pelanggan,
        on_delete=models.PROTECT,
        related_name='sales_orders'
    )
    catatan = models.TextField(blank=True)
    status = models.CharField(
        max_length=15,
        choices=StatusSO.choices,
        default=StatusSO.DRAFT,
        db_index=True
    )
    ppn_persen = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0'))
    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0'))
    ppn_nominal = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0'))
    grand_total = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0'))

    class Meta:
        db_table = 'tx_sales_order'
        ordering = ['-tanggal', '-nomor_so']
        verbose_name_plural = 'Sales Order'

    def __str__(self):
        return f"{self.nomor_so} - {self.pelanggan.nama}"

    def save(self, *args, **kwargs):
        if not self.nomor_so:
            self.nomor_so = generate_nomor_so_dinamis(
                model_class=SalesOrder,
                entitas=self.entitas,
                tanggal=self.tanggal
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.status != StatusSO.DRAFT:
            raise ValidationError('Hanya Sales Order berstatus DRAFT yang boleh dihapus.')
        super().delete(*args, **kwargs)

class SalesOrderItem(TimeStampedModel):
    sales_order = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE,
        related_name='items'
    )
    produk = models.ForeignKey(
        Produk,
        on_delete=models.PROTECT,
        related_name='so_items'
    )
    qty = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    harga_jual = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0'))

    class Meta:
        db_table = 'tx_sales_order_item'
        ordering = ['id']
        verbose_name_plural = 'Sales Order Items'

    def __str__(self):
        return f"{self.sales_order.nomor_so} - {self.produk.nama}"

    def save(self, *args, **kwargs):
        if self.qty and self.harga_jual:
            self.subtotal = self.qty * self.harga_jual
        super().save(*args, **kwargs)