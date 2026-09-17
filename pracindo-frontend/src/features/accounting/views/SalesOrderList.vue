<template>
    <div class="flex flex-col w-full animate-fade-in relative">
        
        <!-- HEADER (Judul & Tombol Aksi) -->
        <div class="mb-5 md:mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 md:gap-0">
            <div class="w-full md:w-auto">
                <p class="text-[11px] md:text-xs text-slate-400 mb-1.5 md:mb-1">
                    <router-link to="/" class="hover:text-slate-700 transition-colors">Dashboard</router-link> ›
                    <span class="text-slate-600 font-medium">Daftar Sales Order</span>
                </p>
                <div class="flex items-center gap-3">
                    <h2 class="text-xl md:text-2xl font-black text-slate-800 tracking-tight">Data Sales Order (SO)</h2>
                    <span class="bg-blue-100 text-blue-700 text-[9px] md:text-[10px] font-bold px-2 py-1 md:px-2.5 md:py-1 rounded-md tracking-wide">AKUNTANSI</span>
                </div>
            </div>
            
            <!-- Perbaikan Tombol Mobile: Gunakan flex-1 & whitespace-nowrap -->
            <div class="flex items-center gap-2 w-full md:w-auto">
                <button type="button" @click="fetchSO" :disabled="isLoading" 
                    class="p-3 md:p-2.5 border border-slate-200 text-slate-600 bg-white hover:bg-slate-50 rounded-xl transition-colors disabled:opacity-50 flex items-center justify-center aspect-square md:aspect-auto shadow-sm">
                    <i class="pi pi-refresh" :class="{ 'pi-spin text-blue-600': isLoading }"></i>
                </button>
                <button type="button" @click="tampilModalSO = true"
                    class="flex-1 md:flex-none justify-center px-4 py-3 md:py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-xs md:text-sm font-bold rounded-xl shadow-[0_4px_12px_rgba(37,99,235,0.2)] hover:shadow-[0_6px_20px_rgba(37,99,235,0.3)] transition-all flex items-center gap-2 whitespace-nowrap">
                    <i class="pi pi-plus"></i> Buat SO Baru
                </button>
            </div>
        </div>

        <!-- MAIN CARD WRAPPER (Membungkus Search, Tab, Tabel, dan Footer jadi satu kesatuan) -->
        <div class="bg-white border border-slate-200 rounded-[20px] md:rounded-[24px] shadow-[0_4px_20px_rgba(0,0,0,0.02)] overflow-hidden flex flex-col w-full">
            
            <!-- TOOLBAR (Search & Tabs) -->
            <div class="p-4 md:p-5 border-b border-slate-100 flex flex-col md:flex-row justify-between items-center gap-4 bg-slate-50/50">
                <!-- Search Input -->
                <div class="relative w-full md:w-80 lg:w-96">
                    <i class="pi pi-search absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400"></i>
                    <input v-model="pencarian" type="text" placeholder="Cari No. SO atau Pelanggan..." 
                        class="w-full pl-10 pr-4 py-3 md:py-2.5 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-colors shadow-sm text-slate-700 font-medium">
                </div>
                
                <!-- Filter Tabs (Bisa di-swipe di Mobile) -->
                <div class="flex items-center gap-1.5 w-full md:w-auto overflow-x-auto pb-1 md:pb-0 hide-scrollbar">
                    <button v-for="tab in tabs" :key="tab.value" @click="filterStatus = tab.value"
                        class="px-5 py-2.5 md:py-2 text-xs font-bold rounded-xl whitespace-nowrap transition-all border"
                        :class="filterStatus === tab.value 
                            ? 'bg-slate-800 text-white border-slate-800 shadow-md' 
                            : 'bg-white text-slate-500 border-slate-200 hover:bg-slate-50 hover:text-slate-700'">
                        {{ tab.label }}
                    </button>
                </div>
            </div>

            <!-- TABLE WRAPPER (Aman dari overflow di Mobile) -->
            <div class="w-full overflow-x-auto bg-white">
                <table class="w-full text-left text-sm whitespace-nowrap min-w-[800px]">
                    <thead class="bg-slate-50/80 border-b border-slate-100 text-slate-500">
                        <tr>
                            <th class="py-4 px-5 text-[11px] font-bold uppercase tracking-wider w-[20%]">No. Dokumen</th>
                            <th class="py-4 px-5 text-[11px] font-bold uppercase tracking-wider w-[15%]">Tanggal</th>
                            <th class="py-4 px-5 text-[11px] font-bold uppercase tracking-wider w-[25%]">Pelanggan</th>
                            <th class="py-4 px-5 text-[11px] font-bold uppercase tracking-wider w-[20%] text-right">Total Tagihan</th>
                            <th class="py-4 px-5 text-[11px] font-bold uppercase tracking-wider w-[15%] text-center">Status</th>
                            <th class="py-4 px-5 text-[11px] font-bold uppercase tracking-wider w-[5%] text-center">Aksi</th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-slate-100">
                        
                        <!-- State Loading -->
                        <tr v-if="isLoading">
                            <td colspan="6" class="py-16 text-center">
                                <i class="pi pi-spinner pi-spin text-3xl text-blue-500 mb-3"></i>
                                <p class="text-slate-500 text-sm font-medium">Memuat data Sales Order...</p>
                            </td>
                        </tr>

                        <!-- State Data Kosong -->
                        <tr v-else-if="filteredSO.length === 0">
                            <td colspan="6" class="py-20 text-center bg-slate-50/30">
                                <div class="w-16 h-16 bg-white border border-slate-100 shadow-sm text-slate-400 rounded-full flex items-center justify-center mx-auto mb-4">
                                    <i class="pi pi-folder-open text-2xl"></i>
                                </div>
                                <p class="text-slate-800 font-bold text-base mb-1">Belum ada dokumen</p>
                                <p class="text-slate-500 text-xs font-medium">Tidak ada data Sales Order yang ditemukan.</p>
                            </td>
                        </tr>

                        <!-- Loop Data Asli -->
                        <template v-else>
                            <tr v-for="so in filteredSO" :key="so.id" class="hover:bg-slate-50/80 transition-colors group">
                                <td class="py-4 px-5">
                                    <span class="font-bold text-slate-800 block mb-0.5">{{ so.nomor_so }}</span>
                                    <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider"><i class="pi pi-building text-[9px] mr-1"></i>{{ so.entitas?.kode || 'UMUM' }}</span>
                                </td>
                                <td class="py-4 px-5 text-slate-600 font-medium">{{ formatDate(so.tanggal) }}</td>
                                <td class="py-4 px-5">
                                    <span class="font-bold text-slate-700 block mb-0.5">{{ so.pelanggan?.nama || '-' }}</span>
                                    <span class="text-[11px] text-slate-500 font-medium"><i class="pi pi-map-marker text-[10px] mr-1"></i>{{ so.pelanggan?.kota || '-' }}</span>
                                </td>
                                <td class="py-4 px-5 text-right font-black text-slate-800">
                                    {{ formatRupiah(so.grand_total) }}
                                </td>
                                <td class="py-4 px-5 text-center">
                                    <span class="px-2.5 py-1 text-[10px] font-bold rounded-md uppercase tracking-wider border" :class="badgeColor(so.status)">
                                        {{ so.status }}
                                    </span>
                                </td>
                                <td class="py-4 px-5 text-center">
                                    <div class="flex items-center justify-center gap-2 opacity-100 lg:opacity-0 lg:group-hover:opacity-100 transition-opacity">
                                        <button class="w-8 h-8 rounded-lg bg-white border border-slate-200 text-blue-600 hover:bg-blue-50 hover:border-blue-200 flex items-center justify-center transition-colors" title="Lihat Detail">
                                            <i class="pi pi-eye text-xs font-bold"></i>
                                        </button>
                                        <button v-if="so.status === 'DRAFT'" class="w-8 h-8 rounded-lg bg-white border border-slate-200 text-emerald-600 hover:bg-emerald-50 hover:border-emerald-200 flex items-center justify-center transition-colors" title="Setujui SO">
                                            <i class="pi pi-check text-xs font-bold"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </template>
                    </tbody>
                </table>
            </div>

            <!-- FOOTER INFO -->
            <div class="p-5 border-t border-slate-100 flex items-center justify-between text-xs font-medium text-slate-500 bg-slate-50/80">
                <span>Menampilkan <b class="text-slate-700">{{ filteredSO.length }}</b> dari <b class="text-slate-700">{{ daftarSO.length }}</b> dokumen</span>
            </div>
        </div>

        <!-- MODAL / DIALOG BIKIN SO -->
        <Dialog v-model:visible="tampilModalSO" modal header="Buat Sales Order Baru" :style="{ width: '90vw', maxWidth: '1100px' }" 
            :pt="{ root: { class: 'border-0 shadow-2xl rounded-2xl overflow-hidden' }, header: { class: 'bg-slate-50 border-b border-slate-100 p-5' }, title: { class: 'text-lg font-black text-slate-800' }, content: { class: 'p-0' } }">
            <LazyFormSO v-if="tampilModalSO" @close="tampilModalSO = false" @saved="soBerhasilDisimpan" />
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, defineAsyncComponent } from 'vue'
import Dialog from 'primevue/dialog'
import { useSalesOrder } from '@/features/accounting/composables/useSalesOrder'

