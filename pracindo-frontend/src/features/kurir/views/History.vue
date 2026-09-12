<template>
    <div class="w-full p-4 flex flex-col gap-4 pb-24 bg-slate-50 min-h-screen">
        <div class="flex justify-between items-end mb-2">
            <div>
                <h1 class="text-xl font-bold text-slate-800">Riwayat Pengiriman</h1>
                <p class="text-xs text-slate-500 mb-2">Daftar tugas yang telah diselesaikan.</p>
            </div>
            <button @click="loadHistory" class="text-blue-600 font-bold text-xs bg-blue-100 px-3 py-1.5 rounded-lg">
                Refresh
            </button>
        </div>

        <div v-if="isLoading" class="text-center py-10 text-slate-500 font-bold animate-pulse">
            Memuat data...
        </div>

        <div v-else-if="history.length === 0" class="bg-white border-2 border-slate-200 rounded-2xl p-10 text-center">
            <span class="text-4xl">🗂️</span>
            <p class="font-bold text-slate-700 mt-3">Belum Ada Riwayat</p>
            <p class="text-xs text-slate-500">Anda belum menyelesaikan pengiriman apapun.</p>
        </div>

        <div v-else class="flex flex-col gap-3">
            <div 
                v-for="item in history" 
                :key="item.id" 
                class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-center justify-between opacity-90"
            >
                <div>
                    <span class="text-[10px] font-bold bg-slate-100 text-slate-600 px-2 py-1 rounded">{{ item.nomor }}</span>
                    <!-- Format tanggal menggunakan method bawaan JS agar rapi -->
                    <h3 class="text-sm font-bold mt-2 text-slate-700">Selesai: {{ formatTanggal(item.waktu_selesai) }}</h3>
                    <p class="text-xs text-slate-500">{{ item.jumlah_perhentian }} Perhentian Toko | {{ item.jarak_total_km }} km</p>
                </div>
                <div class="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600 shadow-inner">
                    <span class="text-lg">✔️</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useHistory } from '@/features/kurir/composables/useHistory' 

const { history, isLoading, loadHistory } = useHistory()

const formatTanggal = (dateString) => {
    if (!dateString) return '-'
    const d = new Date(dateString)
    return d.toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })
}

onMounted(() => loadHistory())
</script>