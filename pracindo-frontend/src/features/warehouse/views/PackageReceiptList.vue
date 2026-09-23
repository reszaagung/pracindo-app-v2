<!-- features/warehouse/views/PackageReceiptList.vue -->
<template>
    <div class="w-full min-w-0 animate-fade-in relative">
        <transition name="page-fade" mode="out-in">

            <section
                v-if="modeForm"
                key="form"
                class="w-full"
            >
                <PackageReceiptForm @tutup="tutupForm" />
            </section>

            <section
                v-else
                key="list"
                class="w-full"
            >
                <header class="mb-5 md:mb-6">
                    <div class="flex flex-col xl:flex-row xl:items-end xl:justify-between gap-4">
                        <div class="min-w-0">
                            <div class="flex items-center gap-2 mb-2">
                                <span class="text-xs font-medium text-slate-400">
                                    Warehouse
                                </span>
                                <i class="pi pi-angle-right text-[9px] text-slate-300"></i>
                                <span class="text-xs font-semibold text-slate-600">
                                    Penerimaan Kemasan
                                </span>
                            </div>

                            <div class="flex flex-wrap items-center gap-3">
                                <h1 class="text-2xl md:text-3xl font-bold text-slate-900 tracking-tight">
                                    Penerimaan Kemasan
                                </h1>

                                <span class="inline-flex items-center justify-center min-w-7 h-7 px-2 rounded-full bg-slate-100 text-slate-700 border border-slate-200 text-xs font-bold">
                                    {{ daftarPenerimaan.length }}
                                </span>
                            </div>

                            <p class="text-xs md:text-sm text-slate-500 mt-1">
                                Kelola penerimaan aset kemasan dan pantau riwayat barang masuk.
                            </p>
                        </div>

                        <div class="flex items-center gap-2">
                            <button
                                type="button"
                                @click="muatSemua"
                                :disabled="sedangProses"
                                class="h-10 px-3.5 rounded-xl border border-slate-200 bg-white text-slate-600 text-xs font-bold hover:bg-slate-50 hover:text-slate-900 hover:border-slate-300 transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center gap-2"
                            >
                                <i
                                    class="pi"
                                    :class="sedangProses ? 'pi-spin pi-spinner' : 'pi-refresh'"
                                ></i>
                                <span class="hidden sm:inline">Refresh</span>
                            </button>
                        </div>
                    </div>
                </header>

                <transition name="slide-fade">
                    <div
                        v-if="galat"
                        class="mb-5 rounded-2xl border border-red-200 bg-red-50 px-4 py-3.5 flex items-start gap-3 shadow-sm"
                    >
                        <div class="w-9 h-9 shrink-0 rounded-xl bg-red-100 text-red-600 flex items-center justify-center">
                            <i class="pi pi-exclamation-triangle text-sm"></i>
                        </div>

                        <div class="min-w-0 flex-1">
                            <p class="text-xs font-bold text-red-900">
                                Gagal memuat data
                            </p>

                            <p class="text-xs text-red-700 mt-0.5 leading-relaxed break-words">
                                {{ galat }}
                            </p>
                        </div>

                        <button
                            type="button"
                            @click="muatSemua"
                            class="shrink-0 text-xs font-bold text-red-700 hover:text-red-900 underline underline-offset-2"
                        >
                            Coba lagi
                        </button>
                    </div>
                </transition>

                <transition name="slide-fade">
                    <div
                        v-if="daftarPOKemasan.length > 0"
                        class="mb-5 relative overflow-hidden rounded-2xl border border-violet-200 bg-gradient-to-r from-violet-50 to-white shadow-sm"
                    >
                        <div class="absolute -right-5 -bottom-8 opacity-[0.06] pointer-events-none">
                            <i class="pi pi-shopping-bag" style="font-size: 9rem;"></i>
                        </div>

                        <div class="relative z-10 p-4 md:p-5">
                            <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                                <div class="flex items-start gap-3.5 min-w-0">
                                    <div class="w-11 h-11 md:w-12 md:h-12 shrink-0 rounded-xl bg-violet-600 text-white flex items-center justify-center shadow-md shadow-violet-200">
                                        <i class="pi pi-bell text-base"></i>
                                    </div>

                                    <div class="min-w-0">
                                        <div class="flex flex-wrap items-center gap-2">
                                            <h2 class="text-sm md:text-base font-bold text-violet-950">
                                                PO Kemasan Menunggu Penerimaan
                                            </h2>

                                            <span class="inline-flex items-center justify-center min-w-6 h-6 px-1.5 rounded-full bg-violet-600 text-white text-[10px] font-black">
                                                {{ daftarPOKemasan.length }}
                                            </span>
                                        </div>

                                        <p class="text-xs md:text-sm text-violet-700 mt-1 leading-relaxed max-w-3xl">
                                            Terdapat
                                            <strong>{{ daftarPOKemasan.length }}</strong>
                                            PO kemasan yang siap diproses sebagai penerimaan fisik gudang.
                                        </p>
                                    </div>
                                </div>

                                <button
                                    type="button"
                                    @click="bukaForm"
                                    class="w-full lg:w-auto h-10 px-5 rounded-xl bg-violet-600 hover:bg-violet-700 active:bg-violet-800 text-white text-xs font-bold transition-all shadow-md shadow-violet-200 hover:-translate-y-0.5 inline-flex items-center justify-center gap-2"
                                >
                                    Proses Penerimaan
                                    <i class="pi pi-arrow-right text-[10px]"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </transition>

                <div class="bg-white border border-slate-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden">

                    <div class="px-4 py-4 md:px-6 md:py-5 border-b border-slate-100">
                        <div class="flex flex-col xl:flex-row xl:items-center xl:justify-between gap-4">
                            <div>
                                <div class="flex items-center gap-2">
                                    <h2 class="text-sm md:text-base font-bold text-slate-900">
                                        Riwayat Penerimaan
                                    </h2>

                                    <span
                                        v-if="kataKunci"
                                        class="inline-flex items-center px-2 py-0.5 rounded-md bg-slate-100 text-slate-500 border border-slate-200 text-[10px] font-semibold"
                                    >
                                        Filter aktif
                                    </span>
                                </div>

                                <p class="text-xs text-slate-500 mt-1">
                                    {{ kataKunci
                                        ? `Hasil pencarian untuk "${kataKunci}"`
                                        : 'Daftar transaksi penerimaan kemasan yang telah dicatat.'
                                    }}
                                </p>
                            </div>

                            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 w-full xl:w-auto">
                                <div class="relative w-full sm:w-[280px] md:w-[320px]">
                                    <i class="pi pi-search absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs pointer-events-none"></i>

                                    <input
                                        v-model="kataKunci"
                                        type="text"
                                        autocomplete="off"
                                        spellcheck="false"
                                        placeholder="Cari No. penerimaan, PO, SJ..."
                                        @keyup.enter="cari"
                                        class="w-full h-10 pl-10 pr-10 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 placeholder:text-slate-400 focus:outline-none focus:bg-white focus:border-slate-400 focus:ring-4 focus:ring-slate-100 transition-all"
                                    />

                                    <button
                                        v-if="kataKunci"
                                        type="button"
                                        @click="bersihkanPencarian"
                                        aria-label="Bersihkan pencarian"
                                        class="absolute right-2 top-1/2 -translate-y-1/2 w-7 h-7 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 flex items-center justify-center transition-colors"
                                    >
                                        <i class="pi pi-times text-[10px]"></i>
                                    </button>
                                </div>

                                <button
                                    type="button"
                                    @click="cari"
                                    :disabled="sedangProses"
                                    class="h-10 px-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center justify-center gap-2"
                                >
                                    <i class="pi pi-search text-[10px]"></i>
                                    Cari
                                </button>
                            </div>
                        </div>
                    </div>

                    <div
                        v-if="sedangProses"
                        class="p-4 md:p-6"
                    >
                        <div class="flex flex-col items-center justify-center py-10">
                            <div class="w-12 h-12 rounded-2xl bg-slate-100 flex items-center justify-center mb-4">
                                <i class="pi pi-spin pi-spinner text-slate-500 text-lg"></i>
                            </div>

                            <h3 class="text-sm font-bold text-slate-800">
                                Memuat penerimaan kemasan
                            </h3>

                            <p class="text-xs text-slate-500 mt-1">
                                Mohon tunggu sebentar...
                            </p>
                        </div>

                        <div class="space-y-3 max-w-5xl mx-auto">
                            <div
                                v-for="n in 4"
                                :key="'skeleton-' + n"
                                class="h-16 rounded-xl bg-slate-50 border border-slate-100 animate-pulse"
                            ></div>
                        </div>
                    </div>

                    <div
                        v-else-if="daftarPenerimaan.length === 0"
                        class="px-4 py-14 md:py-20"
                    >
                        <div class="max-w-md mx-auto text-center">
                            <div class="relative mx-auto w-16 h-16 mb-5">
                                <div class="absolute inset-0 rounded-2xl bg-slate-100"></div>

                                <div class="relative w-16 h-16 rounded-2xl border border-slate-200 bg-white flex items-center justify-center">
                                    <i
                                        class="pi text-2xl text-slate-400"
                                        :class="kataKunci ? 'pi-search' : 'pi-inbox'"
                                    ></i>
                                </div>
                            </div>

                            <h3 class="text-base md:text-lg font-bold text-slate-900">
                                {{ kataKunci
                                    ? 'Data tidak ditemukan'
                                    : 'Belum ada penerimaan kemasan'
                                }}
                            </h3>

                            <p class="text-xs md:text-sm text-slate-500 mt-1.5 leading-relaxed">
                                {{ kataKunci
                                    ? 'Tidak ada transaksi yang sesuai dengan kata kunci pencarian.'
                                    : 'Belum terdapat transaksi penerimaan kemasan yang tercatat.'
                                }}
                            </p>

                            <div class="mt-5 flex flex-col sm:flex-row items-center justify-center gap-2">
                                <button
                                    v-if="kataKunci"
                                    type="button"
                                    @click="bersihkanPencarian"
                                    class="h-9 px-4 rounded-xl border border-slate-200 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 transition-colors"
                                >
                                    Hapus pencarian
                                </button>

                                <button
                                    v-else-if="daftarPOKemasan.length"
                                    type="button"
                                    @click="bukaForm"
                                    class="h-9 px-4 rounded-xl bg-violet-600 hover:bg-violet-700 text-white text-xs font-bold transition-colors inline-flex items-center gap-2"
                                >
                                    <i class="pi pi-plus text-[10px]"></i>
                                    Buat Penerimaan
                                </button>
                            </div>
                        </div>
                    </div>

                    <div
                        v-else
                        class="hidden lg:block overflow-x-auto custom-scrollbar"
                    >
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="bg-slate-50/80 border-b border-slate-100">
                                    <th class="px-6 py-3.5 text-[11px] font-bold text-slate-500 uppercase tracking-wider w-[19%]">
                                        Nomor & Tanggal
                                    </th>

                                    <th class="px-4 py-3.5 text-[11px] font-bold text-slate-500 uppercase tracking-wider w-[25%]">
                                        Supplier
                                    </th>

                                    <th class="px-4 py-3.5 text-[11px] font-bold text-slate-500 uppercase tracking-wider w-[19%]">
                                        Referensi PO
                                    </th>

                                    <th class="px-4 py-3.5 text-[11px] font-bold text-slate-500 uppercase tracking-wider w-[21%]">
                                        Surat Jalan
                                    </th>

                                    <th class="px-6 py-3.5 text-[11px] font-bold text-slate-500 uppercase tracking-wider text-right w-[16%]">
                                        Status
                                    </th>
                                </tr>
                            </thead>

                            <tbody class="divide-y divide-slate-100">
                                <tr
                                    v-for="p in daftarPenerimaan"
                                    :key="p.id"
                                    tabindex="0"
                                    role="button"
                                    @click="bukaDetail(p.id)"
                                    @keyup.enter="bukaDetail(p.id)"
                                    @keyup.space.prevent="bukaDetail(p.id)"
                                    class="group cursor-pointer hover:bg-slate-50/80 focus:bg-slate-50/80 focus:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-slate-400 transition-colors"
                                >
                                    <td class="px-6 py-4 align-middle">
                                        <div class="flex items-center gap-3">
                                            <div class="w-9 h-9 shrink-0 rounded-xl bg-slate-100 group-hover:bg-white border border-transparent group-hover:border-slate-200 text-slate-500 flex items-center justify-center transition-colors">
                                                <i class="pi pi-file text-xs"></i>
                                            </div>

                                            <div class="min-w-0">
                                                <p class="text-sm font-bold text-slate-800 truncate">
                                                    {{ p.nomor || '-' }}
                                                </p>

                                                <p class="text-[11px] text-slate-400 mt-1 flex items-center gap-1.5">
                                                    <i class="pi pi-calendar text-[9px]"></i>
                                                    {{ p.tanggal || '-' }}
                                                </p>
                                            </div>
                                        </div>
                                    </td>

                                    <td class="px-4 py-4 align-middle">
                                        <p
                                            class="text-sm font-semibold text-slate-700 truncate max-w-[260px]"
                                            :title="p.suplier_nama"
                                        >
                                            {{ p.suplier_nama || '-' }}
                                        </p>
                                    </td>

                                    <td class="px-4 py-4 align-middle">
                                        <span
                                            v-if="p.po_nomor"
                                            class="inline-flex px-2.5 py-1 rounded-lg bg-slate-50 border border-slate-200 text-[11px] font-semibold text-slate-600"
                                        >
                                            {{ p.po_nomor }}
                                        </span>

                                        <span
                                            v-else
                                            class="text-sm text-slate-400"
                                        >
                                            —
                                        </span>
                                    </td>

                                    <td class="px-4 py-4 align-middle">
                                        <div class="flex items-center gap-2">
                                            <i class="pi pi-truck text-slate-300 text-xs"></i>

                                            <span class="text-sm font-medium text-slate-600 break-all">
                                                {{ p.no_surat_jalan || '-' }}
                                            </span>
                                        </div>
                                    </td>

                                    <td class="px-6 py-4 align-middle">
                                        <div class="flex items-center justify-end gap-2">
                                            <span
                                                v-if="p.ada_selisih"
                                                class="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-rose-50 text-rose-700 border border-rose-200 text-[10px] font-bold uppercase tracking-wide"
                                            >
                                                <span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                                                Ada Selisih
                                            </span>

                                            <span
                                                v-else
                                                class="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold uppercase tracking-wide"
                                            >
                                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                                                Sesuai
                                            </span>

                                            <i class="pi pi-chevron-right text-[9px] text-slate-300 group-hover:text-slate-500 group-hover:translate-x-0.5 transition-all"></i>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div
                        v-if="!sedangProses && daftarPenerimaan.length > 0"
                        class="lg:hidden p-3 md:p-4 bg-slate-50/40 space-y-3"
                    >
                        <article
                            v-for="p in daftarPenerimaan"
                            :key="p.id"
                            tabindex="0"
                            role="button"
                            @click="bukaDetail(p.id)"
                            @keyup.enter="bukaDetail(p.id)"
                            @keyup.space.prevent="bukaDetail(p.id)"
                            class="group rounded-2xl border border-slate-200 bg-white p-4 shadow-sm hover:shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-400 transition-all cursor-pointer active:scale-[0.99]"
                        >
                            <div class="flex items-start justify-between gap-3 pb-3 border-b border-slate-100">
                                <div class="flex items-start gap-3 min-w-0">
                                    <div class="w-10 h-10 shrink-0 rounded-xl bg-slate-100 border border-slate-200 text-slate-500 flex items-center justify-center">
                                        <i class="pi pi-file text-xs"></i>
                                    </div>

                                    <div class="min-w-0">
                                        <p class="text-sm font-bold text-slate-900 truncate">
                                            {{ p.nomor || '-' }}
                                        </p>

                                        <p class="text-[11px] text-slate-400 mt-1 flex items-center gap-1.5">
                                            <i class="pi pi-calendar text-[9px]"></i>
                                            {{ p.tanggal || '-' }}
                                        </p>
                                    </div>
                                </div>

                                <span
                                    v-if="p.ada_selisih"
                                    class="shrink-0 inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-rose-50 text-rose-700 border border-rose-200 text-[9px] font-bold uppercase"
                                >
                                    <span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                                    Selisih
                                </span>

                                <span
                                    v-else
                                    class="shrink-0 inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200 text-[9px] font-bold uppercase"
                                >
                                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                                    Sesuai
                                </span>
                            </div>

                            <div class="pt-3 space-y-2.5">
                                <div class="flex items-start justify-between gap-4">
                                    <span class="text-[11px] font-semibold text-slate-400 shrink-0">
                                        Supplier
                                    </span>

                                    <span
                                        class="text-xs font-semibold text-slate-700 text-right break-words"
                                        :title="p.suplier_nama"
                                    >
                                        {{ p.suplier_nama || '-' }}
                                    </span>
                                </div>

                                <div class="flex items-start justify-between gap-4">
                                    <span class="text-[11px] font-semibold text-slate-400 shrink-0">
                                        No. PO
                                    </span>

                                    <span class="text-xs font-medium text-slate-600 text-right break-all">
                                        {{ p.po_nomor || '-' }}
                                    </span>
                                </div>

                                <div class="flex items-start justify-between gap-4">
                                    <span class="text-[11px] font-semibold text-slate-400 shrink-0">
                                        Surat Jalan
                                    </span>

                                    <span class="text-xs font-medium text-slate-600 text-right break-all">
                                        {{ p.no_surat_jalan || '-' }}
                                    </span>
                                </div>
                            </div>

                            <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between">
                                <span class="text-[10px] text-slate-400">
                                    Buka detail penerimaan
                                </span>

                                <span class="w-7 h-7 rounded-lg bg-slate-50 group-hover:bg-slate-100 text-slate-400 group-hover:text-slate-700 flex items-center justify-center transition-colors">
                                    <i class="pi pi-chevron-right text-[9px]"></i>
                                </span>
                            </div>
                        </article>
                    </div>

                    <div
                        v-if="!sedangProses && daftarPenerimaan.length > 0"
                        class="px-4 py-3.5 md:px-6 border-t border-slate-100 bg-white flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2"
                    >
                        <p class="text-[11px] text-slate-400">
                            Menampilkan
                            <span class="font-bold text-slate-600">
                                {{ daftarPenerimaan.length }}
                            </span>
                            transaksi penerimaan kemasan
                        </p>

                        <p class="text-[11px] text-slate-400">
                            Klik baris untuk melihat detail
                        </p>
                    </div>
                </div>
            </section>
        </transition>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePackageReceipt } from '../composables/usePackageReceipt'
