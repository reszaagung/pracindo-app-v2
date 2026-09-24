<template>
    <div
        class="flex flex-col w-full animate-fade-in relative pb-8"
    >
        <!-- =========================================================
             ERROR
        ========================================================== -->
        <div
            v-if="galat"
            class="mb-5 rounded-2xl border border-rose-200 bg-rose-50/80 px-4 py-3.5 shadow-sm"
        >
            <div class="flex items-start gap-3">
                <div
                    class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-rose-100 text-rose-600"
                >
                    <i class="pi pi-exclamation-triangle text-sm"></i>
                </div>

                <div class="min-w-0">
                    <p
                        class="text-[11px] font-bold uppercase tracking-[0.12em] text-rose-500"
                    >
                        Terjadi kesalahan
                    </p>

                    <p
                        class="mt-1 text-sm font-medium leading-6 text-rose-700"
                    >
                        {{ galat }}
                    </p>
                </div>
            </div>
        </div>

        <template v-if="stokDetail">
            <!-- =====================================================
                 HEADER
            ====================================================== -->
            <div
                class="mb-6 flex flex-col gap-5 xl:flex-row xl:items-end xl:justify-between"
            >
                <div class="min-w-0">
                    <div
                        class="mb-2 flex items-center gap-2 text-[10px] font-medium text-slate-400"
                    >
                        <router-link
                            to="/inventory"
                            class="inline-flex items-center gap-1.5 transition-colors hover:text-slate-700"
                        >
                            <i class="pi pi-box text-[9px]"></i>
                            Inventory
                        </router-link>

                        <i
                            class="pi pi-angle-right text-[8px] text-slate-300"
                        ></i>

                        <span
                            class="truncate font-semibold text-slate-600"
                        >
                            Posisi Stok
                        </span>

                        <i
                            class="pi pi-angle-right text-[8px] text-slate-300"
                        ></i>

                        <span
                            class="truncate font-semibold text-slate-500"
                        >
                            {{ stokDetail.produk_kode }}
                        </span>
                    </div>

                    <div
                        class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between"
                    >
                        <div class="min-w-0">
                            <div
                                class="flex flex-wrap items-center gap-2"
                            >
                                <span
                                    class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-[9px] font-bold uppercase tracking-wider text-slate-500 shadow-sm"
                                >
                                    <i class="pi pi-tag text-[8px]"></i>
                                    {{ stokDetail.produk_kode }}
                                </span>

                                <span
                                    v-if="stokDetail.lapis"
                                    class="inline-flex items-center rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1 text-[9px] font-bold uppercase tracking-wider text-slate-500"
                                >
                                    {{ stokDetail.lapis }}
                                </span>
                            </div>

                            <h1
                                class="mt-3 break-words text-2xl font-black tracking-tight text-slate-900 md:text-3xl"
                            >
                                {{ stokDetail.produk_kode }}
                            </h1>

                            <div
                                class="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-slate-500"
                            >
                                <span>
                                    {{ stokDetail.grup_bahan_kode }}
                                </span>

                                <span class="text-slate-300">•</span>

                                <span>
                                    Lapis
                                    {{ stokDetail.lapis_label }}
                                </span>

                                <template
                                    v-if="stokDetail.tangki_kode"
                                >
                                    <span class="text-slate-300">•</span>

                                    <span
                                        class="inline-flex items-center gap-1"
                                    >
                                        <i
                                            class="pi pi-database text-[9px] text-slate-400"
                                        ></i>
                                        Tangki
                                        {{ stokDetail.tangki_kode }}
                                    </span>
                                </template>
                            </div>
                        </div>

                        <!-- TOTAL QTY -->
                        <div
                            class="w-full rounded-2xl border border-slate-200 bg-white px-5 py-4 shadow-sm sm:w-auto sm:min-w-[190px]"
                        >
                            <div
                                class="flex items-center justify-between gap-6"
                            >
                                <div>
                                    <p
                                        class="text-[9px] font-bold uppercase tracking-[0.14em] text-slate-400"
                                    >
                                        Total Qty
                                    </p>

                                    <p
                                        class="mt-1 text-[10px] text-slate-400"
                                    >
                                        Posisi saat ini
                                    </p>
                                </div>

                                <div class="text-right">
                                    <div
                                        class="text-2xl font-black tracking-tight text-slate-900"
                                    >
                                        {{ angka(stokDetail.qty, 3) }}
                                    </div>

                                    <div
                                        class="mt-0.5 text-[9px] font-semibold uppercase tracking-wider text-slate-400"
                                    >
                                        Unit
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- =====================================================
                 POOL INFO
            ====================================================== -->
            <div
                v-if="stokDetail.lapis === 'POOL'"
                class="mb-6 overflow-hidden rounded-3xl border border-blue-200 bg-gradient-to-r from-blue-50 via-white to-sky-50 shadow-sm"
            >
                <div
                    class="flex flex-col gap-5 p-5 md:flex-row md:items-center md:justify-between md:p-6"
                >
                    <div class="flex items-start gap-4">
                        <div
                            class="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-blue-100 text-blue-600"
                        >
                            <i class="pi pi-share-alt text-base"></i>
                        </div>

                        <div>
                            <p
                                class="text-[9px] font-bold uppercase tracking-[0.14em] text-blue-500"
                            >
                                Posisi Pool
                            </p>

                            <h3
                                class="mt-1 text-sm font-bold text-blue-950"
                            >
                                Stok fisik tanpa pemilik langsung
                            </h3>

                            <p
                                class="mt-1.5 max-w-2xl text-xs leading-5 text-blue-800/80"
                            >
                                Lapis POOL tidak memiliki pemilik langsung.
                                Yang tercatat adalah
                                <strong class="font-bold text-blue-900">
                                    posisi klaim
                                </strong>
                                masing-masing entitas atas pool ini.
                            </p>
                        </div>
                    </div>

                    <router-link
                        :to="`/inventory/klaim/${stokDetail.grup_bahan}`"
                        class="inline-flex w-full shrink-0 items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-[10px] font-bold text-white shadow-md shadow-blue-600/20 transition-all hover:-translate-y-0.5 hover:bg-blue-700 md:w-auto"
                    >
                        <span>Lihat Posisi Klaim</span>
                        <i class="pi pi-arrow-right text-[9px]"></i>
                    </router-link>
                </div>
            </div>

            <!-- =====================================================
                 OWNERSHIP
            ====================================================== -->
            <section
                v-else
                class="mb-6 overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm"
            >
                <div
                    class="flex flex-col gap-3 border-b border-slate-100 px-5 py-4 md:flex-row md:items-center md:justify-between md:px-6"
                >
                    <div class="flex items-center gap-3">
                        <div
                            class="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600"
                        >
                            <i class="pi pi-users text-sm"></i>
                        </div>

                        <div>
                            <h2
                                class="text-sm font-bold text-slate-800"
                            >
                                Kepemilikan Entitas
                            </h2>

                            <p
                                class="mt-0.5 text-[10px] text-slate-400"
                            >
                                Distribusi qty berdasarkan entitas
                            </p>
                        </div>
                    </div>

                    <span
                        class="inline-flex w-fit items-center rounded-full bg-slate-50 px-2.5 py-1 text-[9px] font-semibold text-slate-500"
                    >
                        {{ stokDetail.kepemilikan?.length || 0 }}
                        Entitas
                    </span>
                </div>

                <div
                    v-if="stokDetail.kepemilikan?.length"
                    class="overflow-x-auto custom-scrollbar"
                >
                    <table
                        class="w-full min-w-[30rem] text-left text-xs"
                    >
                        <thead
                            class="bg-slate-50/80 text-[9px] uppercase tracking-[0.12em] text-slate-400"
                        >
                            <tr>
                                <th
                                    class="px-5 py-3 font-bold md:px-6"
                                >
                                    Entitas
                                </th>

                                <th
                                    class="px-5 py-3 text-right font-bold md:px-6"
                                >
                                    Qty
                                </th>
                            </tr>
                        </thead>

                        <tbody class="divide-y divide-slate-100">
                            <tr
                                v-for="k in stokDetail.kepemilikan"
                                :key="k.entitas"
                                class="group transition-colors hover:bg-slate-50/70"
                            >
                                <td
                                    class="px-5 py-4 md:px-6"
                                >
                                    <div
                                        class="flex items-center gap-3"
                                    >
                                        <div
                                            class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-[9px] font-black text-slate-600 transition-colors group-hover:bg-emerald-50 group-hover:text-emerald-700"
                                        >
                                            {{
                                                String(
                                                    k.entitas_kode || '-'
                                                )
                                                    .slice(0, 2)
                                                    .toUpperCase()
                                            }}
                                        </div>

                                        <div>
                                            <div
                                                class="font-bold text-slate-800"
                                            >
                                                {{ k.entitas_kode || '—' }}
                                            </div>

                                            <div
                                                class="mt-0.5 text-[9px] text-slate-400"
                                            >
                                                Kepemilikan
                                            </div>
                                        </div>
                                    </div>
                                </td>

                                <td
                                    class="px-5 py-4 text-right md:px-6"
                                >
                                    <span
                                        class="font-black tabular-nums text-slate-800"
                                    >
                                        {{ angka(k.qty, 3) }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div
                    v-else
                    class="flex flex-col items-center justify-center px-6 py-12 text-center"
                >
                    <div
                        class="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-slate-400"
                    >
                        <i class="pi pi-users text-base"></i>
                    </div>

                    <p
                        class="mt-3 text-xs font-semibold text-slate-600"
                    >
                        Belum ada kepemilikan
                    </p>

                    <p
                        class="mt-1 max-w-xs text-[10px] leading-5 text-slate-400"
                    >
                        Belum ada distribusi kepemilikan entitas
                        yang tercatat untuk stok ini.
                    </p>
                </div>
            </section>

            <!-- =====================================================
                 MUTATION HISTORY
            ====================================================== -->
            <section
                class="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm"
            >
                <div
                    class="flex flex-col gap-3 border-b border-slate-100 px-5 py-4 md:flex-row md:items-center md:justify-between md:px-6"
                >
                    <div class="flex items-center gap-3">
                        <div
                            class="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-100 text-slate-600"
                        >
                            <i class="pi pi-history text-sm"></i>
                        </div>

                        <div>
                            <h2
                                class="text-sm font-bold text-slate-800"
                            >
                                Riwayat Mutasi
                            </h2>

                            <p
                                class="mt-0.5 text-[10px] text-slate-400"
                            >
                                Jejak pergerakan stok secara kronologis
                            </p>
                        </div>
                    </div>

                    <span
                        class="inline-flex w-fit items-center rounded-full bg-slate-50 px-2.5 py-1 text-[9px] font-semibold text-slate-500"
                    >
                        {{ daftarMutasi.length || 0 }} Mutasi
                    </span>
                </div>

                <div
                    v-if="daftarMutasi.length"
                    class="overflow-x-auto custom-scrollbar"
                >
                    <table
                        class="w-full min-w-[54rem] text-left text-xs"
                    >
                        <thead
                            class="sticky top-0 z-10 bg-slate-50/95 text-[9px] uppercase tracking-[0.12em] text-slate-400 backdrop-blur"
                        >
                            <tr>
                                <th
                                    class="px-4 py-3 font-bold md:px-5"
                                >
                                    Tanggal
                                </th>

                                <th
                                    class="px-4 py-3 font-bold md:px-5"
                                >
                                    Jenis
                                </th>

                                <th
                                    class="px-4 py-3 text-right font-bold md:px-5"
                                >
                                    Masuk
                                </th>

                                <th
                                    class="px-4 py-3 text-right font-bold md:px-5"
                                >
                                    Keluar
                                </th>

                                <th
                                    class="px-4 py-3 text-right font-bold md:px-5"
                                >
                                    Saldo Akhir
                                </th>

                                <th
                                    class="px-4 py-3 font-bold md:px-5"
                                >
                                    Referensi
                                </th>
                            </tr>
                        </thead>

                        <tbody class="divide-y divide-slate-100">
                            <tr
                                v-for="m in daftarMutasi"
                                :key="m.id"
                                class="group transition-colors hover:bg-slate-50/70"
                            >
                                <td
                                    class="whitespace-nowrap px-4 py-4 font-medium text-slate-500 md:px-5"
                                >
                                    {{ tanggal(m.tanggal) }}
                                </td>

                                <td
                                    class="px-4 py-4 md:px-5"
                                >
                                    <span
                                        class="inline-flex max-w-[170px] items-center truncate rounded-lg border px-2.5 py-1.5 text-[9px] font-bold"
                                        :class="
                                            String(m.jenis_label || '')
                                                .toLowerCase()
                                                .includes('setor')
                                                ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
                                                : String(m.jenis_label || '')
                                                      .toLowerCase()
                                                      .includes('tarik')
                                                    ? 'border-rose-200 bg-rose-50 text-rose-700'
                                                    : 'border-slate-200 bg-slate-50 text-slate-600'
                                        "
                                    >
                                        {{ m.jenis_label || '—' }}
                                    </span>
                                </td>

                                <td
                                    class="px-4 py-4 text-right md:px-5"
                                >
                                    <span
                                        v-if="m.masuk"
                                        class="inline-flex items-center gap-1 font-semibold tabular-nums text-emerald-600"
                                    >
                                        <i
                                            class="pi pi-arrow-down-left text-[8px]"
                                        ></i>

                                        {{ angka(m.masuk, 3) }}
                                    </span>

                                    <span
                                        v-else
                                        class="text-slate-300"
                                    >
                                        —
                                    </span>
                                </td>

                                <td
                                    class="px-4 py-4 text-right md:px-5"
                                >
                                    <span
                                        v-if="m.keluar"
                                        class="inline-flex items-center gap-1 font-semibold tabular-nums text-rose-600"
                                    >
                                        <i
                                            class="pi pi-arrow-up-right text-[8px]"
                                        ></i>

                                        {{ angka(m.keluar, 3) }}
                                    </span>

                                    <span
                                        v-else
                                        class="text-slate-300"
                                    >
                                        —
                                    </span>
                                </td>

                                <td
                                    class="px-4 py-4 text-right md:px-5"
                                >
                                    <span
                                        class="font-black tabular-nums text-slate-800"
                                    >
                                        {{
                                            angka(
                                                m.saldo_akhir,
                                                3
                                            )
                                        }}
                                    </span>
                                </td>

                                <td
                                    class="max-w-[220px] px-4 py-4 md:px-5"
                                >
                                    <span
                                        class="block truncate text-[10px] font-medium text-slate-500"
                                        :title="
                                            m.referensi ||
                                            ''
                                        "
                                    >
                                        {{ m.referensi || '—' }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div
                    v-else
                    class="flex flex-col items-center justify-center px-6 py-14 text-center"
                >
                    <div
                        class="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-slate-400"
                    >
                        <i class="pi pi-history text-base"></i>
                    </div>

                    <p
                        class="mt-3 text-xs font-semibold text-slate-600"
                    >
                        Belum ada mutasi
                    </p>

                    <p
                        class="mt-1 max-w-xs text-[10px] leading-5 text-slate-400"
                    >
                        Riwayat pergerakan stok akan muncul di sini
                        setelah transaksi tercatat.
                    </p>
                </div>
            </section>
        </template>

        <!-- =========================================================
             EMPTY / NOT FOUND
        ========================================================== -->
        <div
            v-else-if="!galat"
            class="flex min-h-[420px] flex-col items-center justify-center rounded-3xl border border-dashed border-slate-200 bg-white/70 px-6 text-center shadow-sm"
        >
            <div
                class="flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-100 text-slate-400"
            >
                <i class="pi pi-box text-xl"></i>
            </div>

            <h2
                class="mt-4 text-sm font-bold text-slate-700"
            >
                Detail stok belum tersedia
            </h2>

            <p
                class="mt-1 max-w-sm text-xs leading-5 text-slate-400"
            >
                Data detail stok belum dapat ditampilkan.
            </p>
        </div>
    </div>
</template>


<script setup>
import {
    onMounted,
    watch,
} from 'vue'

import {
    useRoute,
} from 'vue-router'

import {
    useStock,
} from '../composables/useStock'

import {
    angka,
} from '@/utils/format'


const route = useRoute()

const {
    stokDetail,
    daftarMutasi,
    galat,
    muatStokDetail,
    muatMutasi,
} = useStock()


/* =========================================================
   TANGGAL
========================================================= */

const tanggal = (nilai) => {
    if (!nilai) {
        return '—'
    }

    const date = new Date(nilai)

    if (Number.isNaN(date.getTime())) {
        return nilai
    }

    return date.toLocaleString(
        'id-ID',
        {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        }
    )
}


/* =========================================================
   MUAT DATA
========================================================= */

const muatData = async () => {
    const id = route.params.id

    if (!id) {
        return
    }

    await Promise.all([
        muatStokDetail(id),
        muatMutasi({
            stok: id,
        }),
    ])
}


/* =========================================================
   INIT
========================================================= */

onMounted(() => {
    muatData()
})


/* =========================================================
   ROUTE CHANGE
========================================================= */

watch(
    () => route.params.id,
    (id, idLama) => {
        if (
            id &&
            id !== idLama
        ) {
            muatData()
        }
    }
)
</script>


<style scoped>
.animate-fade-in {
    animation: fadeIn 0.35s ease-out forwards;
}

.slide-enter-active,
.slide-leave-active {
    transition:
        opacity 0.2s ease,
        transform 0.2s ease;
}

.slide-enter-from,
.slide-leave-to {
    opacity: 0;
    transform: translateY(-6px);
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
</style>
