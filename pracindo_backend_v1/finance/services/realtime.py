"""
Stempel versi data untuk dashboard realtime. Bukan model, tanpa migration.

Di sistem ini tidak ada saldo yang berubah tanpa menulis baris
append-only baru, jadi MAX(id) tabel-tabel itu cukup jadi penanda versi.
MAX(id) dipakai, bukan COUNT, karena COUNT memindai seluruh tabel
sementara MAX(id) hanya membaca ujung indeks.
"""
from hashlib import blake2s

from django.db.models import Max


class CountRealtime:
    """Stempel versi dari tabel append-only."""

    @classmethod
    def _tabel(cls):
        from akunting.models import JurnalUmum, KartuHutang, KartuPiutang
        from inventory.models import MutasiKlaim, Packing, Pembelian
        from produksi.models import Batch

        return {
            'jurnal': JurnalUmum,
            'kartu_hutang': KartuHutang,
            'kartu_piutang': KartuPiutang,
            'mutasi_klaim': MutasiKlaim,
            'packing': Packing,
            'pembelian': Pembelian,
            'batch': Batch,
        }

    @classmethod
    def cacah(cls):
        hasil = {}
        for nama, model in cls._tabel().items():
            hasil[nama] = model.objects.aggregate(m=Max('id'))['m'] or 0
        return hasil

    @classmethod
    def stempel(cls):
        c = cls.cacah()
        mentah = '|'.join(f'{k}:{c[k]}' for k in sorted(c))
        return blake2s(mentah.encode(), digest_size=8).hexdigest()

    @classmethod
    def ringkas(cls):
        return {'versi': cls.stempel(), 'cacah': cls.cacah()}

    @classmethod
    def berubah_dari(cls, versi_lama):
        return cls.stempel() != versi_lama
