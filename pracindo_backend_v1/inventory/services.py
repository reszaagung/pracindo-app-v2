from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import DecimalField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from core.models import CounterDokumen, PeriodeAkuntansi
from produksi.models import Batch, Tangki

from .models import (
    Kemasan,
    MutasiKlaim,
    Packing,
    Pembelian,
    PoolKemasan,
    PoolResource,
    SaldoEntitas,
    SumberPembelian,
    StokBarangJadi,
    StatusDokumen,
    TipeMutasi,
)


D0 = Decimal("0")
D0_RP = Decimal("0.00")
D0_QTY = Decimal("0.000")

TOL_QTY = Decimal("0.001")
TOL_RP = Decimal("0.01")

Q_RP = Decimal("0.01")
Q_QTY = Decimal("0.001")
Q_HARGA = Decimal("0.000001")

F_RP = DecimalField(
    max_digits=20,
    decimal_places=2,
)


class GalatInventory(ValidationError):
    http = 422


class KonflikSaldo(GalatInventory):
    http = 409


class InvariantMelenceng(GalatInventory):
    http = 500


# ============================================================
# UTILITAS
# ============================================================

def rp(value):
    return Decimal(str(value)).quantize(
        Q_RP,
        rounding=ROUND_HALF_UP,
    )


def qty(value):
    return Decimal(str(value)).quantize(
        Q_QTY,
        rounding=ROUND_HALF_UP,
    )


def harga(value):
    return Decimal(str(value)).quantize(
        Q_HARGA,
        rounding=ROUND_HALF_UP,
    )


def _wajib_user(user):
    if not getattr(user, "is_authenticated", False):
        raise GalatInventory(
            "Operasi ini wajib punya pembuat yang tercatat."
        )
    return user


def _pastikan_periode_terbuka(entitas, tanggal):
    tertutup = PeriodeAkuntansi.objects.filter(
        entitas=entitas,
        tahun=tanggal.year,
        bulan=tanggal.month,
        ditutup=True,
    ).exists()

    if tertutup:
        raise GalatInventory(
            f"Periode {tanggal.month:02d}/{tanggal.year} "
            f"untuk {entitas.kode} sudah ditutup."
        )


def _kunci_saldo(entitas_id):
    try:
        return (
            SaldoEntitas.objects
            .select_for_update()
            .get(entitas_id=entitas_id)
        )
    except SaldoEntitas.DoesNotExist:
        raise InvariantMelenceng(
            f"Entitas id {entitas_id} tidak punya "
            f"baris SaldoEntitas."
        )


def _pastikan_status_packing(packing, status):
    if packing.status != status:
        raise KonflikSaldo(
            f"Packing {packing.nomor} berstatus "
            f"{packing.status}. "
            f"Status yang diperlukan: {status}."
        )


def _kategori_kemasan_valid(kategori):
    kategori = str(kategori or "").strip().upper()

    if kategori not in {
        "PRIMER",
        "SEKUNDER",
        "PRIMER_SEKUNDER",
    }:
        raise GalatInventory(
            "Kategori kemasan harus PRIMER, "
            "SEKUNDER, atau PRIMER_SEKUNDER."
        )

    return kategori


def _pastikan_kategori_primer(pool):
    if pool.kategori not in {
        "PRIMER",
        "PRIMER_SEKUNDER",
    }:
        raise GalatInventory(
            f"Kemasan {pool.produk.nama} dengan kategori "
            f"{pool.get_kategori_display()} tidak dapat "
            f"digunakan sebagai Kemasan Primer."
        )


def _pastikan_kategori_sekunder(pool):
    if pool.kategori not in {
        "SEKUNDER",
        "PRIMER_SEKUNDER",
    }:
        raise GalatInventory(
            f"Kemasan {pool.produk.nama} dengan kategori "
            f"{pool.get_kategori_display()} tidak dapat "
            f"digunakan sebagai Kemasan Sekunder."
        )


# ============================================================
# POOL RESOURCE
# ============================================================

def tambah_ke_pool_resource(
    produk_id,
    q,
    nilai_tambahan,
):
    pool, _ = (
        PoolResource.objects
        .select_for_update()
        .get_or_create(
            produk_id=produk_id,
        )
    )

    pool.qty_kg = qty(
        pool.qty_kg + q
    )

    pool.nilai = rp(
        pool.nilai + nilai_tambahan
    )

    pool.save(
        update_fields=[
            "qty_kg",
            "nilai",
        ]
    )

    return pool


def potong_dari_pool_resource(
    produk_id,
    q,
    nilai_potongan,
):
    try:
        pool = (
            PoolResource.objects
            .select_for_update()
            .get(
                produk_id=produk_id,
            )
        )
    except PoolResource.DoesNotExist:
        raise InvariantMelenceng(
            f"PoolResource produk ID "
            f"{produk_id} tidak ditemukan."
        )

    pool.qty_kg = qty(
        pool.qty_kg - q
    )

    pool.nilai = rp(
        pool.nilai - nilai_potongan
    )

    if pool.qty_kg < 0 or pool.nilai < 0:
        raise InvariantMelenceng(
            "Pengurangan PoolResource menyebabkan "
            "nilai negatif."
        )

    if pool.qty_kg == 0:
        pool.nilai = D0_RP

    pool.save(
        update_fields=[
            "qty_kg",
            "nilai",
        ]
    )

    return pool


# ============================================================
# POOL KEMASAN
# ============================================================

def tambah_ke_pool_kemasan(
    produk_id,
    kategori,
    q_unit,
    nilai_tambahan,
):
    kategori = _kategori_kemasan_valid(
        kategori
    )

    q_unit = int(q_unit)

    if q_unit <= 0:
        raise GalatInventory(
            "Jumlah kemasan harus lebih dari 0 unit."
        )

    pool = (
        PoolKemasan.objects
        .select_for_update()
        .filter(
            produk_id=produk_id,
        )
        .first()
    )

    if pool is None:
        pool = PoolKemasan.objects.create(
            produk_id=produk_id,
            kategori=kategori,
            qty_unit=0,
            nilai=D0_RP,
        )

        pool = (
            PoolKemasan.objects
            .select_for_update()
            .get(pk=pool.pk)
        )

    else:
        if pool.kategori != kategori:
            raise GalatInventory(
                f"Kategori {pool.produk.nama} tidak konsisten. "
                f"Pool sudah "
                f"{pool.get_kategori_display()}."
            )

    pool.qty_unit += q_unit

    pool.nilai = rp(
        pool.nilai + nilai_tambahan
    )

    pool.save(
        update_fields=[
            "qty_unit",
            "nilai",
        ]
    )

    return pool


