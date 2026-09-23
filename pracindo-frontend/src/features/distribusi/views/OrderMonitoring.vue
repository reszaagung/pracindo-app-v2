<template>
    <div
        class="relative min-h-screen w-full animate-fade-in bg-[#F8FAFC] p-4 sm:p-5 lg:p-6"
    >
        <div class="mx-auto flex w-full max-w-7xl flex-col">
            <header
                class="mb-5 flex flex-col gap-5 border-b border-slate-200 pb-5 md:mb-7 md:flex-row md:items-end md:justify-between"
            >
                <div class="min-w-0">
                    <div
                        class="mb-2 flex flex-wrap items-center gap-1.5 text-[10px] font-extrabold uppercase tracking-[0.12em] text-slate-400"
                    >
                        <span>Logistics</span>

                        <span
                            class="text-slate-300"
                            aria-hidden="true"
                        >
                            /
                        </span>

                        <span class="text-slate-600">
                            Monitoring Order
                        </span>
                    </div>

                    <div class="flex items-start gap-3">
                        <div
                            class="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-slate-900 text-white shadow-md shadow-slate-900/10"
                            aria-hidden="true"
                        >
                            <i class="pi pi-chart-line text-lg"></i>
                        </div>

                        <div class="min-w-0">
                            <h1
                                class="text-2xl font-extrabold tracking-tight text-slate-800 md:text-3xl"
                            >
                                Monitoring Order
                            </h1>

                            <p
                                class="mt-1 max-w-3xl text-xs leading-5 text-slate-500 sm:text-sm"
                            >
                                Pantau status persetujuan logistik dan posisi pengiriman secara real-time.
                            </p>
                        </div>
                    </div>
                </div>

                <button
                    type="button"
                    @click="muatData"
                    :disabled="memuat"
                    :aria-busy="memuat"
                    class="group flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-extrabold text-slate-700 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-slate-300 hover:bg-slate-50 hover:shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
                >
                    <i
                        :class="[
                            'pi pi-sync text-xs transition-transform duration-500',
                            memuat ? 'pi-spin' : 'group-hover:rotate-180'
                        ]"
                        aria-hidden="true"
                    ></i>

                    <span>
                        {{ memuat ? 'Memperbarui...' : 'Segarkan Data' }}
                    </span>
                </button>
            </header>

            <section
                class="mb-5 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
                aria-label="Filter monitoring order"
            >
                <div
                    class="border-b border-slate-100 bg-slate-50/70 px-4 py-3 sm:px-5"
                >
                    <div class="flex items-center gap-2">
                        <div
                            class="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-900 text-white"
                            aria-hidden="true"
                        >
                            <i class="pi pi-filter text-xs"></i>
                        </div>

                        <div>
                            <h2 class="text-xs font-extrabold text-slate-700">
                                Filter Monitoring
                            </h2>

                            <p class="text-[10px] font-medium text-slate-400">
                                Saring dokumen berdasarkan nomor, status, atau tanggal.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 gap-4 p-4 md:grid-cols-3 sm:p-5">
                    <div class="flex flex-col gap-1.5">
                        <label
                            for="filter-cari"
                            class="text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                        >
                            Cari Dokumen
                        </label>

                        <div
                            class="flex items-center overflow-hidden rounded-xl border border-slate-200 bg-slate-50 transition-colors focus-within:border-slate-400 focus-within:bg-white focus-within:ring-2 focus-within:ring-slate-100"
                        >
                            <div
                                class="flex h-10 w-10 shrink-0 items-center justify-center text-slate-400"
                                aria-hidden="true"
                            >
                                <i class="pi pi-search text-sm"></i>
                            </div>

                            <input
                                id="filter-cari"
                                v-model="filter.cari"
                                @keyup.enter="muatData"
                                type="text"
                                autocomplete="off"
                                placeholder="Ketik No. Order..."
                                :disabled="memuat"
                                class="min-w-0 flex-1 bg-transparent py-2.5 pr-4 text-sm font-semibold text-slate-800 outline-none placeholder:text-slate-400 disabled:cursor-not-allowed disabled:opacity-60"
                            />
                        </div>
                    </div>

                    <div class="flex flex-col gap-1.5">
                        <label
                            for="filter-status"
                            class="text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                        >
                            Status Logistik
                        </label>

                        <div class="relative">
                            <select
                                id="filter-status"
                                v-model="filter.status"
                                @change="muatData"
                                :disabled="memuat"
                                class="w-full cursor-pointer appearance-none rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 pr-10 text-sm font-semibold text-slate-800 outline-none transition focus:border-slate-400 focus:bg-white focus:ring-2 focus:ring-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
                            >
                                <option value="">
                                    Semua Status
                                </option>

                                <option value="DRAFT">
                                    Menunggu ACC Logistik
                                </option>

                                <option value="TERJADWAL">
                                    Disetujui & Terjadwal
                                </option>

                                <option value="LOADING">
                                    Proses Loading
                                </option>

                                <option value="DIKIRIM">
                                    Sedang Dikirim
                                </option>
                            </select>

                            <i
                                class="pi pi-chevron-down pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-[10px] text-slate-400"
                                aria-hidden="true"
                            ></i>
                        </div>
                    </div>

                    <div class="flex flex-col gap-1.5">
                        <label
                            for="filter-tanggal"
                            class="text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                        >
                            Tanggal
                        </label>

                        <input
                            id="filter-tanggal"
                            type="date"
                            v-model="filter.tanggal"
                            @change="muatData"
                            :disabled="memuat"
                            class="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-sm font-semibold text-slate-800 outline-none transition focus:border-slate-400 focus:bg-white focus:ring-2 focus:ring-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
                        />
                    </div>
                </div>
            </section>

            <section
                class="relative overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
                aria-label="Daftar monitoring order"
                :aria-busy="memuat"
            >
                <div
                    v-if="memuat && daftarOrder.length === 0"
                    class="grid grid-cols-1 divide-y divide-slate-100"
                >
                    <div
                        v-for="index in 6"
                        :key="index"
                        class="flex items-center gap-4 px-4 py-5 sm:px-5"
                    >
                        <div
                            class="h-10 w-10 shrink-0 animate-pulse rounded-xl bg-slate-100"
                            aria-hidden="true"
                        ></div>

                        <div class="min-w-0 flex-1 space-y-2">
                            <div
                                class="h-3.5 w-40 animate-pulse rounded bg-slate-200"
                                aria-hidden="true"
                            ></div>

                            <div
                                class="h-3 w-24 animate-pulse rounded bg-slate-100"
                                aria-hidden="true"
                            ></div>
                        </div>

                        <div
                            class="hidden h-7 w-24 animate-pulse rounded-lg bg-slate-100 md:block"
                            aria-hidden="true"
                        ></div>

                        <div
                            class="hidden h-7 w-28 animate-pulse rounded-lg bg-slate-100 lg:block"
                            aria-hidden="true"
                        ></div>

                        <div
                            class="h-7 w-24 animate-pulse rounded-full bg-slate-100"
                            aria-hidden="true"
                        ></div>
                    </div>
                </div>

                <div
                    v-else-if="daftarOrder.length === 0"
                    class="flex min-h-[420px] flex-col items-center justify-center px-6 py-14 text-center"
                >
                    <div
                        class="flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-100 text-slate-400"
                        aria-hidden="true"
                    >
                        <i class="pi pi-inbox text-2xl"></i>
                    </div>

                    <h3 class="mt-4 text-sm font-extrabold text-slate-700">
                        Tidak Ada Order
                    </h3>

                    <p class="mx-auto mt-1 max-w-md text-xs leading-5 text-slate-500">
                        Belum ada request pengiriman yang cocok dengan filter yang dipilih.
                    </p>

                    <button
                        type="button"
                        @click="muatData"
                        class="mt-5 inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2.5 text-xs font-extrabold text-white shadow-sm transition-all hover:-translate-y-0.5 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:translate-y-0"
                    >
                        <i
                            class="pi pi-refresh text-[10px]"
                            aria-hidden="true"
                        ></i>

                        Muat Ulang
                    </button>
                </div>

                <div
                    v-else
                    class="relative"
                >
                    <div
                        v-if="memuat"
                        class="absolute inset-x-0 top-0 z-20 flex items-center justify-center border-b border-blue-100 bg-blue-50/90 px-4 py-2 backdrop-blur-sm"
                        role="status"
                        aria-live="polite"
                    >
                        <div class="flex items-center gap-2">
                            <i
                                class="pi pi-spin pi-spinner text-xs text-blue-600"
                                aria-hidden="true"
                            ></i>

                            <span class="text-[10px] font-extrabold text-blue-700">
                                Memperbarui data...
                            </span>
                        </div>
                    </div>

                    <div class="overflow-x-auto custom-scrollbar">
                        <table class="w-full min-w-[1080px] border-collapse text-left">
                            <thead>
                                <tr class="border-b border-slate-200 bg-slate-50/80">
                                    <th
                                        class="px-5 py-4 text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                                    >
                                        No. Order / Tanggal
                                    </th>

                                    <th
                                        class="px-5 py-4 text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                                    >
                                        Tujuan
                                    </th>

                                    <th
                                        class="px-5 py-4 text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                                    >
                                        Tipe
                                    </th>

                                    <th
                                        class="px-5 py-4 text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                                    >
                                        Armada & Supir
                                    </th>

                                    <th
                                        class="px-5 py-4 text-center text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                                    >
                                        Status
                                    </th>
                                </tr>
                            </thead>

                            <tbody class="divide-y divide-slate-100">
                                <tr
                                    v-for="item in daftarOrder"
                                    :key="item.id"
                                    class="group transition-colors hover:bg-slate-50/70"
                                >
                                    <td class="px-5 py-4 align-top">
                                        <div class="flex items-start gap-3">
                                            <div
                                                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
                                                aria-hidden="true"
                                            >
                                                <i class="pi pi-file text-xs"></i>
                                            </div>

                                            <div class="min-w-0">
                                                <p class="truncate text-sm font-extrabold text-slate-800">
                                                    {{
                                                        item.nomor ||
                                                        `REQ-${item.id}`
                                                    }}
                                                </p>

                                                <p
                                                    class="mt-1 flex items-center gap-1.5 text-[10px] font-medium text-slate-400"
                                                >
                                                    <i
                                                        class="pi pi-calendar text-[9px]"
                                                        aria-hidden="true"
                                                    ></i>

                                                    {{ item.tanggal || '-' }}
                                                </p>
                                            </div>
                                        </div>
                                    </td>

                                    <td class="px-5 py-4 align-top">
                                        <p class="max-w-[250px] truncate text-sm font-extrabold text-slate-700">
                                            {{
                                                item.tujuan_nama ||
                                                item.pelanggan_nama ||
                                                'Multidrop'
                                            }}
                                        </p>

                                        <p class="mt-1 max-w-[260px] truncate text-[10px] font-medium text-slate-400">
                                            {{
                                                item.alamat ||
                                                item.tujuan_alamat ||
                                                '-'
                                            }}
                                        </p>
                                    </td>

                                    <td class="px-5 py-4 align-top">
                                        <span
                                            class="inline-flex items-center gap-1.5 rounded-lg border px-2.5 py-1.5 text-[9px] font-extrabold uppercase tracking-[0.06em]"
                                            :class="
                                                item.jenis_tujuan === 'CABANG'
                                                    ? 'border-blue-200 bg-blue-50 text-blue-700'
                                                    : 'border-emerald-200 bg-emerald-50 text-emerald-700'
                                            "
                                        >
                                            <i
                                                :class="
                                                    item.jenis_tujuan === 'CABANG'
                                                        ? 'pi pi-building'
                                                        : 'pi pi-send'
                                                "
                                                class="text-[8px]"
                                                aria-hidden="true"
                                            ></i>

                                            {{
                                                item.jenis_tujuan === 'CABANG'
                                                    ? 'Distribusi Retail'
                                                    : 'Delivery B2C'
                                            }}
                                        </span>
                                    </td>

                                    <td class="px-5 py-4 align-top">
                                        <div
                                            v-if="
                                                item.kendaraan_id ||
                                                item.kurir_id
                                            "
                                            class="flex items-start gap-3"
                                        >
                                            <div
                                                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
                                                aria-hidden="true"
                                            >
                                                <i class="pi pi-truck text-xs"></i>
                                            </div>

                                            <div class="min-w-0">
                                                <p class="truncate text-sm font-extrabold text-slate-700">
                                                    {{
                                                        item.kendaraan_plat ||
                                                        (
                                                            item.kendaraan &&
                                                            item.kendaraan
                                                                .plat_nomor
                                                        ) ||
                                                        'Truk Reguler'
                                                    }}
                                                </p>

                                                <p
                                                    class="mt-1 flex items-center gap-1.5 truncate text-[10px] font-medium text-slate-400"
                                                >
                                                    <i
                                                        class="pi pi-user text-[8px]"
                                                        aria-hidden="true"
                                                    ></i>

                                                    {{
                                                        item.kurir_nama ||
                                                        (
                                                            item.kurir &&
                                                            item.kurir.nama
                                                        ) ||
                                                        'Kurir Internal'
                                                    }}
                                                </p>
                                            </div>
                                        </div>

                                        <span
                                            v-else
                                            class="inline-flex items-center gap-1.5 rounded-lg border border-amber-200 bg-amber-50 px-2.5 py-1.5 text-[9px] font-extrabold uppercase tracking-[0.05em] text-amber-700"
                                        >
                                            <i
                                                class="pi pi-hourglass text-[8px]"
                                                aria-hidden="true"
                                            ></i>

                                            Menunggu ACC
                                        </span>
                                    </td>

                                    <td class="px-5 py-4 text-center align-top">
                                        <span
                                            class="inline-flex items-center justify-center rounded-lg border px-3 py-1.5 text-[9px] font-extrabold uppercase tracking-[0.08em] shadow-sm"
                                            :class="
                                                badgeWarna(
                                                    item.status,
                                                    item.kendaraan_id
                                                )
                                            "
                                        >
                                            {{ getStatusTeks(
                                                item.status,
                                                item.kendaraan_id
                                            ) }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div
                        class="flex items-center justify-between border-t border-slate-100 bg-slate-50/50 px-5 py-3"
                    >
                        <p class="text-[10px] font-medium text-slate-400">
                            Menampilkan
                            <span class="font-extrabold text-slate-600">
                                {{ daftarOrder.length }}
                            </span>
                            order
                        </p>

                        <p
                            v-if="memuat"
                            class="flex items-center gap-1.5 text-[10px] font-bold text-blue-600"
                        >
                            <i
                                class="pi pi-spin pi-spinner text-[9px]"
                                aria-hidden="true"
                            ></i>

                            Memperbarui
                        </p>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { apiDistribusi } from '@/features/distribusi/api'
import api from '@/utils/api'

const memuat = ref(false)
const daftarOrder = ref([])

const filter = reactive({
    cari: '',
    status: '',
    tanggal: ''
})

const normalisasiList = (response) => {
    const data = response?.data ?? response

    if (Array.isArray(data)) {
        return data
    }

    if (Array.isArray(data?.results)) {
        return data.results
    }

    if (Array.isArray(data?.data)) {
        return data.data
    }

    return []
}

const getStatusTeks = (status, adaKendaraan) => {
    const s = (status || 'DRAFT').toUpperCase()

    if (s === 'DRAFT' && !adaKendaraan) {
        return 'MENUNGGU ACC'
    }

    if (s === 'DRAFT' && adaKendaraan) {
        return 'TERJADWAL'
    }

    return s
}

const badgeWarna = (status, adaKendaraan) => {
    const s = getStatusTeks(status, adaKendaraan)

    switch (s) {
        case 'MENUNGGU ACC':
            return 'bg-amber-100 text-amber-700 border-amber-300'

        case 'TERJADWAL':
            return 'bg-blue-100 text-blue-700 border-blue-300'

        case 'LOADING':
            return 'bg-indigo-100 text-indigo-700 border-indigo-300'

        case 'DIKIRIM':
            return 'bg-purple-100 text-purple-700 border-purple-300'

        case 'SELESAI':
            return 'bg-emerald-100 text-emerald-700 border-emerald-300'

        default:
            return 'bg-slate-100 text-slate-600 border-slate-300'
    }
}

const muatData = async () => {
    if (memuat.value) return

    memuat.value = true

    try {
        const params = {}

        if (filter.cari) {
            params.search = filter.cari
        }

        if (filter.status) {
            params.status = filter.status
        }

        if (filter.tanggal) {
            params.tanggal = filter.tanggal
        }

        const [
            resDistribusi,
            resDelivery
        ] = await Promise.all([
            api.get(
                'warehouse/distribusi/',
                { params }
            ).catch(() => ({
                data: {
                    results: []
                }
            })),
            api.get(
                'logistik/pengiriman/',
                { params }
            ).catch(() => ({
                data: {
                    results: []
                }
            }))
        ])

        const dataDistribusi =
            normalisasiList(resDistribusi)

        const dataDelivery =
            normalisasiList(resDelivery)

        const gabungan = [
            ...dataDistribusi,
            ...dataDelivery
        ].sort((a, b) => {
            const tanggalA = new Date(
                a.tanggal_dibuat ||
                a.tanggal ||
                0
            ).getTime()

            const tanggalB = new Date(
                b.tanggal_dibuat ||
                b.tanggal ||
                0
            ).getTime()

            return tanggalB - tanggalA
        })

        daftarOrder.value = gabungan
    } catch (err) {
        console.error(err)
        daftarOrder.value = []
    } finally {
        memuat.value = false
    }
}

onMounted(() => {
    muatData()
})
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

.custom-scrollbar::-webkit-scrollbar {
    height: 6px;
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

@media (prefers-reduced-motion: reduce) {
    .animate-fade-in,
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
