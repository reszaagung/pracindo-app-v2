from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.db import models, transaction
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.utils import timezone

from core.models import DiauditModel, TimeStampedModel


D0 = Decimal("0")
Q_RP = Decimal("0.01")
Q_QTY = Decimal("0.001")
Q_HARGA = Decimal("0.000001")


def rp(x):
    return Decimal(str(x)).quantize(
        Q_RP,
        rounding=ROUND_HALF_UP,
    )


def qty(x):
    return Decimal(str(x)).quantize(
        Q_QTY,
        rounding=ROUND_HALF_UP,
    )


def harga(x):
    return Decimal(str(x)).quantize(
        Q_HARGA,
        rounding=ROUND_HALF_UP,
    )


class StatusDokumen(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    POSTED = "POSTED", "Diposting"
    VOID = "VOID", "Dibatalkan"


class SumberPembelian(models.TextChoices):
    PENERIMAAN = "PENERIMAAN", "Dari penerimaan gudang"
    MANUAL = "MANUAL", "Input manual (saldo awal / koreksi)"


class PoolResource(TimeStampedModel):
    """
    Pool stok raw material bersama.

    Tidak terikat entitas.
    Seluruh stok fisik satu produk digabung.
    Nilai digunakan untuk weighted-average cost.
    """

    produk = models.ForeignKey(
        "master.Produk",
        on_delete=models.PROTECT,
        related_name="pool_resource",
    )

    qty_kg = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=D0,
    )

    nilai = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=D0,
    )

    class Meta:
        db_table = "inventory_pool_resource"
        ordering = ["produk"]
        verbose_name = "Pool Resource"
        verbose_name_plural = "Pool Resources"

        constraints = [
            UniqueConstraint(
                fields=["produk"],
                name="inv_pool_res_unik_per_produk",
            ),
            CheckConstraint(
                condition=Q(qty_kg__gte=0),
                name="inv_pool_res_qty_non_negatif",
            ),
            CheckConstraint(
                condition=Q(nilai__gte=0),
                name="inv_pool_res_nilai_non_negatif",
            ),
            CheckConstraint(
                condition=(
                    ~Q(qty_kg=0)
                    | Q(nilai=0)
                ),
                name="inv_pool_res_kosong_tanpa_nilai",
            ),
        ]

    def __str__(self):
        return (
            f"{self.produk.kode} - "
            f"{self.produk.nama}: "
            f"{self.qty_kg}"
        )

    @property
    def harga_rata(self):
        if self.qty_kg <= 0:
            return D0

        return harga(
            self.nilai / self.qty_kg
        )


