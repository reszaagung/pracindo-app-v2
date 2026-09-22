from decimal import Decimal

from master.models import MasterProduk
from produksi.models import Tangki
from rest_framework import serializers

from .models import (
    KategoriKemasan,
    Kemasan,
    MutasiKlaim,
    Packing,
    Pembelian,
    PoolKemasan,
    PoolResource,
    SaldoEntitas,
    StatusDokumen,
)


class KemasanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kemasan
        fields = [
            "id",
            "nama",
            "bobot_kg",
            "aktif",
        ]


class PoolResourceSerializer(serializers.ModelSerializer):
    produk_kode = serializers.CharField(
        source="produk.kode",
        read_only=True,
    )

    produk_nama = serializers.CharField(
        source="produk.nama",
        read_only=True,
    )

    harga_rata = serializers.DecimalField(
        max_digits=20,
        decimal_places=6,
        read_only=True,
    )

    class Meta:
        model = PoolResource
        fields = [
            "id",
            "produk",
            "produk_kode",
            "produk_nama",
            "qty_kg",
            "nilai",
            "harga_rata",
            "diubah_pada",
        ]
        read_only_fields = [
            "id",
            "produk",
            "produk_kode",
            "produk_nama",
            "qty_kg",
            "nilai",
            "harga_rata",
            "diubah_pada",
        ]


class SaldoEntitasSerializer(serializers.ModelSerializer):
    entitas_kode = serializers.CharField(
        source="entitas.kode",
        read_only=True,
    )

    entitas_nama = serializers.CharField(
        source="entitas.nama",
        read_only=True,
    )

    grup_kode = serializers.CharField(
        source="entitas.grup_bahan.kode",
        read_only=True,
    )

    status = serializers.SerializerMethodField()

    class Meta:
        model = SaldoEntitas
        fields = [
            "entitas",
            "entitas_kode",
            "entitas_nama",
            "grup_kode",
            "qty_setor",
            "qty_tarik",
            "total_setor",
            "total_tarik",
            "total_rugi",
            "saldo",
            "status",
            "diubah_pada",
        ]
        read_only_fields = fields

    def get_status(self, obj):
        if obj.saldo == Decimal("0"):
            return "IMPAS"

        return "KLAIM" if obj.saldo > 0 else "HUTANG"


