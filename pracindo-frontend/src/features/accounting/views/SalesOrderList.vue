<template>
    <div class="flex w-full flex-col animate-fade-in">

        <!-- =========================================================
             HEADER
        ========================================================== -->
        <div class="mb-6 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
                <div class="mb-2 flex items-center gap-2 text-[11px] font-medium text-slate-400">
                    <router-link
                        to="/"
                        class="transition-colors hover:text-slate-700"
                    >
                        Dashboard
                    </router-link>

                    <i class="pi pi-angle-right text-[9px]"></i>

                    <span class="font-semibold text-slate-600">
                        Sales Order
                    </span>
                </div>

                <div class="flex items-center gap-3">
                    <div
                        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-blue-50 text-blue-600 ring-1 ring-blue-100"
                    >
                        <i class="pi pi-file-edit text-lg"></i>
                    </div>

                    <div>
                        <div class="flex flex-wrap items-center gap-2">
                            <h1 class="text-2xl font-black tracking-tight text-slate-900">
                                Sales Order
                            </h1>

                            <span
                                class="rounded-lg border border-blue-100 bg-blue-50 px-2.5 py-1 text-[9px] font-black uppercase tracking-wider text-blue-700"
                            >
                                Akuntansi
                            </span>
                        </div>

                        <p class="mt-1 text-xs text-slate-500 md:text-sm">
                            Kelola pesanan penjualan, pelanggan, nilai transaksi, dan status SO.
                        </p>
                    </div>
                </div>
            </div>


            <!-- ACTIONS -->
            <div class="flex w-full items-center gap-2 sm:w-auto">
                <button
                    type="button"
                    @click="fetchSO"
                    :disabled="isLoading"
                    title="Muat ulang data"
                    class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-600 shadow-sm transition-all hover:border-slate-300 hover:bg-slate-50 hover:text-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                >
                    <i
                        class="pi pi-refresh"
                        :class="{ 'pi-spin text-blue-600': isLoading }"
                    ></i>
                </button>

                <button
                    type="button"
                    @click="tampilModalSO = true"
                    class="flex h-11 flex-1 items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 text-xs font-bold text-white shadow-[0_5px_18px_rgba(37,99,235,0.2)] transition-all hover:-translate-y-0.5 hover:bg-blue-700 hover:shadow-[0_8px_24px_rgba(37,99,235,0.28)] active:scale-[0.98] sm:flex-none md:text-sm"
                >
                    <i class="pi pi-plus"></i>
                    <span>Buat SO Baru</span>
                </button>
            </div>
        </div>


        <!-- =========================================================
             SUMMARY
        ========================================================== -->
        <div class="mb-5 grid grid-cols-2 gap-3 xl:grid-cols-4">

            <div class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                <div class="flex items-center justify-between gap-3">
                    <div>
                        <div class="text-[10px] font-bold uppercase tracking-[0.14em] text-slate-400">
                            Total SO
                        </div>

                        <div class="mt-2 text-xl font-black text-slate-900">
                            {{ daftarSO.length }}
                        </div>
                    </div>

                    <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-500">
                        <i class="pi pi-file"></i>
                    </div>
                </div>
            </div>


            <div class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                <div class="flex items-center justify-between gap-3">
                    <div>
                        <div class="text-[10px] font-bold uppercase tracking-[0.14em] text-slate-400">
                            Draft
                        </div>

                        <div class="mt-2 text-xl font-black text-slate-700">
                            {{ jumlahStatus('DRAFT') }}
                        </div>
                    </div>

                    <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-500">
                        <i class="pi pi-file-edit"></i>
                    </div>
                </div>
            </div>


            <div class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                <div class="flex items-center justify-between gap-3">
                    <div>
                        <div class="text-[10px] font-bold uppercase tracking-[0.14em] text-slate-400">
                            Disetujui
                        </div>

                        <div class="mt-2 text-xl font-black text-blue-600">
                            {{ jumlahStatus('DISETUJUI') }}
                        </div>
                    </div>

                    <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                        <i class="pi pi-check-circle"></i>
                    </div>
                </div>
            </div>


            <div class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                <div class="flex items-center justify-between gap-3">
                    <div>
                        <div class="text-[10px] font-bold uppercase tracking-[0.14em] text-slate-400">
                            Selesai
                        </div>

                        <div class="mt-2 text-xl font-black text-emerald-600">
                            {{ jumlahStatus('SELESAI') }}
                        </div>
                    </div>

                    <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
                        <i class="pi pi-check-circle"></i>
                    </div>
                </div>
            </div>
        </div>


        <!-- =========================================================
             MAIN CARD
        ========================================================== -->
        <div
            class="overflow-hidden rounded-[24px] border border-slate-200 bg-white shadow-[0_8px_30px_rgba(15,23,42,0.04)]"
        >

            <!-- TOOLBAR -->
            <div class="border-b border-slate-100 bg-slate-50/60 p-4 md:p-5">
                <div class="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">

                    <!-- SEARCH -->
                    <div
                        class="flex w-full items-center rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 shadow-sm transition-all focus-within:border-blue-400 focus-within:ring-4 focus-within:ring-blue-500/10 xl:max-w-md"
                    >
                        <i class="pi pi-search text-sm text-slate-400"></i>

                        <input
                            v-model="pencarian"
                            type="text"
                            placeholder="Cari nomor SO atau pelanggan..."
                            class="min-w-0 flex-1 border-0 bg-transparent px-2.5 text-xs font-medium text-slate-700 outline-none placeholder:text-slate-400 focus:ring-0 md:text-sm"
                        />

                        <button
                            v-if="pencarian"
                            type="button"
                            @click="pencarian = ''"
                            class="flex h-6 w-6 items-center justify-center rounded-lg text-slate-400 transition hover:bg-slate-100 hover:text-slate-600"
                        >
                            <i class="pi pi-times text-[10px]"></i>
                        </button>
                    </div>


                    <!-- STATUS TABS -->
                    <div class="w-full overflow-x-auto pb-1 xl:w-auto xl:pb-0 hide-scrollbar">
                        <div class="flex min-w-max items-center gap-1.5">
                            <button
                                v-for="tab in tabs"
                                :key="tab.value"
                                type="button"
                                @click="filterStatus = tab.value"
                                class="flex items-center gap-2 rounded-xl border px-4 py-2.5 text-xs font-bold transition-all"
                                :class="
                                    filterStatus === tab.value
                                        ? 'border-slate-800 bg-slate-800 text-white shadow-md'
                                        : 'border-slate-200 bg-white text-slate-500 hover:border-slate-300 hover:bg-slate-50 hover:text-slate-700'
                                "
                            >
                                <span>{{ tab.label }}</span>

                                <span
                                    class="rounded-md px-1.5 py-0.5 text-[9px] font-black"
                                    :class="
                                        filterStatus === tab.value
                                            ? 'bg-white/15 text-white'
                                            : 'bg-slate-100 text-slate-500'
                                    "
                                >
                                    {{ jumlahTab(tab.value) }}
                                </span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>


            <!-- =====================================================
                 TABLE
            ====================================================== -->
            <div class="w-full overflow-x-auto custom-scrollbar">
                <table class="w-full min-w-[950px] text-left text-sm">

                    <thead class="border-b border-slate-100 bg-slate-50/70">
                        <tr>
                            <th class="w-[20%] px-5 py-4 text-[10px] font-black uppercase tracking-wider text-slate-500">
                                No. Dokumen
                            </th>

                            <th class="w-[14%] px-5 py-4 text-[10px] font-black uppercase tracking-wider text-slate-500">
                                Tanggal
                            </th>

                            <th class="w-[25%] px-5 py-4 text-[10px] font-black uppercase tracking-wider text-slate-500">
                                Pelanggan
                            </th>

                            <th class="w-[18%] px-5 py-4 text-right text-[10px] font-black uppercase tracking-wider text-slate-500">
                                Total Tagihan
                            </th>

                            <th class="w-[15%] px-5 py-4 text-center text-[10px] font-black uppercase tracking-wider text-slate-500">
                                Status
                            </th>

                            <th class="w-[8%] px-5 py-4 text-center text-[10px] font-black uppercase tracking-wider text-slate-500">
                                Aksi
                            </th>
                        </tr>
                    </thead>


                    <tbody class="divide-y divide-slate-100">

                        <tr v-if="isLoading">
                            <td colspan="6" class="px-5 py-20 text-center">
                                <div class="mx-auto flex max-w-xs flex-col items-center">
                                    <div
                                        class="flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-50 text-blue-600"
                                    >
                                        <i class="pi pi-spin pi-spinner text-xl"></i>
                                    </div>

                                    <div class="mt-4 text-sm font-bold text-slate-700">
                                        Memuat Sales Order
                                    </div>

                                    <div class="mt-1 text-xs text-slate-400">
                                        Mengambil data terbaru dari server...
                                    </div>
                                </div>
                            </td>
                        </tr>


                        <tr v-else-if="filteredSO.length === 0">
                            <td colspan="6" class="bg-slate-50/30 px-5 py-20 text-center">
                                <div
                                    class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl border border-slate-200 bg-white text-slate-300 shadow-sm"
                                >
                                    <i class="pi pi-folder-open text-2xl"></i>
                                </div>

                                <div class="mt-4 text-sm font-black text-slate-700">
                                    {{ pencarian || filterStatus !== 'SEMUA'
                                        ? 'Data tidak ditemukan'
                                        : 'Belum ada Sales Order'
                                    }}
                                </div>

                                <div class="mx-auto mt-1 max-w-sm text-xs leading-5 text-slate-400">
                                    {{
                                        pencarian || filterStatus !== 'SEMUA'
                                            ? 'Tidak ada Sales Order yang sesuai dengan pencarian atau filter.'
                                            : 'Belum terdapat dokumen Sales Order yang dapat ditampilkan.'
                                    }}
                                </div>

                                <button
                                    v-if="pencarian || filterStatus !== 'SEMUA'"
                                    type="button"
                                    @click="resetFilter"
                                    class="mt-4 rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-white transition hover:bg-slate-800"
                                >
                                    Reset Filter
                                </button>
                            </td>
                        </tr>

                        <template v-else>
                            <tr
                                v-for="so in filteredSO"
                                :key="so.id"
                                class="group transition-colors hover:bg-slate-50/70"
                            >

                                <td class="px-5 py-4">
                                    <div class="flex items-center gap-3">
                                        <div
                                            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600 transition-colors group-hover:bg-blue-100"
                                        >
                                            <i class="pi pi-file text-xs"></i>
                                        </div>

                                        <div class="min-w-0">
                                            <div class="truncate font-black text-slate-800">
                                                {{ so.nomor_so || '-' }}
                                            </div>

                                            <div class="mt-0.5 flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider text-slate-400">
                                                <i class="pi pi-building text-[8px]"></i>
                                                {{ so.entitas?.kode || 'UMUM' }}
                                            </div>
                                        </div>
                                    </div>
                                </td>


                                <td class="px-5 py-4">
                                    <div class="font-semibold text-slate-600">
                                        {{ formatDate(so.tanggal) }}
                                    </div>
                                </td>


                                <td class="px-5 py-4">
                                    <div class="min-w-0">
                                        <div class="truncate font-bold text-slate-700">
                                            {{ so.pelanggan?.nama || '-' }}
                                        </div>

                                        <div class="mt-1 flex items-center gap-1 text-[11px] font-medium text-slate-400">
                                            <i class="pi pi-map-marker text-[9px]"></i>
                                            {{ so.pelanggan?.kota || 'Lokasi tidak tersedia' }}
                                        </div>
                                    </div>
                                </td>


                                <td class="px-5 py-4 text-right">
                                    <div class="font-black text-slate-800">
                                        {{ formatRupiah(so.grand_total) }}
                                    </div>
                                </td>


                                <td class="px-5 py-4 text-center">
                                    <span
                                        class="inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1.5 text-[10px] font-black uppercase tracking-wide"
                                        :class="badgeColor(so.status)"
                                    >
                                        <span class="h-1.5 w-1.5 rounded-full bg-current opacity-70"></span>
                                        {{ so.status || '-' }}
                                    </span>
                                </td>


                                <td class="px-5 py-4 text-center">
                                    <div class="flex justify-center">
                                        <span
                                            class="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-slate-50 px-2.5 py-1.5 text-[9px] font-bold text-slate-400"
                                            title="Aksi detail dan approval belum terhubung"
                                        >
                                            <i class="pi pi-info-circle text-[9px]"></i>
                                            Segera
                                        </span>
                                    </div>
                                </td>
                            </tr>
                        </template>

                    </tbody>
                </table>
            </div>

            <div
                class="flex flex-col gap-2 border-t border-slate-100 bg-slate-50/70 px-5 py-4 text-xs font-medium text-slate-500 sm:flex-row sm:items-center sm:justify-between"
            >
                <span>
                    Menampilkan
                    <strong class="font-black text-slate-700">
                        {{ filteredSO.length }}
                    </strong>
                    dari
                    <strong class="font-black text-slate-700">
                        {{ daftarSO.length }}
                    </strong>
                    Sales Order
                </span>

                <span v-if="pencarian">
                    Pencarian:
                    <strong class="font-bold text-slate-700">
                        "{{ pencarian }}"
                    </strong>
                </span>
            </div>
        </div>

        <Dialog
            v-model:visible="tampilModalSO"
            modal
            header="Buat Sales Order Baru"
            :style="{ width: '90vw', maxWidth: '1100px' }"
            :pt="{
                root: {
                    class: 'border-0 shadow-2xl rounded-2xl overflow-hidden'
                },
                header: {
                    class: 'bg-slate-50 border-b border-slate-100 p-5'
                },
                title: {
                    class: 'text-lg font-black text-slate-800'
                },
                content: {
                    class: 'p-0'
                }
            }"
        >
            <LazyFormSO
                v-if="tampilModalSO"
                @close="tampilModalSO = false"
                @saved="soBerhasilDisimpan"
            />
        </Dialog>
    </div>
