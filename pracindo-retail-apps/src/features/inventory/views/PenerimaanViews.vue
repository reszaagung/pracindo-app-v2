<template>
    <div class="max-w-7xl mx-auto pb-10 space-y-6 font-sans mt-4">
        <!-- Header Halaman -->
        <header class="flex flex-col gap-4 border-b border-slate-200 pb-4">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div class="flex items-center gap-4">
                    <button @click="$router.push('/dashboard')" class="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-white px-3 py-2 rounded-lg text-sm font-bold transition-colors">
                        <i class="pi pi-arrow-left"></i> Dashboard
                    </button>
                    <div>
                        <p class="text-sm text-slate-500 mb-1">Logistik / Inventory</p>
                        <h1 class="text-2xl font-bold text-slate-800">Penerimaan Surat Jalan (DO)</h1>
                    </div>
                </div>

                <div class="bg-slate-100 p-1 rounded-xl flex gap-1">
                    <button @click="$router.push('/stok')" class="text-slate-500 hover:text-slate-700 font-medium px-4 py-2 rounded-lg text-sm transition-all flex items-center gap-2">
                        <i class="pi pi-box"></i> Stok
                    </button>
                    <button class="bg-white text-blue-600 shadow-sm font-bold px-4 py-2 rounded-lg text-sm transition-all flex items-center gap-2">
                        <i class="pi pi-truck"></i> Terima Barang
                    </button>
                </div>
            </div>

            <div class="self-end mt-2">
                <button @click="fetchDO"
                    class="bg-white border border-slate-200 text-slate-600 px-4 py-2 rounded-xl text-sm font-bold hover:bg-slate-50 transition-colors shadow-sm flex items-center gap-2">
                    <i :class="isLoading ? 'pi pi-spin pi-spinner' : 'pi pi-refresh'"></i> Refresh Data
                </button>
            </div>
        </header>

        <div class="flex flex-col lg:flex-row gap-6">
            <!-- KIRI: Daftar Surat Jalan (DO) dari Gudang -->
            <div class="w-full lg:w-1/3 bg-white rounded-[20px] shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col h-[calc(100vh-270px)] overflow-hidden">
                <div class="p-4 md:p-5 border-b border-slate-100 bg-slate-50/50">
                    <h2 class="font-bold text-slate-700">Daftar Kiriman (Pending)</h2>
                </div>
                <div class="flex-1 overflow-y-auto p-4 custom-scrollbar space-y-3">
                    <div v-if="doList.length === 0 && !isLoading"
                        class="flex flex-col items-center justify-center h-full text-slate-400 opacity-70">
                        <i class="pi pi-inbox text-5xl mb-3"></i>
                        <p class="text-sm font-medium">Tidak ada kiriman baru.</p>
                    </div>

                    <button v-for="kiriman in doList" :key="kiriman.id" @click="pilihDO(kiriman)"
                        :class="selectedDO?.id === kiriman.id ? 'border-emerald-500 bg-emerald-50' : 'border-slate-200 bg-white hover:border-emerald-300'"
                        class="w-full text-left p-4 rounded-xl shadow-sm border transition-all group flex flex-col gap-2">
                        <div class="flex justify-between items-start">
                            <span class="font-bold text-slate-800">{{ kiriman.nomor_penerimaan }}</span>
                            <span class="text-[10px] font-bold bg-orange-100 text-orange-600 px-2 py-1 rounded-md uppercase">{{ kiriman.status }}</span>
                        </div>
                        <div class="text-xs text-slate-500 font-medium flex items-center gap-1">
                            <i class="pi pi-calendar"></i> {{ kiriman.tanggal_kirim }}
                        </div>
                        <div class="text-xs font-semibold text-slate-600 bg-slate-100 px-2 py-1.5 rounded-lg inline-block w-fit mt-1">
                            Surat Jalan: {{ kiriman.referensi_logistik }}
                        </div>
                    </button>
                </div>
            </div>

            <!-- KANAN: Detail & Checklist Penerimaan -->
            <div class="w-full lg:w-2/3 bg-white rounded-[20px] shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col h-[calc(100vh-270px)] overflow-hidden">
                <div v-if="!selectedDO" class="flex flex-col items-center justify-center h-full text-slate-400">
                    <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-4">
                        <i class="pi pi-list-check text-3xl"></i>
                    </div>
                    <h3 class="font-bold text-slate-600 mb-1">Pilih Surat Jalan</h3>
                    <p class="text-sm">Klik salah satu kiriman di sebelah kiri untuk mulai pengecekan fisik.</p>
                </div>

                <template v-else>
                    <div class="p-4 md:p-5 border-b border-slate-100 bg-emerald-50/50 flex justify-between items-center">
                        <div>
                            <p class="text-xs font-bold text-emerald-600 mb-1">Pengecekan Fisik</p>
                            <h2 class="font-bold text-slate-800 text-lg">{{ selectedDO.nomor_penerimaan }}</h2>
                        </div>
                        <div class="text-right text-sm">
                            <span class="text-slate-500">Total Item: </span>
                            <span class="font-bold text-slate-800">{{ checklistItems.length }}</span>
                        </div>
                    </div>

                    <div class="flex-1 overflow-y-auto p-4 md:p-5 custom-scrollbar">
                        <table class="min-w-full">
                            <thead class="bg-slate-50 border-b border-slate-200">
                                <tr>
                                    <th class="px-4 py-3 text-left text-xs font-bold text-slate-500 uppercase">Nama Produk</th>
                                    <th class="px-4 py-3 text-center text-xs font-bold text-slate-500 uppercase">Dikirim (Qty)</th>
                                    <th class="px-4 py-3 text-center text-xs font-bold text-emerald-600 uppercase">Diterima Fisik</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                <tr v-for="item in checklistItems" :key="item.id" class="hover:bg-slate-50/50">
                                    <td class="px-4 py-4 text-sm font-bold text-slate-700">
                                        {{ item.nama_produk }}
                                        <p class="text-xs text-slate-400 font-normal mt-0.5">{{ item.kemasan }}</p>
                                    </td>
                                    <td class="px-4 py-4 text-sm font-bold text-slate-500 text-center bg-slate-50/50">
                                        {{ item.qty_kirim }}
                                    </td>
                                    <td class="px-4 py-4 text-center">
                                        <input type="number" v-model.number="item.qty_terima" min="0"
                                            class="w-20 text-center border-2 rounded-lg px-2 py-2 outline-none font-bold text-emerald-700 transition-colors"
                                            :class="item.qty_terima === item.qty_kirim ? 'border-emerald-200 bg-emerald-50 focus:border-emerald-400' : 'border-orange-300 bg-orange-50 focus:border-orange-500'" />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="p-4 md:p-5 bg-slate-50/80 border-t border-slate-100">
                        <div v-if="adaSelisih"
                            class="mb-4 p-3 bg-orange-50 border border-orange-200 rounded-xl flex items-start gap-3 text-sm text-orange-800">
                            <i class="pi pi-exclamation-triangle mt-0.5 text-orange-500"></i>
                            <p><strong>Perhatian:</strong> Ada selisih antara jumlah barang yang dikirim dengan yang Anda terima. Sistem akan mencatat ini sebagai <em>Retur/Selisih</em>.</p>
                        </div>
                        <button @click="submitPenerimaan"
                            :disabled="isLoading || selectedDO?.status === 'SELESAI'"
                            class="w-full bg-emerald-600 text-white font-bold py-4 rounded-xl hover:bg-emerald-700 transition-all shadow-md disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2">
                            <i v-if="isLoading" class="pi pi-spin pi-spinner"></i>
                            <i v-else class="pi pi-check-circle"></i>
                            {{ selectedDO?.status === 'SELESAI' ? 'Sudah Diterima' : (isLoading ? 'Memproses...' : 'KONFIRMASI BARANG DITERIMA') }}
                        </button>
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { usePenerimaan } from '../composables/usePenerimaanBarang'
const errorPesan = ref('')
const { doList, isLoading, fetchDO, prosesPenerimaan } = usePenerimaan()

const selectedDO = ref(null)
const checklistItems = ref([])

onMounted(() => {
    fetchDO()
})

const pilihDO = (kiriman) => {
    selectedDO.value = kiriman
    checklistItems.value = (kiriman.items || []).map(item => ({
        id: item.id,
        kode_produk: item.produk,
        nama_produk: item.produk_nama,
        kemasan: item.kemasan,
        qty_kirim: item.unit_dikirim,
        qty_terima: item.unit_dikirim,
    }))
}

const adaSelisih = computed(() => {
    return checklistItems.value.some(item => item.qty_terima !== item.qty_kirim)
})

const submitPenerimaan = async () => {
    if (!selectedDO.value) return

    const payloadItems = checklistItems.value.map(item => ({
        id: item.id,
        unit_diterima: item.qty_terima
    }))
    const result = await prosesPenerimaan(selectedDO.value.id, payloadItems)

    if (result.status === 'sukses') {
        selectedDO.value = null
        fetchDO()
    } else {
        // pakai state di halaman, bukan alert() yang bisa diblokir browser
        errorPesan.value = result.pesan || 'Gagal memproses penerimaan.'
    }
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 999px;
}
</style>