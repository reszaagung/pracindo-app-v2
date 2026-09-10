<script setup>
import { onMounted } from 'vue'
import { useMyDeliveries } from '@/features/kurir/composables/useMyDeliveries'
import { STATUS_WARNA, STATUS_LABEL } from '@/features/kurir/uiConfigKurir'
const { deliveries, isLoading, loadDeliveries } = useMyDeliveries()

onMounted(() => {
    loadDeliveries()
})
</script>

<template>
  <div>
    <div class="flex justify-between items-end mb-4">
        <h2 class="text-base font-bold text-[#111827]">Daftar Tugas</h2>
        <router-link to="/kurir/on-go-delivery" class="text-[10px] text-emerald-600 font-bold hover:underline">
            Lihat Semua
        </router-link>
    </div>

    <div v-if="isLoading" class="text-center py-10 text-slate-400 font-bold text-xs animate-pulse">
        Memeriksa tugas aktif...
    </div>

    <div v-else-if="deliveries.length === 0" class="bg-white rounded-2xl p-8 shadow-sm border border-slate-200 flex flex-col items-center justify-center text-center">
      <div class="w-12 h-12 bg-slate-50 rounded-full flex items-center justify-center mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
      </div>
      <h3 class="text-[13px] font-bold text-[#111827] mb-1">Tidak Ada Tugas</h3>
      <p class="text-xs text-slate-500 leading-relaxed">
        Anda tidak memiliki jadwal pengiriman aktif saat ini.
      </p>
    </div>

    <div v-else class="flex flex-col gap-4">
        <div v-for="delivery in deliveries" :key="delivery.id" class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200 relative overflow-hidden">
            <div class="absolute top-0 left-0 w-1 h-full bg-emerald-500"></div>
            
            <div class="flex justify-between items-start mb-2">
                <div>
                    <span class="text-[10px] font-bold px-2 py-1 rounded border" 
                          :class="STATUS_WARNA[delivery.status] || 'bg-slate-100 text-slate-600 border-slate-200'">
                        {{ STATUS_LABEL[delivery.status] || delivery.status }}
                    </span>
                    <h3 class="text-sm font-bold text-slate-800 mt-2">{{ delivery.nomor }}</h3>
                </div>
            </div>
            
            <p class="text-xs text-slate-500 mt-1">Total: <span class="font-bold text-slate-700">{{ delivery.perhentian?.length || 0 }} Tujuan Toko</span></p>
            
            <router-link to="/kurir/on-go-delivery" class="mt-4 flex items-center justify-center w-full py-2.5 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs rounded-xl transition-colors">
                Eksekusi Pengiriman
            </router-link>
        </div>
    </div>
  </div>
</template>