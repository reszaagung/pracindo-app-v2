<template>
    <div class="flex flex-col w-full animate-fade-in relative">
        <!-- Header Halaman -->
        <div class="mb-6 flex justify-between items-end">
            <div>
                <p class="text-xs text-slate-400 mb-1">
                    <span class="hover:text-slate-700 transition-colors cursor-pointer">Helper</span>
                    <span class="mx-1">/</span>
                    <span class="text-slate-600 font-semibold">Generate Stiker</span>
                </p>
                <h1 class="text-xl md:text-2xl font-bold text-slate-800 tracking-tight">Cetak Stiker Logistik</h1>
                <p class="text-xs md:text-sm text-slate-500 mt-1">
                    Otomatisasi pembuatan dokumen Word (.docx) berdasarkan kuantitas dan antrean stiker.
                </p>
            </div>
        </div>

        <!-- Notifikasi Error -->
        <div v-if="galat" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600 font-medium flex items-start gap-3 shadow-sm">
            <i class="pi pi-exclamation-triangle mt-0.5"></i>
            <span>{{ galat }}</span>
        </div>

        <!-- Banner Sukses & Tombol Unduh -->
        <div v-if="hasilCetak" class="mb-6 p-6 bg-emerald-50 border border-emerald-200 rounded-[24px] flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow-sm animate-fade-in">
            <div>
                <h3 class="text-sm font-bold text-emerald-900 mb-1 flex items-center gap-2">
                    <i class="pi pi-check-circle text-emerald-600"></i> Dokumen Berhasil Dibuat
                </h3>
                <p class="text-xs text-emerald-700 m-0">
                    Sistem mendeteksi <strong>{{ hasilCetak.total_unit }} item</strong> dan otomatis menggunakan pola <strong>{{ hasilCetak.pola_terdeteksi }}</strong>.
                </p>
            </div>
            <a :href="hasilCetak.file_hasil" target="_blank" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl transition-colors shadow-md flex items-center gap-2 whitespace-nowrap">
                <i class="pi pi-download text-xs"></i>
                <span>Unduh File .DOCX</span>
            </a>
        </div>

        <!-- Kartu Form Input -->
        <div class="bg-white border border-slate-200 rounded-[24px] p-4 md:p-6 shadow-sm w-full mb-6">
            <div class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 mb-6 pb-4 border-b border-slate-100">
                <div>
                    <h3 class="text-sm font-bold text-slate-800 flex items-center gap-2">
                        <i class="pi pi-box text-blue-600"></i> Data Item Stiker
                    </h3>
                    <p class="text-xs text-slate-500 mt-1">Tambahkan maksimal 4 item untuk didistribusikan ke dalam satu lembar cetak.</p>
                </div>
                
                <!-- Pilihan Template -->
                <div class="flex w-full xl:w-auto flex-col">
                    <label class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Jenis Template</label>
                    <select v-model="payload.jenis" class="text-sm border border-slate-300 rounded-lg px-4 py-2 bg-slate-50 text-slate-800 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all font-medium appearance-none cursor-pointer">
                        <option value="polos_besar">Polos Besar</option>
                        <option value="cv_besar">CV Besar</option>
                    </select>
                </div>
            </div>

            <!-- Grid Slot Input -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
                <div v-for="(item, index) in payload.items" :key="index" class="p-5 bg-slate-50/50 border border-slate-200 rounded-[16px] hover:border-slate-300 transition-colors relative">
                    <div class="flex justify-between items-center mb-4 border-b border-slate-100 pb-3">
                        <span class="text-[11px] font-bold text-slate-600 bg-white border border-slate-200 px-2.5 py-1 rounded-md shadow-sm uppercase tracking-wider flex items-center gap-2">
                            <i class="pi pi-tag text-[10px] text-blue-500"></i>
                            Slot {{ index + 1 }}
                        </span>
                        <button v-if="payload.items.length > 1" @click="hapusItem(index)" class="w-7 h-7 flex items-center justify-center rounded-lg bg-white border border-rose-100 text-rose-500 hover:bg-rose-500 hover:text-white hover:border-rose-500 transition-colors shadow-sm" title="Hapus Slot">
                            <i class="pi pi-trash text-[11px]"></i>
                        </button>
                    </div>
                    
                    <div class="flex flex-col gap-4">
                        <div>
                            <label class="text-[11px] font-semibold text-slate-500 mb-1.5 block">Nama Barang</label>
                            <input v-model="item.nama_item" type="text" class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 bg-white text-slate-800 focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50 transition-all shadow-sm" placeholder="Contoh: SUPER WHITE SC SC">
                        </div>
                        <div>
                            <label class="text-[11px] font-semibold text-slate-500 mb-1.5 block">Tipe / Kemasan</label>
                            <input v-model="item.tipe" type="text" class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 bg-white text-slate-800 focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50 transition-all shadow-sm" placeholder="Contoh: Pack / Roll">
                        </div>
                        <div class="flex gap-3">
                            <div class="flex-1">
                                <label class="text-[11px] font-semibold text-slate-500 mb-1.5 block">Tanggal Lot</label>
                                <input v-model="item.lot" type="date" class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 bg-white text-slate-800 focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50 transition-all shadow-sm">
                            </div>
                            <div class="flex-1">
                                <label class="text-[11px] font-semibold text-slate-500 mb-1.5 block">Net (KGS)</label>
                                <input v-model="item.net" type="number" step="0.01" class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 bg-white text-slate-800 focus:outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-50 transition-all shadow-sm" placeholder="0.00">
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Tombol Tambah Slot (Hanya muncul jika item < 4) -->
                <button v-if="payload.items.length < 4" @click="tambahItem" class="p-5 border-2 border-dashed border-slate-200 rounded-[16px] flex flex-col items-center justify-center text-slate-400 hover:bg-blue-50 hover:text-blue-600 hover:border-blue-300 transition-all min-h-[280px]">
                    <div class="w-10 h-10 bg-white border border-slate-100 rounded-full flex items-center justify-center mb-3 shadow-sm">
                        <i class="pi pi-plus text-lg"></i>
                    </div>
                    <span class="text-sm font-bold">Tambah Slot Baru</span>
                    <span class="text-[11px] mt-1 font-medium">Sisa {{ 4 - payload.items.length }} slot tersedia</span>
                </button>
            </div>

            <!-- Tombol Submit Utama -->
            <div class="mt-8 flex justify-end border-t border-slate-100 pt-5">
                <button @click="kirimData" :disabled="sedangProses || payload.items.length === 0" class="px-8 py-3 bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 disabled:cursor-not-allowed text-white text-sm font-bold rounded-xl transition-all shadow-md hover:shadow-lg flex items-center gap-3">
                    <i class="pi" :class="sedangProses ? 'pi-spin pi-spinner' : 'pi-cog'"></i>
                    <span>{{ sedangProses ? 'Menyiapkan Dokumen...' : 'Proses & Generate' }}</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useSticker } from '../composables/useSticker'

const { sedangProses, galat, hasilCetak, buatDanCetakStiker } = useSticker()

const payload = ref({
    jenis: 'polos_besar',
    items: [
        { nama_item: '', tipe: '', lot: '', net: null }
    ]
})

const tambahItem = () => {
    if (payload.value.items.length < 4) {
        payload.value.items.push({ nama_item: '', tipe: '', lot: '', net: null })
    }
}

const hapusItem = (index) => {
    payload.value.items.splice(index, 1)
}

const kirimData = async () => {
    const dataBersih = {
        jenis: payload.value.jenis,
        items: payload.value.items.map(item => ({ ...item }))
    }
    
    await buatDanCetakStiker(dataBersih)
    
    if (!galat.value) {
        payload.value.items = [{ nama_item: '', tipe: '', lot: '', net: null }]
    }
}
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
</style>