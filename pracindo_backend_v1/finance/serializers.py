from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import (
    Budget, BudgetLine,
    FixedCost,
    RevenueTarget, COGSTarget,
    Forecast,
    RekapPurchaseOrder, RekapMutasiProduksi, RekapMutasiKlaim,
)


class FullCleanModelSerializer(serializers.ModelSerializer):
    """Menjalankan Model.clean() lewat API, supaya aturan bisnis yang
    sudah ditulis di model (tipe akun, budget terkunci, rentang tanggal)
    ditegakkan juga dari endpoint, bukan cuma dari admin/shell."""

    def validate(self, attrs):
        instance = self.instance or self.Meta.model()
        for field, value in attrs.items():
            setattr(instance, field, value)
        try:
            instance.clean()
        except DjangoValidationError as exc:
            detail = (exc.message_dict if hasattr(exc, 'message_dict')
                      else {'non_field_errors': exc.messages})
            raise serializers.ValidationError(detail)
        return attrs


class BudgetLineSerializer(FullCleanModelSerializer):
    akun_kode = serializers.CharField(source='akun.kode', read_only=True)
    akun_nama = serializers.CharField(source='akun.nama', read_only=True)
    dibuat_oleh_nama = serializers.CharField(source='dibuat_oleh.username', read_only=True)

    class Meta:
        model = BudgetLine
        fields = [
            'id', 'budget', 'akun', 'akun_kode', 'akun_nama',
            'bulan', 'nominal_anggaran', 'keterangan',
            'is_active', 'dibuat_pada', 'diubah_pada', 'dibuat_oleh_nama',
        ]
        read_only_fields = ['budget', 'dibuat_pada', 'diubah_pada']


class BudgetSerializer(FullCleanModelSerializer):
    entitas_kode = serializers.CharField(source='entitas.kode', read_only=True)
    entitas_nama = serializers.CharField(source='entitas.nama', read_only=True)
    total_anggaran = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    terkunci = serializers.BooleanField(read_only=True)
    lines = BudgetLineSerializer(many=True, read_only=True)
    dibuat_oleh_nama = serializers.CharField(source='dibuat_oleh.username', read_only=True)

    class Meta:
        model = Budget
        fields = [
            'id', 'entitas', 'entitas_kode', 'entitas_nama',
            'nama', 'tahun', 'basis_periode', 'status', 'versi', 'keterangan',
            'total_anggaran', 'terkunci', 'lines',
            'is_active', 'dibuat_pada', 'diubah_pada', 'dibuat_oleh_nama',
        ]
        read_only_fields = ['dibuat_pada', 'diubah_pada']


class FixedCostSerializer(FullCleanModelSerializer):
    entitas_kode = serializers.CharField(source='entitas.kode', read_only=True)
    entitas_nama = serializers.CharField(source='entitas.nama', read_only=True)
    akun_beban_kode = serializers.CharField(source='akun_beban.kode', read_only=True)
    akun_beban_nama = serializers.CharField(source='akun_beban.nama', read_only=True)
    dibuat_oleh_nama = serializers.CharField(source='dibuat_oleh.username', read_only=True)

    class Meta:
        model = FixedCost
        fields = [
            'id', 'entitas', 'entitas_kode', 'entitas_nama',
            'akun_beban', 'akun_beban_kode', 'akun_beban_nama',
            'nama', 'nominal_bulanan', 'tanggal_mulai', 'tanggal_selesai',
            'aktif', 'auto_masuk_budget', 'keterangan',
            'is_active', 'dibuat_pada', 'diubah_pada', 'dibuat_oleh_nama',
        ]
        read_only_fields = ['dibuat_pada', 'diubah_pada']


class RevenueTargetSerializer(FullCleanModelSerializer):
    entitas_kode = serializers.CharField(source='entitas.kode', read_only=True)
    akun_kode = serializers.CharField(source='akun_pendapatan.kode', read_only=True)
    akun_nama = serializers.CharField(source='akun_pendapatan.nama', read_only=True)

    class Meta:
        model = RevenueTarget
        fields = [
            'id', 'entitas', 'entitas_kode',
            'akun_pendapatan', 'akun_kode', 'akun_nama',
            'tahun', 'bulan', 'nominal_target',
            'is_active', 'dibuat_pada', 'diubah_pada',
        ]
        read_only_fields = ['dibuat_pada', 'diubah_pada']


class COGSTargetSerializer(FullCleanModelSerializer):
    entitas_kode = serializers.CharField(source='entitas.kode', read_only=True)
    akun_kode = serializers.CharField(source='akun_cogs.kode', read_only=True)
    akun_nama = serializers.CharField(source='akun_cogs.nama', read_only=True)

    class Meta:
        model = COGSTarget
        fields = [
            'id', 'entitas', 'entitas_kode',
            'akun_cogs', 'akun_kode', 'akun_nama',
            'tahun', 'bulan', 'nominal_target',
            'is_active', 'dibuat_pada', 'diubah_pada',
        ]
        read_only_fields = ['dibuat_pada', 'diubah_pada']