</template>


<script setup>
import {
    ref,
    computed,
    onMounted,
    defineAsyncComponent,
} from 'vue'

import Dialog from 'primevue/dialog'
import { useSalesOrder } from '@/features/accounting/composables/useSalesOrder'


const LazyFormSO = defineAsyncComponent(() =>
    import('@/features/accounting/views/SalesOrderCreate.vue')
)


const {
    isLoading,
    daftarSO,
    fetchSO,
} = useSalesOrder()


const tampilModalSO = ref(false)
const pencarian = ref('')
const filterStatus = ref('SEMUA')

const tabs = [
    {
        label: 'Semua Data',
        value: 'SEMUA',
    },
    {
        label: 'Draft',
        value: 'DRAFT',
    },
    {
        label: 'Disetujui',
        value: 'DISETUJUI',
    },
    {
        label: 'Selesai',
        value: 'SELESAI',
    },
]

onMounted(() => {
    fetchSO()
})

const filteredSO = computed(() => {
    const keyword =
        pencarian.value
            .toLowerCase()
            .trim()

    return daftarSO.value.filter(so => {
        const status =
            String(
                so.status || ''
            ).toUpperCase()

        const matchStatus =
            filterStatus.value === 'SEMUA' ||
            status === filterStatus.value

        const safeNomorSo =
            String(
                so.nomor_so || ''
            ).toLowerCase()

        const safePelangganNama =
            String(
                so.pelanggan?.nama || ''
            ).toLowerCase()

        const safeKota =
            String(
                so.pelanggan?.kota || ''
            ).toLowerCase()

        const matchSearch =
            !keyword ||
            safeNomorSo.includes(keyword) ||
            safePelangganNama.includes(keyword) ||
            safeKota.includes(keyword)

        return (
            matchStatus &&
            matchSearch
        )
    })
})