class PembelianSerializer(serializers.ModelSerializer):
    entitas_kode = serializers.CharField(
        source="entitas.kode",
        read_only=True,
    )

    grup_kode = serializers.CharField(
        source="grup_bahan.kode",
        read_only=True,
    )

    produk_kode = serializers.CharField(
        source="produk.kode",
        read_only=True,
    )

    produk_nama = serializers.CharField(
        source="produk.nama",
        read_only=True,
    )

    kategori_kemasan_label = serializers.SerializerMethodField()

    class Meta:
        model = Pembelian
        fields = [
            "id",
            "nomor",
            "no_po",
            "entitas",
            "entitas_kode",
            "grup_bahan",
            "grup_kode",
            "produk",
            "produk_kode",
            "produk_nama",
            "qty_kg",
            "harga_per_kg",
            "qty_unit",
            "harga_per_unit",
            "kategori_kemasan",
            "kategori_kemasan_label",
            "nilai",
            "tanggal",
            "waktu",
            "status",
            "sumber",
            "penerimaan_item",
            "catatan",
            "dibuat_oleh",
            "dibuat_pada",
            "posted_at",
        ]
        read_only_fields = [
            "id",
            "nomor",
            "nilai",
            "status",
            "sumber",
            "penerimaan_item",
            "grup_bahan",
            "dibuat_oleh",
            "dibuat_pada",
            "posted_at",
            "kategori_kemasan_label",
        ]

    def get_kategori_kemasan_label(self, obj):
        if not obj.kategori_kemasan:
            return None

        return obj.get_kategori_kemasan_display()

    def validate(self, data):
        instance = self.instance

        if (
            instance
            and instance.status != StatusDokumen.DRAFT
        ):
            raise serializers.ValidationError({
                "kode": "DOKUMEN_TERKUNCI",
                "pesan": (
                    f"Pembelian {instance.nomor} sudah "
                    f"{instance.status} dan tidak bisa diubah."
                ),
            })

        qty_kg = data.get(
            "qty_kg",
            getattr(instance, "qty_kg", None),
        )

        harga_per_kg = data.get(
            "harga_per_kg",
            getattr(instance, "harga_per_kg", None),
        )

        qty_unit = data.get(
            "qty_unit",
            getattr(instance, "qty_unit", None),
        )

        harga_per_unit = data.get(
            "harga_per_unit",
            getattr(instance, "harga_per_unit", None),
        )

        kategori = data.get(
            "kategori_kemasan",
            getattr(instance, "kategori_kemasan", None),
        )

        if qty_kg is not None and qty_kg <= 0:
            raise serializers.ValidationError({
                "qty_kg": "Qty harus lebih dari 0."
            })

        if harga_per_kg is not None and harga_per_kg < 0:
            raise serializers.ValidationError({
                "harga_per_kg": "Harga tidak boleh negatif."
            })

        produk = data.get(
            "produk",
            getattr(instance, "produk", None),
        )

        if produk is not None and produk.jenis == "KEMASAN":
            if qty_unit is None or qty_unit <= 0:
                raise serializers.ValidationError({
                    "qty_unit": (
                        "Qty Kemasan wajib diisi dalam Unit."
                    )
                })

            if (
                harga_per_unit is None
                or harga_per_unit < 0
            ):
                raise serializers.ValidationError({
                    "harga_per_unit": (
                        "Harga per Unit Kemasan wajib diisi."
                    )
                })

            if kategori not in (
                KategoriKemasan.PRIMER,
                KategoriKemasan.SEKUNDER,
                KategoriKemasan.PRIMER_SEKUNDER,
            ):
                raise serializers.ValidationError({
                    "kategori_kemasan": (
                        "Kategori kemasan wajib Primer, "
                        "Sekunder, atau Primer & Sekunder."
                    )
                })

        entitas = data.get(
            "entitas",
            getattr(instance, "entitas", None),
        )

        if entitas is not None and not entitas.aktif:
            raise serializers.ValidationError({
                "entitas": (
                    f"Entitas {entitas.kode} "
                    "nonaktif dan tidak bisa menyetor."
                )
            })

        return data


class PoolKemasanSerializer(serializers.ModelSerializer):
    produk_kode = serializers.CharField(
        source="produk.kode",
        read_only=True,
    )

    produk_nama = serializers.CharField(
        source="produk.nama",
        read_only=True,
    )

    kategori_label = serializers.SerializerMethodField()

    harga_satuan = serializers.DecimalField(
        max_digits=20,
        decimal_places=6,
        read_only=True,
    )

    tersedia = serializers.SerializerMethodField()

    class Meta:
        model = PoolKemasan
        fields = [
            "id",
            "produk",
            "produk_kode",
            "produk_nama",
            "kategori",
            "kategori_label",
            "qty_unit",
            "nilai",
            "harga_satuan",
            "tersedia",
            "diubah_pada",
        ]
        read_only_fields = fields

    def get_kategori_label(self, obj):
        return obj.get_kategori_display()

    def get_tersedia(self, obj):
        return obj.qty_unit > 0


