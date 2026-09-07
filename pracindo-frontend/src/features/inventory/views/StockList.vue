<template>
    <div class="flex flex-col w-full animate-fade-in relative">
        <div class="mb-4 md:mb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
            <div>
                <p class="text-xs text-slate-400 mb-1">
                    <span class="hover:text-slate-700 transition-colors">Inventory</span> /
                    <span class="hover:text-slate-700 transition-colors font-semibold">Stok Gudang</span>
                </p>
                <h1 class="text-xl md:text-2xl font-bold text-slate-800 tracking-tight">Posisi Stok</h1>
                <p class="text-xs md:text-sm text-slate-500 mt-1">Pantau rekap mutasi entitas dan fisik saldo pool</p>
            </div>
        </div>

        <div v-if="galat"
            class="mb-4 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600 font-medium flex items-start gap-3 shadow-sm">
            <i class="pi pi-exclamation-triangle mt-0.5"></i>
            <span>{{ galat }}</span>
        </div>

        <div class="bg-white border border-slate-200 rounded-[24px] p-4 md:p-6 shadow-sm w-full min-h-[400px]">
            <div
                class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 mb-6 pb-4 border-b border-slate-100">
                <div>
                    <h3 class="text-sm font-bold text-slate-800">Daftar Persediaan</h3>
                    <p class="text-xs text-slate-500">Pilih laporan stok di bawah ini</p>
                </div>
                <div class="flex bg-slate-50 p-1 rounded-xl w-full xl:w-auto overflow-x-auto custom-scrollbar">
                    <button v-for="l in LAPIS" :key="l.nilai" @click="pilihLapis(l.nilai)"
                        :class="lapis === l.nilai ? 'bg-white text-emerald-700 shadow-[0_2px_8px_rgba(0,0,0,0.04)] font-bold' : 'text-slate-500 hover:text-slate-700'"
                        class="px-6 py-2 text-xs md:text-sm rounded-lg transition-all whitespace-nowrap flex-1 text-center xl:flex-none">
                        {{ l.label }}
                    </button>
                </div>
            </div>

            <div v-if="sedangProses" class="flex flex-col items-center justify-center py-12 text-center">
                <i class="pi pi-spin pi-spinner text-emerald-500 text-3xl mb-3"></i>
                <p class="text-xs text-slate-500 font-medium">Memuat data dari server...</p>
            </div>

            <!-- TAB 1: ENTITAS -->
            <div v-else-if="lapis === 'ENTITAS'" class="overflow-x-auto custom-scrollbar">
                <table class="w-full text-left text-sm table-auto min-w-[800px]">
                    <thead class="text-slate-500 bg-slate-50/50">
                        <tr>
                            <th class="py-3 px-4 font-semibold rounded-tl-xl">Entitas</th>
                            <th class="py-3 px-4 font-semibold text-right">Qty Setor (Kg)</th>
                            <th class="py-3 px-4 font-semibold text-right">Qty Tarik (Kg)</th>
                            <th class="py-3 px-4 font-semibold text-right">Total Setor</th>
                            <th class="py-3 px-4 font-semibold text-right">Total Tarik</th>
                            <th class="py-3 px-4 font-semibold text-right">Total Rugi</th>
                            <th class="py-3 px-4 font-semibold text-right">Saldo (Rp)</th>
                            <th class="py-3 px-4 font-semibold text-center rounded-tr-xl">Status</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        <tr v-for="s in daftarStok" :key="s.entitas_id" class="hover:bg-slate-50/50 transition-colors">
                            <td class="py-3.5 px-4">
                                <div class="font-bold text-slate-800 uppercase">{{ s.kode }}</div>
                                <div class="text-[10px] text-slate-500">{{ s.nama }}</div>
                            </td>
                            <td class="py-3.5 px-4 text-right font-medium text-emerald-600">{{ angka(s.qty_setor, 3) }}</td>
                            <td class="py-3.5 px-4 text-right font-medium text-amber-600">{{ angka(s.qty_tarik, 3) }}</td>
                            <td class="py-3.5 px-4 text-right text-slate-500">{{ angka(s.total_setor) }}</td>
                            <td class="py-3.5 px-4 text-right text-slate-500">{{ angka(s.total_tarik) }}</td>
                            <td class="py-3.5 px-4 text-right text-rose-500">{{ angka(s.total_rugi) }}</td>
                            <td class="py-3.5 px-4 text-right font-bold"
                                :class="s.saldo > 0 ? 'text-emerald-600' : (s.saldo < 0 ? 'text-rose-600' : 'text-slate-700')">
                                {{ angka(s.saldo) }}
                            </td>
                            <td class="py-3.5 px-4 text-center">
                                <span :class="getStatusBadge(s.status)"
                                    class="px-2.5 py-1 rounded-md text-[10px] font-bold tracking-wide border">
                                    {{ s.status }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div v-if="daftarStok.length === 0" class="py-12 text-center text-slate-500 text-sm">Tidak ada mutasi entitas.</div>
            </div>

            <!-- TAB 2: POOL RAW MATERIAL -->
            <div v-else-if="lapis === 'POOL'" class="overflow-x-auto custom-scrollbar">
                <table class="w-full text-left text-sm table-fixed min-w-[500px]">
                    <thead class="text-slate-500 bg-slate-50/50">
                        <tr>
                            <th class="py-3 px-4 font-semibold rounded-tl-xl w-[40%]">Produk (Raw)</th>
                            <th class="py-3 px-4 font-semibold text-right w-[20%]">Qty (Kg)</th>
                            <th class="py-3 px-4 font-semibold text-right w-[20%]">Nilai (Rp)</th>
                            <th class="py-3 px-4 font-semibold text-right rounded-tr-xl w-[20%]">Harga Rata/Kg</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        <tr v-for="s in daftarStok" :key="s.produk_id" class="hover:bg-slate-50/50 transition-colors">
                            <td class="py-3.5 px-4">
                                <div class="font-bold text-slate-800 uppercase">{{ s.produk_kode }}</div>
                                <div class="text-xs text-slate-500">{{ s.produk_nama }}</div>
                            </td>
                            <td class="py-3.5 px-4 text-right font-black text-slate-800 text-base">{{ angka(s.qty_kg, 3) }}</td>
                            <td class="py-3.5 px-4 text-right font-bold text-emerald-600">{{ angka(s.nilai) }}</td>
                            <td class="py-3.5 px-4 text-right text-slate-500">{{ angka(s.harga_rata) }}</td>
                        </tr>
                    </tbody>
                </table>
                <div v-if="daftarStok.length === 0" class="py-12 text-center text-slate-500 text-sm">Pool sedang kosong.</div>
            </div>

            <!-- TAB 3: STOK BARANG JADI (TABEL PIVOT CLASSIC) -->
            <div v-else-if="lapis === 'JADI'" class="overflow-x-auto custom-scrollbar">
                <table class="w-full text-left text-sm border-collapse border border-slate-900 min-w-[800px]">
                    <thead class="bg-white">
                        <tr>
                            <th class="py-2 px-3 border border-slate-900 font-medium text-slate-900 uppercase whitespace-nowrap">
                                NAMA BARANG
                            </th>
                            <th v-for="kemasan in kemasanUnik" :key="kemasan" 
                                class="py-2 px-3 border border-slate-900 font-medium whitespace-nowrap uppercase">
                                <span class="text-blue-600 underline cursor-pointer">{{ kemasan }}</span>
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white">
                        <tr v-if="stokPivot.length === 0">
                            <td :colspan="kemasanUnik.length + 1" class="py-8 text-center text-slate-500">
                                Belum ada stok barang jadi tercatat.
                            </td>
                        </tr>
                        <!-- Baris Data -->
                        <tr v-for="baris in stokPivot" :key="baris.nama">
                            <td class="py-2 px-3 border border-slate-900 text-slate-900 uppercase">
                                {{ baris.nama }}
                            </td>
                            <td v-for="kemasan in kemasanUnik" :key="kemasan" 
                                class="py-2 px-3 border border-slate-900 text-slate-900 whitespace-nowrap">
                                {{ renderCell(kemasan, baris[kemasan]) }}
                            </td>
                        </tr>
                        <!-- Tiga baris kosong estetika seperti di gambar -->
                        <tr v-for="i in 3" :key="'blank-' + i">
                            <td class="py-3 px-3 border border-slate-900"></td>
                            <td v-for="k in kemasanUnik" :key="'b-' + k" class="py-3 px-3 border border-slate-900"></td>
                        </tr>
                    </tbody>
                </table>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStock } from '../composables/useStock'
