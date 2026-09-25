<template>
    <div class="min-h-screen bg-slate-100 text-slate-800 font-sans">
        <div class="w-full max-w-[1700px] mx-auto p-4 lg:p-6">

            <header class="mb-5">
                <div class="bg-white border border-slate-200 shadow-sm">
                    <div class="px-5 py-4">
                        <div class="flex flex-col xl:flex-row xl:items-center xl:justify-between gap-4">

                            <div class="flex items-center gap-4">
                                <button
                                    type="button"
                                    @click="router.push('/dashboard')"
                                    class="h-10 px-4 bg-slate-900 text-white flex items-center gap-2 text-sm font-semibold hover:bg-slate-800 transition"
                                >
                                    <i class="pi pi-arrow-left text-xs"></i>
                                    Dashboard
                                </button>

                                <div class="hidden sm:block h-8 w-px bg-slate-200"></div>

                                <div>
                                    <div class="flex items-center gap-2">
                                        <span class="w-2 h-2 rounded-full bg-blue-600"></span>

                                        <span
                                            class="text-[10px] uppercase tracking-[0.2em] font-black text-slate-400"
                                        >
                                            Logistik / Inventory
                                        </span>
                                    </div>

                                    <h1 class="text-xl lg:text-2xl font-black tracking-tight text-slate-900 mt-1">
                                        Manajemen Stok
                                    </h1>
                                </div>
                            </div>

                            <div class="grid grid-cols-2 border-b-2 border-slate-200 w-full xl:w-auto">
                                <button
                                    type="button"
                                    class="px-5 py-2.5 -mb-[2px] border-b-2 border-blue-600 text-xs font-black text-blue-600 flex items-center justify-center gap-2"
                                >
                                    <i class="pi pi-box text-[10px]"></i>
                                    Stok
                                </button>

                                <button
                                    type="button"
                                    @click="router.push('/stok/penerimaan')"
                                    class="px-5 py-2.5 text-xs font-black text-slate-400 hover:text-slate-700 transition flex items-center justify-center gap-2"
                                >
                                    <i class="pi pi-truck text-[10px]"></i>
                                    Terima Barang
                                </button>
                            </div>
                        </div>

                        <div class="mt-5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">

                            <div class="flex flex-wrap items-center gap-4">
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 bg-emerald-500"></span>
                                    <span class="text-[11px] font-semibold text-slate-500">
                                        Stok Aman
                                    </span>
                                </div>

                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 bg-orange-500"></span>
                                    <span class="text-[11px] font-semibold text-slate-500">
                                        Menipis ≤ 5
                                    </span>
                                </div>

                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 bg-rose-500"></span>
                                    <span class="text-[11px] font-semibold text-slate-500">
                                        Habis
                                    </span>
                                </div>
                            </div>

                            <div class="flex items-center gap-5">
                                <div class="relative w-full md:w-[320px]">
                                    <i
                                        class="pi pi-search absolute left-0 top-1/2 -translate-y-1/2 text-slate-400 text-sm"
                                    ></i>

                                    <input
                                        v-model="searchQuery"
                                        type="text"
                                        placeholder="Cari kode, nama, atau pemilik..."
                                        class="w-full pl-7 pr-8 py-2.5 bg-transparent border-0 border-b-2 border-slate-200 focus:border-blue-600 focus:ring-0 outline-none text-sm font-medium placeholder:text-slate-400 transition"
                                    />

                                    <button
                                        v-if="searchQuery"
                                        type="button"
                                        @click="searchQuery = ''"
                                        class="absolute right-0 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700 transition"
                                    >
                                        <i class="pi pi-times text-xs"></i>
                                    </button>
                                </div>

                                <button
                                    type="button"
                                    @click="refreshData"
                                    :disabled="isLoading"
                                    class="w-10 h-10 shrink-0 border border-slate-200 bg-white text-slate-500 flex items-center justify-center hover:border-blue-400 hover:text-blue-600 transition disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    <i
                                        :class="isLoading ? 'pi pi-spin pi-spinner' : 'pi pi-refresh'"
                                    ></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <section class="bg-white border border-slate-200 shadow-sm flex flex-col xl:h-[calc(100vh-235px)]">

                <div class="px-5 py-4 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                    <div>
                        <p class="text-[10px] uppercase tracking-[0.18em] font-black text-slate-400">
                            Inventory Overview
                        </p>

                        <h2 class="text-lg font-black text-slate-900 mt-1">
                            Daftar Stok Barang
                        </h2>
                    </div>

                    <div class="flex items-center gap-5">
                        <div>
                            <p class="text-[10px] uppercase tracking-wider font-bold text-slate-400">
                                Total Data
                            </p>

                            <p class="text-lg font-black text-slate-900">
                                {{ filteredStok.length }}
                            </p>
                        </div>

                        <div class="h-8 w-px bg-slate-200"></div>

                        <div>
                            <p class="text-[10px] uppercase tracking-wider font-bold text-slate-400">
                                Hasil Filter
                            </p>

                            <p class="text-lg font-black text-blue-600">
                                {{ filteredStok.length }}
                            </p>
                        </div>
                    </div>
                </div>

                <div class="flex-1 overflow-y-auto overflow-x-auto custom-scrollbar relative">

                    <div
                        v-if="isLoading && stokList.length === 0"
                        class="absolute inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center z-20"
                    >
                        <div class="text-center">
                            <i class="pi pi-spin pi-spinner text-2xl text-blue-600"></i>

                            <p class="mt-3 text-sm font-semibold text-slate-500">
                                Memuat data stok...
                            </p>
                        </div>
                    </div>

                    <table class="w-full min-w-[1000px] text-left border-collapse">
                        <thead class="sticky top-0 z-10 bg-white border-b border-slate-200">
                            <tr>
                                <th class="px-5 py-4 text-[10px] uppercase tracking-wider font-black text-slate-400 w-32">
                                    Pemilik
                                </th>

                                <th class="px-5 py-4 text-[10px] uppercase tracking-wider font-black text-slate-400 w-36">
                                    Kode SKU
                                </th>

                                <th class="px-5 py-4 text-[10px] uppercase tracking-wider font-black text-slate-400">
                                    Nama Produk
                                </th>

                                <th class="px-5 py-4 text-[10px] uppercase tracking-wider font-black text-slate-400 w-40">
                                    Kategori
                                </th>

                                <th class="px-5 py-4 text-[10px] uppercase tracking-wider font-black text-slate-400 w-32 text-center">
                                    Satuan
                                </th>

                                <th class="px-5 py-4 text-[10px] uppercase tracking-wider font-black text-slate-400 w-36 text-right">
                                    Stok Fisik
                                </th>
                            </tr>
                        </thead>

                        <tbody class="divide-y divide-slate-100">

                            <tr
                                v-if="filteredStok.length === 0 && !isLoading"
                            >
                                <td colspan="6" class="px-6 py-16 text-center">
                                    <div class="max-w-sm mx-auto">
                                        <div
                                            class="w-16 h-16 mx-auto mb-4 border border-dashed border-slate-300 flex items-center justify-center"
                                        >
                                            <i class="pi pi-box text-xl text-slate-300"></i>
                                        </div>

                                        <p class="text-sm font-bold text-slate-600">
                                            Data stok tidak ditemukan
                                        </p>

                                        <p class="text-xs text-slate-400 mt-1">
                                            Coba ubah kata pencarian.
                                        </p>
                                    </div>
                                </td>
                            </tr>

                            <tr
                                v-for="item in filteredStok"
                                :key="item.id"
                                class="hover:bg-slate-50 transition"
                            >
                                <td class="px-5 py-4">
                                    <span
                                        v-if="item?.grup_kode"
                                        :class="
                                            item?.grup_kode === 'PT'
                                                ? 'bg-amber-50 text-amber-700 border-amber-200'
                                                : 'bg-sky-50 text-sky-700 border-sky-200'
                                        "
                                        class="inline-flex px-2 py-1 text-[10px] font-black border"
                                    >
                                        {{ item.entitas_kode }}
                                    </span>

                                    <span
                                        v-else
                                        class="text-xs text-slate-300"
                                    >
                                        —
                                    </span>
                                </td>

                                <td class="px-5 py-4">
                                    <span class="text-xs font-mono font-black text-slate-600">
                                        {{ item.kode_produk }}
                                    </span>
                                </td>

                                <td class="px-5 py-4">
                                    <div>
                                        <p class="text-sm font-bold text-slate-800">
                                            {{ item.nama_produk }}
                                        </p>

                                        <p
                                            v-if="item.kode_produk"
                                            class="text-[10px] text-slate-400 mt-1"
                                        >
                                            SKU {{ item.kode_produk }}
                                        </p>
                                    </div>
                                </td>

                                <td class="px-5 py-4">
                                    <span class="text-sm text-slate-500">
                                        {{ item.kategori || 'Umum' }}
                                    </span>
                                </td>

                                <td class="px-5 py-4 text-center">
                                    <span
                                        class="text-xs font-bold text-slate-500"
                                    >
                                        {{ item.satuan || 'Pcs' }}
                                    </span>
                                </td>

                                <td class="px-5 py-4 text-right">
                                    <div class="flex items-center justify-end gap-3">
                                        <span
                                            class="w-2 h-2"
                                            :class="
                                                item.qty <= 0
                                                    ? 'bg-rose-500'
                                                    : item.qty <= 5
                                                        ? 'bg-orange-500'
                                                        : 'bg-emerald-500'
                                            "
                                        ></span>

                                        <span
                                            class="min-w-16 text-right text-sm font-black"
                                            :class="
                                                item.qty <= 0
                                                    ? 'text-rose-600'
                                                    : item.qty <= 5
                                                        ? 'text-orange-600'
                                                        : 'text-emerald-600'
                                            "
                                        >
                                            {{ item.qty ?? 0 }}
                                        </span>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div
                    class="px-5 py-3 border-t border-slate-200 bg-slate-50 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2"
                >
                    <p class="text-xs text-slate-400">
                        Menampilkan {{ filteredStok.length }} data stok
                    </p>

                    <p class="text-[10px] uppercase tracking-wider font-bold text-slate-400">
                        Inventory Management
                    </p>
                </div>
            </section>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStok } from '../composables/useStock'

const router = useRouter()

const {
    stokList,
    isLoading,
    fetchStok
} = useStok()

const searchQuery = ref('')

onMounted(() => {
    fetchStok()
})

const filteredStok = computed(() => {
    const data = Array.isArray(stokList.value)
        ? stokList.value
        : []

    const query = searchQuery.value.trim().toLowerCase()

    if (!query) {
        return data
    }

    return data.filter(item =>
        item.nama_produk?.toLowerCase().includes(query) ||
        item.kode_produk?.toLowerCase().includes(query) ||
        item.entitas_kode?.toLowerCase().includes(query) ||
        item.kategori?.toLowerCase().includes(query)
    )
})

const refreshData = async () => {
    await fetchStok()
}
</script>

<style scoped>
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
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}
</style>
