<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    
    <header class="sticky top-0 z-10 bg-white border-b border-gray-100 shadow-sm px-4 py-3 flex items-center justify-between gap-4">
      <h2 class="text-lg font-bold text-gray-800 whitespace-nowrap m-0">Riwayat Tugas</h2>
      <button 
        @click="fetchHistory" 
        class="!w-10 !h-10 !min-w-[40px] !max-w-[40px] !flex-none !flex !items-center !justify-center bg-gray-50 hover:bg-gray-100 active:bg-gray-200 !rounded-full shadow-sm border border-gray-200 !p-0 !m-0 !outline-none"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="!w-5 !h-5 !shrink-0 transition-colors" :class="{'animate-spin text-blue-600': loadingHistory, 'text-gray-700': !loadingHistory}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </header>

    <div class="p-4">
      <div v-if="loadingHistory" class="flex flex-col items-center justify-center py-16">
        <div class="inline-block animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full mb-3"></div>
        <p class="text-gray-500 text-sm font-medium">Memuat riwayat...</p>
      </div>

      <div v-else-if="historyDeliveries.length === 0" class="flex flex-col items-center justify-center bg-white px-6 py-12 rounded-2xl shadow-sm border border-gray-100 mt-2 text-center">
        <p class="text-gray-800 font-bold text-base">Belum Ada Riwayat</p>
        <p class="text-gray-500 text-sm mt-1">Tugas yang sudah selesai atau dibatalkan akan muncul di sini.</p>
      </div>

      <div v-else class="flex flex-col gap-4">
        <div v-for="delivery in historyDeliveries" :key="delivery.id" class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden flex flex-col opacity-90 hover:opacity-100 transition-opacity">
          
          <div class="px-4 py-3 border-b border-gray-50 flex justify-between items-center bg-gray-50/50">
            <div>
              <h3 class="font-bold text-gray-800 text-sm truncate">{{ delivery.nomor }}</h3>
              <p class="text-[10px] text-gray-500 mt-0.5">{{ delivery.tanggal }}</p>
            </div>
            <span :class="delivery.status === 'SELESAI' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'" class="px-2 py-1 text-[10px] uppercase font-bold tracking-wider rounded whitespace-nowrap ml-2">
              {{ delivery.status }}
            </span>
          </div>

          <div class="p-4">
            <p v-if="delivery.status === 'BATAL'" class="text-xs text-rose-600 font-medium mb-3 bg-rose-50 p-2 rounded border border-rose-100">
              Alasan Batal: {{ extractBatalReason(delivery.catatan) }}
            </p>

            <button @click="toggleDetail(delivery.id)" class="flex items-center justify-center w-full gap-2 text-xs font-bold text-gray-500 hover:text-gray-800 transition-colors py-2 bg-gray-50 rounded-lg border border-gray-100">
              <span v-if="expandedId === delivery.id">Tutup Detail Rute ▴</span>
              <span v-else>Lihat Muatan & Alamat Tujuan ▾</span>
            </button>

            <!-- KONTEN DETAIL RIWAYAT -->
            <div v-if="expandedId === delivery.id" class="mt-4 pt-3 border-t border-gray-100">
              <div class="relative border-l-2 border-gray-200 ml-2 space-y-4">
                
                <div v-for="(stop, index) in delivery.perhentian" :key="stop.id" class="relative pl-5">
                  <div class="absolute -left-[7px] top-1.5 w-3 h-3 rounded-full border-2 border-white bg-gray-400"></div>
                  
                  <div class="bg-white border border-gray-100 rounded-lg p-3 shadow-sm">
                    <div class="flex justify-between items-start mb-2">
                      <span class="font-bold text-gray-700 text-sm leading-tight">{{ index + 1 }}. {{ stop.pelanggan_nama || 'Tujuan ' + (index + 1) }}</span>
                      <span class="text-[9px] font-bold px-2 py-0.5 rounded uppercase" :class="stop.status === 'DITERIMA' ? 'bg-emerald-100 text-emerald-700' : (stop.status === 'DIRETUR' ? 'bg-rose-100 text-rose-700' : 'bg-gray-100 text-gray-600')">
                        {{ stop.status }}
                      </span>
                    </div>
                    
                    <div class="space-y-1 text-xs text-gray-500">
                      <div class="flex items-start gap-2">
                        <span class="shrink-0">📍</span>
                        <span class="leading-relaxed">{{ stop.alamat || 'Alamat tidak tersedia' }}</span>
                      </div>
                      <div class="flex items-center gap-2">
                        <span class="shrink-0">📦</span>
                        <span>DO: <strong class="text-gray-600">{{ stop.nomor_distribusi || 'N/A' }}</strong></span>
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useKurir } from '../composables/useKurir'

const { historyDeliveries, loadingHistory, fetchHistory } = useKurir()

const expandedId = ref(null)

onMounted(() => {
  fetchHistory()
})

const toggleDetail = (id) => {
  expandedId.value = expandedId.value === id ? null : id
}

// Helper untuk mengambil alasan batal dari field catatan backend (jika ada)
const extractBatalReason = (catatan) => {
  if (!catatan) return 'Dibatalkan oleh sistem/admin.'
  const match = catatan.match(/\[BATAL\](.*)/)
  return match ? match[1].trim() : catatan
}
</script>