def potong_dari_pool_kemasan(
    pool_id,
    q_unit,
    nilai_potongan,
):
    q_unit = int(q_unit)

    if q_unit <= 0:
        raise GalatInventory(
            "Jumlah kemasan yang diambil "
            "harus lebih dari 0 unit."
        )

    pool = (
        PoolKemasan.objects
        .select_for_update()
        .select_related("produk")
        .get(pk=pool_id)
    )

    if pool.qty_unit < q_unit:
        raise KonflikSaldo(
            f"Stok {pool.produk.nama} tinggal "
            f"{pool.qty_unit} Unit."
        )

    pool.qty_unit -= q_unit

    pool.nilai = rp(
        pool.nilai - nilai_potongan
    )

    if pool.qty_unit < 0 or pool.nilai < 0:
        raise InvariantMelenceng(
            "Pengurangan PoolKemasan menyebabkan "
            "nilai negatif."
        )

    if pool.qty_unit == 0:
        pool.nilai = D0_RP

    pool.save(
        update_fields=[
            "qty_unit",
            "nilai",
        ]
    )

    return pool


# ============================================================
# PEMBELIAN
# ============================================================

@transaction.atomic
def posting_pembelian(
    pembelian,
    user=None,
):
    user = _wajib_user(user)

    pembelian = (
        Pembelian.objects
        .select_for_update()
        .get(pk=pembelian.pk)
    )

    if pembelian.sumber == SumberPembelian.PENERIMAAN:
        raise KonflikSaldo(
            f"{pembelian.nomor} terbit dari penerimaan "
            f"gudang dan sudah POSTED sejak lahir."
        )

    if pembelian.status != StatusDokumen.DRAFT:
        raise KonflikSaldo(
            f"Pembelian {pembelian.nomor} sudah "
            f"{pembelian.status}."
        )

    if not pembelian.entitas.aktif:
        raise GalatInventory(
            f"Entitas {pembelian.entitas.kode} "
            f"nonaktif dan tidak bisa menyetor."
        )

    _pastikan_periode_terbuka(
        pembelian.entitas,
        pembelian.tanggal,
    )

    nilai = rp(
        pembelian.qty_kg
        * pembelian.harga_per_kg
    )

    pembelian.nilai = nilai

    if pembelian.produk.jenis == "KEMASAN":
        kategori = getattr(
            pembelian,
            "kategori_kemasan",
            None,
        )

        if not kategori:
            raise GalatInventory(
                "Kategori kemasan wajib ditentukan "
                "sebelum pembelian diposting."
            )

        q_unit = getattr(
            pembelian,
            "qty_unit",
            None,
        )

        if q_unit is None:
            q_unit = pembelian.qty_kg

        tambah_ke_pool_kemasan(
            produk_id=pembelian.produk_id,
            kategori=kategori,
            q_unit=q_unit,
            nilai_tambahan=nilai,
        )

        keterangan = (
            f"PO Kemasan {pembelian.nomor} "
            f"- {pembelian.produk}"
        )
    else:
        tambah_ke_pool_resource(
            pembelian.produk_id,
            pembelian.qty_kg,
            nilai,
        )

        keterangan = (
            f"{pembelian.nomor} "
            f"- {pembelian.produk}"
        )

    MutasiKlaim.objects.create(
        entitas=pembelian.entitas,
        grup_bahan=pembelian.grup_bahan,
        tipe=TipeMutasi.SETOR,
        arah=1,
        qty_kg=pembelian.qty_kg,
        nilai=nilai,
        ref_type="Pembelian",
        ref_id=pembelian.id,
        keterangan=keterangan,
        waktu=pembelian.waktu,
        dibuat_oleh=user,
    )

    saldo = _kunci_saldo(
        pembelian.entitas_id
    )

    saldo.total_setor = rp(
        saldo.total_setor + nilai
    )

    saldo.qty_setor = qty(
        saldo.qty_setor
        + pembelian.qty_kg
    )

    saldo.saldo = rp(
        saldo.saldo + nilai
    )

    saldo.save(
        update_fields=[
            "total_setor",
            "qty_setor",
            "saldo",
        ]
    )

    pembelian.status = StatusDokumen.POSTED
    pembelian.posted_at = timezone.now()

    pembelian.save(
        update_fields=[
            "status",
            "nilai",
            "posted_at",
        ]
    )

    assert_invarian()

    return pembelian


@transaction.atomic
def void_pembelian(
    pembelian,
    alasan,
    user=None,
):
    user = _wajib_user(user)

    pembelian = (
        Pembelian.objects
        .select_for_update()
        .get(pk=pembelian.pk)
    )

    if pembelian.sumber == SumberPembelian.PENERIMAAN:
        raise KonflikSaldo(
            f"{pembelian.nomor} melekat pada "
            f"penerimaan "
            f"{pembelian.penerimaan_item.penerimaan.nomor}."
        )

    if pembelian.status != StatusDokumen.POSTED:
        raise KonflikSaldo(
            f"Hanya pembelian POSTED yang bisa di-VOID. "
            f"{pembelian.nomor} berstatus "
            f"{pembelian.status}."
        )

    if not alasan or not alasan.strip():
        raise GalatInventory(
            "Alasan VOID wajib diisi."
        )

    _pastikan_periode_terbuka(
        pembelian.entitas,
        timezone.localdate(),
    )

    bergerak = (
        Pembelian.objects
        .filter(
            produk_id=pembelian.produk_id,
            status=StatusDokumen.POSTED,
            waktu__gt=pembelian.waktu,
        )
        .exists()
    )

    if bergerak or _pool_terpakai_sejak(pembelian):
        raise KonflikSaldo(
            f"Pool {pembelian.produk} sudah bergerak "
            f"sejak {pembelian.nomor} diposting."
        )

    if pembelian.produk.jenis == "KEMASAN":
        pool = (
            PoolKemasan.objects
            .select_for_update()
            .get(
                produk_id=pembelian.produk_id,
            )
        )

        q_unit = getattr(
            pembelian,
            "qty_unit",
            None,
        )

        if q_unit is None:
            q_unit = pembelian.qty_kg

        q_unit = int(q_unit)

        if pool.qty_unit < q_unit:
            raise KonflikSaldo(
                f"Pool {pembelian.produk} tinggal "
                f"{pool.qty_unit} Unit."
            )

        nilai_unit = (
            pool.harga_satuan
            if pool.qty_unit > 0
            else D0_RP
        )

        nilai_potongan = rp(
            nilai_unit * q_unit
        )

        if nilai_potongan > pembelian.nilai + TOL_RP:
            nilai_potongan = pembelian.nilai

        potong_dari_pool_kemasan(
            pool.id,
            q_unit,
            nilai_potongan,
        )
    else:
        pool = (
            PoolResource.objects
            .select_for_update()
            .get(
                produk_id=pembelian.produk_id,
            )
        )

        if pool.qty_kg < (
            pembelian.qty_kg - TOL_QTY
        ):
            raise KonflikSaldo(
                f"Pool {pembelian.produk} tinggal "
                f"{pool.qty_kg} Kg."
            )

        potong_dari_pool_resource(
            pembelian.produk_id,
            pembelian.qty_kg,
            pembelian.nilai,
        )

    MutasiKlaim.objects.create(
        entitas=pembelian.entitas,
        grup_bahan=pembelian.grup_bahan,
        tipe=TipeMutasi.PENYESUAIAN,
        arah=-1,
        qty_kg=pembelian.qty_kg,
        nilai=pembelian.nilai,
        ref_type="VoidPembelian",
        ref_id=pembelian.id,
        keterangan=(
            f"VOID {pembelian.nomor}: {alasan}"
        ),
        waktu=timezone.now(),
        dibuat_oleh=user,
    )

    saldo = _kunci_saldo(
        pembelian.entitas_id
    )

    saldo.total_setor = rp(
        saldo.total_setor
        - pembelian.nilai
    )

    saldo.qty_setor = qty(
        saldo.qty_setor
        - pembelian.qty_kg
    )

    saldo.saldo = rp(
        saldo.saldo
        - pembelian.nilai
    )

    saldo.save(
        update_fields=[
            "total_setor",
            "qty_setor",
            "saldo",
        ]
    )

    pembelian.status = StatusDokumen.VOID

    pembelian.catatan = (
        f"{pembelian.catatan}\n"
        f"[VOID] {alasan}"
    ).strip()

    pembelian.save(
        update_fields=[
            "status",
            "catatan",
        ]
    )

    assert_invarian()

    return pembelian


