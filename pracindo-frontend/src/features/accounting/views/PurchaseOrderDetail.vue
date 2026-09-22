<template>
    <div class="po-detail w-full min-h-[400px] p-4 md:p-5 relative font-inter">

        <!-- LOADING -->
        <div
            v-if="loading"
            class="absolute inset-0 z-20 flex flex-col items-center justify-center bg-white/90 backdrop-blur-[2px]"
        >
            <div class="flex h-11 w-11 items-center justify-center rounded-full bg-slate-100 mb-3">
                <i class="pi pi-spin pi-spinner text-slate-500 text-lg"></i>
            </div>

            <p class="text-[11px] font-semibold text-slate-500">
                Memuat rincian dokumen...
            </p>
        </div>

        <!-- ERROR -->
        <div
            v-else-if="error"
            class="flex min-h-[360px] flex-col items-center justify-center text-center px-6"
        >
            <div class="flex h-14 w-14 items-center justify-center rounded-2xl bg-red-50 border border-red-100 mb-4">
                <i class="pi pi-exclamation-triangle text-red-500 text-xl"></i>
            </div>

            <h4 class="text-sm font-bold text-slate-800 mb-1.5">
                Gagal Memuat Data
            </h4>

            <p class="max-w-md text-[11px] leading-5 text-slate-500">
                {{ error }}
            </p>
        </div>

        <!-- CONTENT -->
        <div
            v-else-if="data"
            class="flex flex-col gap-5 animate-fade-in"
        >

            <!-- HEADER -->
            <section class="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden">
                <div class="px-5 py-5 md:px-6 md:py-6">

                    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5">

                        <!-- LEFT -->
                        <div class="min-w-0">
                            <div class="flex items-center gap-2 mb-2">
                                <span
                                    class="inline-flex h-7 w-7 items-center justify-center rounded-lg bg-slate-900 text-white"
                                >
                                    <i class="pi pi-file text-[10px]"></i>
                                </span>

                                <span class="text-[9px] font-bold tracking-[0.14em] uppercase text-slate-400">
                                    Purchase Order
                                </span>
                            </div>

                            <h2 class="text-xl md:text-2xl font-bold tracking-tight text-slate-900 truncate">
                                {{ data.nomor }}
                            </h2>

                            <div class="mt-2 flex flex-wrap items-center gap-x-4 gap-y-2 text-[10px] text-slate-500">

                                <span class="inline-flex items-center gap-1.5">
                                    <i class="pi pi-calendar text-[9px] text-slate-400"></i>
                                    {{ data.tanggal }}
                                </span>

                                <span class="hidden sm:inline text-slate-300">•</span>

                                <span class="inline-flex items-center gap-1.5">
                                    <i class="pi pi-building text-[9px] text-slate-400"></i>
                                    <span class="font-medium text-slate-600">
                                        {{ data.entitas }}
                                    </span>
                                </span>
                            </div>
                        </div>

                        <!-- RIGHT -->
                        <div class="flex flex-col items-start lg:items-end gap-2">
                            <span
                                :class="badgeColor(data.status)"
                                class="inline-flex items-center rounded-full px-3 py-1.5 text-[9px] font-bold uppercase tracking-wider border"
                            >
                                <span
                                    class="mr-1.5 h-1.5 w-1.5 rounded-full bg-current opacity-70"
                                ></span>

                                {{ data.status }}
                            </span>

                            <div class="flex items-center gap-1.5 text-[10px] text-slate-500">
                                <i class="pi pi-users text-[9px] text-slate-400"></i>
                                <span class="font-semibold text-slate-700">
                                    {{ data.suplier }}
                                </span>
                            </div>
                        </div>

                    </div>
                </div>

                <!-- SUMMARY STRIP -->
                <div class="grid grid-cols-2 md:grid-cols-3 border-t border-slate-100 bg-slate-50/70">

                    <div class="px-5 py-3.5 border-r border-slate-100">
                        <p class="text-[8px] uppercase tracking-wider font-bold text-slate-400">
                            Item
                        </p>

                        <p class="mt-1 text-xs font-bold text-slate-800">
                            {{ data.item?.length || 0 }}
                        </p>
                    </div>

                    <div class="px-5 py-3.5 md:border-r border-slate-100">
                        <p class="text-[8px] uppercase tracking-wider font-bold text-slate-400">
                            Supplier
                        </p>

                        <p class="mt-1 text-xs font-bold text-slate-800 truncate">
                            {{ data.suplier }}
                        </p>
                    </div>

                    <div class="hidden md:block px-5 py-3.5">
                        <p class="text-[8px] uppercase tracking-wider font-bold text-slate-400">
                            Total PO
                        </p>

                        <p class="mt-1 text-xs font-bold text-emerald-700">
                            Rp {{ formatRupiah(data.total_nilai) }}
                        </p>
                    </div>

                </div>
            </section>

            <!-- DETAIL ITEM -->
            <section>
                <div class="flex items-center justify-between mb-3 px-1">
                    <div>
                        <h3 class="text-xs font-bold text-slate-800">
                            Rincian Pesanan
                        </h3>

                        <p class="text-[9px] text-slate-400 mt-0.5">
                            Daftar item dalam Purchase Order
                        </p>
                    </div>

                    <span class="text-[9px] font-semibold text-slate-400">
                        {{ data.item?.length || 0 }} item
                    </span>
                </div>

                <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">

                    <div class="overflow-x-auto custom-scrollbar">
                        <table class="w-full min-w-[720px] text-left border-collapse">

                            <thead class="bg-slate-50 border-b border-slate-200">
                                <tr>
                                    <th class="w-[34%] px-5 py-3.5 text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                        Produk
                                    </th>

                                    <th class="w-[15%] px-4 py-3.5 text-right text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                        Qty
                                    </th>

                                    <th class="w-[18%] px-4 py-3.5 text-right text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                        Harga
                                    </th>

                                    <th class="w-[21%] px-4 py-3.5 text-right text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                        Subtotal
                                    </th>

                                    <th class="w-[12%] px-4 py-3.5 text-center text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                        Status
                                    </th>
                                </tr>
                            </thead>

                            <tbody class="divide-y divide-slate-100">
                                <tr
                                    v-for="(item, index) in data.item"
                                    :key="index"
                                    class="group transition-colors hover:bg-slate-50/70"
                                >
                                    <!-- PRODUCT -->
                                    <td class="px-5 py-4">
                                        <div class="flex items-start gap-3">
                                            <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-500 group-hover:bg-slate-200 transition-colors">
                                                <i class="pi pi-box text-[10px]"></i>
                                            </div>

                                            <div class="min-w-0">
                                                <p class="text-[10px] font-semibold text-slate-800 leading-4">
                                                    {{ item.nama }}
                                                </p>

                                                <p class="mt-0.5 text-[8px] text-slate-400 font-mono truncate">
                                                    {{ item.produk }}
                                                </p>
                                            </div>
                                        </div>
                                    </td>

                                    <!-- QTY -->
                                    <td class="px-4 py-4 text-right">
                                        <p class="text-[10px] font-semibold text-slate-700">
                                            {{ formatNum(item.pesan) }}
                                        </p>

                                        <span class="text-[8px] text-slate-400">
                                            Kg
                                        </span>
                                    </td>

                                    <!-- PRICE -->
                                    <td class="px-4 py-4 text-right">
                                        <p class="text-[10px] font-medium text-slate-600">
                                            Rp {{ formatRupiah(item.harga) }}
                                        </p>
                                    </td>

                                    <!-- SUBTOTAL -->
                                    <td class="px-4 py-4 text-right">
                                        <p class="text-[10px] font-bold text-slate-800">
                                            Rp {{ formatRupiah(item.amount) }}
                                        </p>
                                    </td>

                                    <!-- STATUS -->
                                    <td class="px-4 py-4 text-center">
                                        <div
                                            v-if="Number(item.diterima) >= Number(item.pesan)"
                                            class="inline-flex h-7 w-7 items-center justify-center rounded-full bg-emerald-50 border border-emerald-100"
                                            title="Diterima Penuh"
                                        >
                                            <i class="pi pi-check text-[10px] text-emerald-600"></i>
                                        </div>

                                        <div
                                            v-else-if="Number(item.diterima) > 0"
                                            class="inline-flex h-7 w-7 items-center justify-center rounded-full bg-amber-50 border border-amber-100"
                                            :title="`Sisa: ${item.sisa} Kg`"
                                        >
                                            <i class="pi pi-clock text-[10px] text-amber-600"></i>
                                        </div>

                                        <div
                                            v-else
                                            class="inline-flex h-7 w-7 items-center justify-center rounded-full bg-slate-50 border border-slate-200"
                                            title="Belum Diterima"
                                        >
                                            <i class="pi pi-minus text-[10px] text-slate-300"></i>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>

                            <!-- TOTAL -->
                            <tfoot class="border-t border-slate-200 bg-slate-50/70">
                                <tr>
                                    <td colspan="3" class="px-5 py-4 text-right">
                                        <span class="text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                            Total Nilai PO
                                        </span>
                                    </td>

                                    <td class="px-4 py-4 text-right">
                                        <span class="text-sm font-bold text-emerald-700">
                                            Rp {{ formatRupiah(data.total_nilai) }}
                                        </span>
                                    </td>

                                    <td></td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                </div>

                <!-- LEGEND -->
                <div class="flex flex-wrap items-center gap-4 mt-3 px-1">
                    <div class="flex items-center gap-1.5">
                        <span class="h-2 w-2 rounded-full bg-emerald-500"></span>
                        <span class="text-[8px] text-slate-400">
                            Diterima penuh
                        </span>
                    </div>

                    <div class="flex items-center gap-1.5">
                        <span class="h-2 w-2 rounded-full bg-amber-500"></span>
                        <span class="text-[8px] text-slate-400">
                            Sebagian
                        </span>
                    </div>

                    <div class="flex items-center gap-1.5">
                        <span class="h-2 w-2 rounded-full bg-slate-300"></span>
                        <span class="text-[8px] text-slate-400">
                            Belum diterima
                        </span>
                    </div>
                </div>
            </section>

            <!-- RIWAYAT PENERIMAAN -->
            <section>
                <div class="flex items-center justify-between mb-3 px-1">
                    <div>
                        <h3 class="text-xs font-bold text-slate-800">
                            Riwayat Penerimaan
                        </h3>

                        <p class="text-[9px] text-slate-400 mt-0.5">
                            Aktivitas penerimaan barang oleh gudang
                        </p>
                    </div>

                    <i class="pi pi-truck text-xs text-slate-300"></i>
                </div>

                <!-- ADA PENERIMAAN -->
                <div
                    v-if="data.penerimaan && data.penerimaan.length > 0"
                    class="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden"
                >
                    <div class="divide-y divide-slate-100">

                        <div
                            v-for="(pn, index) in data.penerimaan"
                            :key="pn.nomor"
                            class="relative flex items-center justify-between gap-4 px-5 py-4 hover:bg-slate-50/70 transition-colors"
                        >
                            <!-- TIMELINE -->
                            <div class="flex items-start gap-3 min-w-0">

                                <div class="relative shrink-0">
                                    <div class="flex h-8 w-8 items-center justify-center rounded-full bg-emerald-50 border border-emerald-100">
                                        <i class="pi pi-check text-[9px] text-emerald-600"></i>
                                    </div>

                                    <div
                                        v-if="index < data.penerimaan.length - 1"
                                        class="absolute left-1/2 top-8 h-full w-px bg-slate-200 -translate-x-1/2"
                                    ></div>
                                </div>

                                <div class="min-w-0 pt-0.5">
                                    <p class="text-[10px] font-bold text-slate-800">
                                        {{ pn.nomor }}
                                    </p>

                                    <p class="mt-1 text-[9px] text-slate-500">
                                        Surat Jalan:
                                        <span class="font-semibold text-slate-600">
                                            {{ pn.surat_jalan || '-' }}
                                        </span>
                                    </p>

                                    <span
                                        v-if="pn.ada_selisih"
                                        class="inline-flex items-center mt-2 rounded-md bg-red-50 border border-red-100 px-2 py-1 text-[8px] font-bold uppercase tracking-wide text-red-600"
                                    >
                                        <i class="pi pi-exclamation-triangle mr-1 text-[7px]"></i>
                                        Ada Selisih
                                    </span>
                                </div>
                            </div>

                            <!-- DATE -->
                            <div class="shrink-0 text-right">
                                <span class="inline-flex items-center rounded-lg bg-slate-50 border border-slate-100 px-2.5 py-1.5 text-[8px] font-semibold text-slate-500">
                                    <i class="pi pi-calendar mr-1.5 text-[7px] text-slate-400"></i>
                                    {{ pn.tanggal }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- BELUM ADA PENERIMAAN -->
                <div
                    v-else
                    class="rounded-2xl border border-dashed border-slate-200 bg-slate-50/60 px-6 py-8 text-center"
                >
                    <div class="mx-auto flex h-10 w-10 items-center justify-center rounded-xl bg-white border border-slate-200 mb-3">
                        <i class="pi pi-inbox text-slate-300 text-sm"></i>
                    </div>

                    <p class="text-[10px] font-semibold text-slate-600">
                        Belum ada penerimaan
                    </p>

                    <p class="mt-1 text-[9px] text-slate-400">
                        Belum ada transaksi penerimaan barang di gudang untuk PO ini.
                    </p>
                </div>
            </section>

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'
import { bacaError } from '@/utils/error'

const props = defineProps({
    poId: {
        type: [Number, String],
        required: true
    }
})

const data = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
    loading.value = true
    error.value = ''

    try {
        const response = await api.get(
            `akunting/purchase-order/${props.poId}/ringkasan/`
        )

        data.value = response.data
    } catch (err) {
        console.error('Gagal memuat rincian PO:', err)

        error.value = bacaError(
            err,
            'Gagal memuat rincian PO.'
        )
    } finally {
        loading.value = false
    }
})

