<template>
    <div class="flex flex-col w-full animate-fade-in bg-slate-50 min-h-screen p-6">
        <div class="flex justify-between items-center mb-6 border-b-2 border-slate-200 pb-4">
            <div>
                <h1 class="text-2xl font-bold text-slate-800 tracking-tight">Form Delivery</h1>
                <p class="text-sm text-slate-500 mt-1"></p>
            </div>
            <button @click="$router.push('/distribusi')" class="px-6 py-2 bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold text-sm transition-colors">
                KEMBALI
            </button>
        </div>

        <form @submit.prevent="simpanDelivery" class="flex flex-col gap-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="flex flex-col gap-4">
                    <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col">
                        <label class="text-xs font-bold text-slate-500 uppercase text-center mb-2">Tanggal</label>
                        <input type="date" v-model="form.tanggal" required
                            class="w-full text-center text-lg font-bold focus:outline-none text-slate-800" />
                    </div>

                    <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col">
                        <label class="text-xs font-bold text-slate-500 uppercase text-center mb-2">
                            Entitas
                        </label>
                        <select v-model="form.entitas_id" required @change="muatAntrean"
                            class="w-full text-center text-lg font-bold focus:outline-none text-slate-800 bg-transparent">
                            <option value="" disabled></option>
                            <option v-for="toko in daftarToko" :key="toko.id" :value="toko.id">
                                {{ toko.nama }} ({{ toko.kode }})
                            </option>
                        </select>
                    </div>
                </div>

                <div class="flex flex-col gap-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col justify-center">
                            <label class="text-xs font-bold text-slate-500 uppercase text-center mb-2">No Surat Jalan</label>
                            <input type="text" v-model="form.nomor_surat_jalan"
                                class="w-full text-center text-sm font-bold focus:outline-none text-slate-800" />
                        </div>
                        <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col justify-center">
                            <label class="text-xs font-bold text-slate-500 uppercase text-center mb-2">Nama Pengirim</label>
                            <select v-model="form.kurir_id" required
                                class="w-full text-center text-sm font-bold focus:outline-none text-slate-800 bg-transparent">
                                <option value="" disabled></option>
                                <option v-for="kurir in daftarKurir" :key="kurir.id" :value="kurir.id">
                                    {{ kurir.nama }}
                                </option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="bg-white border-2 border-slate-800 p-4 shadow-sm flex flex-col">
                        <label class="text-xs font-bold text-slate-500 uppercase text-center mb-2">No Kendaraan</label>
                        <select v-model="form.kendaraan_id"
                            class="w-full text-center text-lg font-bold focus:outline-none text-slate-800 bg-transparent">
                            <option value=""></option>
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
                            <th class="p-3 border-r-2 border-slate-800 text-center text-sm font-bold uppercase w-16">Pilih</th>
                            <th class="p-3 border-r-2 border-slate-800 text-center text-sm font-bold uppercase">No Distribusi</th>
                            <th class="p-3 text-center text-sm font-bold uppercase">Tujuan</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="antrean in daftarAntrean" :key="antrean.id" class="border-b border-slate-200 hover:bg-slate-50">
                            <td class="p-3 border-r-2 border-slate-800 text-center font-bold">
                                <input type="checkbox" :value="antrean.id" v-model="form.distribusi_ids" class="w-5 h-5 accent-slate-800" />
                            </td>
                            <td class="p-3 border-r-2 border-slate-800 font-bold text-center">
                                {{ antrean.nomor }}
                            </td>
                            <td class="p-3 text-center">
                                {{ antrean.tujuan }}
                            </td>
                        </tr>
                        <tr v-if="!daftarAntrean.length">
                            <td colspan="3" class="p-6 text-center text-slate-500 font-bold"></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="flex justify-end mt-4">
                <button type="submit" :disabled="sedangProses || form.distribusi_ids.length === 0" class="px-10 py-3 bg-slate-800 text-white font-bold hover:bg-slate-700 disabled:bg-slate-400 transition-colors w-full md:w-auto">
                    SIMPAN
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiDistribusi } from '@/features/distribusi/api'
import { useMasterLogistik } from '../composables/useMasterLogistik'
const router = useRouter()
const { daftarArmada, daftarKurir, daftarToko, muatDataMaster } = useMasterLogistik()

const sedangProses = ref(false)
const daftarAntrean = ref([])

const form = reactive({
    tanggal: new Date().toISOString().split('T')[0],
    entitas_id: '',
    nomor_surat_jalan: '', 
    kurir_id: '',
    kendaraan_id: '',
    distribusi_ids: []
})

const muatAntrean = async () => {
    if (!form.entitas_id) return
    try {
        const res = await apiDistribusi.getDistribusiTersedia(form.entitas_id)
        daftarAntrean.value = res.results || res || []
        form.distribusi_ids = []
    } catch (err) {
        console.error(err)
    }
}

const simpanDelivery = async () => {
    sedangProses.value = true
    try {
        const payload = {
            is_direct_push: false,
            tanggal: form.tanggal,
            entitas_id: form.entitas_id,
            nomor_surat_jalan: form.nomor_surat_jalan,
            kurir_id: form.kurir_id,
            kendaraan_id: form.kendaraan_id || null,
            perhentian: form.distribusi_ids.map((id, index) => ({
                distribusi_id: id,
                urutan: index + 1
            }))
        }
        await apiDistribusi.rakitPengiriman(payload)
        router.push('/distribusi')
    } catch (err) {
        console.error(err)
    } finally {
        sedangProses.value = false
    }
}

onMounted(() => {
    muatDataMaster()
})
</script>