import { angka } from '@/utils/format'

const LAPIS = [
    { nilai: 'ENTITAS', label: 'Mutasi Entitas' },
    { nilai: 'POOL', label: 'Saldo Pool (Fisik)' },
    { nilai: 'JADI', label: 'Stok Barang Jadi' } // TAB BARU
]

const router = useRouter()
const { daftarStok, sedangProses, galat, muatStok } = useStock()
const lapis = ref('ENTITAS')

const pilihLapis = (l) => {
    lapis.value = l
    muatStok({ lapis: l })
}

const getStatusBadge = (status) => {
    const s = String(status).toUpperCase();
    if (s === 'KLAIM') return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    if (s === 'HUTANG') return 'bg-rose-50 text-rose-700 border-rose-200';
    return 'bg-slate-100 text-slate-600 border-slate-200';
}

// ==========================================
// LOGIKA PIVOT TABEL STOK BARANG JADI
// ==========================================

// 1. Ekstrak nama kemasan unik untuk dijadikan Header Kolom
const kemasanUnik = computed(() => {
    if (lapis.value !== 'JADI') return []
    const unik = new Set()
    daftarStok.value.forEach(item => {
        if (item.kemasan_nama) unik.add(item.kemasan_nama)
    })
    return Array.from(unik).sort() 
})