def _pool_terpakai_sejak(
    pembelian,
):
    from produksi.models import BatchInputRaw

    return (
        BatchInputRaw.objects
        .filter(
            produk_id=pembelian.produk_id,
            batch__posted_at__isnull=False,
            batch__posted_at__gte=(
                pembelian.posted_at
                or pembelian.waktu
            ),
        )
        .exists()
    )


# ============================================================
# PENERIMAAN → PEMBELIAN → POOL
# ============================================================

@transaction.atomic
def terbitkan_pembelian_dari_penerimaan(
    penerimaan,
    user=None,
):
    user = _wajib_user(user)

    po = penerimaan.purchase_order
    entitas = getattr(
        po,
        "entitas",
        None,
    )

    if entitas is None:
        raise GalatInventory(
            f"PO pada {penerimaan.nomor} tidak punya "
            f"entitas pemilik hak."
        )

    if not entitas.aktif:
        raise GalatInventory(
            f"Entitas {entitas.kode} nonaktif "
            f"dan tidak bisa menyetor."
        )

    _pastikan_periode_terbuka(
        entitas,
        penerimaan.tanggal,
    )

    grup = entitas.grup_bahan

    baris = list(
        penerimaan.item
        .select_related(
            "po_item",
            "po_item__produk",
        )
        .order_by(
            "po_item__produk_id"
        )
    )

    if not baris:
        raise GalatInventory(
            f"Penerimaan {penerimaan.nomor} "
            f"tidak punya item."
        )

    saldo = _kunci_saldo(
        entitas.id
    )

    terbit = []

    for b in baris:
        if (
            Pembelian.objects
            .filter(
                penerimaan_item=b
            )
            .exists()
        ):
            continue

        q = qty(
            b.qty_diterima or 0
        )

        if q <= 0:
            continue

        item = b.po_item
        sekarang = timezone.now()

        h = harga(
            item.harga_per_kg
        )

        nilai = rp(
            q * h
        )

        is_kemasan = (
            item.produk.jenis == "KEMASAN"
        )

        kategori = None

        if is_kemasan:
            kategori = getattr(
                b,
                "kategori_kemasan",
                None,
            )

            if not kategori:
                kategori = getattr(
                    item,
                    "kategori_kemasan",
                    None,
                )

            if not kategori:
                raise GalatInventory(
                    f"Kategori kemasan untuk "
                    f"{item.produk.nama} "
                    f"wajib ditentukan."
                )

            kategori = _kategori_kemasan_valid(
                kategori
            )

        p = Pembelian.objects.create(
            nomor=CounterDokumen.berikutnya(
                entitas,
                "PB",
                penerimaan.tanggal,
            ),
            no_po=str(po),
            entitas=entitas,
            grup_bahan=grup,
            produk=item.produk,
            qty_kg=q,
            harga_per_kg=h,
            nilai=nilai,
            tanggal=penerimaan.tanggal,
            waktu=sekarang,
            status=StatusDokumen.POSTED,
            posted_at=sekarang,
            sumber=SumberPembelian.PENERIMAAN,
            penerimaan_item=b,
            catatan=(
                f"Otomatis dari {penerimaan.nomor} "
                f"- SJ {penerimaan.no_surat_jalan}"
            ),
            dibuat_oleh=user,
        )

        if is_kemasan:
            q_unit = q

            tambah_ke_pool_kemasan(
                produk_id=item.produk_id,
                kategori=kategori,
                q_unit=q_unit,
                nilai_tambahan=nilai,
            )
        else:
            tambah_ke_pool_resource(
                item.produk_id,
                q,
                nilai,
            )

        MutasiKlaim.objects.create(
            entitas=entitas,
            grup_bahan=grup,
            tipe=TipeMutasi.SETOR,
            arah=1,
            qty_kg=q,
            nilai=nilai,
            ref_type="Pembelian",
            ref_id=p.id,
            keterangan=(
                f"{p.nomor} - "
                f"{item.produk} - "
                f"{penerimaan.nomor}"
            ),
            waktu=p.waktu,
            dibuat_oleh=user,
        )

        saldo.total_setor = rp(
            saldo.total_setor + nilai
        )

        saldo.qty_setor = qty(
            saldo.qty_setor + q
        )

        saldo.saldo = rp(
            saldo.saldo + nilai
        )

        terbit.append(p)

    if terbit:
        saldo.save(
            update_fields=[
                "total_setor",
                "qty_setor",
                "saldo",
            ]
        )

    assert_invarian()

    return terbit


# ============================================================
# PACKING
# ============================================================

