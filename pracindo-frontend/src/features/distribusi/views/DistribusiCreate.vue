<template>
    <div class="w-full">
        <form @submit.prevent="simpanDistribusi" class="flex flex-col gap-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                <div class="flex flex-col gap-4">
                    <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col">
                        <label class="text-xs font-bold text-slate-500 uppercase text-center mb-2">Perusahaan (PT/CV)</label>
                        <select v-model="form.entitas_id" required
                            class="w-full text-center text-lg font-bold text-slate-800 !bg-transparent !border-none !shadow-none !ring-0 !outline-none p-0 m-0">
                            <option value="" disabled>-- Pilih Perusahaan --</option>
                            <option v-for="entitas in daftarEntitas" :key="entitas.id" :value="entitas.id">
                                {{ entitas.nama }} ({{ entitas.kode }})
                            </option>
                        </select>
                    </div>

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
                    <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col justify-center bg-slate-50 h-[104px]">
                        <label class="text-xs font-bold text-slate-500 uppercase text-center mb-2">No Surat Jalan</label>
                        <input type="text" v-model="form.nomor_surat_jalan" readonly
                            class="w-full text-center text-sm font-bold text-slate-600 !bg-transparent !border-none !shadow-none !ring-0 !outline-none p-0 m-0 cursor-not-allowed" />
                    </div>
                    
                    <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col h-[104px]">
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
                                <select v-model="item.barang_nama" @change="resetKemasan(item)" required class="w-full bg-transparent focus:outline-none font-semibold text-slate-800">
                                    <option value="" disabled>Pilih Barang...</option>
                                    <option v-for="nama in daftarBarangUnik" :key="nama" :value="nama">
                                        {{ nama }}
                                    </option>
                                </select>
                            </td>
                            
                            <td class="p-3 border-r-2 border-slate-800">
                                <select v-model="item.stok_terpilih" @change="hitungOtomatis(item)" :disabled="!item.barang_nama" required class="w-full bg-transparent focus:outline-none font-semibold text-slate-800 disabled:text-slate-400">
                                    <option :value="null" disabled>Pilih Kemasan...</option>
                                    <option v-for="(kemasan, idx) in getKemasanTersedia(item.barang_nama)" :key="idx" :value="kemasan">
                                        {{ kemasan.kemasan_nama || kemasan.kemasan }} (Stok: {{ kemasan.qty_unit || kemasan.qty || 0 }})
                                    </option>
                                </select>
                            </td>
                            
                            <td class="p-3 border-r-2 border-slate-800">
                                <input type="number" v-model="item.total_unit" @input="kalkulasiBerat(item)" 
                                    :max="item.stok_terpilih?.qty_unit || item.stok_terpilih?.qty" min="1" :disabled="!item.stok_terpilih" required 
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

const daftarEntitas = ref([])
const daftarToko = ref([])
const daftarArmada = ref([])
const daftarStokPabrik = ref([]) 

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
        if (nama && !map.has(nama)) {
            map.set(nama, nama)
        }
    })
    return Array.from(map.values())
})

const getKemasanTersedia = (namaDipilih) => {
    if (!namaDipilih) return []
    return daftarStokPabrik.value.filter(stok => getNamaAsli(stok) === namaDipilih)
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
    if (item.stok_terpilih && item.total_unit > batasMaksimal) {
        alert(`Gagal! Jumlah melebihi batas stok tersedia (${batasMaksimal}).`)
        item.total_unit = batasMaksimal
    }
    
    if(item.berat_per_unit > 0 && item.total_unit > 0) {
        item.total_berat = (item.total_unit * item.berat_per_unit).toFixed(2)
    } else {
        item.total_berat = 0
    }
}

const muatDataMaster = async () => {
    try {
        const [resArmada, resToko, resStok, resEntitas] = await Promise.all([
            apiDistribusi.getArmada(),
            api.get('core/cabangtoko/'), 
            apiDistribusi.getStokPabrik(),
            api.get('core/entitas/').catch(() => ({ data: { results: [] } }))
        ])
        
        daftarArmada.value = resArmada.results || resArmada || []
        daftarToko.value = resToko.data?.results || resToko.data || []
        daftarStokPabrik.value = resStok.rincian || resStok.results || resStok || []
        daftarEntitas.value = resEntitas.data?.results || resEntitas.data || []
    } catch (err) {
        console.error("Gagal muat master:", err)
    }
}

const simpanDistribusi = async () => {
    sedangProses.value = true
    try {
        const tokoTerpilih = daftarToko.value.find(t => t.id === form.tujuan_toko_id)
        const namaToko = tokoTerpilih ? tokoTerpilih.nama : 'Cabang Retail'
        const alamatToko = tokoTerpilih?.alamat ? tokoTerpilih.alamat : 'Alamat belum diisi'

        const itemsValid = form.items.filter(i => i.barang_nama && i.stok_terpilih)

        if (itemsValid.length === 0) {
            alert('Wajib memilih minimal 1 barang dan kemasannya sebelum menyimpan!')
            sedangProses.value = false
            return
        }

        const payload = {
            entitas_id: parseInt(form.entitas_id, 10), 
            jenis_tujuan: 'CABANG',
            tujuan_cabang_id: parseInt(form.tujuan_toko_id, 10), 
            pelanggan_nama: namaToko,
            alamat: alamatToko,
            tanggal: form.tanggal,
            berat_total_kg: itemsValid.reduce((sum, item) => sum + (parseFloat(item.total_berat) || 0), 0),
            
            baris: itemsValid.map(i => {
                // KIRIM TEKS KODE ASLI SECARA LANGSUNG (contoh: "signal_red")
                const stringId = i.stok_terpilih.item_id || i.stok_terpilih.produk_id || i.stok_terpilih.id
                return {
                    produk_id: stringId,
                    kemasan: i.kemasan,
                    qty: parseInt(i.total_unit, 10) || 1
                }
            })
        }

        await apiDistribusi.createDistribusi(payload)
        router.push('/distribusi') 
    } catch (err) {
        console.error("Detail Error Backend:", err.response?.data || err)
        if (err.response?.data?.baris) {
            alert('Gagal! Rincian barang ditolak server: \n\n' + JSON.stringify(err.response.data.baris, null, 2))
        } else {
            alert('Gagal menyimpan Distribusi! Pastikan jaringan aman.')
        }
    } finally {
        sedangProses.value = false
    }
}

onMounted(() => {
    muatDataMaster()
})
</script>