// 2. Kelompokkan Data menjadi Baris (Barang) x Kolom (Kemasan)
const stokPivot = computed(() => {
    if (lapis.value !== 'JADI') return []
    const pivotMap = {}

    daftarStok.value.forEach(item => {
        const namaBarang = item.item_nama || item.produk_nama || '-'
        const namaKemasan = item.kemasan_nama || '-'
        
        if (!pivotMap[namaBarang]) {
            pivotMap[namaBarang] = { nama: namaBarang }
        }
        
        // Simpan unit ke dalam object dengan key nama kemasan
        pivotMap[namaBarang][namaKemasan] = {
            qty: item.qty_unit || 0
        }
    })

    // Kembalikan sebagai Array lalu urutkan sesuai abjad
    return Object.values(pivotMap).sort((a, b) => a.nama.localeCompare(b.nama))
})

// 3. Format Cell (Auto-detect satuan dari teks kemasan)
const renderCell = (namaKemasan, cellData) => {
    if (!cellData || !cellData.qty) return '' // Kosong jika tidak ada stok
    
    // Auto tebak satuan berdasarkan judul kolom
    let satuan = ''
    const str = String(namaKemasan).toUpperCase()
    
    if (str.includes('PCS')) satuan = 'PCS'
    else if (str.includes('GALON') || str.includes('GL')) satuan = 'GL'
    else if (str.includes('DUS') || str.includes('DS')) satuan = 'DS'
    else if (str.includes('PAIL') || str.includes('PL')) satuan = 'PL'
    
    return `${cellData.qty} ${satuan}`.trim()
}

onMounted(() => {
    muatStok({ lapis: lapis.value })
})
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-out forwards;
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
    height: 6px;
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}
</style>