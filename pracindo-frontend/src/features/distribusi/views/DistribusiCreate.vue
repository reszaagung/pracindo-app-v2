<template>
    <div class="w-full">
        <form
            @submit.prevent="simpanDistribusi"
            class="flex flex-col gap-5 sm:gap-6"
            :aria-busy="sedangProses || sedangMuatStok"
        >
            <div class="grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-6">
                <div class="flex flex-col gap-4">
                    <div
                        class="rounded-2xl border border-slate-200 bg-slate-50 p-4 shadow-sm transition-colors focus-within:border-slate-300 focus-within:bg-white"
                    >
                        <label
                            for="tanggal-distribusi"
                            class="mb-2 block text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                        >
                            Tanggal Distribusi
                            <span class="text-red-500">*</span>
                        </label>

                        <div class="flex items-center gap-3">
                            <div
                                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-slate-500 shadow-sm"
                                aria-hidden="true"
                            >
                                <i class="pi pi-calendar text-sm"></i>
                            </div>

                            <input
                                id="tanggal-distribusi"
                                v-model="form.tanggal"
                                type="date"
                                required
                                class="min-w-0 flex-1 border-0 border-b border-slate-300 bg-transparent px-0 pb-2 text-sm font-bold text-slate-800 outline-none transition-colors focus:border-slate-900 focus:ring-0"
                            />
                        </div>
                    </div>

                    <div
                        class="rounded-2xl border border-blue-200 bg-gradient-to-br from-blue-50 to-white p-4 shadow-sm transition-colors focus-within:border-blue-300"
                    >
                        <label
                            for="tujuan-cabang"
                            class="mb-2 block text-[10px] font-extrabold uppercase tracking-[0.08em] text-blue-600"
                        >
                            Tujuan Cabang Retail
                            <span class="text-red-500">*</span>
                        </label>

                        <div class="flex items-center gap-3">
                            <div
                                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-100 text-blue-600"
                                aria-hidden="true"
                            >
                                <i class="pi pi-building text-sm"></i>
                            </div>

                            <select
                                id="tujuan-cabang"
                                v-model="form.tujuan_toko_id"
                                required
                                :disabled="sedangMuatStok || sedangProses"
                                class="min-w-0 flex-1 cursor-pointer appearance-none border-0 border-b border-blue-200 bg-transparent px-0 pb-2 text-sm font-bold text-slate-800 outline-none transition-colors focus:border-blue-600 focus:ring-0 disabled:cursor-not-allowed disabled:opacity-60"
                            >
                                <option value="" disabled>
                                    -- Pilih Cabang Retail --
                                </option>

                                <option
                                    v-for="toko in daftarToko"
                                    :key="toko.id"
                                    :value="toko.id"
                                >
                                    {{ toko.nama }}

                                    <template v-if="toko.kode">
                                        ({{ toko.kode }})
                                    </template>
                                </option>
                            </select>

                            <i
                                class="pi pi-chevron-down text-[11px] text-blue-400"
                                aria-hidden="true"
                            ></i>
                        </div>
                    </div>
                </div>

                <div class="flex flex-col gap-4">
                    <div
                        class="rounded-2xl border border-blue-200 bg-blue-50 p-4 shadow-sm"
                    >
                        <label
                            for="nomor-do"
                            class="mb-2 block text-[10px] font-extrabold uppercase tracking-[0.08em] text-blue-500"
                        >
                            No Surat Jalan (DO)
                        </label>

                        <div class="flex items-center gap-3">
                            <div
                                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-blue-600 shadow-sm"
                                aria-hidden="true"
                            >
                                <i class="pi pi-file text-sm"></i>
                            </div>

                            <input
                                id="nomor-do"
                                type="text"
                                :value="previewNomor"
                                readonly
                                class="min-w-0 flex-1 cursor-not-allowed border-0 border-b border-blue-200 bg-transparent px-0 pb-2 text-sm font-extrabold tracking-tight text-blue-700 outline-none focus:border-blue-300 focus:ring-0"
                            />
                        </div>

                        <p
                            class="mt-2 pl-12 text-[10px] font-medium text-blue-500"
                        >
                            Nomor final akan ditentukan otomatis oleh sistem.
                        </p>
                    </div>

                    <div
                        class="rounded-2xl border border-slate-200 bg-slate-50 p-4 shadow-sm transition-colors focus-within:border-slate-300 focus-within:bg-white"
                    >
                        <label
                            for="kendaraan"
                            class="mb-2 block text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                        >
                            Armada / Kendaraan
                        </label>

                        <div class="flex items-center gap-3">
                            <div
                                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-slate-500 shadow-sm"
                                aria-hidden="true"
                            >
                                <i class="pi pi-truck text-sm"></i>
                            </div>

                            <select
                                id="kendaraan"
                                v-model="form.kendaraan_id"
                                :disabled="sedangMuatStok || sedangProses"
                                class="min-w-0 flex-1 cursor-pointer appearance-none border-0 border-b border-slate-300 bg-transparent px-0 pb-2 text-sm font-bold text-slate-800 outline-none transition-colors focus:border-slate-900 focus:ring-0 disabled:cursor-not-allowed disabled:opacity-60"
                            >
                                <option value="">
                                    -- Bebas (Ditentukan Kemudian) --
                                </option>

                                <option
                                    v-for="armada in daftarArmada"
                                    :key="armada.id"
                                    :value="armada.id"
                                >
                                    {{ armada.plat_nomor }} -
                                    {{ armada.nama }}
                                </option>
                            </select>

                            <i
                                class="pi pi-chevron-down text-[11px] text-slate-400"
                                aria-hidden="true"
                            ></i>
                        </div>
                    </div>
                </div>
            </div>

            <section
                class="relative overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
                aria-labelledby="rincian-barang-title"
            >
                <div
                    v-if="sedangMuatStok"
                    class="absolute inset-0 z-20 flex items-center justify-center bg-white/75 backdrop-blur-sm"
                    role="status"
                    aria-live="polite"
                >
                    <div
                        class="flex min-w-[190px] flex-col items-center gap-3 rounded-2xl border border-slate-200 bg-white px-6 py-5 shadow-xl"
                    >
                        <div
                            class="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-50 text-blue-600"
                            aria-hidden="true"
                        >
                            <i class="pi pi-spin pi-spinner text-lg"></i>
                        </div>

                        <div class="text-center">
                            <p class="text-xs font-extrabold text-slate-700">
                                Memuat Stok Pabrik
                            </p>

                            <p
                                class="mt-1 text-[10px] font-medium text-slate-400"
                            >
                                Menyiapkan data barang dan kemasan...
                            </p>
                        </div>
                    </div>
                </div>

                <div
                    class="flex flex-col gap-3 border-b border-slate-200 bg-slate-50/80 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-5"
                >
                    <div class="flex min-w-0 items-center gap-3">
                        <div
                            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-white shadow-sm"
                            aria-hidden="true"
                        >
                            <i class="pi pi-box text-sm"></i>
                        </div>

                        <div class="min-w-0">
                            <h2
                                id="rincian-barang-title"
                                class="truncate text-sm font-extrabold text-slate-800"
                            >
                                Rincian Barang
                            </h2>

                            <p
                                class="mt-0.5 text-[10px] font-medium text-slate-400"
                            >
                                Pilih barang, kemasan, dan jumlah yang akan dikirim.
                            </p>
                        </div>
                    </div>

                    <div
                        class="self-start rounded-full bg-white px-3 py-1.5 text-[10px] font-extrabold text-slate-500 shadow-sm ring-1 ring-slate-200 sm:self-auto"
                    >
                        {{ form.items.length }}
                        {{
                            form.items.length === 1
                                ? 'Baris'
                                : 'Baris'
                        }}
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table
                        class="w-full min-w-[920px] border-collapse text-left"
                    >
                        <thead>
                            <tr
                                class="border-b border-slate-200 bg-white"
                            >
                                <th
                                    class="w-16 px-4 py-3 text-center text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400"
                                >
                                    No
                                </th>

                                <th
                                    class="w-52 px-4 py-3 text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400"
                                >
                                    Group / Klaim
                                </th>

                                <th
                                    class="min-w-[200px] px-4 py-3 text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400"
                                >
                                    Pilih Barang
                                </th>

                                <th
                                    class="min-w-[210px] px-4 py-3 text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400"
                                >
                                    Kemasan & Stok
                                </th>

                                <th
                                    class="w-28 px-4 py-3 text-center text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400"
                                >
                                    Qty Kirim
                                </th>

                                <th
                                    class="w-28 px-4 py-3 text-right text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400"
                                >
                                    Total Berat
                                </th>

                                <th
                                    class="w-16 px-4 py-3 text-center text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400"
                                >
                                    Aksi
                                </th>
                            </tr>
                        </thead>

                        <tbody class="divide-y divide-slate-100">
                            <tr
                                v-for="(item, index) in form.items"
                                :key="index"
                                class="transition-colors hover:bg-slate-50/60"
                            >
                                <td
                                    class="px-4 py-4 text-center align-top"
                                >
                                    <span
                                        class="inline-flex h-7 w-7 items-center justify-center rounded-lg bg-slate-100 text-[10px] font-extrabold text-slate-500"
                                    >
                                        {{ index + 1 }}
                                    </span>
                                </td>

                                <td class="px-3 py-3 align-top">
                                    <label
                                        :for="`grup-${index}`"
                                        class="sr-only"
                                    >
                                        Grup untuk baris
                                        {{ index + 1 }}
                                    </label>

                                    <select
                                        :id="`grup-${index}`"
                                        v-model="item.stiker"
                                        @change="resetBarang(item)"
                                        required
                                        :disabled="sedangProses"
                                        class="w-full border-0 border-b border-slate-300 bg-transparent px-0 py-2.5 text-sm font-bold text-blue-700 outline-none transition-colors focus:border-blue-600 focus:ring-0 disabled:cursor-not-allowed disabled:bg-transparent"
                                    >
                                        <option
                                            value=""
                                            disabled
                                        >
                                            -- Pilih Grup --
                                        </option>

                                        <option
                                            v-for="grup in daftarGrupUnik"
                                            :key="grup"
                                            :value="grup"
                                        >
                                            {{ grup }}
                                        </option>
                                    </select>
                                </td>

                                <td class="px-3 py-3 align-top">
                                    <label
                                        :for="`barang-${index}`"
                                        class="sr-only"
                                    >
                                        Barang untuk baris
                                        {{ index + 1 }}
                                    </label>

                                    <select
                                        :id="`barang-${index}`"
                                        v-model="item.barang_nama"
                                        @change="resetKemasan(item)"
                                        :disabled="
                                            !item.stiker ||
                                            sedangProses
                                        "
                                        required
                                        class="w-full border-0 border-b border-slate-300 bg-transparent px-0 py-2.5 text-sm font-bold text-slate-800 outline-none transition-colors focus:border-blue-600 focus:ring-0 disabled:cursor-not-allowed disabled:bg-transparent disabled:text-slate-400"
                                    >
                                        <option
                                            value=""
                                            disabled
                                        >
                                            {{
                                                item.stiker
                                                    ? '-- Pilih Barang --'
                                                    : 'Pilih Grup Dulu'
                                            }}
                                        </option>

                                        <option
                                            v-for="nama in getBarangTersedia(item)"
                                            :key="nama"
                                            :value="nama"
                                        >
                                            {{ nama }}
                                        </option>
                                    </select>

                                    <div
                                        v-if="
                                            item.barang_nama &&
                                            item.stiker
                                        "
                                        class="mt-2 flex items-start gap-1.5 rounded-lg bg-emerald-50 px-2.5 py-2 text-[10px] font-semibold leading-4 text-emerald-700"
                                    >
                                        <i
                                            class="pi pi-info-circle mt-0.5 text-[10px]"
                                            aria-hidden="true"
                                        ></i>

                                        <span>
                                            {{
                                                getInfoStokBarang(item)
                                            }}
                                        </span>
                                    </div>
                                </td>

                                <td class="px-3 py-3 align-top">
                                    <label
                                        :for="`kemasan-${index}`"
                                        class="sr-only"
                                    >
                                        Kemasan untuk baris
                                        {{ index + 1 }}
                                    </label>

                                    <select
                                        :id="`kemasan-${index}`"
                                        v-model="item.stok_terpilih"
                                        @change="hitungOtomatis(item)"
                                        :disabled="
                                            !item.barang_nama ||
                                            sedangProses
                                        "
                                        required
                                        class="w-full border-0 border-b border-slate-300 bg-transparent px-0 py-2.5 text-sm font-bold text-slate-800 outline-none transition-colors focus:border-blue-600 focus:ring-0 disabled:cursor-not-allowed disabled:bg-transparent disabled:text-slate-400"
                                    >
                                        <option
                                            :value="null"
                                            disabled
                                        >
                                            -- Pilih Kemasan --
                                        </option>

                                        <option
                                            v-for="(
                                                kemasan,
                                                idx
                                            ) in getKemasanTersedia(
                                                item
                                            )"
                                            :key="idx"
                                            :value="kemasan"
                                        >
                                            {{
                                                kemasan.kemasan_nama ||
                                                kemasan.kemasan
                                            }}
                                            · Ada:
                                            {{
                                                kemasan.qty_unit ||
                                                kemasan.qty ||
                                                0
                                            }}
                                        </option>
                                    </select>
                                </td>

                                <td
                                    class="px-3 py-3 align-top"
                                >
                                    <label
                                        :for="`qty-${index}`"
                                        class="sr-only"
                                    >
                                        Qty kirim untuk baris
                                        {{ index + 1 }}
                                    </label>

                                    <input
                                        :id="`qty-${index}`"
                                        type="number"
                                        v-model="item.total_unit"
                                        @input="
                                            kalkulasiBerat(item)
                                        "
                                        min="1"
                                        :disabled="
                                            !item.stok_terpilih ||
                                            sedangProses
                                        "
                                        required
                                        class="w-full border-0 border-b border-slate-300 bg-transparent px-0 py-2.5 text-center text-sm font-extrabold text-blue-600 outline-none transition-colors focus:border-blue-600 focus:ring-0 disabled:cursor-not-allowed disabled:bg-transparent disabled:text-slate-400"
                                    />
                                </td>

                                <td
                                    class="px-4 py-3 text-right align-top"
                                >
                                    <div
                                        class="mt-2 whitespace-nowrap text-sm font-extrabold text-slate-700"
                                    >
                                        {{
                                            item.total_berat
                                                ? `${item.total_berat} Kg`
                                                : '0 Kg'
                                        }}
                                    </div>
                                </td>

                                <td
                                    class="px-3 py-3 text-center align-top"
                                >
                                    <button
                                        v-if="
                                            form.items.length > 1
                                        "
                                        type="button"
                                        :disabled="sedangProses"
                                        :aria-label="`Hapus baris barang ${index + 1}`"
                                        :title="`Hapus baris ${index + 1}`"
                                        @click="hapusItem(index)"
                                        class="mt-1 flex h-9 w-9 items-center justify-center rounded-xl border border-transparent text-red-500 transition-all hover:border-red-200 hover:bg-red-50 hover:text-red-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    >
                                        <i
                                            class="pi pi-trash text-sm"
                                            aria-hidden="true"
                                        ></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div
                    class="border-t border-slate-200 bg-slate-50 px-4 py-3 sm:px-5"
                >
                    <button
                        type="button"
                        @click="tambahItem"
                        :disabled="
                            sedangProses ||
                            sedangMuatStok
                        "
                        class="mx-auto flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-xs font-extrabold text-blue-600 transition-all hover:bg-blue-50 hover:text-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        <span
                            class="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-100"
                            aria-hidden="true"
                        >
                            <i class="pi pi-plus text-[10px]"></i>
                        </span>

                        Tambah Baris Barang
                    </button>
                </div>
            </section>

            <div
                class="flex flex-col-reverse gap-3 border-t border-slate-200 pt-4 sm:flex-row sm:items-center sm:justify-end"
            >
                <div
                    class="mr-auto hidden text-[10px] font-medium text-slate-400 sm:block"
                >
                    Pastikan seluruh barang dan quantity sudah sesuai sebelum dikirim.
                </div>

                <button
                    type="submit"
                    :disabled="
                        sedangProses ||
                        sedangMuatStok ||
                        form.items.length === 0
                    "
                    :aria-busy="sedangProses"
                    class="group flex w-full items-center justify-center gap-2 rounded-xl bg-slate-900 px-6 py-3 text-sm font-extrabold text-white shadow-lg shadow-slate-900/10 transition-all hover:-translate-y-0.5 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:translate-y-0 active:scale-[0.99] disabled:cursor-not-allowed disabled:translate-y-0 disabled:bg-slate-300 disabled:shadow-none sm:w-auto sm:px-8"
                >
                    <i
                        v-if="sedangProses"
                        class="pi pi-spin pi-spinner text-sm"
                        aria-hidden="true"
                    ></i>

                    <i
                        v-else
                        class="pi pi-send text-sm transition-transform duration-200 group-hover:translate-x-0.5"
                        aria-hidden="true"
                    ></i>

                    <span>
                        {{
                            sedangProses
                                ? 'Menyimpan...'
                                : 'Kirim Request Distribusi'
                        }}
                    </span>
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDistribusiForm } from '../composables/useDistribusiForm'

const {
    sedangProses,
    sedangMuatStok,
    daftarToko,
    daftarArmada,
    form,
    previewNomor,
    daftarGrupUnik,
    getBarangTersedia,
    tambahItem,
    hapusItem,
    getKemasanTersedia,
    getInfoStokBarang,
    resetBarang,
    resetKemasan,
    hitungOtomatis,
    kalkulasiBerat,
    muatDataMaster,
    simpanDistribusi
} = useDistribusiForm()

onMounted(() => {
    muatDataMaster()
})
</script>

<style scoped>
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