class Pembelian(DiauditModel):
    nomor = models.CharField(
        max_length=48,
        unique=True,
        editable=False,
    )

    no_po = models.CharField(
        max_length=64,
        blank=True,
        default="",
        db_index=True,
    )

    entitas = models.ForeignKey(
        "core.Entitas",
        on_delete=models.PROTECT,
        related_name="pembelian_pool",
    )

    grup_bahan = models.ForeignKey(
        "core.GrupBahan",
        on_delete=models.PROTECT,
        related_name="pembelian_pool",
    )

    produk = models.ForeignKey(
        "master.Produk",
        on_delete=models.PROTECT,
        related_name="pembelian_pool",
    )

    # Basis nilai akuntansi / material
    qty_kg = models.DecimalField(
        max_digits=18,
        decimal_places=3,
    )

    harga_per_kg = models.DecimalField(
        max_digits=20,
        decimal_places=6,
    )

    nilai = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    # Basis operasional untuk kemasan.
    # Untuk produk non-kemasan boleh NULL.
    qty_unit = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=None,
    )

    harga_per_unit = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        null=True,
        blank=True,
        default=None,
    )

    kategori_kemasan = models.CharField(
        max_length=20,
        choices=(
            ("PRIMER", "Primer"),
            ("SEKUNDER", "Sekunder"),
            ("PRIMER_SEKUNDER", "Primer & Sekunder"),
        ),
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )

    tanggal = models.DateField(
        db_index=True,
    )

    waktu = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    status = models.CharField(
        max_length=10,
        choices=StatusDokumen.choices,
        default=StatusDokumen.DRAFT,
        db_index=True,
    )

    sumber = models.CharField(
        max_length=12,
        choices=SumberPembelian.choices,
        default=SumberPembelian.MANUAL,
        db_index=True,
    )

    penerimaan_item = models.OneToOneField(
        "warehouse.PenerimaanItem",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pembelian",
    )

    catatan = models.TextField(
        blank=True,
        default="",
    )

    posted_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        db_table = "inventory_pembelian"
        ordering = ["-waktu", "-id"]
        verbose_name = "Pembelian"
        verbose_name_plural = "Pembelian"

        indexes = [
            models.Index(
                fields=["entitas", "waktu"],
                name="ix_beli_entitas",
            ),
            models.Index(
                fields=["tanggal", "status"],
                name="ix_beli_tanggal",
            ),
        ]

        constraints = [
            CheckConstraint(
                condition=Q(qty_kg__gt=0),
                name="ck_beli_qty_positif",
            ),
            CheckConstraint(
                condition=Q(harga_per_kg__gte=0),
                name="ck_beli_harga_non_negatif",
            ),
            CheckConstraint(
                condition=Q(nilai__gte=0),
                name="ck_beli_nilai_non_negatif",
            ),
            CheckConstraint(
                condition=(
                    ~Q(
                        sumber=SumberPembelian.PENERIMAAN
                    )
                    | Q(
                        penerimaan_item__isnull=False
                    )
                ),
                name="ck_beli_penerimaan_ada_jejak",
            ),
        ]

    def __str__(self):
        return self.nomor

    def delete(self, *args, **kwargs):
        raise models.ProtectedError(
            "Pembelian tidak bisa dihapus. Terbitkan VOID.",
            [self],
        )


class Kemasan(TimeStampedModel):
    """
    Master ukuran kemasan barang jadi.

    Ini berbeda dengan PoolKemasan.
    Kemasan = master ukuran.
    PoolKemasan = stok fisik kemasan.
    """

    nama = models.CharField(
        max_length=40,
        unique=True,
    )

    bobot_kg = models.DecimalField(
        max_digits=10,
        decimal_places=3,
    )

    aktif = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "inventory_kemasan"
        ordering = ["nama"]
        verbose_name = "Kemasan"
        verbose_name_plural = "Kemasan"

        constraints = [
            CheckConstraint(
                condition=Q(bobot_kg__gt=0),
                name="ck_kemasan_bobot_positif",
            ),
        ]

    def __str__(self):
        return self.nama


