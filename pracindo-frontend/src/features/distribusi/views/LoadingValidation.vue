<template>
    <div class="relative w-full animate-fade-in">
        <div
            class="mb-5 flex flex-col gap-5 border-b border-slate-200 pb-5 md:mb-7 md:flex-row md:items-end md:justify-between"
        >
            <div class="min-w-0">
                <div
                    class="mb-2 flex flex-wrap items-center gap-1.5 text-[10px] font-extrabold uppercase tracking-[0.12em] text-slate-400"
                >
                    <span>Distribution</span>

                    <span
                        class="text-slate-300"
                        aria-hidden="true"
                    >
                        /
                    </span>

                    <span class="text-slate-600">
                        Validasi Muat
                    </span>
                </div>

                <div class="flex items-start gap-3">
                    <div
                        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-slate-900 text-white shadow-md shadow-slate-900/10"
                        aria-hidden="true"
                    >
                        <i class="pi pi-verified text-lg"></i>
                    </div>

                    <div class="min-w-0">
                        <h1
                            class="text-xl font-extrabold tracking-tight text-slate-800 md:text-2xl"
                        >
                            Validasi Muat Barang
                        </h1>

                        <p class="mt-1 max-w-2xl text-xs leading-5 text-slate-500 sm:text-sm">
                            Pindai atau centang barang yang naik ke armada agar sesuai dengan DO.
                        </p>
                    </div>
                </div>
            </div>

            <div class="flex w-full flex-col gap-2 sm:flex-row md:w-auto">
                <div class="relative min-w-0 flex-1 md:w-56">
                    <i
                        class="pi pi-search pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                        aria-hidden="true"
                    ></i>

                    <input
                        v-model="idCari"
                        @keyup.enter="cariData"
                        type="text"
                        inputmode="text"
                        autocomplete="off"
                        placeholder="ID Pengiriman..."
                        :disabled="memuat || sedangSimpan"
                        aria-label="ID Pengiriman"
                        class="w-full rounded-xl border border-slate-200 bg-white py-2.5 pl-9 pr-3 text-sm font-semibold text-slate-800 shadow-sm outline-none transition focus:border-blue-400 focus:ring-2 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100 disabled:opacity-60"
                    />
                </div>

                <button
                    type="button"
                    @click="cariData"
                    :disabled="!idCari || memuat || sedangSimpan"
                    class="flex items-center justify-center gap-2 rounded-xl bg-slate-900 px-5 py-2.5 text-sm font-extrabold text-white shadow-md shadow-slate-900/10 transition-all hover:-translate-y-0.5 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:translate-y-0 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none"
                >
                    <i
                        v-if="memuat"
                        class="pi pi-spin pi-spinner text-xs"
                        aria-hidden="true"
                    ></i>

                    <i
                        v-else
                        class="pi pi-search text-xs"
                        aria-hidden="true"
                    ></i>

                    <span>
                        {{ memuat ? 'Mencari...' : 'Cari' }}
                    </span>
                </button>

                <button
                    type="button"
                    :disabled="memuat || sedangSimpan"
                    class="flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-extrabold text-white shadow-md shadow-blue-600/10 transition-all hover:-translate-y-0.5 hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:translate-y-0 disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none"
                    aria-label="Scan QR Code"
                >
                    <i
                        class="pi pi-qrcode text-sm"
                        aria-hidden="true"
                    ></i>

                    <span class="hidden sm:inline">
                        Scan
                    </span>
                </button>
            </div>
        </div>

        <div
            v-if="memuat"
            class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
            aria-busy="true"
            aria-label="Memuat dokumen pengiriman"
        >
            <div
                class="border-b border-slate-200 bg-slate-50/80 px-4 py-4 sm:px-6"
            >
                <div class="flex items-center justify-between gap-4">
                    <div class="space-y-2">
                        <div
                            class="h-5 w-36 animate-pulse rounded bg-slate-200"
                            aria-hidden="true"
                        ></div>

                        <div
                            class="h-3 w-48 animate-pulse rounded bg-slate-100"
                            aria-hidden="true"
                        ></div>
                    </div>

                    <div
                        class="h-9 w-28 animate-pulse rounded-xl bg-slate-200"
                        aria-hidden="true"
                    ></div>
                </div>
            </div>

            <div class="space-y-0 divide-y divide-slate-100">
                <div
                    v-for="index in 5"
                    :key="index"
                    class="flex items-center gap-4 px-4 py-5 sm:px-6"
                >
                    <div
                        class="h-10 w-10 shrink-0 animate-pulse rounded-xl bg-slate-100"
                        aria-hidden="true"
                    ></div>

                    <div class="min-w-0 flex-1 space-y-2">
                        <div
                            class="h-3.5 w-1/2 animate-pulse rounded bg-slate-200"
                            aria-hidden="true"
                        ></div>

                        <div
                            class="h-3 w-1/4 animate-pulse rounded bg-slate-100"
                            aria-hidden="true"
                        ></div>
                    </div>

                    <div
                        class="hidden h-6 w-20 animate-pulse rounded-full bg-slate-100 sm:block"
                        aria-hidden="true"
                    ></div>

                    <div
                        class="h-9 w-9 animate-pulse rounded-xl bg-slate-100"
                        aria-hidden="true"
                    ></div>
                </div>
            </div>
        </div>

        <div
            v-else-if="galat"
            class="rounded-2xl border border-red-200 bg-red-50 p-4 shadow-sm sm:p-5"
            role="alert"
        >
            <div class="flex items-start gap-3">
                <div
                    class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-red-100 text-red-600"
                    aria-hidden="true"
                >
                    <i class="pi pi-exclamation-triangle text-sm"></i>
                </div>

                <div class="min-w-0 flex-1">
                    <p class="text-xs font-extrabold text-red-800">
                        Validasi tidak dapat dilanjutkan
                    </p>

                    <p class="mt-1 text-xs leading-5 text-red-600">
                        {{ galat }}
                    </p>

                    <button
                        type="button"
                        @click="cariData"
                        :disabled="!idCari || memuat"
                        class="mt-3 rounded-lg bg-white px-3 py-2 text-[11px] font-extrabold text-red-700 shadow-sm ring-1 ring-red-200 transition hover:bg-red-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        Coba Lagi
                    </button>
                </div>
            </div>
        </div>

        <div
            v-else-if="!pengiriman"
            class="rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-14 text-center shadow-sm"
        >
            <div
                class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-100 text-slate-400"
                aria-hidden="true"
            >
                <i class="pi pi-search text-2xl"></i>
            </div>

            <h3 class="mt-4 text-sm font-extrabold text-slate-700">
                Cari Dokumen Pengiriman
            </h3>

            <p class="mx-auto mt-1 max-w-md text-xs leading-5 text-slate-500">
                Masukkan ID Pengiriman di atas untuk memulai validasi loading barang ke armada.
            </p>
        </div>

        <section
            v-else
            class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
            aria-labelledby="delivery-document-title"
        >
            <div
                class="border-b border-slate-200 bg-gradient-to-br from-slate-50 to-white px-4 py-5 sm:px-6"
            >
                <div
                    class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"
                >
                    <div class="min-w-0">
                        <div class="flex flex-wrap items-center gap-2">
                            <h2
                                id="delivery-document-title"
                                class="text-lg font-extrabold tracking-tight text-slate-800 sm:text-xl"
                            >
                                {{ pengiriman.nomor || `DO-${pengiriman.id}` }}
                            </h2>

                            <span
                                class="rounded-full border border-blue-200 bg-blue-50 px-2.5 py-1 text-[9px] font-extrabold uppercase tracking-[0.08em] text-blue-700"
                            >
                                Validasi Muat
                            </span>
                        </div>

                        <p class="mt-1.5 flex items-start gap-1.5 text-xs font-medium text-slate-500">
                            <i
                                class="pi pi-map-marker mt-0.5 text-[10px] text-slate-400"
                                aria-hidden="true"
                            ></i>

                            <span class="leading-5">
                                Tujuan:
                                {{
                                    pengiriman.tujuan_nama ||
                                    pengiriman.pelanggan_nama ||
                                    'Multi Tujuan'
                                }}
                            </span>
                        </p>
                    </div>

                    <div
                        class="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-3.5 py-3 shadow-sm lg:min-w-[250px]"
                    >
                        <div
                            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-500"
                            aria-hidden="true"
                        >
                            <i class="pi pi-truck text-sm"></i>
                        </div>

                        <div class="min-w-0">
                            <p class="text-[9px] font-extrabold uppercase tracking-[0.1em] text-slate-400">
                                Armada
                            </p>

                            <p class="mt-0.5 truncate text-xs font-extrabold text-slate-700">
                                {{
                                    pengiriman.kendaraan_plat ||
                                    (pengiriman.kendaraan &&
                                        pengiriman.kendaraan.plat_nomor) ||
                                    'Truk Reguler'
                                }}
                            </p>

                            <p class="truncate text-[10px] font-medium text-slate-400">
                                {{
                                    pengiriman.kurir_nama ||
                                    (pengiriman.kurir &&
                                        pengiriman.kurir.nama) ||
                                    'Kurir'
                                }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="border-b border-slate-200 bg-white px-4 py-3 sm:px-6">
                <div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
                    <div class="rounded-xl bg-slate-50 px-3 py-3">
                        <p class="text-[9px] font-extrabold uppercase tracking-[0.08em] text-slate-400">
                            Total Item
                        </p>

                        <p class="mt-1 text-lg font-extrabold text-slate-800">
                            {{ pengiriman.items?.length || 0 }}
                        </p>
                    </div>

                    <div class="rounded-xl bg-emerald-50 px-3 py-3">
                        <p class="text-[9px] font-extrabold uppercase tracking-[0.08em] text-emerald-500">
                            Sesuai
                        </p>

                        <p class="mt-1 text-lg font-extrabold text-emerald-700">
                            {{ jumlahSesuai }}
                        </p>
                    </div>

                    <div
                        class="col-span-2 rounded-xl bg-amber-50 px-3 py-3 sm:col-span-1"
                    >
                        <p class="text-[9px] font-extrabold uppercase tracking-[0.08em] text-amber-500">
                            Perlu Muat
                        </p>

                        <p class="mt-1 text-lg font-extrabold text-amber-700">
                            {{ jumlahKurang }}
                        </p>
                    </div>
                </div>
            </div>

            <div class="overflow-x-auto custom-scrollbar">
                <table class="w-full min-w-[850px] border-collapse text-left">
                    <thead>
                        <tr class="border-b border-slate-200 bg-slate-50/70">
                            <th
                                class="w-[36%] px-4 py-3 text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400 sm:px-5"
                            >
                                Nama Produk / Varian
                            </th>

                            <th
                                class="w-[14%] px-4 py-3 text-right text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400 sm:px-5"
                            >
                                Qty DO
                            </th>

                            <th
                                class="w-[14%] px-4 py-3 text-right text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400 sm:px-5"
                            >
                                Qty Muat
                            </th>

                            <th
                                class="w-[16%] px-4 py-3 text-center text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400 sm:px-5"
                            >
                                Status
                            </th>

                            <th
                                class="w-[20%] px-4 py-3 text-center text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400 sm:px-5"
                            >
                                Aksi
                            </th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-slate-100">
                        <tr
                            v-if="!pengiriman.items || pengiriman.items.length === 0"
                        >
                            <td
                                colspan="5"
                                class="px-5 py-12 text-center"
                            >
                                <div class="flex flex-col items-center">
                                    <div
                                        class="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-slate-400"
                                        aria-hidden="true"
                                    >
                                        <i class="pi pi-box text-lg"></i>
                                    </div>

                                    <p class="mt-3 text-xs font-extrabold text-slate-600">
                                        Data muatan tidak ditemukan
                                    </p>

                                    <p class="mt-1 text-[11px] font-medium text-slate-400">
                                        Tidak ada item yang dapat divalidasi dari dokumen ini.
                                    </p>
                                </div>
                            </td>
                        </tr>

                        <tr
                            v-for="(item, idx) in pengiriman.items || []"
                            :key="item.id || idx"
                            class="transition-colors hover:bg-slate-50/70"
                        >
                            <td class="px-4 py-4 sm:px-5">
                                <div class="flex min-w-0 items-center gap-3">
                                    <div
                                        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
                                        aria-hidden="true"
                                    >
                                        <i class="pi pi-box text-xs"></i>
                                    </div>

                                    <div class="min-w-0">
                                        <p class="truncate text-sm font-extrabold text-slate-800">
                                            {{
                                                item.produk_nama ||
                                                item.nama_produk ||
                                                `Produk ID ${item.produk_id || idx}`
                                            }}
                                        </p>

                                        <p class="mt-0.5 text-[10px] font-medium text-slate-400">
                                            {{
                                                item.kemasan ||
                                                'Kemasan Standard'
                                            }}
                                        </p>
                                    </div>
                                </div>
                            </td>

                            <td class="px-4 py-4 text-right sm:px-5">
                                <span class="text-sm font-bold text-slate-500">
                                    {{
                                        item.qty_do ||
                                        item.qty_kg ||
                                        0
                                    }}
                                </span>
                            </td>

                            <td class="px-4 py-4 text-right sm:px-5">
                                <span
                                    class="text-base font-extrabold"
                                    :class="
                                        qtySesuai(item)
                                            ? 'text-emerald-600'
                                            : 'text-amber-500'
                                    "
                                >
                                    {{ item.qty_muat || 0 }}
                                </span>
                            </td>

                            <td class="px-4 py-4 text-center sm:px-5">
                                <span
                                    v-if="qtySesuai(item)"
                                    class="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-2.5 py-1.5 text-[9px] font-extrabold uppercase tracking-[0.06em] text-emerald-700"
                                >
                                    <i
                                        class="pi pi-check text-[8px]"
                                        aria-hidden="true"
                                    ></i>

                                    Sesuai
                                </span>

                                <span
                                    v-else
                                    class="inline-flex items-center gap-1.5 rounded-full border border-amber-200 bg-amber-50 px-2.5 py-1.5 text-[9px] font-extrabold uppercase tracking-[0.06em] text-amber-700"
                                >
                                    <i
                                        class="pi pi-clock text-[8px]"
                                        aria-hidden="true"
                                    ></i>

                                    Kurang
                                </span>
                            </td>

                            <td class="px-4 py-4 text-center sm:px-5">
                                <button
                                    v-if="qtySesuai(item)"
                                    type="button"
                                    disabled
                                    class="mx-auto flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 ring-1 ring-emerald-200"
                                    :aria-label="`Item ${idx + 1} sudah sesuai`"
                                >
                                    <i
                                        class="pi pi-check text-xs"
                                        aria-hidden="true"
                                    ></i>
                                </button>

                                <button
                                    v-else
                                    type="button"
                                    @click="tambahMuat(item)"
                                    :disabled="
                                        sedangSimpan ||
                                        sudahMaksimal(item)
                                    "
                                    :aria-label="
                                        sudahMaksimal(item)
                                            ? `Qty muat ${item.produk_nama || item.nama_produk || 'produk'} sudah mencapai Qty DO`
                                            : `Tambah muatan untuk ${item.produk_nama || item.nama_produk || 'produk'}`
                                    "
                                    class="group mx-auto flex h-9 w-9 items-center justify-center rounded-xl bg-blue-50 text-blue-600 shadow-sm ring-1 ring-blue-100 transition-all hover:-translate-y-0.5 hover:bg-blue-600 hover:text-white hover:shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 disabled:cursor-not-allowed disabled:bg-slate-100 disabled:text-slate-300 disabled:shadow-none disabled:ring-slate-200"
                                >
                                    <i
                                        class="pi pi-plus text-xs transition-transform duration-200 group-hover:scale-110"
                                        aria-hidden="true"
                                    ></i>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div
                class="flex flex-col gap-4 border-t border-slate-200 bg-slate-50/70 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6"
            >
                <div class="min-w-0">
                    <p class="text-xs font-extrabold text-slate-700">
                        {{
                            jumlahKurang > 0
                                ? 'Masih ada item yang belum sesuai.'
                                : 'Seluruh item sudah sesuai dengan DO.'
                        }}
                    </p>

                    <p class="mt-1 text-[10px] font-medium leading-4 text-slate-400">
                        Qty Muat tidak dapat melebihi Qty DO.
                    </p>
                </div>

                <button
                    type="button"
                    @click="submitLoading"
                    :disabled="
                        sedangSimpan ||
                        !pengiriman ||
                        pengiriman.items?.length === 0
                    "
                    :aria-busy="sedangSimpan"
                    class="flex w-full items-center justify-center gap-2 rounded-xl bg-slate-900 px-6 py-3 text-sm font-extrabold text-white shadow-lg shadow-slate-900/10 transition-all hover:-translate-y-0.5 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:translate-y-0 disabled:cursor-not-allowed disabled:translate-y-0 disabled:bg-slate-300 disabled:shadow-none sm:w-auto sm:px-8"
                >
                    <i
                        v-if="sedangSimpan"
                        class="pi pi-spin pi-spinner text-sm"
                        aria-hidden="true"
                    ></i>

                    <i
                        v-else
                        class="pi pi-lock text-sm"
                        aria-hidden="true"
                    ></i>

                    <span>
                        {{
                            sedangSimpan
                                ? 'Menyimpan...'
                                : 'Selesaikan Loading & Kunci DO'
                        }}
                    </span>
                </button>
            </div>
        </section>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiDistribusi } from '../api'

