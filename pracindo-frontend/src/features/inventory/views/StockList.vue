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

            <div v-else-if="lapis === 'JADI'" class="flex flex-col gap-4">
                <div class="flex justify-end">
                    <div class="relative w-full md:w-64">
                        <input 
                            type="text" 
                            v-model="pencarianBarang" 
                            class="w-full text-sm border-slate-200 rounded-lg px-4 py-2 focus:ring-emerald-500 focus:border-emerald-500" 
                            placeholder="Cari nama barang..." 
                            list="saran-barang"
                        >
                        <datalist id="saran-barang">
                            <option v-for="nama in saranNamaBarang" :key="nama" :value="nama"></option>
                        </datalist>
                    </div>
                </div>

                <div class="overflow-x-auto custom-scrollbar">
                    <table class="w-full text-left text-sm table-auto min-w-[800px]">
                        <thead class="text-slate-500 bg-slate-50/50">
                            <tr>
                                <th class="py-3 px-4 font-semibold rounded-tl-xl w-[25%] tracking-wider">
                                    NAMA BARANG
                                </th>
                                <th v-for="(kemasan, index) in kemasanUnik" :key="kemasan" 
                                    class="py-3 px-4 font-semibold text-center tracking-wider text-blue-600"
                                    :class="{ 'rounded-tr-xl': index === kemasanUnik.length - 1 }">
                                    {{ kemasan }}
                                </th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 bg-white">
                            <tr v-if="dataYangDitampilkan.length === 0">
                                <td :colspan="kemasanUnik.length + 1" class="py-8 text-center text-slate-500">
                                    Tidak ada data yang sesuai.
                                </td>
                            </tr>
                            
                            <tr v-for="baris in dataYangDitampilkan" :key="baris.nama" class="hover:bg-slate-50/50 transition-colors">
                                <td class="py-3.5 px-4 text-slate-800 uppercase font-bold">
                                    {{ baris.nama }}
                                </td>
                                <td v-for="kemasan in kemasanUnik" :key="kemasan" 
                                    class="py-3.5 px-4 text-slate-600 whitespace-nowrap text-center font-medium">
                                    {{ renderCell(kemasan, baris[kemasan]) }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <div class="text-right text-xs text-slate-400 mt-2" v-if="stokPivot.length > 10 && !pencarianBarang">
                        Menampilkan 10 dari total {{ stokPivot.length }} barang
                    </div>
                </div>
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
    { nilai: 'JADI', label: 'Stok Barang Jadi' }
]

const router = useRouter()
const { daftarStok, sedangProses, galat, muatStok } = useStock()
const lapis = ref('ENTITAS')
const pencarianBarang = ref('')

const STANDAR_KEMASAN = [
    'PCS@1KG', 
    'GALON@5KG', 
    'DUS@12KG', 
    'PAIL@20KG', 
    'PAIL@25KG', 
    'PAIL@30KG'
]

const pilihLapis = (l) => {
    lapis.value = l
    pencarianBarang.value = ''
    muatStok({ lapis: l })
}

const getStatusBadge = (status) => {
    const s = String(status).toUpperCase();
    if (s === 'KLAIM') return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    if (s === 'HUTANG') return 'bg-rose-50 text-rose-700 border-rose-200';
    return 'bg-slate-100 text-slate-600 border-slate-200';
}

const kemasanUnik = computed(() => {
    if (lapis.value !== 'JADI') return []
    
    const unik = new Set(STANDAR_KEMASAN)

    daftarStok.value.forEach(item => {
        if (item.kemasan_nama) {
            unik.add(String(item.kemasan_nama).trim().toUpperCase())
        }
    })

    return Array.from(unik) 
})

const stokPivot = computed(() => {
    if (lapis.value !== 'JADI') return []
    
    const pivotMap = {}
    const headers = kemasanUnik.value 

    daftarStok.value.forEach(item => {
        const namaBarang = item.item_nama || item.produk_nama || '-'
        const namaKemasan = item.kemasan_nama ? String(item.kemasan_nama).trim().toUpperCase() : '-'
        
        if (!pivotMap[namaBarang]) {
            pivotMap[namaBarang] = { nama: namaBarang }
            
            headers.forEach(k => {
                pivotMap[namaBarang][k] = { qty: 0 }
            })
        }
        
        if (pivotMap[namaBarang][namaKemasan] !== undefined) {
            pivotMap[namaBarang][namaKemasan].qty += (item.qty_unit || 0)
        } else {
            pivotMap[namaBarang][namaKemasan] = { qty: (item.qty_unit || 0) }
        }
    })

    return Object.values(pivotMap).sort((a, b) => a.nama.localeCompare(b.nama))
})

const saranNamaBarang = computed(() => {
    return stokPivot.value.map(row => row.nama)
})

const dataYangDitampilkan = computed(() => {
    let hasil = stokPivot.value
    if (pencarianBarang.value) {
        const keyword = pencarianBarang.value.toLowerCase()
        hasil = hasil.filter(row => row.nama.toLowerCase().includes(keyword))
    }
    return hasil.slice(0, 10)
})

const renderCell = (namaKemasan, cellData) => {
    const qty = (cellData && cellData.qty) ? cellData.qty : 0
    let satuan = 'unit'
    const str = String(namaKemasan).toUpperCase()
    
    if (str.includes('DUS') || str.includes('DS')) {
        satuan = 'dus'
    }
    
    return `${qty} ${satuan}`
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

input[type="text"]::-webkit-search-cancel-button {
    display: none; 
}
</style>