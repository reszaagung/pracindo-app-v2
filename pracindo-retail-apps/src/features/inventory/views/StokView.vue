<template>
    <div class="max-w-7xl mx-auto pb-10 space-y-6 font-sans">

        <!-- Header Halaman -->
        <header
            class="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-slate-200 pb-4">
            <div>
                <p class="text-sm text-slate-500 mb-1">Logistik / Inventory</p>
                <h1 class="text-2xl font-bold text-slate-800">Manajemen Stok Cabang</h1>
            </div>
            <div class="flex items-center gap-3 w-full md:w-auto">
                <div class="relative w-full md:w-64">
                    <i class="pi pi-search absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400"></i>
                    <input v-model="searchQuery" type="text" placeholder="Cari kode atau nama barang..."
                        class="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-xl text-sm outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-shadow bg-white">
                </div>
                <button @click="fetchStok"
                    class="bg-white border border-slate-200 text-slate-600 w-10 h-10 rounded-xl flex items-center justify-center hover:bg-slate-50 transition-colors shadow-sm shrink-0">
                    <i :class="isLoading ? 'pi pi-spin pi-spinner' : 'pi pi-refresh'"></i>
                </button>
            </div>
        </header>

        <!-- Tabel Data Stok -->
        <div
            class="bg-white rounded-[20px] shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 overflow-hidden flex flex-col h-[calc(100vh-200px)]">

            <!-- Ringkasan Cepat -->
            <div class="p-4 bg-slate-50/50 border-b border-slate-100 flex gap-6">
                <div class="flex items-center gap-2">
                    <div class="w-3 h-3 rounded-full bg-emerald-500"></div>
                    <span class="text-xs font-semibold text-slate-600">Stok Aman</span>
                </div>
                <div class="flex items-center gap-2">
                    <div class="w-3 h-3 rounded-full bg-orange-500"></div>
                    <span class="text-xs font-semibold text-slate-600">Menipis (≤ 5)</span>
                </div>
                <div class="flex items-center gap-2">
                    <div class="w-3 h-3 rounded-full bg-rose-500"></div>
                    <span class="text-xs font-semibold text-slate-600">Habis (0)</span>
                </div>
            </div>

            <!-- Area Tabel (Scrollable) -->
            <div class="flex-1 overflow-y-auto custom-scrollbar relative">

                <!-- Loading State -->
                <div v-if="isLoading && stokList.length === 0"
                    class="absolute inset-0 bg-white/80 backdrop-blur-sm flex flex-col items-center justify-center z-10">
                    <i class="pi pi-spin pi-spinner text-4xl text-blue-500 mb-3"></i>
                    <p class="text-sm font-semibold text-slate-600">Memuat data stok...</p>
                </div>

                <table class="min-w-full text-left border-collapse">
                    <thead class="bg-white sticky top-0 shadow-sm z-10 border-b border-slate-200">
                        <tr>
                            <th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider w-32">Kode
                                SKU</th>
                            <th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Nama Produk
                            </th>
                            <th class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider w-40">
                                Kategori</th>
                            <th
                                class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider w-32 text-center">
                                Satuan</th>
                            <th
                                class="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider w-32 text-right">
                                Stok Fisik</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 bg-white">

                        <!-- State Kosong / Tidak Ketemu -->
                        <tr v-if="filteredStok.length === 0 && !isLoading">
                            <td colspan="5" class="px-6 py-12 text-center text-slate-400">
                                <i class="pi pi-box text-4xl mb-3 text-slate-300"></i>
                                <p>Tidak ada data stok yang ditemukan.</p>
                            </td>
                        </tr>

                        <!-- Looping Data Stok -->
                        <tr v-for="item in filteredStok" :key="item.id" class="hover:bg-slate-50 transition-colors">
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-slate-700">
                                {{ item.kode_produk }}
                            </td>
                            <td class="px-6 py-4 text-sm font-semibold text-slate-800">
                                {{ item.nama_produk }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                                {{ item.kategori || 'Umum' }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500 text-center">
                                <span class="bg-slate-100 px-2 py-1 rounded-md">{{ item.satuan || 'Pcs' }}</span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-right">
                                <!-- Logika Warna Indikator Stok -->
                                <div class="inline-flex items-center justify-center px-3 py-1 rounded-lg text-sm font-black min-w-[3rem]"
                                    :class="[
                                        item.qty <= 0 ? 'bg-rose-100 text-rose-700 border border-rose-200' :
                                            item.qty <= 5 ? 'bg-orange-100 text-orange-700 border border-orange-200' :
                                                'bg-emerald-50 text-emerald-700 border border-emerald-100'
                                    ]">
                                    {{ item.qty }}
                                </div>
                            </td>
                        </tr>

                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStok } from '../composables/useStok'

const { stokList, isLoading, fetchStok } = useStok()
const searchQuery = ref('')

onMounted(() => {
    fetchStok()
})

// Fitur Pencarian Real-time (Filter di sisi Client agar cepat)
const filteredStok = computed(() => {
    if (!searchQuery.value) return stokList.value

    const keyword = searchQuery.value.toLowerCase()
    return stokList.value.filter(item =>
        (item.nama_produk && item.nama_produk.toLowerCase().includes(keyword)) ||
        (item.kode_produk && item.kode_produk.toLowerCase().includes(keyword))
    )
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 999px;
}
</style>