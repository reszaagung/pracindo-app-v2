<template>
    <div class="flex flex-col w-full animate-fade-in relative p-5 md:p-6 lg:p-8 bg-white/50">
        <div class="mb-5 md:mb-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-4 md:gap-0">
            <div>
                <p class="text-xs text-slate-400 mb-2">
                    <router-link
                        to="/"
                        class="hover:text-slate-700 transition-colors"
                    >
                        Dashboard
                    </router-link>
                    ›
                    <router-link
                        to="/produksi"
                        class="hover:text-slate-700 transition-colors"
                    >
                        Produksi
                    </router-link>
                    › Riwayat Packing
                </p>

                <div class="flex items-center gap-3">
                    <h2 class="text-xl md:text-2xl font-black text-slate-800 tracking-tight">
                        Riwayat Packing
                    </h2>

                    <span class="bg-indigo-100 text-indigo-700 text-[10px] font-bold px-2.5 py-1 rounded-md tracking-wide uppercase">
                        PACKING
                    </span>
                </div>
            </div>

            <button
                type="button"
                @click="$router.push({ name: 'InputPackingForm' })"
                class="w-full md:w-auto justify-center px-5 py-3 md:py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl shadow-[0_4px_12px_rgba(37,99,235,0.2)] hover:shadow-[0_6px_20px_rgba(37,99,235,0.3)] transition-all flex items-center gap-2"
            >
                <i class="pi pi-plus text-sm"></i>
                Buat Packing Baru
            </button>
        </div>

        <div class="bg-white border border-slate-200 rounded-[24px] p-2 md:p-4 shadow-[0_4px_20px_rgba(0,0,0,0.03)] w-full">
            <div
                v-if="isLoading"
                class="text-center py-16 text-slate-500 flex flex-col items-center"
            >
                <i class="pi pi-spin pi-spinner text-3xl mb-3 text-blue-500"></i>

                <p class="text-sm font-medium">
                    Memuat data riwayat...
                </p>
            </div>

            <div
                v-else-if="error"
                class="text-red-600 m-4 bg-red-50 p-4 rounded-xl border border-red-200 flex items-center gap-2 text-sm font-medium"
            >
                <i class="pi pi-exclamation-triangle"></i>
                <span>{{ error }}</span>
            </div>

            <div
                v-else
                class="overflow-x-auto w-full custom-scrollbar p-2"
            >
                <table class="w-full text-left text-sm table-auto min-w-[1180px]">
                    <thead class="border-b-2 border-slate-200">
                        <tr>
                            <th class="py-4 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                                Nomor
                            </th>

                            <th class="py-4 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                                Tanggal
                            </th>

                            <th class="py-4 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                                Barang Jadi
                            </th>

                            <th class="py-4 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                                Tangki
                            </th>

                            <th class="py-4 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                                Kemasan Primer
                            </th>

                            <th class="py-4 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                                Kemasan Sekunder
                            </th>

                            <th class="py-4 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider text-right">
                                Unit
                            </th>

                            <th class="py-4 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider text-right">
                                Berat
                            </th>

                            <th class="py-4 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider text-center">
                                Status
                            </th>

                            <th class="py-4 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider text-center">
                                Aksi
                            </th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-slate-100 bg-transparent">
                        <tr v-if="packings.length === 0">
                            <td
                                colspan="10"
                                class="py-12 text-center text-slate-500 text-sm"
                            >
                                <div class="w-12 h-12 bg-slate-50 border border-slate-100 rounded-full flex items-center justify-center mx-auto mb-3">
                                    <i class="pi pi-box text-xl text-slate-300"></i>
                                </div>

                                Belum ada riwayat packing.
                            </td>
                        </tr>

                        <tr
                            v-for="item in packings"
                            :key="item.id"
                            class="hover:bg-slate-50/80 transition-colors"
                        >
                            <td class="py-4 px-4 whitespace-nowrap font-bold text-slate-800">
                                {{ item.nomor || '-' }}
                            </td>

                            <td class="py-4 px-4 whitespace-nowrap text-slate-600 font-medium">
                                {{ item.tanggal || '-' }}
                            </td>

                            <td class="py-4 px-4 whitespace-nowrap">
                                <div class="font-semibold text-slate-700">
                                    {{
                                        item.produk_nama ||
                                        '-'
                                    }}
                                </div>

                                <div
                                    v-if="item.produk_kode"
                                    class="mt-1 text-[10px] text-slate-400 font-mono"
                                >
                                    {{ item.produk_kode }}
                                </div>
                            </td>

                            <td class="py-4 px-4 whitespace-nowrap">
                                <div class="text-slate-700 font-semibold">
                                    {{
                                        item.tangki_kode ||
                                        '-'
                                    }}
                                </div>
                            </td>

                            <td class="py-4 px-4 whitespace-nowrap text-slate-700">
                                {{ item.kemasan_primer_nama || '-' }}
                            </td>

                            <td class="py-4 px-4 whitespace-nowrap text-slate-700">
                                <template
                                    v-if="
                                        item.kemasan_sekunder_nama
                                    "
                                >
                                    <div>
                                        {{ item.kemasan_sekunder_nama }}
                                    </div>

                                    <div
                                        v-if="
                                            Number(
                                                item.qty_kemasan_sekunder || 0
                                            ) > 0
                                        "
                                        class="mt-1 text-[10px] text-slate-400"
                                    >
                                        {{
                                            formatAngka(
                                                item.qty_kemasan_sekunder
                                            )
                                        }}
                                        / unit
                                    </div>
                                </template>

                                <span v-else>
                                    -
                                </span>
                            </td>

                            <td class="py-4 px-4 whitespace-nowrap text-right font-black text-slate-800">
                                {{ formatAngka(item.total_unit) }}
                            </td>

                            <td class="py-4 px-4 whitespace-nowrap text-right">
                                <div class="font-black text-slate-800">
                                    {{ formatKg(item.qty_kg) }}
                                </div>

                                <div class="text-[10px] text-slate-400">
                                    Kg
                                </div>
                            </td>

                            <td class="py-4 px-4 whitespace-nowrap text-center">
                                <span
                                    class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[10px] font-bold uppercase tracking-wider border"
                                    :class="statusClass(item.status)"
                                >
                                    <i
                                        class="text-[10px]"
                                        :class="statusIcon(item.status)"
                                    ></i>

                                    {{
                                        item.status_label ||
                                        statusLabel(item.status)
                                    }}
                                </span>
                            </td>

                            <td class="py-4 px-4 whitespace-nowrap text-center">
                                <button
                                    type="button"
                                    @click="lihatDetail(item)"
                                    class="inline-flex items-center justify-center gap-2 px-3 py-2 rounded-lg border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 hover:border-slate-300 hover:text-slate-800 transition-colors text-[10px] font-bold"
                                >
                                    <i class="pi pi-eye"></i>
                                    Lihat
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div
            v-if="detailVisible"
            class="fixed inset-0 z-[200] flex items-center justify-center p-4 bg-slate-950/40 backdrop-blur-[2px]"
            @mousedown.self="tutupDetail"
        >
            <div class="w-full max-w-3xl max-h-[90vh] overflow-hidden bg-white rounded-2xl shadow-2xl border border-slate-200">
                <div class="flex items-start justify-between gap-4 px-6 py-5 border-b border-slate-100">
                    <div>
                        <div class="text-[10px] font-extrabold text-slate-400 uppercase tracking-[0.14em]">
                            Detail Packing
                        </div>

                        <h3 class="mt-1 text-xl font-black text-slate-800">
                            {{ detail.nomor || '-' }}
                        </h3>
                    </div>

                    <button
                        type="button"
                        @click="tutupDetail"
                        class="w-9 h-9 rounded-lg border border-slate-200 text-slate-500 hover:bg-slate-50 hover:text-slate-800 transition-colors flex items-center justify-center"
                    >
                        <i class="pi pi-times"></i>
                    </button>
                </div>

                <div class="max-h-[calc(90vh-82px)] overflow-y-auto p-6 custom-scrollbar">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="detail-card">
                            <span class="detail-label">
                                Status
                            </span>

                            <div class="mt-2">
                                <span
                                    class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-[10px] font-bold uppercase tracking-wider border"
                                    :class="statusClass(detail.status)"
                                >
                                    <i
                                        class="text-[10px]"
                                        :class="statusIcon(detail.status)"
                                    ></i>

                                    {{
                                        detail.status_label ||
                                        statusLabel(detail.status)
                                    }}
                                </span>
                            </div>
                        </div>

                        <div class="detail-card">
                            <span class="detail-label">
                                Tanggal
                            </span>

                            <strong class="detail-value">
                                {{ detail.tanggal || '-' }}
                            </strong>
                        </div>

                        <div class="detail-card">
                            <span class="detail-label">
                                Entitas
                            </span>

                            <strong class="detail-value">
                                {{
                                    detail.entitas_kode ||
                                    '-'
                                }}

                                <template
                                    v-if="detail.entitas_nama"
                                >
                                    — {{ detail.entitas_nama }}
                                </template>
                            </strong>
                        </div>

                        <div class="detail-card">
                            <span class="detail-label">
                                Tangki Sumber
                            </span>

                            <strong class="detail-value">
                                {{
                                    detail.tangki_kode ||
                                    '-'
                                }}

                                <template
                                    v-if="detail.tangki_nama"
                                >
                                    — {{ detail.tangki_nama }}
                                </template>
                            </strong>
                        </div>

                        <div class="detail-card">
                            <span class="detail-label">
                                Barang Jadi
                            </span>

                            <strong class="detail-value">
                                {{
                                    detail.produk_nama ||
                                    '-'
                                }}
                            </strong>
                        </div>

                        <div class="detail-card">
                            <span class="detail-label">
                                Total Unit
                            </span>

                            <strong class="detail-value">
                                {{
                                    formatAngka(
                                        detail.total_unit
                                    )
                                }}
                                Unit
                            </strong>
                        </div>

                        <div class="detail-card">
                            <span class="detail-label">
                                Total Berat
                            </span>

                            <strong class="detail-value">
                                {{
                                    formatKg(
                                        detail.qty_kg
                                    )
                                }}
                                Kg
                            </strong>
                        </div>
                    </div>

                    <div class="mt-6 detail-section">
                        <div class="detail-section-title">
                            Kemasan
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
                            <div class="detail-card">
                                <span class="detail-label">
                                    Kemasan Primer
                                </span>

                                <strong class="detail-value">
                                    {{
                                        detail.kemasan_primer_nama ||
                                        '-'
                                    }}
                                </strong>

                                <span class="detail-subvalue">
                                    {{
                                        formatRupiah(
                                            detail.nilai_kemasan_primer
                                        )
                                    }}
                                </span>
                            </div>

                            <div class="detail-card">
                                <span class="detail-label">
                                    Kemasan Sekunder
                                </span>

                                <strong class="detail-value">
                                    {{
                                        detail.kemasan_sekunder_nama ||
                                        '-'
                                    }}
                                </strong>

                                <span
                                    v-if="
                                        detail.kemasan_sekunder_nama
                                    "
                                    class="detail-subvalue"
                                >
                                    {{
                                        formatAngka(
                                            Number(
                                                detail.qty_kemasan_sekunder ||
                                                0
                                            ) *
                                            Number(
                                                detail.total_unit || 0
                                            )
                                        )
                                    }}
                                    Unit

                                    ·

                                    {{
                                        formatRupiah(
                                            detail.nilai_kemasan_sekunder
                                        )
                                    }}
                                </span>
                            </div>
                        </div>
                    </div>

                    <div class="mt-6 detail-section">
                        <div class="detail-section-title">
                            Nilai Packing
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3">
                            <div class="detail-card">
                                <span class="detail-label">
                                    Nilai Kemasan
                                </span>

                                <strong class="detail-value">
                                    {{
                                        formatRupiah(
                                            detail.total_nilai_kemasan
                                        )
                                    }}
                                </strong>
                            </div>

                            <div class="detail-card">
                                <span class="detail-label">
                                    Harga Bahan / Kg
                                </span>

                                <strong class="detail-value">
                                    {{
                                        formatRupiah(
                                            detail.harga_per_kg
                                        )
                                    }}
                                </strong>
                            </div>

                            <div class="detail-card">
                                <span class="detail-label">
                                    Total Cost
                                </span>

                                <strong class="detail-value">
                                    {{
                                        formatRupiah(
                                            detail.cost_nom
                                        )
                                    }}
                                </strong>
                            </div>
                        </div>
                    </div>

                    <div class="mt-6 flex justify-end">
                        <button
                            type="button"
                            @click="tutupDetail"
                            class="px-5 py-2.5 rounded-lg bg-slate-900 text-white text-xs font-bold hover:bg-slate-800 transition-colors"
                        >
                            Tutup
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import {
    onMounted,
    reactive,
    ref
} from 'vue'

