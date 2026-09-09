<template>
    <div class="w-full p-4 flex flex-col gap-4 pb-24 bg-slate-50 min-h-screen">
        <div class="flex justify-between items-end mb-2">
            <div>
                <h1 class="text-xl font-bold text-slate-800">Order Pool</h1>
                <p class="text-xs text-slate-500">Ambil tiket pengiriman yang tersedia</p>
            </div>
            <button @click="loadTasks" class="text-emerald-600 font-bold text-xs bg-emerald-100 px-3 py-1.5 rounded-lg">
                Refresh
            </button>
        </div>

        <div v-if="isLoading" class="text-center py-10 text-slate-500 font-bold animate-pulse">
            Memuat data...
        </div>

        <div v-else-if="tasks.length === 0" class="bg-white border-2 border-slate-200 rounded-2xl p-10 text-center">
            <span class="text-4xl">📭</span>
            <p class="font-bold text-slate-700 mt-3">Kosong</p>
            <p class="text-xs text-slate-500">Belum ada tugas baru dari gudang.</p>
        </div>

        <div v-else class="flex flex-col gap-4">
            <div v-for="task in tasks" :key="task.id" class="bg-white border-2 border-slate-200 rounded-2xl p-4 shadow-sm relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full bg-emerald-500"></div>
                
                <div class="flex justify-between items-start">
                    <div>
                        <span class="text-[10px] font-bold bg-slate-100 text-slate-600 px-2 py-1 rounded">{{ task.nomor }}</span>
                        <h3 class="text-sm font-bold mt-2 text-slate-800">Total Tujuan: {{ task.jumlah_perhentian }} Toko</h3>
                        <p class="text-xs text-slate-500 mt-1">📅 {{ task.tanggal }}</p>
                    </div>
                </div>

                <button @click="handleClaim(task.id)" :disabled="claimingId === task.id"
                    class="w-full mt-4 py-3 bg-slate-800 hover:bg-slate-700 text-white font-bold text-sm rounded-xl disabled:bg-slate-300 transition-colors">
                    {{ claimingId === task.id ? 'MENGAMBIL...' : 'KLAIM TUGAS' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAvailableTasks } from '@/features/kurir/composables/useAvailableTasks'

const router = useRouter()
const { tasks, isLoading, claimingId, loadTasks, claim } = useAvailableTasks()

const handleClaim = async (id) => {
    const success = await claim(id)
    if (success) {
        router.push('/kurir/on-go-delivery')
    }
}

onMounted(() => loadTasks())
</script>