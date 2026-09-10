<template>
    <div class="w-full">
        <form @submit.prevent="simpanDistribusi" class="flex flex-col gap-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="flex flex-col gap-4">
                    <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col">
                        <label class="text-[10px] font-bold text-slate-500 uppercase mb-2">Perusahaan (PT/CV)</label>
                        <select v-model="form.entitas_id" @change="pilihEntitas" required
                            class="w-full text-sm font-bold text-slate-800 bg-transparent focus:outline-none appearance-none cursor-pointer">
                            <option value="" disabled>-- Pilih Perusahaan --</option>
                            <option v-for="entitas in daftarEntitas" :key="entitas.id" :value="entitas.id">
                                {{ entitas.nama }} ({{ entitas.kode }})
                            </option>
                        </select>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col">
                        <label class="text-[10px] font-bold text-slate-500 uppercase mb-2">Tanggal Distribusi</label>
                        <input type="date" v-model="form.tanggal" required
                            class="w-full text-sm font-bold text-slate-800 bg-transparent focus:outline-none" />
                    </div>
                    <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col">
                        <label class="text-[10px] font-bold text-slate-500 uppercase mb-2">Tujuan (Cabang Retail)</label>
                        <select v-model="form.tujuan_toko_id" required
                            class="w-full text-sm font-bold text-slate-800 bg-transparent focus:outline-none appearance-none cursor-pointer">
                            <option value="" disabled>-- Pilih Cabang Retail --</option>
                            <option v-for="toko in daftarToko" :key="toko.id" :value="toko.id">
                                {{ toko.nama }} ({{ toko.kode }})
                            </option>
                        </select>
                    </div>
                </div>
                <div class="flex flex-col gap-4">
                        <div class="bg-white border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col justify-center h-[90px] opacity-70">
                            <label class="text-[10px] font-bold text-slate-400 uppercase mb-1">No Surat Jalan</label>
                            <input type="text" :value="previewNomor" readonly
                                class="w-full text-sm font-bold text-slate-500 bg-transparent focus:outline-none cursor-not-allowed" />
                        </div>
                    <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col">
                        <label class="text-[10px] font-bold text-slate-500 uppercase mb-2">Armada / Kendaraan</label>
                        <select v-model="form.kendaraan_id"
                            class="w-full text-sm font-bold text-slate-800 bg-transparent focus:outline-none appearance-none cursor-pointer">
                            <option value="">-- Bebas (Ditentukan Kemudian) --</option>
                            <option v-for="armada in daftarArmada" :key="armada.id" :value="armada.id">
                                {{ armada.plat_nomor }} - {{ armada.nama }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden mt-2 relative">
                <div v-if="sedangMuatStok" class="absolute inset-0 bg-white/60 backdrop-blur-sm z-10 flex items-center justify-center">
                    <i class="pi pi-spin pi-spinner text-3xl text-blue-600"></i>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-200">
                                <th class="p-4 text-xs font-bold text-slate-500 uppercase w-16 text-center">No</th>
                                <th class="p-4 text-xs font-bold text-slate-500 uppercase">Barang</th>
                                <th class="p-4 text-xs font-bold text-slate-500 uppercase w-48">Kemasan</th>
                                <th class="p-4 text-xs font-bold text-slate-500 uppercase w-32 text-center">Qty Unit</th>
                                <th class="p-4 text-xs font-bold text-slate-500 uppercase w-32 text-center">Total Berat</th>
                                <th class="p-4 w-16"></th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <tr v-for="(item, index) in form.items" :key="index" class="hover:bg-slate-50/50 transition-colors">
                                <td class="p-4 text-center font-bold text-slate-700">{{ index + 1 }}</td>
                                <td class="p-4 align-top">
                                    <select v-model="item.barang_nama" @change="resetKemasan(item)" :disabled="!form.entitas_id" required class="w-full bg-transparent focus:outline-none font-semibold text-slate-800 text-sm disabled:text-slate-400 cursor-pointer">
                                        <option value="" disabled>{{ form.entitas_id ? 'Pilih Barang...' : 'Pilih Perusahaan Dulu' }}</option>
                                        <option v-for="nama in daftarBarangUnik" :key="nama" :value="nama">{{ nama }}</option>
                                    </select>
                                    
                                    <div v-if="item.barang_nama" class="text-[11px] font-medium text-emerald-600 mt-2 flex items-start gap-1">
                                        <i class="pi pi-info-circle text-[10px] mt-[2px]"></i>
                                        <span class="leading-tight">{{ getInfoStokBarang(item.barang_nama) }}</span>
                                    </div>
                                </td>
                                <td class="p-4">
                                    <select v-model="item.stok_terpilih" @change="hitungOtomatis(item)" :disabled="!item.barang_nama" required class="w-full bg-transparent focus:outline-none font-semibold text-slate-800 text-sm disabled:text-slate-400 cursor-pointer">
                                        <option :value="null" disabled>Pilih Kemasan...</option>
                                        <option v-for="(kemasan, idx) in getKemasanTersedia(item.barang_nama)" :key="idx" :value="kemasan">
                                            {{ kemasan.kemasan_nama || kemasan.kemasan }} (Stok: {{ kemasan.qty_unit || kemasan.qty || 0 }})
                                        </option>
                                    </select>
                                </td>
                                <td class="p-4">
                                    <input type="number" v-model="item.total_unit" @input="kalkulasiBerat(item)" :max="item.stok_terpilih?.qty_unit || item.stok_terpilih?.qty" min="1" :disabled="!item.stok_terpilih" required class="w-full text-center bg-transparent focus:outline-none font-bold text-blue-600 text-sm disabled:text-slate-400" />
                                </td>
                                <td class="p-4 text-center">
                                    <span class="font-bold text-slate-700 text-sm">{{ item.total_berat ? item.total_berat + ' Kg' : '0 Kg' }}</span>
                                </td>
                                <td class="p-4 text-center">
                                    <button type="button" @click="hapusItem(index)" v-if="form.items.length > 1" class="w-8 h-8 rounded-lg flex items-center justify-center text-red-500 hover:bg-red-50 transition-colors">
                                        <i class="pi pi-trash text-sm"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="p-3 bg-slate-50 border-t border-slate-200 text-center">
                    <button type="button" @click="tambahItem" :disabled="!form.entitas_id" class="text-sm font-bold text-blue-600 hover:text-blue-700 disabled:text-slate-400 flex items-center justify-center gap-2 mx-auto transition-colors">
                        <i class="pi pi-plus text-xs"></i> Tambah Baris Barang
                    </button>
                </div>
            </div>

            <div class="flex justify-end mt-4">
                <button type="submit" :disabled="sedangProses" class="px-8 py-3 bg-slate-900 text-white font-bold hover:bg-slate-800 disabled:bg-slate-400 transition-colors rounded-xl shadow-md flex items-center gap-2">
                    <i v-if="sedangProses" class="pi pi-spin pi-spinner text-sm"></i>
                    <i v-else class="pi pi-save text-sm"></i>
                    <span>{{ sedangProses ? 'Menyimpan...' : 'Kirim Request Distribusi' }}</span>
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { apiDistribusi } from '@/features/distribusi/api'
import api from '@/utils/api'

const router = useRouter()
const sedangProses = ref(false)
const sedangMuatStok = ref(false)

const daftarEntitas = ref([])
const daftarToko = ref([])
const daftarArmada = ref([])
const daftarStokPabrik = ref([])


const previewNomor = computed(() => {
    if (!form.entitas_id) return 'Otomatis (Pilih Perusahaan)'
    
    const entitas = daftarEntitas.value.find(e => e.id === form.entitas_id)
    if (!entitas) return 'Otomatis (Setelah Disimpan)'
    
    const date = new Date()
    const tahun = date.getFullYear()
    const romawi = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
    const bulan = romawi[date.getMonth()]
    
    return `DO/${entitas.kode}/${tahun}/${bulan}/[Otomatis]`
})

const form = reactive({
    entitas_id: '',
    tanggal: new Date().toISOString().split('T')[0],
    tujuan_toko_id: '',
    nomor_surat_jalan: 'Otomatis (Saat Disimpan)',
    kendaraan_id: '',
    items: [
        { stok_terpilih: null, barang_nama: '', kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 }
    ]
})

const tambahItem = () => form.items.push({ stok_terpilih: null, barang_nama: '', kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 })
const hapusItem = (index) => form.items.splice(index, 1)

const getNamaAsli = (data) => {
    if (!data) return 'Barang Unknown'
    return data.item_nama || data.produk_nama || data.nama || (data.produk && data.produk.nama) || 'Barang Unknown'
}

const daftarBarangUnik = computed(() => {
    const map = new Map()
    daftarStokPabrik.value.forEach(stok => {
        const nama = getNamaAsli(stok)
        if (nama && !map.has(nama)) map.set(nama, nama)
    })
    return Array.from(map.values())
})

const getKemasanTersedia = (namaDipilih) => {
    if (!namaDipilih) return []
    return daftarStokPabrik.value.filter(stok => getNamaAsli(stok) === namaDipilih)
}

const getInfoStokBarang = (namaBarang) => {
    if (!namaBarang) return ''
    const kemasanList = getKemasanTersedia(namaBarang)
    if (!kemasanList.length) return 'Stok kosong'
    
    const rincian = kemasanList.map(k => {
        const qty = k.qty_unit || k.qty || 0
        const namaKemasan = k.kemasan_nama || k.kemasan || 'Unknown'
        return `${qty} ${namaKemasan}`
    })
    
    return 'Stok: ' + rincian.join(', ')
}

const resetKemasan = (item) => {
    item.stok_terpilih = null
    item.kemasan = ''
    item.total_unit = 1
    item.total_berat = 0
    item.berat_per_unit = 0
}

const hitungOtomatis = (item) => {
    if (!item.stok_terpilih) return
    item.kemasan = item.stok_terpilih.kemasan_nama || item.stok_terpilih.kemasan || 'CURAH'
    const totalKg = parseFloat(item.stok_terpilih.qty_kg || item.stok_terpilih.berat_total_kg) || 0
    const stokTersedia = parseInt(item.stok_terpilih.qty_unit || item.stok_terpilih.qty) || 1
    item.berat_per_unit = totalKg / stokTersedia
    item.total_unit = 1
    kalkulasiBerat(item)
}

const kalkulasiBerat = (item) => {
    const batasMaksimal = item.stok_terpilih?.qty_unit || item.stok_terpilih?.qty || 1
    if (item.total_unit > batasMaksimal) item.total_unit = batasMaksimal
    item.total_berat = (item.berat_per_unit > 0 && item.total_unit > 0) ? (item.total_unit * item.berat_per_unit).toFixed(2) : 0
}

const pilihEntitas = async () => {
    form.items = [{ stok_terpilih: null, barang_nama: '', kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 }]
    daftarStokPabrik.value = []
    
    if (!form.entitas_id) return
    
    sedangMuatStok.value = true
    try {
        const resStok = await apiDistribusi.getStokPabrik({ entitas: form.entitas_id })
        daftarStokPabrik.value = resStok.rincian || resStok.results || resStok || []
    } catch (err) {
        console.error(err)
    } finally {
        sedangMuatStok.value = false
    }
}

const muatDataMaster = async () => {
    try {
        const [resArmada, resToko, resEntitas] = await Promise.all([
            apiDistribusi.getArmada(),
            api.get('core/cabangtoko/'),
            api.get('core/entitas/').catch(() => ({ data: { results: [] } }))
        ])
        daftarArmada.value = resArmada.results || resArmada || []
        daftarToko.value = resToko.data?.results || resToko.data || []
        
        let entitasData = resEntitas.data?.results || resEntitas.data || []
        if (Array.isArray(entitasData)) {
            daftarEntitas.value = entitasData.filter(e => e.aktif !== false)
        }
    } catch (err) {
        console.error(err)
    }
}

const simpanDistribusi = async () => {
    sedangProses.value = true
    try {
        const tokoTerpilih = daftarToko.value.find(t => t.id === form.tujuan_toko_id)
        const itemsValid = form.items.filter(i => i.barang_nama && i.stok_terpilih)
        
        const payload = {
            entitas_id: parseInt(form.entitas_id, 10),
            jenis_tujuan: 'CABANG',
            tujuan_cabang_id: parseInt(form.tujuan_toko_id, 10),
            pelanggan_nama: tokoTerpilih ? tokoTerpilih.nama : 'Cabang Retail',
            alamat: tokoTerpilih?.alamat || '-',
            berat_total_kg: itemsValid.reduce((sum, i) => sum + (parseFloat(i.total_berat) || 0), 0),
            baris: itemsValid.map(i => ({
                produk_id: i.stok_terpilih.item_id || i.stok_terpilih.produk_id || i.stok_terpilih.id,
                kemasan: i.kemasan,
                qty: parseInt(i.total_unit, 10) || 1
            }))
        }
        await apiDistribusi.createDistribusi(payload)
        router.push('/distribusi/monitoring')
    } catch (err) {
        console.error(err)
        alert('Gagal menyimpan.')
    } finally {
        sedangProses.value = false
    }
}

onMounted(() => muatDataMaster())
</script>