const jumlahStatus = (status) => {
    return daftarSO.value.filter(
        so =>
            String(
                so.status || ''
            ).toUpperCase() === status
    ).length
}


const jumlahTab = (value) => {
    if (value === 'SEMUA') {
        return daftarSO.value.length
    }

    return jumlahStatus(value)
}


const resetFilter = () => {
    pencarian.value = ''
    filterStatus.value = 'SEMUA'
}

const formatRupiah = (angka) => {
    return new Intl.NumberFormat(
        'id-ID',
        {
            style: 'currency',
            currency: 'IDR',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0,
        }
    ).format(
        Number(angka || 0)
    )
}


const formatDate = (dateString) => {
    if (!dateString) {
        return '-'
    }

    const date =
        new Date(dateString)

    if (Number.isNaN(date.getTime())) {
        return '-'
    }

    return date.toLocaleDateString(
        'id-ID',
        {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
        }
    )
}

const badgeColor = (status) => {
    switch (
        String(status || '')
            .toUpperCase()
    ) {
        case 'DRAFT':
            return 'bg-slate-100 text-slate-600 border-slate-200'

        case 'DISETUJUI':
            return 'bg-blue-50 text-blue-700 border-blue-200'

        case 'SELESAI':
            return 'bg-emerald-50 text-emerald-700 border-emerald-200'

        case 'BATAL':
            return 'bg-rose-50 text-rose-700 border-rose-200'

        default:
            return 'bg-slate-100 text-slate-600 border-slate-200'
    }
}


const soBerhasilDisimpan = () => {
    tampilModalSO.value = false
    fetchSO()
}
</script>


<style scoped>


.animate-fade-in {
    animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}


.hide-scrollbar::-webkit-scrollbar {
    display: none;
}

.hide-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

.custom-scrollbar::-webkit-scrollbar {
    height: 7px;
    width: 7px;
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

button:focus-visible,
input:focus-visible {
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
    .animate-fade-in {
        animation: none;
    }

    *,
    *::before,
    *::after {
        scroll-behavior: auto !important;
    }
}
</style>