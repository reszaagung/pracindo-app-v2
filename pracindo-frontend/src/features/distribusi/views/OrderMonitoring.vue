<template>
    <div class="flex flex-col w-full animate-fade-in relative min-h-screen p-6 bg-slate-50">
        <div class="mb-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b-2 border-slate-200 pb-5">
            <div>
                <p class="text-xs text-slate-400 mb-1">
                    <span class="hover:text-slate-700 transition-colors">Logistics</span> /
                    <span class="text-slate-600 font-semibold">Monitoring Order</span>
                </p>
                <h1 class="text-2xl md:text-3xl font-bold text-slate-800 tracking-tight">Monitoring Order</h1>
                <p class="text-sm text-slate-500 mt-1">Pantau status persetujuan logistik dan posisi pengiriman secara real-time.</p>
            </div>
            <button @click="muatData" class="px-5 py-2.5 bg-white border-2 border-slate-200 hover:bg-slate-100 text-slate-700 text-sm font-bold rounded-xl transition-colors shadow-sm flex items-center gap-2">
                <i :class="['pi pi-sync text-xs', memuat ? 'pi-spin' : '']"></i>
                <span>Segarkan Data</span>
            </button>
        </div>

        <div class="bg-white border border-slate-200 rounded-2xl shadow-sm w-full mb-6 p-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="flex flex-col gap-1.5">
                    <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Cari Dokumen</label>
                    <div class="flex items-center bg-slate-50 border border-slate-200 rounded-xl focus-within:ring-2 focus-within:ring-slate-800 transition-colors overflow-hidden">
                        <div class="pl-4 pr-2 flex items-center justify-center">
                            <i class="pi pi-search text-slate-400"></i>
                        </div>
                        <input type="text" v-model="filter.cari" @keyup.enter="muatData" placeholder="Ketik No. Order..."
                            class="w-full py-2.5 pr-4 bg-transparent text-sm focus:outline-none text-slate-800 font-medium" />
                    </div>
                </div>
                <div class="flex flex-col gap-1.5">
                    <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Status Logistik</label>
                    <select v-model="filter.status" @change="muatData"
                        class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-slate-800 text-slate-800 font-medium appearance-none cursor-pointer">
                        <option value="">Semua Status</option>
                        <option value="DRAFT">Menunggu ACC Logistik</option>
                        <option value="TERJADWAL">Disetujui & Terjadwal</option>
                        <option value="LOADING">Proses Loading</option>
                        <option value="DIKIRIM">Sedang Dikirim</option>
                    </select>
                </div>
                <div class="flex flex-col gap-1.5">
                    <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Tanggal</label>
                    <input type="date" v-model="filter.tanggal" @change="muatData"
                        class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-slate-800 text-slate-800 font-medium" />
                </div>
            </div>
        </div>

        <div class="bg-white border border-slate-200 rounded-2xl shadow-sm w-full min-h-[400px] overflow-hidden relative">
            <div v-if="memuat" class="absolute inset-0 bg-white/70 backdrop-blur-sm z-10 flex flex-col items-center justify-center">
                <i class="pi pi-spin pi-spinner text-blue-600 text-4xl mb-4"></i>
                <p class="text-sm font-bold text-slate-600">Memuat data order...</p>
            </div>

            <div class="overflow-x-auto custom-scrollbar">
                <table class="w-full text-left text-sm table-auto min-w-[70rem]">
                    <thead class="text-slate-500 bg-slate-50/80 border-b border-slate-200">
                        <tr>
                            <th class="py-4 px-5 font-bold uppercase text-[11px] tracking-wider">No. Order / Tanggal</th>
                            <th class="py-4 px-5 font-bold uppercase text-[11px] tracking-wider">Tujuan</th>
                            <th class="py-4 px-5 font-bold uppercase text-[11px] tracking-wider">Tipe</th>
                            <th class="py-4 px-5 font-bold uppercase text-[11px] tracking-wider">Armada & Supir</th>
                            <th class="py-4 px-5 font-bold uppercase text-[11px] tracking-wider text-center">Status</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                        <tr v-if="daftarOrder.length === 0 && !memuat">
                            <td colspan="5" class="py-16 text-center">
                                <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-3 border border-slate-200">
                                    <i class="pi pi-inbox text-slate-300 text-2xl"></i>
                                </div>
                                <h4 class="text-slate-700 font-bold mb-1">Tidak Ada Order</h4>
                                <p class="text-xs text-slate-500">Belum ada request pengiriman yang cocok dengan filter.</p>
                            </td>
                        </tr>
                        <tr v-for="item in daftarOrder" :key="item.id" class="hover:bg-slate-50/50 transition-colors group">
                            <td class="py-4 px-5 align-top">
                                <div class="font-bold text-slate-800 text-sm">{{ item.nomor || `REQ-${item.id}` }}</div>
                                <div class="text-xs text-slate-500 mt-1 flex items-center gap-1">
                                    <i class="pi pi-calendar text-[10px]"></i> {{ item.tanggal }}
                                </div>
                            </td>
                            <td class="py-4 px-5 align-top">
                                <div class="font-bold text-slate-700 text-sm">{{ item.tujuan_nama || item.pelanggan_nama || 'Multidrop' }}</div>
                                <div class="text-[11px] text-slate-500 mt-1 line-clamp-1 max-w-[250px]">{{ item.alamat || item.tujuan_alamat || '-' }}</div>
                            </td>
                            <td class="py-4 px-5 align-top">
                                <span class="px-2.5 py-1 rounded-md text-[10px] font-bold tracking-wide uppercase"
                                    :class="item.jenis_tujuan === 'CABANG' ? 'bg-blue-50 text-blue-600 border border-blue-200' : 'bg-emerald-50 text-emerald-600 border border-emerald-200'">
                                    {{ item.jenis_tujuan === 'CABANG' ? 'DISTRIBUSI (RETAIL)' : 'DELIVERY (B2C)' }}
                                </span>
                            </td>
                            <td class="py-4 px-5 align-top">
                                <div v-if="item.kendaraan_id || item.kurir_id">
                                    <div class="font-bold text-slate-700 text-sm">{{ item.kendaraan_plat || (item.kendaraan && item.kendaraan.plat_nomor) || 'Truk Reguler' }}</div>
                                    <div class="text-xs text-slate-500 mt-1 flex items-center gap-1">
                                        <i class="pi pi-user text-[10px]"></i> {{ item.kurir_nama || (item.kurir && item.kurir.nama) || 'Kurir Internal' }}
                                    </div>
                                </div>
                                <div v-else class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-amber-50 border border-amber-200 text-amber-600 rounded-md text-[10px] font-bold">
                                    <i class="pi pi-hourglass text-[10px]"></i> Menunggu ACC
                                </div>
                            </td>
                            <td class="py-4 px-5 align-top text-center">
                                <span class="px-3 py-1.5 rounded-lg text-[10px] font-bold tracking-widest uppercase border shadow-sm"
                                    :class="badgeWarna(item.status, item.kendaraan_id)">
                                    {{ getStatusTeks(item.status, item.kendaraan_id) }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { apiDistribusi } from '@/features/distribusi/api'
import api from '@/utils/api'

const memuat = ref(false)
const daftarOrder = ref([])

const filter = reactive({
    cari: '',
    status: '',
    tanggal: ''
})

const getStatusTeks = (status, adaKendaraan) => {
    const s = (status || 'DRAFT').toUpperCase()
    if (s === 'DRAFT' && !adaKendaraan) return 'MENUNGGU ACC'
    if (s === 'DRAFT' && adaKendaraan) return 'TERJADWAL'
    return s
}

const badgeWarna = (status, adaKendaraan) => {
    const s = getStatusTeks(status, adaKendaraan)
    switch (s) {
        case 'MENUNGGU ACC': return 'bg-amber-100 text-amber-700 border-amber-300'
        case 'TERJADWAL': return 'bg-blue-100 text-blue-700 border-blue-300'
        case 'LOADING': return 'bg-indigo-100 text-indigo-700 border-indigo-300'
        case 'DIKIRIM': return 'bg-purple-100 text-purple-700 border-purple-300'
        case 'SELESAI': return 'bg-emerald-100 text-emerald-700 border-emerald-300'
        default: return 'bg-slate-100 text-slate-600 border-slate-300'
    }
}

const muatData = async () => {
    memuat.value = true
    try {
        const params = {}
        if (filter.cari) params.search = filter.cari
        if (filter.status) params.status = filter.status
        if (filter.tanggal) params.tanggal = filter.tanggal

        const [resDistribusi, resDelivery] = await Promise.all([
            api.get('warehouse/distribusi/', { params }).catch(() => ({ data: { results: [] } })),
            api.get('logistik/pengiriman/', { params }).catch(() => ({ data: { results: [] } }))
        ])

        const data1 = resDistribusi.data?.results || resDistribusi.data || []
        const data2 = resDelivery.data?.results || resDelivery.data || []
        
        const gabungan = [...data1, ...data2].sort((a, b) => new Date(b.tanggal_dibuat || b.tanggal) - new Date(a.tanggal_dibuat || a.tanggal))
        
        daftarOrder.value = gabungan
    } catch (err) {
        console.error(err)
    } finally {
        memuat.value = false
    }
}

onMounted(() => muatData())
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.custom-scrollbar::-webkit-scrollbar { height: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>