import { usePacking } from '../composables/usePacking'

const {
    packings,
    isLoading,
    error,
    fetchPackings
} = usePacking()

const detailVisible = ref(false)

const detail = reactive({
    id: null,
    nomor: '',
    tanggal: '',
    status: '',
    status_label: '',
    entitas_kode: '',
    entitas_nama: '',
    tangki_kode: '',
    tangki_nama: '',
    produk_kode: '',
    produk_nama: '',
    kemasan_primer_nama: '',
    kemasan_sekunder_nama: '',
    qty_kemasan_sekunder: 0,
    total_unit: 0,
    qty_kg: 0,
    nilai_kemasan_primer: 0,
    nilai_kemasan_sekunder: 0,
    total_nilai_kemasan: 0,
    harga_per_kg: 0,
    cost_nom: 0
})

const lihatDetail = (item) => {
    Object.assign(
        detail,
        item
    )

    detailVisible.value = true
}

const tutupDetail = () => {
    detailVisible.value = false
}

const formatAngka = (value) => {
    if (
        value == null ||
        value === ''
    ) {
        return '-'
    }

    return new Intl.NumberFormat(
        'id-ID',
        {
            maximumFractionDigits: 0
        }
    ).format(
        Number(value) || 0
    )
}

const formatKg = (value) => {
    if (
        value == null ||
        value === ''
    ) {
        return '-'
    }

    return new Intl.NumberFormat(
        'id-ID',
        {
            minimumFractionDigits: 0,
            maximumFractionDigits: 3
        }
    ).format(
        Number(value) || 0
    )
}