const formatNum = (num) => {
    return Number(num).toLocaleString('id-ID', {
        maximumFractionDigits: 2
    })
}

const formatRupiah = (num) => {
    return Number(num).toLocaleString('id-ID')
}

const badgeColor = (status) => {
    const st = String(status).toUpperCase()

    if (st === 'DRAFT') {
        return 'bg-slate-50 text-slate-600 border-slate-200'
    }

    if (st === 'PENDING') {
        return 'bg-amber-50 text-amber-700 border-amber-100'
    }

    if (st === 'APPROVED' || st === 'DISETUJUI') {
        return 'bg-emerald-50 text-emerald-700 border-emerald-100'
    }

    if (st === 'TERKIRIM') {
        return 'bg-blue-50 text-blue-700 border-blue-100'
    }

    if (st === 'SEBAGIAN') {
        return 'bg-orange-50 text-orange-700 border-orange-100'
    }

    if (
        st === 'SELESAI' ||
        st === 'DITERIMA PENUH'
    ) {
        return 'bg-emerald-50 text-emerald-700 border-emerald-100'
    }

    if (
        st === 'BATAL' ||
        st === 'DITOLAK'
    ) {
        return 'bg-red-50 text-red-700 border-red-100'
    }

    return 'bg-slate-50 text-slate-600 border-slate-200'
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap");

.font-inter {
    font-family:
        "Inter",
        "Segoe UI",
        -apple-system,
        BlinkMacSystemFont,
        sans-serif;
}

.animate-fade-in {
    animation: fadeIn 0.25s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(6px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.custom-scrollbar::-webkit-scrollbar {
    height: 5px;
    width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 999px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}
</style>