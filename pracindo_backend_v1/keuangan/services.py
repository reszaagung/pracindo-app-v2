import uuid

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import MutasiKas, PengeluaranKas, RekeningBank


@transaction.atomic
def catat_pengeluaran(
    entitas_id,
    kategori,
    keterangan,
    pemohon,
    nominal,
    user,
    bukti_nota=None,
):
    pengeluaran = PengeluaranKas.objects.create(
        entitas_id=entitas_id,
        kategori=kategori,
        keterangan=keterangan,
        pemohon=pemohon,
        nominal=nominal,
        bukti_nota=bukti_nota,
    )

    rekening = (
        RekeningBank.objects
        .select_for_update()
        .filter(
            entitas_id=entitas_id,
            jenis="KAS_KECIL",
            aktif=True,
        )
        .first()
    )

    if not rekening:
        raise ValidationError(
            "Rekening Kas Kecil untuk entitas ini belum dikonfigurasi."
        )

    if rekening.saldo < nominal:
        raise ValidationError(
            f"Saldo kas kecil tidak cukup. "
            f"Sisa saldo: {rekening.saldo}"
        )

    rekening.urutan_terakhir += 1
    rekening.saldo -= nominal

    rekening.save(
        update_fields=[
            "urutan_terakhir",
            "saldo",
            "diubah_pada",
        ]
    )

    referensi_trx = (
        f"PC-{timezone.now().strftime('%y%m%d')}-{pengeluaran.id}"
    )

    mutasi = MutasiKas.objects.create(
        rekening=rekening,
        urutan=rekening.urutan_terakhir,
        kredit=nominal,
        saldo_akhir=rekening.saldo,
        keterangan=keterangan,
        referensi=referensi_trx,
        idempotency_key=f"pc-{pengeluaran.id}-{uuid.uuid4().hex}",
    )

    pengeluaran.mutasi = mutasi
    pengeluaran.save(
        update_fields=[
            "mutasi",
            "diubah_pada",
        ]
    )

    from akunting.services import posting

    posting(
        kejadian="BEBAN_KAS",
        entitas_id=entitas_id,
        tanggal=timezone.localdate(),
        referensi=referensi_trx,
        nilai={"nominal": nominal},
        idem_key=mutasi.idempotency_key,
        user=user,
        keterangan=f"Kas Kecil: {keterangan}",
    )

    return pengeluaran