class ForecastSerializer(serializers.ModelSerializer):
    # entitas tidak disimpan di Forecast — dibaca lewat periode.
    entitas_kode = serializers.CharField(source='periode.entitas.kode', read_only=True)
    entitas_nama = serializers.CharField(source='periode.entitas.nama', read_only=True)
    periode_tahun = serializers.IntegerField(source='periode.tahun', read_only=True)
    periode_bulan = serializers.IntegerField(source='periode.bulan', read_only=True)
    periode_ditutup = serializers.BooleanField(source='periode.ditutup', read_only=True)

    forecast_gross_profit = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    forecast_operating_profit = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    forecast_net_profit = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    dibuat_oleh_nama = serializers.CharField(source='dibuat_oleh.username', read_only=True)

    class Meta:
        model = Forecast
        fields = [
            'id', 'periode', 'periode_tahun', 'periode_bulan', 'periode_ditutup',
            'entitas_kode', 'entitas_nama',
            'forecast_revenue', 'forecast_cogs', 'forecast_opex',
            'forecast_other_income', 'forecast_other_expense',
            'forecast_gross_profit', 'forecast_operating_profit', 'forecast_net_profit',
            'catatan', 'is_active', 'dibuat_pada', 'dibuat_oleh_nama',
        ]
        read_only_fields = ['dibuat_pada']


class RekapPurchaseOrderSerializer(serializers.ModelSerializer):
    entitas_kode = serializers.CharField(source='entitas.kode', read_only=True)
    entitas_nama = serializers.CharField(source='entitas.nama', read_only=True)
    entitas_jenis = serializers.CharField(source='entitas.jenis', read_only=True)
    nilai_belum_diterima = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    nilai_pesan_dengan_ppn = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)

    class Meta:
        model = RekapPurchaseOrder
        fields = [
            'id', 'entitas', 'entitas_kode', 'entitas_nama', 'entitas_jenis',
            'tahun', 'bulan', 'jumlah_po', 'jumlah_item',
            'nilai_pesan', 'nilai_diterima', 'nilai_belum_diterima',
            'nilai_ppn', 'nilai_pesan_dengan_ppn',
            'dibekukan', 'dihitung_pada', 'is_active',
        ]
        read_only_fields = [f for f in fields if f not in ('dibekukan',)]


class GenerateRekapSerializer(serializers.Serializer):
    tahun = serializers.IntegerField(min_value=2000, max_value=2100)
    bulan = serializers.IntegerField(min_value=1, max_value=12)
    entitas = serializers.IntegerField(required=False, allow_null=True)

class RekapMutasiProduksiSerializer(serializers.ModelSerializer):
    total_batch = serializers.IntegerField(read_only=True)
    persediaan_akhir = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    rasio_susut = serializers.DecimalField(max_digits=10, decimal_places=6, read_only=True)

    class Meta:
        model = RekapMutasiProduksi
        fields = [
            'id', 'tahun', 'bulan',
            'batch_mixing', 'batch_blending', 'total_batch',
            'qty_hasil', 'nilai_hasil', 'qty_susut', 'nilai_susut', 'rasio_susut',
            'qty_packing', 'nilai_packing',
            'wip_akhir_kg', 'wip_akhir_nilai',
            'pool_akhir_nilai', 'pool_kemasan_akhir_nilai', 'persediaan_akhir',
            'dibekukan', 'dihitung_pada', 'is_active',
        ]
        read_only_fields = [f for f in fields if f != 'dibekukan']


class RekapMutasiKlaimSerializer(serializers.ModelSerializer):
    entitas_kode = serializers.CharField(source='entitas.kode', read_only=True)
    entitas_nama = serializers.CharField(source='entitas.nama', read_only=True)
    mutasi_bersih = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    qty_bersih = serializers.DecimalField(max_digits=18, decimal_places=3, read_only=True)

    class Meta:
        model = RekapMutasiKlaim
        fields = [
            'id', 'entitas', 'entitas_kode', 'entitas_nama', 'tahun', 'bulan',
            'jumlah_mutasi',
            'qty_setor', 'nilai_setor', 'qty_tarik', 'nilai_tarik',
            'mutasi_bersih', 'qty_bersih',
            'saldo_akhir', 'qty_setor_kumulatif', 'qty_tarik_kumulatif',
            'dibekukan', 'dihitung_pada', 'is_active',
        ]
        read_only_fields = [f for f in fields if f != 'dibekukan']


class GenerateRekapProduksiSerializer(serializers.Serializer):
    tahun = serializers.IntegerField(min_value=2000, max_value=2100)
    bulan = serializers.IntegerField(min_value=1, max_value=12)
