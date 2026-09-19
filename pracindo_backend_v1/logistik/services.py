# logistik/services.py

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from . import integrasi_warehouse as gudang
from .models import (
    BuktiTerima, Pengiriman, Perhentian, Retur,
    StatusPengiriman, StatusPerhentian
)

def distribusi_tersedia(entitas_id=None):
    calon = gudang.distribusi_siap_kirim(entitas_id=entitas_id)
    sudah_dipakai = set(
        Perhentian.objects
        .exclude(pengiriman__status=StatusPengiriman.BATAL)
        .values_list('distribusi_id', flat=True)
    )
    return [d for d in calon if d['id'] not in sudah_dipakai]

@transaction.atomic
def rakit_pengiriman(*, entitas_id, distribusi_ids, kurir_id=None, tanggal=None,
                     kendaraan_id=None, catatan='', user=None):
    if not distribusi_ids:
        raise ValidationError('Pilih minimal satu distribusi untuk dikirim.')

    ganda = {d for d in distribusi_ids if distribusi_ids.count(d) > 1}
    if ganda:
        raise ValidationError(f'Distribusi dipilih lebih dari sekali: {sorted(ganda)}.')

    terpakai = set(
        Perhentian.objects
        .filter(distribusi_id__in=distribusi_ids)
        .exclude(pengiriman__status=StatusPengiriman.BATAL)
        .values_list('distribusi_id', flat=True)
    )
    if terpakai:
        raise ValidationError(f'Distribusi berikut sudah masuk pengiriman lain: {sorted(terpakai)}.')

    kirim = Pengiriman.objects.create(
        entitas_id=entitas_id,
        tanggal=tanggal or timezone.localdate(),
        kurir_id=kurir_id,
        kendaraan_id=kendaraan_id,
        catatan=catatan,
        dibuat_oleh=user,
    )

    for urut, dist_id in enumerate(distribusi_ids, start=1):
        rincian = gudang.rincian_distribusi(dist_id)
        Perhentian.objects.create(
            pengiriman=kirim,
            distribusi_id=dist_id,
            nomor_distribusi=rincian.get('nomor', ''),
            pelanggan_nama=rincian.get('pelanggan_nama', ''),
            alamat=rincian.get('alamat', ''),
            urutan=urut,
        )

    return kirim

@transaction.atomic
def klaim_pengiriman(*, pengiriman_id, kurir):
    kirim = Pengiriman.objects.select_for_update().get(pk=pengiriman_id)
    
    if kirim.kurir_id is not None:
        raise ValidationError('Pengiriman ini sudah diambil oleh kurir lain.')
    if kirim.status != StatusPengiriman.DISIAPKAN:
        raise ValidationError('Hanya pengiriman berstatus DISIAPKAN yang bisa diklaim.')

    kirim.kurir = kurir
    kirim.save(update_fields=['kurir'])
    return kirim

@transaction.atomic
def berangkatkan(*, pengiriman_id, oleh):
    kirim = Pengiriman.objects.select_for_update().get(pk=pengiriman_id)
    
    if not kirim.kurir_id and oleh is not None:
        kirim.kurir = oleh
        
    if oleh is not None and not getattr(oleh, 'is_superuser', False) and not getattr(oleh, 'supervisor', False):
        if kirim.kurir_id != oleh.id:
            raise ValidationError('Gagal ACC: Anda bukan kurir yang ditugaskan untuk dokumen ini.')

    if kirim.status != StatusPengiriman.DISIAPKAN:
        raise ValidationError(f'Pengiriman sudah {kirim.get_status_display()}.')
            
    if not kirim.perhentian.exists():
        raise ValidationError('Pengiriman tanpa perhentian tidak bisa berangkat.')

    kirim.status = StatusPengiriman.BERANGKAT
    kirim.waktu_berangkat = timezone.now()
    
    if oleh is not None:
        nama_staf = oleh.get_full_name() or oleh.get_username()
        waktu_teks = kirim.waktu_berangkat.strftime("%d-%m-%Y %H:%M")
        tambahan_catatan = f"\n[INFO] Di-ACC & dikirim oleh: {nama_staf} pada {waktu_teks}"
        kirim.catatan = (kirim.catatan + tambahan_catatan).strip()

    kirim.save(update_fields=['status', 'waktu_berangkat', 'kurir', 'catatan'])
    return kirim