@transaction.atomic
def eksekusi_packing_langsung(
    packing,
    user,
):
    user = _wajib_user(user)

    packing = (
        Packing.objects
        .select_for_update()
        .get(pk=packing.pk)
    )

    _pastikan_status_packing(
        packing,
        StatusDokumen.DRAFT,
    )

    if packing.posted_at is not None:
        raise KonflikSaldo(
            f"Packing {packing.nomor} sudah pernah diposting."
        )

    _pastikan_periode_terbuka(
        packing.entitas,
        packing.tanggal,
    )

    if packing.qty_kg <= 0:
        raise GalatInventory(
            "Qty packing harus lebih dari 0 Kg."
        )

    if packing.total_unit <= 0:
        raise GalatInventory(
            "Total unit harus lebih dari 0."
        )

    tangki = (
        Tangki.objects
        .select_for_update()
        .get(
            pk=packing.tangki_id
        )
    )

    if tangki.saldo_kg <= D0_QTY:
        raise KonflikSaldo(
            f"Tangki {tangki.kode} sudah kosong."
        )

    if packing.qty_kg > (
        tangki.saldo_kg + TOL_QTY
    ):
        raise KonflikSaldo(
            f"Cairan di {tangki.kode} sisa "
            f"{tangki.saldo_kg} Kg. Anda mengambil "
            f"{packing.qty_kg} Kg."
        )

    menghabiskan = (
        abs(
            packing.qty_kg
            - tangki.saldo_kg
        )
        <= TOL_QTY
    )

    harga_rata_tangki = (
        rp(
            tangki.saldo_nilai
            / tangki.saldo_kg
        )
        if tangki.saldo_kg > 0
        else D0_RP
    )

    cost_bahan = (
        tangki.saldo_nilai
        if menghabiskan
        else rp(
            packing.qty_kg
            * harga_rata_tangki
        )
    )

    # --------------------------------------------------------
    # KEMASAN PRIMER
    # --------------------------------------------------------

    if not packing.kemasan_primer_id:
        raise GalatInventory(
            "Kemasan Primer wajib dipilih."
        )

    pool_primer = (
        PoolKemasan.objects
        .select_for_update()
        .select_related("produk")
        .get(
            pk=packing.kemasan_primer_id
        )
    )

    _pastikan_kategori_primer(
        pool_primer
    )

    total_unit_primer = int(
        packing.total_unit
    )

    if total_unit_primer <= 0:
        raise GalatInventory(
            "Total unit Primer harus lebih dari 0."
        )

    if pool_primer.qty_unit < total_unit_primer:
        raise KonflikSaldo(
            f"Stok Kemasan Primer "
            f"{pool_primer.produk.nama} "
            f"tinggal {pool_primer.qty_unit} Unit."
        )

    harga_primer = (
        pool_primer.harga_satuan
        if pool_primer.qty_unit > 0
        else D0_RP
    )

    nilai_primer = rp(
        harga_primer
        * total_unit_primer
    )

    # --------------------------------------------------------
    # KEMASAN SEKUNDER
    # --------------------------------------------------------

    nilai_sekunder = D0_RP
    total_unit_sekunder = 0

    pool_sekunder = None

    if packing.kemasan_sekunder_id:
        pool_sekunder = (
            PoolKemasan.objects
            .select_for_update()
            .select_related("produk")
            .get(
                pk=packing.kemasan_sekunder_id
            )
        )

        _pastikan_kategori_sekunder(
            pool_sekunder
        )

        qty_per_unit = int(
            packing.qty_kemasan_sekunder or 0
        )

        if qty_per_unit <= 0:
            raise GalatInventory(
                "Qty Kemasan Sekunder harus lebih "
                "dari 0 bila Kemasan Sekunder digunakan."
            )

        total_unit_sekunder = (
            total_unit_primer
            * qty_per_unit
        )

        if pool_sekunder.qty_unit < total_unit_sekunder:
            raise KonflikSaldo(
                f"Stok Kemasan Sekunder "
                f"{pool_sekunder.produk.nama} "
                f"tinggal {pool_sekunder.qty_unit} Unit."
            )

        harga_sekunder = (
            pool_sekunder.harga_satuan
            if pool_sekunder.qty_unit > 0
            else D0_RP
        )

        nilai_sekunder = rp(
            harga_sekunder
            * total_unit_sekunder
        )

    total_cost = rp(
        cost_bahan
        + nilai_primer
        + nilai_sekunder
    )

    # --------------------------------------------------------
    # POTONG POOL
    # --------------------------------------------------------

    potong_dari_pool_kemasan(
        pool_primer.id,
        total_unit_primer,
        nilai_primer,
    )

    if pool_sekunder is not None:
        potong_dari_pool_kemasan(
            pool_sekunder.id,
            total_unit_sekunder,
            nilai_sekunder,
        )

    # --------------------------------------------------------
    # STOK BARANG JADI
    # --------------------------------------------------------

    isi_per_kemasan = (
        packing.qty_kg
        / Decimal(
            str(packing.total_unit)
        )
    ).quantize(
        Decimal("0.001")
    )

    kemasan_cocok = (
        Kemasan.objects
        .filter(
            aktif=True,
            bobot_kg__gte=(
                isi_per_kemasan
                - Decimal("0.001")
            ),
            bobot_kg__lte=(
                isi_per_kemasan
                + Decimal("0.001")
            ),
        )
        .first()
    )

    if kemasan_cocok:
        stok_jadi, _ = (
            StokBarangJadi.objects
            .select_for_update()
            .get_or_create(
                entitas_id=packing.entitas_id,
                grup_bahan_id=(
                    packing.entitas.grup_bahan_id
                ),
                item_id=packing.nama_hasil_id,
                kemasan=kemasan_cocok,
                defaults={
                    "qty_unit": 0,
                    "qty_kg": D0_QTY,
                    "nilai": D0_RP,
                },
            )
        )

        stok_jadi.qty_unit += int(
            packing.total_unit
        )

        stok_jadi.qty_kg = qty(
            stok_jadi.qty_kg
            + packing.qty_kg
        )

        stok_jadi.nilai = rp(
            stok_jadi.nilai
            + total_cost
        )

        stok_jadi.save(
            update_fields=[
                "qty_unit",
                "qty_kg",
                "nilai",
            ]
        )

    # --------------------------------------------------------
    # SIMPAN NILAI HISTORIS PACKING
    # --------------------------------------------------------

    packing.harga_per_kg = (
        harga_rata_tangki
    )

    packing.nilai_kemasan_primer = (
        nilai_primer
    )

    packing.nilai_kemasan_sekunder = (
        nilai_sekunder
    )

    packing.cost_nom = (
        total_cost
    )

    packing.menghabiskan = (
        menghabiskan
    )

    packing.status = (
        StatusDokumen.POSTED
    )

    packing.posted_at = (
        timezone.now()
    )

    packing.save(
        update_fields=[
            "harga_per_kg",
            "nilai_kemasan_primer",
            "nilai_kemasan_sekunder",
            "cost_nom",
            "menghabiskan",
            "status",
            "posted_at",
        ]
    )

    # --------------------------------------------------------
    # POTONG TANGKI
    # --------------------------------------------------------

    tangki.saldo_kg = qty(
        tangki.saldo_kg
        - packing.qty_kg
    )

    tangki.saldo_nilai = rp(
        tangki.saldo_nilai
        - cost_bahan
    )

    if tangki.saldo_kg <= D0_QTY:
        tangki.saldo_kg = D0_QTY
        tangki.saldo_nilai = D0_RP

    tangki.save(
        update_fields=[
            "saldo_kg",
            "saldo_nilai",
        ]
    )

    # --------------------------------------------------------
    # MUTASI KLAIM
    # --------------------------------------------------------

    MutasiKlaim.objects.create(
        entitas=packing.entitas,
        grup_bahan=(
            packing.entitas.grup_bahan
        ),
        tipe=TipeMutasi.TARIK,
        arah=-1,
        qty_kg=packing.qty_kg,
        nilai=total_cost,
        ref_type="Packing",
        ref_id=packing.id,
        keterangan=(
            f"Packing {packing.nomor}"
        ),
        waktu=packing.waktu,
        dibuat_oleh=user,
    )

    saldo = _kunci_saldo(
        packing.entitas_id
    )

    saldo.total_tarik = rp(
        saldo.total_tarik
        + total_cost
    )

    saldo.qty_tarik = qty(
        saldo.qty_tarik
        + packing.qty_kg
    )

    saldo.saldo = rp(
        saldo.saldo
        - total_cost
    )

    saldo.save(
        update_fields=[
            "total_tarik",
            "qty_tarik",
            "saldo",
        ]
    )

    assert_invarian()

    return packing