const route = useRoute()
const router = useRouter()

const pengiriman = ref(null)
const memuat = ref(false)
const sedangSimpan = ref(false)
const galat = ref('')
const idCari = ref('')

const getQtyDO = (item) => {
    return Number(
        item.qty_do ??
        item.qty_kg ??
        0
    ) || 0
}

const getQtyMuat = (item) => {
    return Number(
        item.qty_muat ??
        0
    ) || 0
}

const sudahMaksimal = (item) => {
    return getQtyMuat(item) >= getQtyDO(item)
}

const qtySesuai = (item) => {
    return getQtyMuat(item) >= getQtyDO(item)
}

const jumlahSesuai = computed(() => {
    return (pengiriman.value?.items || []).filter(
        (item) => qtySesuai(item)
    ).length
})

const jumlahKurang = computed(() => {
    return (pengiriman.value?.items || []).filter(
        (item) => !qtySesuai(item)
    ).length
})

const cariData = async () => {
    if (!idCari.value || memuat.value) return

    memuat.value = true
    galat.value = ''
    pengiriman.value = null

    try {
        const data =
            await apiDistribusi.getDetailPengiriman(
                idCari.value
            )

        pengiriman.value = data

        for (const item of pengiriman.value?.items || []) {
            const batas = getQtyDO(item)
            const qtySaatIni = getQtyMuat(item)

            if (qtySaatIni > batas) {
                item.qty_muat = batas
            }
        }
    } catch (error) {
        console.error(error)

        galat.value =
            'Dokumen pengiriman tidak ditemukan atau terjadi kesalahan server.'
    } finally {
        memuat.value = false
    }
}

const tambahMuat = (item) => {
    if (
        sedangSimpan.value ||
        sudahMaksimal(item)
    ) {
        return
    }

    const batas = getQtyDO(item)
    const qtySekarang = getQtyMuat(item)

    item.qty_muat = Math.min(
        qtySekarang + 1,
        batas
    )
}

const submitLoading = async () => {
    if (
        !pengiriman.value ||
        sedangSimpan.value
    ) {
        return
    }

    sedangSimpan.value = true
    galat.value = ''

    try {
        const payload = {
            items: (
                pengiriman.value.items || []
            ).map((item) => ({
                id: item.id,
                qty_muat: Math.min(
                    getQtyMuat(item),
                    getQtyDO(item)
                )
            }))
        }

        await apiDistribusi.validasiLoading(
            pengiriman.value.id,
            payload
        )

        await router.push('/distribusi')
    } catch (err) {
        console.error(err)

        galat.value =
            err.response?.data?.detail ||
            'Gagal menyimpan validasi loading ke server.'
    } finally {
        sedangSimpan.value = false
    }
}

onMounted(() => {
    if (route.query.id) {
        idCari.value = route.query.id
        cariData()
    }
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
