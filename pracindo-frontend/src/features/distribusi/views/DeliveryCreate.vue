<template>
    <div class="w-full">
        <form @submit.prevent="simpanDelivery" class="flex flex-col gap-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="flex flex-col gap-4">
                    <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col">
                        <label class="text-[10px] font-bold text-slate-500 uppercase mb-2">Tanggal Pengiriman</label>
                        <input type="date" v-model="form.tanggal" required
                            class="w-full text-sm font-bold text-slate-800 bg-transparent focus:outline-none" />
                    </div>
                    <div class="bg-blue-50 border border-blue-200 p-4 rounded-xl shadow-sm flex flex-col">
                        <label class="text-[10px] font-bold text-blue-600 uppercase mb-2">Pilih Sales Order (Disetujui)</label>
                        <select v-model="form.sales_order_id" @change="pilihSO" required
                            class="w-full text-sm font-bold text-slate-800 bg-transparent focus:outline-none appearance-none cursor-pointer">
                            <option value="" disabled>-- Pilih Dokumen SO --</option>
                            <option v-for="so in daftarSO" :key="so.id" :value="so.id">
                                {{ so.nomor_so }} - {{ so.pelanggan_nama }}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="flex flex-col gap-4">
                    <div class="bg-white border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col justify-center min-h-[90px] opacity-80">
                        <label class="text-[10px] font-bold text-slate-400 uppercase mb-1">Informasi Kustomer</label>
                        <div v-if="soTerpilih" class="text-sm font-bold text-slate-700">
                            {{ soTerpilih.pelanggan_nama }}
                        </div>
                        <div v-else class="text-xs font-medium text-slate-400 italic">Pilih SO terlebih dahulu</div>
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

            <div v-if="soTerpilih" class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden mt-2 animate-fade-in">
                <div class="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
                    <h3 class="text-sm font-bold text-slate-700">Rincian Barang (Berdasarkan SO)</h3>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-200">
                                <th class="p-4 text-xs font-bold text-slate-500 uppercase w-16 text-center">No</th>
                                <th class="p-4 text-xs font-bold text-slate-500 uppercase">Nama Produk</th>
                                <th class="p-4 text-xs font-bold text-slate-500 uppercase text-right w-32">Qty Pesanan</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <tr v-for="(item, index) in soTerpilih.items" :key="item.id" class="hover:bg-slate-50/50 transition-colors">
                                <td class="p-4 text-center font-bold text-slate-700">{{ index + 1 }}</td>
                                <td class="p-4 font-semibold text-slate-800 text-sm">{{ item.produk_nama }}</td>
                                <td class="p-4 font-bold text-blue-600 text-right text-sm">{{ item.qty }} {{ item.satuan_kode }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="flex justify-end mt-4">
                <button type="submit" :disabled="sedangProses || !soTerpilih" class="px-8 py-3 bg-slate-900 text-white font-bold hover:bg-slate-800 disabled:bg-slate-400 transition-colors rounded-xl shadow-md flex items-center gap-2">
                    <i v-if="sedangProses" class="pi pi-spin pi-spinner text-sm"></i>
                    <i v-else class="pi pi-send text-sm"></i>
                    <span>{{ sedangProses ? 'Memproses...' : 'Kirim Request Delivery' }}</span>
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiDistribusi } from '@/features/distribusi/api'
import api from '@/utils/api'

const router = useRouter()
const sedangProses = ref(false)
const daftarSO = ref([])
const daftarArmada = ref([])
const soTerpilih = ref(null)

const form = reactive({
    tanggal: new Date().toISOString().split('T')[0],
    sales_order_id: '',
    kendaraan_id: ''
})

const muatDataMaster = async () => {
    try {
        const [resArmada, resSO] = await Promise.all([
            apiDistribusi.getArmada(),
            api.get('sales_order/sales-order/', { params: { status: 'DISETUJUI' } }).catch(() => ({ data: { results: [] } }))
        ])
        daftarArmada.value = resArmada.results || resArmada || []
        daftarSO.value = resSO.data?.results || resSO.data || []
    } catch (err) {
        console.error(err)
    }
}

const pilihSO = () => {
    soTerpilih.value = daftarSO.value.find(so => so.id === form.sales_order_id) || null
}

const simpanDelivery = async () => {
    sedangProses.value = true
    try {
        const payload = {
            jenis_tujuan: 'CUSTOMER',
            sales_order_id: form.sales_order_id,
            tanggal: form.tanggal,
            kendaraan_id: form.kendaraan_id || null
        }
        await api.post('logistik/pengiriman/', payload)
        router.push('/distribusi')
    } catch (err) {
        console.error(err)
    } finally {
        sedangProses.value = false
    }
}

onMounted(() => muatDataMaster())
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>