import PackageReceiptForm from './PackageReceiptForm.vue'

const router = useRouter()

const {
    daftarPenerimaan,
    daftarPOKemasan,
    sedangProses,
    galat,
    muatPenerimaan,
    muatPOKemasan,
} = usePackageReceipt()

const modeForm = ref(false)
const kataKunci = ref('')

const cari = async () => {
    await muatPenerimaan({
        search: kataKunci.value.trim(),
    })
}

const bersihkanPencarian = async () => {
    kataKunci.value = ''
    await muatPenerimaan()
}

const bukaForm = () => {
    modeForm.value = true
}

const bukaDetail = (id) => {
    if (!id) return

    router.push(`/warehouse/input/package-receipt/${id}`)
}

const tutupForm = async () => {
    modeForm.value = false

    await Promise.all([
        muatPenerimaan(
            kataKunci.value.trim()
                ? { search: kataKunci.value.trim() }
                : {}
        ),
        muatPOKemasan(),
    ])
}

const muatSemua = async () => {
    await Promise.all([
        muatPenerimaan(
            kataKunci.value.trim()
                ? { search: kataKunci.value.trim() }
                : {}
        ),
        muatPOKemasan(),
    ])
}

onMounted(() => {
    muatSemua()
})
</script>

<style scoped>
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

.page-fade-enter-active,
.page-fade-leave-active {
    transition:
        opacity 0.22s ease,
        transform 0.22s ease;
}

.page-fade-enter-from {
    opacity: 0;
    transform: translateX(8px);
}

.page-fade-leave-to {
    opacity: 0;
    transform: translateX(-8px);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
    transition:
        opacity 0.2s ease,
        transform 0.2s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
    opacity: 0;
    transform: translateY(-6px);
}

.custom-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 transparent;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
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

button:focus-visible,
input:focus-visible,
[role="button"]:focus-visible {
    outline: 2px solid #64748b;
    outline-offset: 2px;
}
</style>