class Packing(DiauditModel):
    nomor = models.CharField(
        max_length=48,
        unique=True,
        editable=False,
    )

    entitas = models.ForeignKey(
        "core.Entitas",
        on_delete=models.PROTECT,
        related_name="packing",
    )

    tangki = models.ForeignKey(
        "produksi.Tangki",
        on_delete=models.PROTECT,
        related_name="packing_set",
    )

    nama_hasil = models.ForeignKey(
        "master.MasterProduk",
        on_delete=models.PROTECT,
        related_name="packing_hasil",
    )

    # ========================================================
    # KEMASAN PRIMER — WAJIB
    # ========================================================

    kemasan_primer = models.ForeignKey(
        "PoolKemasan",
        on_delete=models.PROTECT,
        related_name="packing_primer",
    )

    # ========================================================
    # KEMASAN SEKUNDER — OPSIONAL
    # ========================================================

    kemasan_sekunder = models.ForeignKey(
        "PoolKemasan",
        on_delete=models.PROTECT,
        related_name="packing_sekunder",
        null=True,
        blank=True,
    )

    qty_kemasan_sekunder = models.PositiveIntegerField(
        default=0,
    )

    # ========================================================
    # OUTPUT
    # ========================================================

    total_unit = models.PositiveIntegerField()

    qty_kg = models.DecimalField(
        max_digits=18,
        decimal_places=3,
    )

    # ========================================================
    # COST BAHAN / HPP
    # ========================================================

    harga_per_kg = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        default=D0,
    )

    # Nilai total packing:
    # bahan + primer + sekunder
    cost_nom = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=D0,
    )

    # Snapshot historis biaya kemasan.
    # Penting untuk rollback / VOID.
    nilai_kemasan_primer = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=D0,
    )

    nilai_kemasan_sekunder = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=D0,
    )

    menghabiskan = models.BooleanField(
        default=False,
    )

    # ========================================================
    # WAKTU
    # ========================================================

    tanggal = models.DateField(
        default=timezone.localdate,
        db_index=True,
    )

    waktu = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    # ========================================================
    # STATUS
    # ========================================================

    status = models.CharField(
        max_length=10,
        choices=StatusDokumen.choices,
        default=StatusDokumen.DRAFT,
        db_index=True,
    )

    posted_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        db_index=True,
    )

    voided_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        db_index=True,
    )

    class Meta:
        db_table = "inventory_packing"
        ordering = ["-waktu", "-id"]
        verbose_name = "Packing"
        verbose_name_plural = "Packing"

        indexes = [
            models.Index(
                fields=["tangki", "status"],
                name="ix_pack_tangki_baru",
            ),
            models.Index(
                fields=["entitas", "waktu"],
                name="ix_pack_entitas",
            ),
            models.Index(
                fields=["nama_hasil", "status"],
                name="ix_pack_hasil_baru",
            ),
        ]

        constraints = [
            CheckConstraint(
                condition=Q(qty_kg__gt=0),
                name="ck_pack_qty_positif",
            ),
            CheckConstraint(
                condition=Q(total_unit__gt=0),
                name="ck_pack_unit_positif",
            ),
            CheckConstraint(
                condition=Q(cost_nom__gte=0),
                name="ck_pack_nilai_non_negatif",
            ),
            CheckConstraint(
                condition=Q(nilai_kemasan_primer__gte=0),
                name="ck_pack_nilai_primer_nonneg",
            ),
            CheckConstraint(
                condition=Q(nilai_kemasan_sekunder__gte=0),
                name="ck_pack_nilai_sekunder_nonneg",
            ),

            # DRAFT:
            # belum posting dan belum VOID
            models.CheckConstraint(
                condition=(
                    Q(
                        status=StatusDokumen.DRAFT,
                        posted_at__isnull=True,
                        voided_at__isnull=True,
                    )
                    |
                    Q(
                        status=StatusDokumen.POSTED,
                        posted_at__isnull=False,
                        voided_at__isnull=True,
                    )
                    |
                    Q(
                        status=StatusDokumen.VOID,
                        posted_at__isnull=False,
                        voided_at__isnull=False,
                    )
                ),
                name="ck_pack_status_konsisten",
            ),

            # Sekunder kosong berarti qty harus 0.
            # Sekunder ada berarti qty > 0.
            models.CheckConstraint(
                condition=(
                    Q(
                        kemasan_sekunder__isnull=True,
                        qty_kemasan_sekunder=0,
                    )
                    |
                    Q(
                        kemasan_sekunder__isnull=False,
                        qty_kemasan_sekunder__gt=0,
                    )
                ),
                name="ck_pack_sekunder_konsisten",
            ),
        ]

    def save(self, *args, **kwargs):
        # JANGAN otomatis mengubah DRAFT menjadi POSTED.
        # Posting hanya boleh dilakukan oleh service.
        if not self.nomor:
            with transaction.atomic():
                last = (
                    Packing.objects
                    .select_for_update()
                    .filter(
                        entitas=self.entitas
                    )
                    .order_by("-id")
                    .first()
                )

                urutan = 1

                if last and last.nomor:
                    try:
                        urutan = (
                            int(
                                last.nomor
                                .split("-")[-1]
                            )
                            + 1
                        )
                    except (
                        ValueError,
                        IndexError,
                    ):
                        urutan = 1

                self.nomor = (
                    f"PKG-{self.entitas_id}-"
                    f"{urutan:03d}"
                )

                super().save(
                    *args,
                    **kwargs,
                )

                return

        super().save(
            *args,
            **kwargs,
        )

    def __str__(self):
        return self.nomor


class TipeMutasi(models.TextChoices):
    SETOR = "SETOR", "Setoran (pembelian raw)"
    TARIK = "TARIK", "Penarikan (packing barang jadi)"
    RUGI = "RUGI", "Beban susut produksi"
    PENYESUAIAN = "PENYESUAIAN", "Penyesuaian manual"