# ============================================================
# ROLLBACK PACKING
# ============================================================

@transaction.atomic
def rollback_hapus_packing(
    packing,
):
    packing = (
        Packing.objects
        .select_for_update()
        .get(pk=packing.pk)
    )

    _pastikan_status_packing(
        packing,
        StatusDokumen.POSTED,
    )

    if not packing.posted_at:
        raise KonflikSaldo(
            f"Packing {packing.nomor} tidak memiliki "
            f"posted_at."
        )

    tangki = (
        Tangki.objects
        .select_for_update()
        .get(
            pk=packing.tangki_id
        )
    )

    pool_primer = (
        PoolKemasan.objects
        .select_for_update()
        .get(
            pk=packing.kemasan_primer_id
        )
    )

    nilai_primer = rp(
        packing.nilai_kemasan_primer
        or 0
    )

    nilai_sekunder = rp(
        packing.nilai_kemasan_sekunder
        or 0
    )

    total_unit_primer = int(
        packing.total_unit
    )

    # Kembalikan bahan ke tangki
    nilai_bahan = rp(
        packing.cost_nom
        - nilai_primer
        - nilai_sekunder
    )

    if nilai_bahan < D0_RP:
        raise InvariantMelenceng(
            f"Nilai bahan Packing {packing.nomor} "
            f"menjadi negatif."
        )

    tangki.saldo_kg = qty(
        tangki.saldo_kg
        + packing.qty_kg
    )

    tangki.saldo_nilai = rp(
        tangki.saldo_nilai
        + nilai_bahan
    )

    tangki.save(
        update_fields=[
            "saldo_kg",
            "saldo_nilai",
        ]
    )

    # Kembalikan primer dengan nilai historis
    pool_primer.qty_unit += (
        total_unit_primer
    )

    pool_primer.nilai = rp(
        pool_primer.nilai
        + nilai_primer
    )

    pool_primer.save(
        update_fields=[
            "qty_unit",
            "nilai",
        ]
    )

    # Kembalikan sekunder dengan nilai historis
    if (
        packing.kemasan_sekunder_id
        and packing.qty_kemasan_sekunder
        and packing.qty_kemasan_sekunder > 0
    ):
        pool_sekunder = (
            PoolKemasan.objects
            .select_for_update()
            .get(
                pk=packing.kemasan_sekunder_id
            )
        )

        total_unit_sekunder = (
            total_unit_primer
            * int(
                packing.qty_kemasan_sekunder
            )
        )

        pool_sekunder.qty_unit += (
            total_unit_sekunder
        )

        pool_sekunder.nilai = rp(
            pool_sekunder.nilai
            + nilai_sekunder
        )

        pool_sekunder.save(
            update_fields=[
                "qty_unit",
                "nilai",
            ]
        )

    # Stok barang jadi dikurangi kembali
    isi_per_kemasan = (
        packing.qty_kg
        / Decimal(
            str(packing.total_unit)
        )
    ).quantize(
        Decimal("0.001")
    )

    kemasan_cocok = (
        Kemasan.objects
        .filter(
            aktif=True,
            bobot_kg__gte=(
                isi_per_kemasan
                - Decimal("0.001")
            ),
            bobot_kg__lte=(
                isi_per_kemasan
                + Decimal("0.001")
            ),
        )
        .first()
    )

    if kemasan_cocok:
        stok_jadi = (
            StokBarangJadi.objects
            .select_for_update()
            .filter(
                entitas_id=packing.entitas_id,
                grup_bahan_id=(
                    packing.entitas.grup_bahan_id
                ),
                item_id=packing.nama_hasil_id,
                kemasan=kemasan_cocok,
            )
            .first()
        )

        if stok_jadi:
            stok_jadi.qty_unit -= int(
                packing.total_unit
            )

            stok_jadi.qty_kg = qty(
                stok_jadi.qty_kg
                - packing.qty_kg
            )

            stok_jadi.nilai = rp(
                stok_jadi.nilai
                - packing.cost_nom
            )

            if stok_jadi.qty_unit <= 0:
                stok_jadi.qty_unit = 0

            if stok_jadi.qty_kg < 0:
                stok_jadi.qty_kg = D0_QTY

            if stok_jadi.nilai < 0:
                stok_jadi.nilai = D0_RP

            stok_jadi.save(
                update_fields=[
                    "qty_unit",
                    "qty_kg",
                    "nilai",
                ]
            )

    MutasiKlaim.objects.create(
        entitas_id=packing.entitas_id,
        grup_bahan_id=(
            packing.entitas.grup_bahan_id
        ),
        tipe=TipeMutasi.SETOR,
        arah=1,
        qty_kg=packing.qty_kg,
        nilai=packing.cost_nom,
        ref_type="PACKING_BATAL",
        ref_id=str(packing.id),
        keterangan=(
            f"Pembatalan {packing.nomor}"
        ),
    )

    saldo = (
        SaldoEntitas.objects
        .select_for_update()
        .get(
            entitas_id=packing.entitas_id
        )
    )

    saldo.saldo = rp(
        saldo.saldo
        + packing.cost_nom
    )

    saldo.qty_tarik = qty(
        saldo.qty_tarik
        - packing.qty_kg
    )

    saldo.save(
        update_fields=[
            "saldo",
            "qty_tarik",
        ]
    )

    packing.status = (
        StatusDokumen.DRAFT
    )

    packing.posted_at = None
    packing.cost_nom = D0_RP
    packing.nilai_kemasan_primer = D0_RP
    packing.nilai_kemasan_sekunder = D0_RP
    packing.menghabiskan = False

    packing.save(
        update_fields=[
            "status",
            "posted_at",
            "cost_nom",
            "nilai_kemasan_primer",
            "nilai_kemasan_sekunder",
            "menghabiskan",
        ]
    )

    assert_invarian()