const formatRupiah = (value) => {
    if (
        value == null ||
        value === ''
    ) {
        return 'Rp 0'
    }

    return new Intl.NumberFormat(
        'id-ID',
        {
            style: 'currency',
            currency: 'IDR',
            minimumFractionDigits: 0,
            maximumFractionDigits: 2
        }
    ).format(
        Number(value) || 0
    )
}

const statusLabel = (status) => {
    switch (
        String(
            status || ''
        ).toUpperCase()
    ) {
        case 'POSTED':
            return 'Diposting'

        case 'VOID':
            return 'Dibatalkan'

        case 'DRAFT':
            return 'Draft'

        default:
            return status || '-'
    }
}

const statusIcon = (status) => {
    switch (
        String(
            status || ''
        ).toUpperCase()
    ) {
        case 'POSTED':
            return 'pi pi-check-circle'

        case 'VOID':
            return 'pi pi-ban'

        case 'DRAFT':
            return 'pi pi-file'

        default:
            return 'pi pi-circle'
    }
}

const statusClass = (status) => {
    switch (
        String(
            status || ''
        ).toUpperCase()
    ) {
        case 'POSTED':
            return 'bg-emerald-50 text-emerald-600 border-emerald-200'

        case 'VOID':
            return 'bg-rose-50 text-rose-600 border-rose-200'

        case 'DRAFT':
            return 'bg-amber-50 text-amber-600 border-amber-200'

        default:
            return 'bg-slate-50 text-slate-500 border-slate-200'
    }
}

onMounted(() => {
    fetchPackings()
})
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.custom-scrollbar::-webkit-scrollbar {
    height: 6px;
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 6px;
}

.detail-card {
    min-width: 0;
    padding: 14px;
    border: 1px solid #e5eaf0;
    border-radius: 12px;
    background: #f8fafc;
}

.detail-label {
    display: block;
    color: #94a3b8;
    font-size: 9px;
    font-weight: 800;
    line-height: 1.3;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.detail-value {
    display: block;
    margin-top: 6px;
    color: #172033;
    font-size: 12px;
    line-height: 1.4;
    font-weight: 800;
}

.detail-subvalue {
    display: block;
    margin-top: 5px;
    color: #64748b;
    font-size: 10px;
    line-height: 1.4;
    font-weight: 600;
}

.detail-section {
    padding-top: 18px;
    border-top: 1px solid #edf1f5;
}

.detail-section-title {
    color: #172033;
    font-size: 12px;
    line-height: 1.4;
    font-weight: 800;
}

@media (max-width: 640px) {
    .detail-card {
        padding: 12px;
    }
}
</style>