class MutasiKlaim(models.Model):
    entitas = models.ForeignKey(
        "core.Entitas",
        on_delete=models.PROTECT,
        related_name="mutasi_klaim",
    )

    grup_bahan = models.ForeignKey(
        "core.GrupBahan",
        on_delete=models.PROTECT,
        related_name="mutasi_klaim",
    )

    tipe = models.CharField(
        max_length=14,
        choices=TipeMutasi.choices,
    )

    arah = models.SmallIntegerField()

    qty_kg = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=D0,
    )

    nilai = models.DecimalField(
        max_digits=20,
        decimal_places=2,
    )

    ref_type = models.CharField(
        max_length=30,
    )

    ref_id = models.BigIntegerField()

    keterangan = models.TextField(
        blank=True,
        default="",
    )

    waktu = models.DateTimeField(
        db_index=True,
    )

    dibuat_pada = models.DateTimeField(
        auto_now_add=True,
    )

    dibuat_oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="+",
        editable=False,
    )

    class Meta:
        db_table = "inventory_mutasi_klaim"
        ordering = ["waktu", "id"]
        verbose_name_plural = "Mutasi klaim"

        indexes = [
            models.Index(
                fields=[
                    "entitas",
                    "waktu",
                    "id",
                ],
                name="ix_mutasi_entitas",
            ),
        ]

        constraints = [
            UniqueConstraint(
                fields=[
                    "ref_type",
                    "ref_id",
                    "tipe",
                    "entitas",
                ],
                name="uq_mutasi_idempoten",
            ),
            CheckConstraint(
                condition=Q(arah__in=[-1, 1]),
                name="ck_mutasi_arah_valid",
            ),
            CheckConstraint(
                condition=Q(nilai__gte=0),
                name="ck_mutasi_nilai_non_negatif",
            ),
        ]

    def __str__(self):
        return (
            f"{self.entitas.kode} "
            f"{self.tipe} "
            f"{self.arah:+d} "
            f"{self.nilai}"
        )

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError(
                "MutasiKlaim bersifat append-only."
            )

        super().save(
            *args,
            **kwargs,
        )

    def delete(self, *args, **kwargs):
        raise ValueError(
            "MutasiKlaim tidak boleh dihapus."
        )


class SaldoEntitas(TimeStampedModel):
    entitas = models.OneToOneField(
        "core.Entitas",
        on_delete=models.CASCADE,
        related_name="saldo_klaim",
    )

    total_setor = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=D0,
    )

    total_tarik = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=D0,
    )

    total_rugi = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=D0,
    )

    qty_setor = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=D0,
    )

    qty_tarik = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=D0,
    )

    saldo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=D0,
    )

    class Meta:
        db_table = "inventory_saldo_entitas"
        verbose_name = "Saldo entitas"
        verbose_name_plural = "Saldo entitas"

    def __str__(self):
        return (
            f"{self.entitas.kode}: "
            f"{self.saldo}"
        )


class KategoriKemasan(models.TextChoices):
    PRIMER = "PRIMER", "Primer"
    SEKUNDER = "SEKUNDER", "Sekunder"
    PRIMER_SEKUNDER = (
        "PRIMER_SEKUNDER",
        "Primer & Sekunder",
    )


class PoolKemasan(TimeStampedModel):
    """
    Pool stok kemasan bersama.

    Tidak terikat entitas.
    Seluruh stok satu produk kemasan digabung.
    Nilai dihitung dengan weighted-average cost per unit.
    """

    produk = models.ForeignKey(
        "master.Produk",
        on_delete=models.PROTECT,
        related_name="pool_kemasan",
    )

    kategori = models.CharField(
        max_length=20,
        choices=KategoriKemasan.choices,
        default=KategoriKemasan.PRIMER,
        db_index=True,
    )

    qty_unit = models.IntegerField(
        default=0,
    )

    nilai = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=D0,
    )

    class Meta:
        db_table = "inventory_pool_kemasan"
        ordering = ["kategori", "produk"]

        verbose_name = "Pool Kemasan"
        verbose_name_plural = "Pool Kemasan"

        constraints = [
            UniqueConstraint(
                fields=["produk"],
                name="inv_pool_kms_unik_per_produk",
            ),
            CheckConstraint(
                condition=Q(qty_unit__gte=0),
                name="inv_pool_kms_qty_non_negatif",
            ),
            CheckConstraint(
                condition=Q(nilai__gte=0),
                name="inv_pool_kms_nilai_non_negatif",
            ),
            CheckConstraint(
                condition=(
                    ~Q(qty_unit=0)
                    | Q(nilai=0)
                ),
                name="inv_pool_kms_kosong_tanpa_nilai",
            ),
        ]

    def __str__(self):
        return (
            f"{self.produk.kode} - "
            f"{self.produk.nama}: "
            f"{self.qty_unit} Unit"
        )

    @property
    def harga_satuan(self):
        if self.qty_unit <= 0:
            return D0

        return harga(
            self.nilai
            / Decimal(self.qty_unit)
        )


