"""
Pengiriman dan bukti terima — logistik/models.py

BATAS MODUL YANG TIDAK BOLEH DILANGGAR

    logistik TIDAK PERNAH MENULIS STOK.

Rantainya: sales_order -> akunting -> warehouse -> logistik -> kurir.
Saat sebuah Distribusi sampai ke logistik, stok SUDAH berkurang di warehouse.
Kalau logistik ikut mengurangi, angkanya berkurang dua kali dan tidak ada
error yang muncul -- selisihnya baru ketahuan saat opname, dan saat itu tidak
ada yang bisa menelusuri jalur mana yang salah.

Rujukan ke Distribusi memakai INTEGER, bukan ForeignKey, karena aturan impor
satu arah di repo ini melarang logistik mengimpor model warehouse. Semua
percakapan dengan warehouse lewat integrasi_warehouse.py.

STIKER SUDAH MENUTUP KLAIM
    Barang yang sampai di sini sudah berstiker, dan barang berstiker tidak
    bisa diklaim lagi. Atribusi badan hukum selesai di hulu. Karena itu tidak
    ada MutasiKlaim di modul ini, dan logistik tidak punya cara merusak
    invariant konservasi nilai.
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from core.models import CounterDokumen, DiauditModel, TimeStampedModel

class Kendaraan(TimeStampedModel):
    kode = models.CharField(max_length=16, unique=True)
    nama = models.CharField(max_length=120)
    plat_nomor = models.CharField(max_length=16, blank=True)
    kapasitas_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    aktif = models.BooleanField(default=True)

    class Meta:
        db_table = 'logistik_kendaraan'
        ordering = ['kode']
        verbose_name_plural = 'Kendaraan'

    def __str__(self):
        return f"{self.kode} - {self.nama}"

class StatusPengiriman(models.TextChoices):
    DISIAPKAN = 'DISIAPKAN', 'Disiapkan'
    BERANGKAT = 'BERANGKAT', 'Berangkat'
    SELESAI   = 'SELESAI',   'Selesai'
    BATAL     = 'BATAL',     'Dibatalkan'

class Pengiriman(DiauditModel):
    nomor = models.CharField(max_length=32, editable=False)
    entitas = models.ForeignKey('core.Entitas', on_delete=models.PROTECT, related_name='pengiriman')
    tanggal = models.DateField(default=timezone.localdate, db_index=True)
    
    kurir = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name='pengiriman_dibawa')
    kendaraan = models.ForeignKey(Kendaraan, null=True, blank=True, on_delete=models.PROTECT, related_name='pengiriman')
    
    dibuat_oleh = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='pengiriman_dibuat')
    
    status = models.CharField(max_length=12, choices=StatusPengiriman.choices, default=StatusPengiriman.DISIAPKAN, db_index=True)
    waktu_berangkat = models.DateTimeField(null=True, blank=True, editable=False)
    waktu_selesai = models.DateTimeField(null=True, blank=True, editable=False)
    catatan = models.TextField(blank=True)

    class Meta:
        db_table = 'logistik_pengiriman'
        ordering = ['-tanggal', '-id']
        constraints = [
            models.UniqueConstraint(fields=['entitas', 'nomor'], name='uq_pengiriman_nomor'),
        ]
        indexes = [
            models.Index(fields=['kurir', 'status', '-tanggal'], name='ix_kirim_kurir_status'),
            models.Index(fields=['status', '-tanggal'], name='ix_kirim_status'),
        ]

    def __str__(self):
        return f"{self.nomor} - {self.kurir}"

    @property
    def jumlah_perhentian(self):
        return self.perhentian.count()

    @property
    def semua_perhentian_tuntas(self):
        return not self.perhentian.filter(status__in=[StatusPerhentian.MENUNGGU, StatusPerhentian.SAMPAI]).exists()

    def save(self, *args, **kwargs):
        if not self.nomor:
            self.nomor = CounterDokumen.berikutnya(self.entitas, 'KIRIM', self.tanggal)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.status != StatusPengiriman.DISIAPKAN:
            raise ValidationError('Pengiriman yang sudah berangkat tidak bisa dihapus.')
        return super().delete(*args, **kwargs)

class StatusPerhentian(models.TextChoices):
    MENUNGGU = 'MENUNGGU', 'Menunggu'
    SAMPAI   = 'SAMPAI',   'Sampai di lokasi'
    DITERIMA = 'DITERIMA', 'Diterima'
    DIRETUR  = 'DIRETUR',  'Diretur'

class Perhentian(models.Model):
    pengiriman = models.ForeignKey(Pengiriman, on_delete=models.CASCADE, related_name='perhentian')
    distribusi_id = models.PositiveIntegerField(db_index=True)
    nomor_distribusi = models.CharField(max_length=32, blank=True)
    pelanggan_nama = models.CharField(max_length=200, blank=True)
    urutan = models.PositiveSmallIntegerField(default=1)
    alamat = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=StatusPerhentian.choices, default=StatusPerhentian.MENUNGGU, db_index=True)
    waktu_sampai = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        db_table = 'logistik_perhentian'
        ordering = ['pengiriman', 'urutan']
        constraints = [
            models.UniqueConstraint(fields=['pengiriman', 'distribusi_id'], name='uq_perhentian_distribusi'),
        ]

    def __str__(self):
        return f"{self.urutan}. {self.pelanggan_nama or self.nomor_distribusi}"

    @property
    def tuntas(self):
        return self.status in (StatusPerhentian.DITERIMA, StatusPerhentian.DIRETUR)

class BuktiTerima(models.Model):
    perhentian = models.ForeignKey(Perhentian, on_delete=models.PROTECT, related_name='bukti')
    foto = models.ImageField(upload_to='logistik/bukti/%Y/%m/')
    waktu = models.DateTimeField(auto_now_add=True)
    catatan = models.TextField(blank=True)
    diunggah_oleh = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='bukti_terima_diunggah')
    idem_key = models.CharField(max_length=128, blank=True, db_index=True)

    class Meta:
        db_table = 'logistik_bukti_terima'
        ordering = ['perhentian', 'waktu']
        constraints = [
            models.UniqueConstraint(fields=['idem_key'], name='uq_bukti_idem', condition=~Q(idem_key='')),
        ]

    def __str__(self):
        return f"Bukti {self.perhentian_id} {self.waktu:%Y-%m-%d %H:%M}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError('BuktiTerima append-only.')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError('BuktiTerima append-only.')

class Retur(models.Model):
    perhentian = models.OneToOneField(Perhentian, on_delete=models.PROTECT, related_name='retur')
    alasan = models.TextField()
    foto = models.ImageField(upload_to='logistik/retur/%Y/%m/', null=True, blank=True)
    dicatat_oleh = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='retur_dicatat')
    dicatat_pada = models.DateTimeField(auto_now_add=True)
    disetujui_oleh = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name='retur_disetujui')
    disetujui_pada = models.DateTimeField(null=True, blank=True)
    stok_dikembalikan = models.BooleanField(default=False)
    idem_key = models.CharField(max_length=128, blank=True, db_index=True)

    class Meta:
        db_table = 'logistik_retur'
        ordering = ['-dicatat_pada']
        constraints = [
            models.UniqueConstraint(fields=['idem_key'], name='uq_retur_idem', condition=~Q(idem_key='')),
        ]

    def __str__(self):
        return f"Retur {self.perhentian_id}"

    @property
    def menunggu_persetujuan(self):
        return self.disetujui_pada is None