const LazyFormSO = defineAsyncComponent(() =>
    import('@/features/accounting/views/SalesOrderCreate.vue')
)

const tampilModalSO = ref(false)

const soBerhasilDisimpan = () => {
    tampilModalSO.value = false
    fetchSO()
}
const { isLoading, daftarSO, fetchSO } = useSalesOrder()

const pencarian = ref('')
const filterStatus = ref('SEMUA')

const tabs = [
    { label: 'Semua Data', value: 'SEMUA' },
    { label: 'Draft', value: 'DRAFT' },
    { label: 'Disetujui', value: 'DISETUJUI' },
    { label: 'Selesai', value: 'SELESAI' },
]

onMounted(() => {
    fetchSO()
})

const filteredSO = computed(() => {
    return daftarSO.value.filter(so => {
        const matchStatus = filterStatus.value === 'SEMUA' || so.status === filterStatus.value
        const keyword = pencarian.value.toLowerCase()

        const safeNomorSo = String(so.nomor_so || '').toLowerCase()
        const safePelangganNama = String(so.pelanggan?.nama || '').toLowerCase()

        const matchSearch = safeNomorSo.includes(keyword) || safePelangganNama.includes(keyword)

        return matchStatus && matchSearch
    })
})

const formatRupiah = (angka) => {
    return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(angka || 0)
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    const options = { day: '2-digit', month: 'short', year: 'numeric' }
    return new Date(dateString).toLocaleDateString('id-ID', options)
}

const badgeColor = (status) => {
    switch (status) {
        case 'DRAFT': return 'bg-slate-100 text-slate-600 border-slate-200'
        case 'DISETUJUI': return 'bg-blue-50 text-blue-600 border-blue-200'
        case 'SELESAI': return 'bg-emerald-50 text-emerald-600 border-emerald-200'
        case 'BATAL': return 'bg-red-50 text-red-600 border-red-200'
        default: return 'bg-slate-100 text-slate-600 border-slate-200'
    }
}
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

::-webkit-scrollbar { height: 6px; width: 6px; }
::-webkit-scrollbar-track { background: #f8fafc; border-radius: 10px; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>