class PackingSerializer(serializers.ModelSerializer):
    entitas_kode = serializers.CharField(
        source="entitas.kode",
        read_only=True,
    )

    entitas_nama = serializers.CharField(
        source="entitas.nama",
        read_only=True,
    )

    tangki_kode = serializers.CharField(
        source="tangki.kode",
        read_only=True,
    )

    tangki_nama = serializers.CharField(
        source="tangki.nama",
        read_only=True,
    )

    tangki_saldo_kg = serializers.DecimalField(
        source="tangki.saldo_kg",
        max_digits=18,
        decimal_places=3,
        read_only=True,
    )

    tangki_saldo_nilai = serializers.DecimalField(
        source="tangki.saldo_nilai",
        max_digits=20,
        decimal_places=2,
        read_only=True,
    )

    tangki_harga_per_kg = serializers.SerializerMethodField()

    produk = serializers.PrimaryKeyRelatedField(
        source="nama_hasil",
        queryset=MasterProduk.objects.all(),
        required=True,
    )

    produk_kode = serializers.CharField(
        source="nama_hasil.id",
        read_only=True,
    )

    produk_nama = serializers.CharField(
        source="nama_hasil.nama_item",
        read_only=True,
    )

    kemasan_primer_nama = serializers.CharField(
        source="kemasan_primer.produk.nama",
        read_only=True,
    )

    kemasan_primer_kode = serializers.CharField(
        source="kemasan_primer.produk.kode",
        read_only=True,
        default=None,
    )

    kemasan_primer_kategori = serializers.CharField(
        source="kemasan_primer.kategori",
        read_only=True,
    )

    kemasan_primer_harga_satuan = serializers.DecimalField(
        source="kemasan_primer.harga_satuan",
        max_digits=20,
        decimal_places=6,
        read_only=True,
    )

    kemasan_sekunder_nama = serializers.CharField(
        source="kemasan_sekunder.produk.nama",
        read_only=True,
        allow_null=True,
    )

    kemasan_sekunder_kode = serializers.CharField(
        source="kemasan_sekunder.produk.kode",
        read_only=True,
        allow_null=True,
    )

    kemasan_sekunder_kategori = serializers.CharField(
        source="kemasan_sekunder.kategori",
        read_only=True,
        allow_null=True,
    )

    kemasan_sekunder_harga_satuan = serializers.DecimalField(
        source="kemasan_sekunder.harga_satuan",
        max_digits=20,
        decimal_places=6,
        read_only=True,
        allow_null=True,
    )

    harga_kemasan_primer = serializers.SerializerMethodField()
    harga_kemasan_sekunder = serializers.SerializerMethodField()
    total_nilai_kemasan = serializers.SerializerMethodField()
    status_label = serializers.SerializerMethodField()

    class Meta:
        model = Packing
        fields = (
            "id",
            "nomor",
            "tanggal",
            "waktu",
            "status",
            "status_label",
            "posted_at",
            "voided_at",
            "entitas",
            "entitas_kode",
            "entitas_nama",
            "tangki",
            "tangki_kode",
            "tangki_nama",
            "tangki_saldo_kg",
            "tangki_saldo_nilai",
            "tangki_harga_per_kg",
            "produk",
            "produk_kode",
            "produk_nama",
            "kemasan_primer",
            "kemasan_primer_kode",
            "kemasan_primer_nama",
            "kemasan_primer_kategori",
            "kemasan_primer_harga_satuan",
            "nilai_kemasan_primer",
            "harga_kemasan_primer",
            "kemasan_sekunder",
            "kemasan_sekunder_kode",
            "kemasan_sekunder_nama",
            "kemasan_sekunder_kategori",
            "kemasan_sekunder_harga_satuan",
            "qty_kemasan_sekunder",
            "nilai_kemasan_sekunder",
            "harga_kemasan_sekunder",
            "total_nilai_kemasan",
            "total_unit",
            "qty_kg",
            "harga_per_kg",
            "cost_nom",
            "menghabiskan",
            "dibuat_oleh",
            "dibuat_pada",
        )

        read_only_fields = (
            "id",
            "nomor",
            "waktu",
            "tangki_kode",
            "tangki_nama",
            "tangki_saldo_kg",
            "tangki_saldo_nilai",
            "tangki_harga_per_kg",
            "produk_kode",
            "produk_nama",
            "kemasan_primer_kode",
            "kemasan_primer_nama",
            "kemasan_primer_kategori",
            "kemasan_primer_harga_satuan",
            "kemasan_sekunder_kode",
            "kemasan_sekunder_nama",
            "kemasan_sekunder_kategori",
            "kemasan_sekunder_harga_satuan",
            "nilai_kemasan_primer",
            "nilai_kemasan_sekunder",
            "harga_kemasan_primer",
            "harga_kemasan_sekunder",
            "total_nilai_kemasan",
            "harga_per_kg",
            "cost_nom",
            "menghabiskan",
            "status",
            "status_label",
            "posted_at",
            "voided_at",
            "dibuat_oleh",
            "dibuat_pada",
        )

    def get_tangki_harga_per_kg(self, obj):
        saldo_kg = obj.tangki.saldo_kg
        saldo_nilai = obj.tangki.saldo_nilai

        if not saldo_kg or saldo_kg <= Decimal("0"):
            return "0.000000"

        return str(
            saldo_nilai / saldo_kg
        )

    def get_harga_kemasan_primer(self, obj):
        pool = getattr(
            obj,
            "kemasan_primer",
            None,
        )

        if not pool:
            return "0.00"

        return str(pool.harga_satuan)

    def get_harga_kemasan_sekunder(self, obj):
        pool = getattr(
            obj,
            "kemasan_sekunder",
            None,
        )

        if not pool:
            return "0.00"

        return str(pool.harga_satuan)

    def get_total_nilai_kemasan(self, obj):
        primer = (
            obj.nilai_kemasan_primer
            or Decimal("0")
        )

        sekunder = (
            obj.nilai_kemasan_sekunder
            or Decimal("0")
        )

        return str(
            primer + sekunder
        )

    def get_status_label(self, obj):
        return obj.get_status_display()

    def validate(self, data):
        instance = self.instance

        if (
            instance
            and instance.status != StatusDokumen.DRAFT
        ):
            raise serializers.ValidationError({
                "status": (
                    f"Packing {instance.nomor} "
                    f"sudah {instance.get_status_display()} "
                    "dan tidak dapat diubah."
                )
            })

        entitas = data.get(
            "entitas",
            getattr(instance, "entitas", None),
        )

        tangki = data.get(
            "tangki",
            getattr(instance, "tangki", None),
        )

        produk = data.get(
            "nama_hasil",
            getattr(instance, "nama_hasil", None),
        )

        total_unit = data.get(
            "total_unit",
            getattr(instance, "total_unit", None),
        )

        qty_kg = data.get(
            "qty_kg",
            getattr(instance, "qty_kg", None),
        )

        primer = data.get(
            "kemasan_primer",
            getattr(instance, "kemasan_primer", None),
        )

        sekunder = data.get(
            "kemasan_sekunder",
            getattr(instance, "kemasan_sekunder", None),
        )

        qty_sekunder = data.get(
            "qty_kemasan_sekunder",
            getattr(instance, "qty_kemasan_sekunder", 0),
        )

        if not entitas:
            raise serializers.ValidationError({
                "entitas": "Entitas wajib dipilih."
            })

        if not entitas.aktif:
            raise serializers.ValidationError({
                "entitas": (
                    f"Entitas {entitas.kode} tidak aktif."
                )
            })

        if not tangki:
            raise serializers.ValidationError({
                "tangki": (
                    "Tangki sumber wajib dipilih."
                )
            })

        if not tangki.aktif:
            raise serializers.ValidationError({
                "tangki": (
                    f"Tangki {tangki.kode} tidak aktif."
                )
            })

        if tangki.saldo_kg is None:
            raise serializers.ValidationError({
                "tangki": (
                    f"Saldo Tangki {tangki.kode} "
                    "tidak tersedia."
                )
            })

        if tangki.saldo_kg <= Decimal("0"):
            raise serializers.ValidationError({
                "tangki": (
                    f"Tangki {tangki.kode} "
                    "tidak memiliki saldo bahan."
                )
            })

        if not produk:
            raise serializers.ValidationError({
                "produk": (
                    "Produk hasil wajib dipilih."
                )
            })

        if total_unit is None or int(total_unit) <= 0:
            raise serializers.ValidationError({
                "total_unit": (
                    "Total unit harus lebih dari 0."
                )
            })

        if qty_kg is None or Decimal(str(qty_kg)) <= Decimal("0"):
            raise serializers.ValidationError({
                "qty_kg": (
                    "Qty packing harus lebih dari 0."
                )
            })

        if Decimal(str(qty_kg)) > tangki.saldo_kg:
            raise serializers.ValidationError({
                "qty_kg": (
                    f"Qty packing {qty_kg} Kg melebihi "
                    f"saldo Tangki {tangki.kode} "
                    f"sebesar {tangki.saldo_kg} Kg."
                )
            })

        if primer is None:
            raise serializers.ValidationError({
                "kemasan_primer": (
                    "Kemasan Primer wajib dipilih."
                )
            })

        if primer.kategori not in (
            KategoriKemasan.PRIMER,
            KategoriKemasan.PRIMER_SEKUNDER,
        ):
            raise serializers.ValidationError({
                "kemasan_primer": (
                    f"{primer.produk.nama} tidak dapat "
                    "digunakan sebagai Kemasan Primer."
                )
            })

        if primer.qty_unit <= 0:
            raise serializers.ValidationError({
                "kemasan_primer": (
                    f"Stok {primer.produk.nama} "
                    "sedang kosong."
                )
            })

        if primer.qty_unit < int(total_unit):
            raise serializers.ValidationError({
                "kemasan_primer": (
                    f"Stok {primer.produk.nama} hanya "
                    f"{primer.qty_unit} Unit. "
                    f"Kebutuhan {int(total_unit)} Unit."
                )
            })

        if sekunder is None:
            if qty_sekunder not in (None, 0):
                raise serializers.ValidationError({
                    "qty_kemasan_sekunder": (
                        "Qty Sekunder harus 0 "
                        "jika Kemasan Sekunder "
                        "tidak dipilih."
                    )
                })
        else:
            if sekunder.kategori not in (
                KategoriKemasan.SEKUNDER,
                KategoriKemasan.PRIMER_SEKUNDER,
            ):
                raise serializers.ValidationError({
                    "kemasan_sekunder": (
                        f"{sekunder.produk.nama} tidak dapat "
                        "digunakan sebagai Kemasan Sekunder."
                    )
                })

            if (
                qty_sekunder is None
                or int(qty_sekunder) <= 0
            ):
                raise serializers.ValidationError({
                    "qty_kemasan_sekunder": (
                        "Qty Kemasan Sekunder "
                        "harus lebih dari 0."
                    )
                })

            kebutuhan_sekunder = (
                int(total_unit)
                * int(qty_sekunder)
            )

            if sekunder.qty_unit <= 0:
                raise serializers.ValidationError({
                    "kemasan_sekunder": (
                        f"Stok {sekunder.produk.nama} "
                        "sedang kosong."
                    )
                })

            if sekunder.qty_unit < kebutuhan_sekunder:
                raise serializers.ValidationError({
                    "kemasan_sekunder": (
                        f"Stok {sekunder.produk.nama} hanya "
                        f"{sekunder.qty_unit} Unit. "
                        f"Kebutuhan {kebutuhan_sekunder} Unit."
                    )
                })

        return data


class MutasiKlaimSerializer(serializers.ModelSerializer):
    entitas_kode = serializers.CharField(
        source="entitas.kode",
        read_only=True,
    )

    grup_kode = serializers.CharField(
        source="grup_bahan.kode",
        read_only=True,
    )

    class Meta:
        model = MutasiKlaim
        fields = [
            "id",
            "entitas",
            "entitas_kode",
            "grup_bahan",
            "grup_kode",
            "tipe",
            "arah",
            "qty_kg",
            "nilai",
            "ref_type",
            "ref_id",
            "keterangan",
            "waktu",
            "dibuat_pada",
            "dibuat_oleh",
        ]
        read_only_fields = fields