# ============================================================
# VOID PACKING
# ============================================================

@transaction.atomic
def void_packing(
    packing,
    alasan,
    user=None,
):
    user = _wajib_user(user)

    packing = (
        Packing.objects
        .select_for_update()
        .get(pk=packing.pk)
    )

    _pastikan_status_packing(
        packing,
        StatusDokumen.POSTED,
    )

    if packing.voided_at is not None:
        raise KonflikSaldo(
            f"Packing {packing.nomor} sudah di-VOID."
        )

    if not alasan or not alasan.strip():
        raise GalatInventory(
            "Alasan VOID wajib diisi."
        )

    if not packing.posted_at:
        raise KonflikSaldo(
            f"Packing {packing.nomor} tidak memiliki posted_at."
        )

    _pastikan_periode_terbuka(
        packing.entitas,
        timezone.localdate(),
    )

    nilai_primer = rp(
        packing.nilai_kemasan_primer
        or 0
    )

    nilai_sekunder = rp(
        packing.nilai_kemasan_sekunder
        or 0
    )

    total_unit_primer = int(
        packing.total_unit
    )

    # --------------------------------------------------------
    # KEMBALIKAN PRIMER
    # --------------------------------------------------------

    pool_primer = (
        PoolKemasan.objects
        .select_for_update()
        .get(
            pk=packing.kemasan_primer_id
        )
    )

    pool_primer.qty_unit += (
        total_unit_primer
    )

    pool_primer.nilai = rp(
        pool_primer.nilai
        + nilai_primer
    )

    pool_primer.save(
        update_fields=[
            "qty_unit",
            "nilai",
        ]
    )

    # --------------------------------------------------------
    # KEMBALIKAN SEKUNDER
    # --------------------------------------------------------

    if (
        packing.kemasan_sekunder_id
        and packing.qty_kemasan_sekunder
        and packing.qty_kemasan_sekunder > 0
    ):
        pool_sekunder = (
            PoolKemasan.objects
            .select_for_update()
            .get(
                pk=packing.kemasan_sekunder_id
            )
        )

        total_unit_sekunder = (
            total_unit_primer
            * int(
                packing.qty_kemasan_sekunder
            )
        )

        pool_sekunder.qty_unit += (
            total_unit_sekunder
        )

        pool_sekunder.nilai = rp(
            pool_sekunder.nilai
            + nilai_sekunder
        )

        pool_sekunder.save(
            update_fields=[
                "qty_unit",
                "nilai",
            ]
        )

    # --------------------------------------------------------
    # KEMBALIKAN BAHAN KE TANGKI
    # --------------------------------------------------------

    nilai_bahan = rp(
        packing.cost_nom
        - nilai_primer
        - nilai_sekunder
    )

    if nilai_bahan < D0_RP:
        raise InvariantMelenceng(
            f"Nilai bahan Packing {packing.nomor} "
            f"menjadi negatif saat VOID."
        )

    tangki = (
        Tangki.objects
        .select_for_update()
        .get(
            pk=packing.tangki_id
        )
    )

    tangki.saldo_kg = qty(
        tangki.saldo_kg
        + packing.qty_kg
    )

    tangki.saldo_nilai = rp(
        tangki.saldo_nilai
        + nilai_bahan
    )

    tangki.save(
        update_fields=[
            "saldo_kg",
            "saldo_nilai",
        ]
    )

    # --------------------------------------------------------
    # KURANGI BARANG JADI
    # --------------------------------------------------------

    isi_per_kemasan = (
        packing.qty_kg
        / Decimal(
            str(packing.total_unit)
        )
    ).quantize(
        Decimal("0.001")
    )

    kemasan_cocok = (
        Kemasan.objects
        .filter(
            aktif=True,
            bobot_kg__gte=(
                isi_per_kemasan
                - Decimal("0.001")
            ),
            bobot_kg__lte=(
                isi_per_kemasan
                + Decimal("0.001")
            ),
        )
        .first()
    )

    if kemasan_cocok:
        stok_jadi = (
            StokBarangJadi.objects
            .select_for_update()
            .filter(
                entitas_id=packing.entitas_id,
                grup_bahan_id=(
                    packing.entitas.grup_bahan_id
                ),
                item_id=packing.nama_hasil_id,
                kemasan=kemasan_cocok,
            )
            .first()
        )

        if stok_jadi:
            stok_jadi.qty_unit -= int(
                packing.total_unit
            )

            stok_jadi.qty_kg = qty(
                stok_jadi.qty_kg
                - packing.qty_kg
            )

            stok_jadi.nilai = rp(
                stok_jadi.nilai
                - packing.cost_nom
            )

            if stok_jadi.qty_unit <= 0:
                stok_jadi.qty_unit = 0
                stok_jadi.qty_kg = D0_QTY
                stok_jadi.nilai = D0_RP

            if stok_jadi.qty_kg < 0:
                stok_jadi.qty_kg = D0_QTY

            if stok_jadi.nilai < 0:
                stok_jadi.nilai = D0_RP

            stok_jadi.save(
                update_fields=[
                    "qty_unit",
                    "qty_kg",
                    "nilai",
                ]
            )

    # --------------------------------------------------------
    # MUTASI
    # --------------------------------------------------------

    MutasiKlaim.objects.create(
        entitas=packing.entitas,
        grup_bahan=(
            packing.entitas.grup_bahan
        ),
        tipe=TipeMutasi.PENYESUAIAN,
        arah=1,
        qty_kg=packing.qty_kg,
        nilai=packing.cost_nom,
        ref_type="VoidPacking",
        ref_id=packing.id,
        keterangan=(
            f"VOID {packing.nomor}: "
            f"{alasan.strip()}"
        ),
        waktu=timezone.now(),
        dibuat_oleh=user,
    )

    saldo = _kunci_saldo(
        packing.entitas_id
    )

    saldo.total_tarik = rp(
        saldo.total_tarik
        - packing.cost_nom
    )

    saldo.qty_tarik = qty(
        saldo.qty_tarik
        - packing.qty_kg
    )

    saldo.saldo = rp(
        saldo.saldo
        + packing.cost_nom
    )

    saldo.save(
        update_fields=[
            "total_tarik",
            "qty_tarik",
            "saldo",
        ]
    )

    packing.status = (
        StatusDokumen.VOID
    )

    packing.voided_at = timezone.now()

    packing.save(
        update_fields=[
            "status",
            "voided_at",
        ]
    )

    assert_invarian()

    return packing