class StokBarangJadi(TimeStampedModel):
    entitas = models.ForeignKey(
        "core.Entitas",
        on_delete=models.PROTECT,
        related_name="stok_barang_jadi",
    )

    grup_bahan = models.ForeignKey(
        "core.GrupBahan",
        on_delete=models.PROTECT,
        related_name="stok_barang_jadi",
    )

    item = models.ForeignKey(
        "master.MasterProduk",
        on_delete=models.PROTECT,
        related_name="stok_barang_jadi",
    )

    kemasan = models.ForeignKey(
        "Kemasan",
        on_delete=models.PROTECT,
        related_name="stok_barang_jadi",
    )

    qty_unit = models.IntegerField(
        default=0,
    )

    qty_kg = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=D0,
    )

    nilai = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=D0,
        help_text=(
            "Nilai persediaan, akumulasi dari "
            "Packing.cost_nom. Bukan harga jual."
        ),
    )

    class Meta:
        db_table = "inventory_stok_barang_jadi"
        verbose_name = "Stok Barang Jadi"
        verbose_name_plural = "Stok Barang Jadi"

        constraints = [
            UniqueConstraint(
                fields=[
                    "entitas",
                    "grup_bahan",
                    "item",
                    "kemasan",
                ],
                name="uq_stok_jadi_unik",
            ),
            CheckConstraint(
                condition=Q(qty_unit__gte=0),
                name="ck_stok_jadi_unit_non_negatif",
            ),
            CheckConstraint(
                condition=Q(qty_kg__gte=0),
                name="ck_stok_jadi_kg_non_negatif",
            ),
            CheckConstraint(
                condition=Q(nilai__gte=0),
                name="ck_stok_jadi_nilai_non_negatif",
            ),
            CheckConstraint(
                condition=(
                    ~Q(qty_unit=0)
                    | Q(nilai=0)
                ),
                name="ck_stok_jadi_kosong_tanpa_nilai",
            ),
        ]

    def __str__(self):
        return (
            f"[{self.entitas.kode}] "
            f"{self.item} - "
            f"{self.qty_unit} Unit"
        )

    @property
    def nilai_per_unit(self):
        if self.qty_unit <= 0:
            return D0

        return rp(
            self.nilai
            / Decimal(self.qty_unit)
        )


class StokItemsPabrik(TimeStampedModel):
    entitas = models.ForeignKey(
        "core.Entitas",
        on_delete=models.PROTECT,
        related_name="stok_items_pabrik",
    )

    grup_bahan = models.ForeignKey(
        "core.GrupBahan",
        on_delete=models.PROTECT,
        related_name="stok_items_pabrik",
    )

    item = models.ForeignKey(
        "master.MasterProduk",
        on_delete=models.PROTECT,
        related_name="stok_items_pabrik",
    )

    qty_kg = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=D0,
    )

    class Meta:
        db_table = "inventory_stok_items_pabrik"
        verbose_name = "Stok Items Pabrik"
        verbose_name_plural = "Stok Items Pabrik"

        constraints = [
            UniqueConstraint(
                fields=[
                    "entitas",
                    "grup_bahan",
                    "item",
                ],
                name="uq_stok_pabrik_unik",
            ),
            CheckConstraint(
                condition=Q(qty_kg__gte=0),
                name="ck_stok_pabrik_kg_non_negatif",
            ),
        ]

    def __str__(self):
        return (
            f"[{self.entitas.kode}] "
            f"{self.item} - "
            f"{self.qty_kg} Kg"
        )

