from django.contrib import admin

from .models import (
    Budget, BudgetLine,
    FixedCost,
    RevenueTarget, COGSTarget,
    Forecast,
    RekapPurchaseOrder,
)


class DiauditAdminMixin:
    """dibuat_oleh non-null + editable=False → admin tidak pernah
    mengisinya lewat form. Harus di-set di sini, kalau tidak setiap
    create dari admin gagal IntegrityError."""

    def save_model(self, request, obj, form, change):
        if not change and obj.dibuat_oleh_id is None:
            obj.dibuat_oleh = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if obj.dibuat_oleh_id is None:
                obj.dibuat_oleh = request.user
            obj.save()
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()


class BudgetLineInline(admin.TabularInline):
    model = BudgetLine
    extra = 0
    fields = ('akun', 'bulan', 'nominal_anggaran', 'keterangan')
    autocomplete_fields = ('akun',)


@admin.register(Budget)
class BudgetAdmin(DiauditAdminMixin, admin.ModelAdmin):
    list_display = ('nama', 'entitas', 'tahun', 'basis_periode', 'versi',
                    'status', 'total_anggaran', 'is_active')
    list_filter = ('status', 'basis_periode', 'tahun', 'entitas', 'is_active')
    search_fields = ('nama', 'entitas__kode', 'entitas__nama')
    list_select_related = ('entitas', 'dibuat_oleh')
    readonly_fields = ('total_anggaran', 'dibuat_pada', 'diubah_pada', 'dibuat_oleh')
    inlines = [BudgetLineInline]


@admin.register(BudgetLine)
class BudgetLineAdmin(DiauditAdminMixin, admin.ModelAdmin):
    list_display = ('budget', 'akun', 'bulan', 'nominal_anggaran')
    list_filter = ('budget__tahun', 'budget__entitas', 'bulan')
    search_fields = ('budget__nama', 'akun__kode', 'akun__nama')
    list_select_related = ('budget', 'akun')
    autocomplete_fields = ('akun',)
    readonly_fields = ('dibuat_pada', 'diubah_pada', 'dibuat_oleh')


@admin.register(FixedCost)
class FixedCostAdmin(DiauditAdminMixin, admin.ModelAdmin):
    list_display = ('nama', 'entitas', 'akun_beban', 'nominal_bulanan',
                    'tanggal_mulai', 'tanggal_selesai', 'aktif', 'auto_masuk_budget')
    list_filter = ('aktif', 'auto_masuk_budget', 'entitas')
    search_fields = ('nama', 'akun_beban__kode', 'akun_beban__nama')
    list_select_related = ('entitas', 'akun_beban')
    autocomplete_fields = ('akun_beban',)
    readonly_fields = ('dibuat_pada', 'diubah_pada', 'dibuat_oleh')


@admin.register(RevenueTarget)
class RevenueTargetAdmin(DiauditAdminMixin, admin.ModelAdmin):
    list_display = ('entitas', 'akun_pendapatan', 'tahun', 'bulan', 'nominal_target')
    list_filter = ('tahun', 'bulan', 'entitas')