# ============================================================
# PREVIEW PACKING
# ============================================================

def pratinjau_packing(
    tangki_id,
    qty_diminta,
):
    try:
        tangki = (
            Tangki.objects
            .get(
                pk=int(tangki_id)
            )
        )
    except (
        ObjectDoesNotExist,
        ValueError,
        TypeError,
    ):
        return {
            "valid": False,
            "kode": "TANGKI_TIDAK_DITEMUKAN",
            "pesan": (
                "Tangki tidak ditemukan "
                "atau ID tidak valid."
            ),
        }

    if not tangki.aktif:
        return {
            "valid": False,
            "kode": "TANGKI_TIDAK_AKTIF",
            "pesan": (
                f"Tangki {tangki.kode} "
                "tidak aktif."
            ),
        }

    if tangki.saldo_kg <= D0_QTY:
        return {
            "valid": False,
            "kode": "SALDO_TANGKI_KOSONG",
            "pesan": (
                f"Tangki {tangki.kode} "
                "tidak memiliki saldo."
            ),
        }

    try:
        q = qty(
            Decimal(
                str(qty_diminta)
            )
        )
    except Exception:
        return {
            "valid": False,
            "kode": "QTY_TIDAK_VALID",
            "pesan": "Qty harus berupa angka.",
        }

    if q <= 0:
        return {
            "valid": False,
            "kode": "QTY_TIDAK_VALID",
            "pesan": "Qty harus lebih dari 0.",
        }

    if q > (
        tangki.saldo_kg
        + TOL_QTY
    ):
        return {
            "valid": False,
            "kode": "SISA_TANGKI_KURANG",
            "pesan": (
                f"Tangki {tangki.kode} "
                f"tinggal {tangki.saldo_kg} Kg."
            ),
        }

    menghabiskan = (
        abs(
            q
            - tangki.saldo_kg
        )
        <= TOL_QTY
    )

    harga_rata = (
        rp(
            tangki.saldo_nilai
            / tangki.saldo_kg
        )
        if tangki.saldo_kg > 0
        else D0_RP
    )

    nilai = (
        tangki.saldo_nilai
        if menghabiskan
        else rp(
            q
            * harga_rata
        )
    )

    return {
        "valid": True,
        "tangki": tangki.kode,
        "tangki_id": tangki.id,
        "saldo_kg": str(tangki.saldo_kg),
        "saldo_nilai": str(tangki.saldo_nilai),
        "qty_kg": str(q),
        "harga_per_kg": str(harga_rata),
        "nilai_tagihan": str(nilai),
        "menghabiskan": menghabiskan,
        "peringatan": (
            [
                f"Pengambilan ini MENGHABISKAN "
                f"sisa tangki {tangki.kode}."
            ]
            if menghabiskan
            else []
        ),
    }


# ============================================================
# NOMOR PACKING
# ============================================================

@transaction.atomic
def generate_nomor_packing(
    entitas_id,
):
    last = (
        Packing.objects
        .select_for_update()
        .filter(
            entitas_id=entitas_id
        )
        .order_by("-id")
        .first()
    )

    nomor_urut = 1

    if last and last.nomor:
        try:
            nomor_urut = (
                int(
                    last.nomor.rsplit(
                        "-",
                        1,
                    )[1]
                )
                + 1
            )
        except (
            ValueError,
            IndexError,
        ):
            nomor_urut = 1

    return (
        f"PKG-{entitas_id}-"
        f"{nomor_urut:03d}"
    )


# ============================================================
# SUSUT
# ============================================================

@transaction.atomic
def bebankan_susut(
    batch,
    user=None,
):
    user = _wajib_user(user)

    nilai_susut = rp(
        batch.nilai_susut or 0
    )

    if nilai_susut <= 0:
        return {}

    baris = list(
        SaldoEntitas.objects
        .select_for_update()
        .filter(
            entitas__aktif=True,
            saldo__gt=0,
        )
        .select_related(
            "entitas",
            "entitas__grup_bahan",
        )
        .order_by(
            "entitas_id"
        )
    )

    if not baris:
        raise InvariantMelenceng(
            f"Susut Rp{nilai_susut:,.2f} "
            f"pada batch {batch.nomor} "
            f"tidak bisa dibebankan."
        )

    total = sum(
        row.saldo
        for row in baris
    )

    urut = sorted(
        baris,
        key=lambda row: (
            -row.saldo,
            row.entitas_id,
        ),
    )

    beban = {}
    terpakai = D0_RP

    for row in urut[1:]:
        nilai = rp(
            nilai_susut
            * row.saldo
            / total
        )

        beban[row.entitas_id] = nilai
        terpakai += nilai

    beban[
        urut[0].entitas_id
    ] = rp(
        nilai_susut
        - terpakai
    )

    peta = {
        row.entitas_id: row
        for row in baris
    }

    for entitas_id, nilai in beban.items():
        if nilai <= 0:
            continue

        saldo = peta[entitas_id]

        MutasiKlaim.objects.create(
            entitas=saldo.entitas,
            grup_bahan=saldo.entitas.grup_bahan,
            tipe=TipeMutasi.RUGI,
            arah=-1,
            qty_kg=D0_QTY,
            nilai=nilai,
            ref_type="Batch",
            ref_id=batch.id,
            keterangan=(
                f"Susut produksi {batch.nomor}"
            ),
            waktu=(
                batch.posted_at
                or timezone.now()
            ),
            dibuat_oleh=user,
        )

        saldo.total_rugi = rp(
            saldo.total_rugi + nilai
        )

        saldo.saldo = rp(
            saldo.saldo - nilai
        )

        saldo.save(
            update_fields=[
                "total_rugi",
                "saldo",
            ]
        )

    if (
        abs(
            sum(beban.values())
            - nilai_susut
        )
        > TOL_RP
    ):
        raise InvariantMelenceng(
            "Pembagian susut tidak "
            "berjumlah sesuai nilai susut."
        )

    return beban


