<template>
    <div class="w-full">
        <form @submit.prevent="simpanDistribusi" class="flex flex-col gap-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="flex flex-col gap-4">
                    <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col">
                        <label class="text-xs font-bold text-slate-500 uppercase text-center mb-2">Tanggal</label>
                        <input type="date" v-model="form.tanggal" required
                            class="w-full text-center text-lg font-bold text-slate-800 !bg-transparent !border-none !shadow-none !ring-0 !outline-none p-0 m-0" />
                    </div>

                    <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col">
                        <label class="text-xs font-bold text-slate-500 uppercase text-center mb-2">
                            Tujuan<br><span class="text-[10px] font-normal">(yang dimaksud disini adalah retail)</span>
                        </label>
                        <select v-model="form.tujuan_toko_id" required
                            class="w-full text-center text-lg font-bold text-slate-800 !bg-transparent !border-none !shadow-none !ring-0 !outline-none p-0 m-0">
                            <option value="" disabled>-- Pilih Cabang Retail --</option>
                            <option v-for="toko in daftarToko" :key="toko.id" :value="toko.id">
                                {{ toko.nama }} ({{ toko.kode }})
                            </option>
                        </select>
                    </div>
                </div>

                <div class="flex flex-col gap-4">
                    <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col justify-center bg-slate-50">
                        <label class="text-xs font-bold text-slate-500 uppercase text-center mb-2">No Surat Jalan</label>
                        <input type="text" v-model="form.nomor_surat_jalan" readonly
                            class="w-full text-center text-sm font-bold text-slate-600 !bg-transparent !border-none !shadow-none !ring-0 !outline-none p-0 m-0 cursor-not-allowed" />
                    </div>
                    
                    <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col">
                        <label class="text-xs font-bold text-slate-500 uppercase text-center mb-2">No Kendaraan</label>
                        <select v-model="form.kendaraan_id"
                            class="w-full text-center text-lg font-bold text-slate-800 !bg-transparent !border-none !shadow-none !ring-0 !outline-none p-0 m-0">
                            <option value="">-- Bebas (Ditentukan Kurir) --</option>
                            <option v-for="armada in daftarArmada" :key="armada.id" :value="armada.id">
                                {{ armada.plat_nomor }} - {{ armada.nama }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="bg-white border-2 border-slate-800 shadow-sm p-1">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="border-b-2 border-slate-800 bg-slate-50">
                            <th class="p-3 border-r-2 border-slate-800 text-center text-sm font-bold uppercase w-16">No</th>
                            <th class="p-3 border-r-2 border-slate-800 text-center text-sm font-bold uppercase">Nama Barang</th>
                            <th class="p-3 border-r-2 border-slate-800 text-center text-sm font-bold uppercase w-48">Kemasan</th>
                            <th class="p-3 border-r-2 border-slate-800 text-center text-sm font-bold uppercase w-32">Total Unit</th>
                            <th class="p-3 text-center text-sm font-bold uppercase w-32">Total Berat</th>
                            <th class="p-3 w-12"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in form.items" :key="index" class="border-b border-slate-200 hover:bg-slate-50">
                            <td class="p-3 border-r-2 border-slate-800 text-center font-bold">{{ index + 1 }}</td>
                            
                            <td class="p-3 border-r-2 border-slate-800">
                                <select v-model="item.barang_id" @change="resetKemasan(item)" required class="w-full bg-transparent focus:outline-none font-semibold text-slate-800">
                                    <option value="" disabled>Pilih Barang...</option>
                                    <option v-for="brg in daftarBarangUnik" :key="brg.id" :value="brg.id">
                                        {{ brg.nama }}
                                    </option>
                                </select>
                            </td>
                            
                            <td class="p-3 border-r-2 border-slate-800">
                                <select v-model="item.stok_terpilih" @change="hitungOtomatis(item)" :disabled="!item.barang_id" required class="w-full bg-transparent focus:outline-none font-semibold text-slate-800 disabled:text-slate-400">
                                    <option :value="null" disabled>Pilih Kemasan...</option>
                                    <option v-for="kemasan in getKemasanTersedia(item.barang_id)" :key="kemasan.kemasan_id" :value="kemasan">
                                        {{ kemasan.kemasan_nama }} (Stok: {{ kemasan.qty_unit }})
                                    </option>
                                </select>
                            </td>
                            
                            <td class="p-3 border-r-2 border-slate-800">
                                <input type="number" v-model="item.total_unit" @input="kalkulasiBerat(item)" 
                                    :max="item.stok_terpilih?.qty_unit" min="1" :disabled="!item.stok_terpilih" required 
                                    class="w-full text-center bg-transparent focus:outline-none font-bold text-blue-600 disabled:text-slate-400" />
                            </td>
                            
                            <td class="p-3 text-center border-r-2 border-slate-800">
                                <span class="font-bold text-slate-700">
                                    {{ item.total_berat ? item.total_berat + ' Kg' : '0 Kg' }}
                                </span>
                            </td>
                            
                            <td class="p-3 text-center">
                                <button type="button" @click="hapusItem(index)" v-if="form.items.length > 1" class="text-red-500 hover:text-red-700">
                                    <span class="font-bold text-xl">✕</span>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div class="p-3 bg-slate-50 border-t-2 border-slate-800 text-center">
                    <button type="button" @click="tambahItem" class="text-sm font-bold text-emerald-600 hover:text-emerald-700">
                        + Tambah Baris Barang
                    </button>
                </div>
            </div>

            <div class="flex justify-end mt-4">
                <button type="submit" :disabled="sedangProses" class="px-12 py-4 !bg-slate-800 !text-white font-bold hover:!bg-slate-700 disabled:!bg-slate-300 transition-colors w-full md:w-auto !rounded-none !border-none !shadow-none text-lg">
                    {{ sedangProses ? 'MENYIMPAN...' : 'SIMPAN DISTRIBUSI' }}
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

const daftarToko = ref([])
const daftarArmada = ref([])
const daftarKurir = ref([])
const daftarStokPabrik = ref([]) 

const form = reactive({
    tanggal: new Date().toISOString().split('T')[0],
    tujuan_toko_id: '',
    nomor_surat_jalan: 'Memuat...', 
    kendaraan_id: '',
    items: [
        { stok_terpilih: null, barang_id: '', kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 }
    ]
})

const tambahItem = () => form.items.push({ stok_terpilih: null, barang_id: '', kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 })
const hapusItem = (index) => form.items.splice(index, 1)

const daftarBarangUnik = computed(() => {
    const map = new Map()
    daftarStokPabrik.value.forEach(stok => {
        if (stok.qty_unit > 0 && !map.has(stok.item_id)) {
            map.set(stok.item_id, { id: stok.item_id, nama: stok.item_nama })
        }
    })
    return Array.from(map.values())
})

const getKemasanTersedia = (barangId) => {
    if (!barangId) return []
    return daftarStokPabrik.value.filter(stok => stok.item_id === barangId && stok.qty_unit > 0)
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
    
    item.kemasan = item.stok_terpilih.kemasan_nama
    
    const totalKg = parseFloat(item.stok_terpilih.qty_kg) || 0
    const stokTersedia = parseInt(item.stok_terpilih.qty_unit) || 1
    item.berat_per_unit = totalKg / stokTersedia

    item.total_unit = 1
    kalkulasiBerat(item)
}

const kalkulasiBerat = (item) => {
    if (item.stok_terpilih && item.total_unit > item.stok_terpilih.qty_unit) {
        alert('Gagal! Jumlah unit melebihi stok tersedia di pabrik.')
        item.total_unit = item.stok_terpilih.qty_unit
    }
    
    if(item.berat_per_unit > 0 && item.total_unit > 0) {
        item.total_berat = (item.total_unit * item.berat_per_unit).toFixed(2)
    } else {
        item.total_berat = 0
    }
}

const muatDataMaster = async () => {
    try {
        const [resArmada, resToko, resStok, resNoSJ] = await Promise.all([
            apiDistribusi.getArmada(),
            api.get('core/cabangtoko/'), 
            apiDistribusi.getStokPabrik(),
            apiDistribusi.getNoSuratJalan()
        ])

        daftarArmada.value = resArmada.results || resArmada || []
        daftarToko.value = resToko.data?.results || resToko.data || []
        daftarStokPabrik.value = resStok.rincian || resStok.results || resStok || []
        form.nomor_surat_jalan = resNoSJ
    } catch (err) {
        console.error(err)
    }
}

const simpanDistribusi = async () => {
    sedangProses.value = true
    try {
        const payload = {
            is_direct_push: true,
            tanggal: form.tanggal,
            tujuan_toko_id: form.tujuan_toko_id,
            nomor_surat_jalan: form.nomor_surat_jalan,
            kurir_id: null, 
            kendaraan_id: form.kendaraan_id || null, 
            items: form.items.map(i => ({
                barang_id: i.barang_id,
                kemasan: i.kemasan,
                total_unit: i.total_unit,
                total_berat: parseFloat(i.total_berat) || 0
            }))
        }
        await apiDistribusi.rakitPengiriman(payload)
        router.push('/distribusi') 
    } catch (err) {
        console.error(err)
        alert('Gagal menyimpan Distribusi!')
    } finally {
        sedangProses.value = false
    }
}

onMounted(() => {
    muatDataMaster()
})
</script>