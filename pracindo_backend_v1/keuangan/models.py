"""
Kas dan bank — sisi KEPUTUSAN atas uang.

Batas dengan akunting:
- RekeningBank adalah objek milik keuangan.
- Akun adalah objek milik akunting.
- RekeningBank hanya menyimpan relasi ke Akun sebagai akun pembukuan.

Ketergantungan satu arah:
keuangan -> akunting

MutasiKas bersifat append-only.
Saldo RekeningBank adalah saldo berjalan yang ditulis saat posting.
Saldo tidak dihitung ulang dengan SUM mutasi saat dibaca.
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

from core.constants import NILAI_DIGITS, NILAI_PLACES
from core.models import DiauditModel, TimeStampedModel


class JenisRekening(models.TextChoices):
    BANK = "BANK", "Rekening bank"
    KAS = "KAS", "Kas tunai"
    KAS_KECIL = "KAS_KECIL", "Kas kecil"


class RekeningBank(TimeStampedModel):
    entitas = models.ForeignKey(
        "core.Entitas",
        on_delete=models.PROTECT,
        related_name="rekening",
    )
    jenis = models.CharField(
        max_length=10,
        choices=JenisRekening.choices,
        db_index=True,
    )

    nama_bank = models.CharField(
        max_length=80,
        blank=True,
    )
    nomor_rekening = models.CharField(
        max_length=40,
        blank=True,
    )
    nama_pemilik = models.CharField(
        max_length=120,
        blank=True,
    )

    akun = models.ForeignKey(
        "akunting.Akun",
        on_delete=models.PROTECT,
        related_name="rekening",
    )

    saldo = models.DecimalField(
        max_digits=NILAI_DIGITS,
        decimal_places=NILAI_PLACES,
        default=Decimal("0"),
        editable=False,
        validators=[MinValueValidator(Decimal("0"))],
    )

    urutan_terakhir = models.BigIntegerField(
        default=0,
        editable=False,
    )

    aktif = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "keuangan_rekening_bank"
        ordering = ["entitas__kode", "jenis", "nama_bank", "id"]
        verbose_name = "Rekening bank"
        verbose_name_plural = "Rekening bank"
        constraints = [
            models.UniqueConstraint(
                fields=["entitas", "nomor_rekening"],
                condition=~Q(nomor_rekening=""),
                name="uq_rekening_nomor",
            ),
            models.CheckConstraint(
                condition=Q(saldo__gte=0),
                name="ck_rekening_saldo_nonneg",
            ),
            models.CheckConstraint(
                condition=Q(urutan_terakhir__gte=0),
                name="ck_rekening_urutan_nonneg",
            ),
        ]
        indexes = [
            models.Index(
                fields=["entitas", "aktif", "jenis"],
                name="ix_rekening_entitas_aktif",
            ),
        ]

    def __str__(self):
        if self.jenis == JenisRekening.BANK:
            return f"{self.nama_bank} {self.nomor_rekening} ({self.entitas.kode})"
        return f"{self.get_jenis_display()} {self.entitas.kode}"

    def clean(self):
        if self.jenis == JenisRekening.BANK:
            if not self.nama_bank.strip():
                raise ValidationError(
                    {"nama_bank": "Rekening bank wajib memiliki nama bank."}
                )

            if not self.nomor_rekening.strip():
                raise ValidationError(
                    {"nomor_rekening": "Rekening bank wajib memiliki nomor rekening."}
                )


class MutasiKas(models.Model):
    """
    Append-only dengan saldo berjalan.

    Setiap mutasi hanya boleh memiliki satu sisi:
    - debit > 0 dan kredit = 0
    - atau debit = 0 dan kredit > 0
    """

    rekening = models.ForeignKey(
        RekeningBank,
        on_delete=models.PROTECT,
        related_name="mutasi",
    )

    urutan = models.BigIntegerField()

    tanggal = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    debit = models.DecimalField(
        max_digits=NILAI_DIGITS,
        decimal_places=NILAI_PLACES,
        default=Decimal("0"),
    )

    kredit = models.DecimalField(
        max_digits=NILAI_DIGITS,
        decimal_places=NILAI_PLACES,
        default=Decimal("0"),
    )

    saldo_akhir = models.DecimalField(
        max_digits=NILAI_DIGITS,
        decimal_places=NILAI_PLACES,
    )

    keterangan = models.CharField(
        max_length=255,
        blank=True,
    )

    referensi = models.CharField(
        max_length=64,
        blank=True,
    )

    idempotency_key = models.CharField(
        max_length=96,
        unique=True,
    )

    dibuat_pada = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "keuangan_mutasi_kas"
        ordering = ["rekening", "urutan"]
        verbose_name = "Mutasi kas"
        verbose_name_plural = "Mutasi kas"
        constraints = [
            models.UniqueConstraint(
                fields=["rekening", "urutan"],
                name="uq_mutasi_kas_urutan",
            ),
            models.CheckConstraint(
                condition=Q(debit__gte=0) & Q(kredit__gte=0),
                name="ck_mutasi_kas_nonneg",
            ),
            models.CheckConstraint(
                condition=(
                    Q(debit__gt=0, kredit=0)
                    | Q(debit=0, kredit__gt=0)
                ),
                name="ck_mutasi_kas_satu_sisi",
            ),
            models.CheckConstraint(
                condition=Q(saldo_akhir__gte=0),
                name="ck_mutasi_kas_saldo_nonneg",
            ),
            models.CheckConstraint(
                condition=Q(urutan__gte=1),
                name="ck_mutasi_kas_urutan_pos",
            ),
        ]
        indexes = [
            models.Index(
                fields=["rekening", "-urutan"],
                name="ix_mutasi_kas_urut",
            ),
            models.Index(
                fields=["rekening", "-tanggal"],
                name="ix_mutasi_kas_tanggal",
            ),
        ]

    def __str__(self):
        arah = f"-{self.debit}" if self.debit else f"+{self.kredit}"
        return f"{self.rekening} {arah} = {self.saldo_akhir}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError("MutasiKas append-only.")

        if self.debit <= 0 and self.kredit <= 0:
            raise ValidationError(
                "MutasiKas harus memiliki debit atau kredit lebih besar dari nol."
            )

        if self.debit > 0 and self.kredit > 0:
            raise ValidationError(
                "MutasiKas tidak boleh memiliki debit dan kredit sekaligus."
            )

        if self.urutan < 1:
            raise ValidationError(
                "Urutan mutasi harus lebih besar dari nol."
            )

        if self.saldo_akhir < 0:
            raise ValidationError(
                "Saldo akhir tidak boleh negatif."
            )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("MutasiKas append-only.")


class StatusRencana(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    DIAJUKAN = "DIAJUKAN", "Diajukan"
    DISETUJUI = "DISETUJUI", "Disetujui"
    DIEKSEKUSI = "DIEKSEKUSI", "Sudah dibayar"
    DITOLAK = "DITOLAK", "Ditolak"


class RencanaBayar(DiauditModel):
    """
    Usulan pembayaran supplier.

    Nominal adalah nominal usulan.
    Nilai final harus divalidasi ulang saat eksekusi
    di bawah database lock.
    """

    entitas = models.ForeignKey(
        "core.Entitas",
        on_delete=models.PROTECT,
        related_name="rencana_bayar",
    )

    suplier = models.ForeignKey(
        "master.Suplier",
        on_delete=models.PROTECT,
        related_name="rencana_bayar",
    )

    rekening = models.ForeignKey(
        RekeningBank,
        on_delete=models.PROTECT,
        related_name="rencana_bayar",
    )

    tanggal_rencana = models.DateField(
        db_index=True,
    )

    nominal = models.DecimalField(
        max_digits=NILAI_DIGITS,
        decimal_places=NILAI_PLACES,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    status = models.CharField(
        max_length=12,
        choices=StatusRencana.choices,
        default=StatusRencana.DRAFT,
        db_index=True,
    )

    disetujui_oleh = models.ForeignKey(
        "staff_user.Profil",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="rencana_disetujui",
    )

    dieksekusi_oleh = models.ForeignKey(
        "staff_user.Profil",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="rencana_dieksekusi",
    )

    mutasi = models.OneToOneField(
        MutasiKas,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="rencana",
    )

    catatan = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "keuangan_rencana_bayar"
        ordering = ["tanggal_rencana", "id"]
        verbose_name = "Rencana bayar"
        verbose_name_plural = "Rencana bayar"
        indexes = [
            models.Index(
                fields=["status", "tanggal_rencana"],
                name="ix_rencana_status",
            ),
            models.Index(
                fields=["entitas", "status"],
                name="ix_rencana_entitas_status",
            ),
        ]

    def __str__(self):
        return (
            f"{self.suplier.nama} - "
            f"{self.nominal} "
            f"({self.get_status_display()})"
        )

    def clean(self):
        if self.rekening_id and self.entitas_id:
            if self.rekening.entitas_id != self.entitas_id:
                raise ValidationError(
                    {
                        "rekening": (
                            "Rekening harus milik entitas "
                            "yang sama dengan rencana pembayaran."
                        )
                    }
                )

        if self.status == StatusRencana.DIEKSEKUSI and not self.mutasi_id:
            raise ValidationError(
                {
                    "mutasi": (
                        "Rencana pembayaran yang sudah dieksekusi "
                        "wajib memiliki mutasi kas."
                    )
                }
            )


class PengeluaranKas(TimeStampedModel):
    """
    Input pengeluaran operasional.

    Pada tahap input:
    PengeluaranKas tidak otomatis mengubah saldo rekening
    dan tidak otomatis membuat MutasiKas.

    MutasiKas hanya dibuat ketika pengeluaran benar-benar
    dieksekusi sebagai transaksi kas.
    """

    entitas = models.ForeignKey(
        "core.Entitas",
        on_delete=models.PROTECT,
        related_name="pengeluaran_kas",
    )

    kategori = models.CharField(
        max_length=50,
        db_index=True,
    )

    keterangan = models.CharField(
        max_length=255,
    )

    pemohon = models.CharField(
        max_length=120,
    )

    nominal = models.DecimalField(
        max_digits=NILAI_DIGITS,
        decimal_places=NILAI_PLACES,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    bukti_nota = models.FileField(
        upload_to="keuangan/nota/",
        null=True,
        blank=True,
    )

    mutasi = models.OneToOneField(
        MutasiKas,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="pengeluaran",
    )

    class Meta:
        db_table = "keuangan_pengeluaran_kas"
        ordering = ["-id"]
        verbose_name = "Pengeluaran kas"
        verbose_name_plural = "Pengeluaran kas"
        indexes = [
            models.Index(
                fields=["entitas", "-id"],
                name="ix_pengeluaran_entitas",
            ),
            models.Index(
                fields=["entitas", "kategori"],
                name="ix_pengeluaran_kategori",
            ),
        ]

    def __str__(self):
        return f"{self.keterangan} - {self.nominal}"