@transaction.atomic
def batalkan_pengiriman(*, pengiriman_id, alasan=''):
    kirim = Pengiriman.objects.select_for_update().get(pk=pengiriman_id)
    if kirim.status != StatusPengiriman.DISIAPKAN:
        raise ValidationError('Pengiriman yang sudah berangkat tidak bisa dibatalkan.')
    kirim.status = StatusPengiriman.BATAL
    kirim.catatan = f'{kirim.catatan}\n[BATAL] {alasan}'.strip()
    kirim.save(update_fields=['status', 'catatan'])
    return kirim

@transaction.atomic
def tandai_sampai(*, perhentian_id, oleh):
    hentian = Perhentian.objects.select_for_update().select_related('pengiriman').get(pk=perhentian_id)
    
    if hentian.pengiriman.status != StatusPengiriman.BERANGKAT:
        raise ValidationError('Pengiriman belum berangkat.')
    
    if hentian.tuntas:
        raise ValidationError(f'Perhentian sudah {hentian.get_status_display()}.')

    hentian.status = StatusPerhentian.SAMPAI
    hentian.waktu_sampai = timezone.now()
    hentian.save(update_fields=['status', 'waktu_sampai'])
    return hentian

def _tutup_bila_tuntas(kirim):
    if kirim.status == StatusPengiriman.BERANGKAT and kirim.semua_perhentian_tuntas:
        kirim.status = StatusPengiriman.SELESAI
        kirim.waktu_selesai = timezone.now()
        kirim.save(update_fields=['status', 'waktu_selesai'])

@transaction.atomic
def unggah_bukti(*, perhentian_id, foto, oleh, catatan='', idem_key=''):
    if idem_key:
        ada = BuktiTerima.objects.filter(idem_key=idem_key).first()
        if ada:
            return ada

    hentian = Perhentian.objects.select_for_update().select_related('pengiriman').get(pk=perhentian_id)
    kirim = hentian.pengiriman

    if kirim.status == StatusPengiriman.BATAL:
        raise ValidationError('Pengiriman sudah dibatalkan.')
    if hentian.status == StatusPerhentian.DIRETUR:
        raise ValidationError('Perhentian ini sudah dicatat sebagai retur.')

    bukti = BuktiTerima.objects.create(
        perhentian=hentian, foto=foto, catatan=catatan,
        diunggah_oleh=oleh, idem_key=idem_key,
    )

    if hentian.status != StatusPerhentian.DITERIMA:
        hentian.status = StatusPerhentian.DITERIMA
        if not hentian.waktu_sampai:
            hentian.waktu_sampai = timezone.now()
        hentian.save(update_fields=['status', 'waktu_sampai'])
        gudang.tandai_terkirim(hentian.distribusi_id, waktu=timezone.now(), oleh=oleh)

    _tutup_bila_tuntas(kirim)
    return bukti

@transaction.atomic
def catat_retur(*, perhentian_id, alasan, oleh, foto=None, idem_key=''):
    if not alasan.strip():
        raise ValidationError('Alasan retur wajib diisi.')
    if idem_key:
        ada = Retur.objects.filter(idem_key=idem_key).first()
        if ada:
            return ada

    hentian = Perhentian.objects.select_for_update().select_related('pengiriman').get(pk=perhentian_id)
    if hentian.pengiriman.status == StatusPengiriman.BATAL:
        raise ValidationError('Pengiriman sudah dibatalkan.')
    if hentian.status == StatusPerhentian.DITERIMA:
        raise ValidationError('Perhentian sudah diterima. Retur tidak bisa lewat pengiriman.')

    retur = Retur.objects.create(
        perhentian=hentian, alasan=alasan, foto=foto, dicatat_oleh=oleh, idem_key=idem_key,
    )
    hentian.status = StatusPerhentian.DIRETUR
    hentian.save(update_fields=['status'])
    _tutup_bila_tuntas(hentian.pengiriman)
    return retur

@transaction.atomic
def setujui_retur(*, retur_id, oleh):
    if not getattr(oleh, 'supervisor', False):
        raise ValidationError('Hanya Supervisor yang boleh menyetujui retur.')

    retur = Retur.objects.select_for_update().select_related('perhentian').get(pk=retur_id)
    if retur.stok_dikembalikan:
        raise ValidationError('Retur ini sudah disetujui sebelumnya.')

    gudang.kembalikan_stok(retur.perhentian.distribusi_id, alasan=retur.alasan, oleh=oleh)

    retur.disetujui_oleh = oleh
    retur.disetujui_pada = timezone.now()
    retur.stok_dikembalikan = True
    retur.save(update_fields=['disetujui_oleh', 'disetujui_pada', 'stok_dikembalikan'])
    return retur