# ============================================================
# POOL RESOURCE
# ============================================================

def get_pool_resource_all():
    qs = (
        PoolResource.objects
        .select_related("produk")
        .all()
    )

    rincian = []
    total_nilai = D0_RP

    for pool in qs:
        rincian.append({
            "produk_id": pool.produk_id,
            "produk_kode": pool.produk.kode,
            "produk_nama": pool.produk.nama,
            "qty_kg": str(pool.qty_kg),
            "nilai": str(pool.nilai),
            "harga_rata": str(pool.harga_rata),
        })

        total_nilai += pool.nilai

    return {
        "rincian": rincian,
        "total_nilai_pool": str(
            rp(total_nilai)
        ),
    }


def get_pool_kemasan_all():
    qs = (
        PoolKemasan.objects
        .select_related("produk")
        .all()
    )

    rincian = []
    total_nilai = D0_RP

    for pool in qs:
        rincian.append({
            "id": pool.id,
            "produk_id": pool.produk_id,
            "produk_kode": pool.produk.kode,
            "produk_nama": pool.produk.nama,
            "kategori": pool.kategori,
            "kategori_label": (
                pool.get_kategori_display()
            ),
            "qty_unit": pool.qty_unit,
            "nilai": str(pool.nilai),
            "harga_satuan": str(
                pool.harga_satuan
            ),
        })

        total_nilai += pool.nilai

    return {
        "rincian": rincian,
        "total_nilai_pool": str(
            rp(total_nilai)
        ),
    }


# ============================================================
# INVARIANT
# ============================================================

def jalankan_pemeriksaan_invarian():
    try:
        return assert_invarian(
            raise_on_fail=False
        )
    except Exception as exc:
        return {
            "cocok": False,
            "catatan": [
                str(exc)
            ],
            "rincian": [],
        }


def assert_invarian(
    raise_on_fail=True,
):
    catatan = []

    hak_total = (
        SaldoEntitas.objects
        .aggregate(
            total=Coalesce(
                Sum("saldo"),
                Value(D0_RP),
                output_field=F_RP,
            )
        )["total"]
    )

    pool_resource_total = (
        PoolResource.objects
        .aggregate(
            total=Coalesce(
                Sum("nilai"),
                Value(D0_RP),
                output_field=F_RP,
            )
        )["total"]
    )

    pool_kemasan_total = (
        PoolKemasan.objects
        .aggregate(
            total=Coalesce(
                Sum("nilai"),
                Value(D0_RP),
                output_field=F_RP,
            )
        )["total"]
    )

    pool_total = rp(
        pool_resource_total
        + pool_kemasan_total
    )

    wip_total = (
        Tangki.objects
        .aggregate(
            total=Coalesce(
                Sum("saldo_nilai"),
                Value(D0_RP),
                output_field=F_RP,
            )
        )["total"]
    )

    fisik_total = rp(
        pool_total
        + wip_total
    )

    selisih = rp(
        hak_total
        - fisik_total
    )

    if (
        PoolResource.objects
        .filter(
            Q(qty_kg__lt=0)
            | Q(nilai__lt=0)
        )
        .exists()
    ):
        catatan.append(
            "PoolResource memiliki saldo negatif."
        )

    if (
        PoolResource.objects
        .filter(qty_kg=0)
        .exclude(nilai=0)
        .exists()
    ):
        catatan.append(
            "PoolResource kosong tetapi masih memiliki nilai."
        )

    if (
        PoolKemasan.objects
        .filter(
            Q(qty_unit__lt=0)
            | Q(nilai__lt=0)
        )
        .exists()
    ):
        catatan.append(
            "PoolKemasan memiliki saldo negatif."
        )

    if (
        PoolKemasan.objects
        .filter(qty_unit=0)
        .exclude(nilai=0)
        .exists()
    ):
        catatan.append(
            "PoolKemasan kosong tetapi masih memiliki nilai."
        )

    if (
        PoolKemasan.objects
        .filter(kategori__isnull=True)
        .exists()
    ):
        catatan.append(
            "Ada PoolKemasan tanpa kategori."
        )

    rincian = [{
        "hak_global": hak_total,
        "pool_global": pool_total,
        "wip_produksi": wip_total,
        "fisik_kalkulasi": fisik_total,
        "selisih": selisih,
    }]

    if catatan and raise_on_fail:
        raise InvariantMelenceng(
            " | ".join(catatan)
        )

    return {
        "cocok": not catatan,
        "catatan": catatan,
        "rincian": rincian,
    }


# ============================================================
# REKAP
# ============================================================

def get_rekap_klaim(
    grup_id=None,
):
    queryset = (
        MutasiKlaim.objects.all()
    )

    if grup_id:
        queryset = queryset.filter(
            grup_bahan_id=grup_id
        )

    data = list(
        queryset.values()
    )

    return {
        "results": data,
        "total": len(data),
    }


# ============================================================
# BARANG JADI
# ============================================================

def get_barang_jadi(
    grup=None,
):
    qs = (
        StokBarangJadi.objects
        .select_related(
            "entitas",
            "item",
            "kemasan",
        )
        .all()
    )

    if grup:
        qs = qs.filter(
            grup_bahan_id=grup
        )

    rincian = [
        {
            "entitas_id": stok.entitas_id,
            "entitas_kode": stok.entitas.kode,
            "item_id": stok.item_id,
            "item_nama": stok.item.nama_item,
            "kemasan_id": stok.kemasan_id,
            "kemasan_nama": stok.kemasan.nama,
            "qty_unit": stok.qty_unit,
            "qty_kg": str(stok.qty_kg),
            "nilai": str(stok.nilai),
        }
        for stok in qs
    ]

    total_nilai = sum(
        (
            stok.nilai
            for stok in qs
        ),
        D0_RP,
    )

    return {
        "rincian": rincian,
        "total_nilai": str(
            rp(total_nilai)
        ),
    }

