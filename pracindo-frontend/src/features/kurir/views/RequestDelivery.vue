<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    
    <header class="sticky top-0 z-10 bg-white border-b border-gray-100 shadow-sm px-4 py-3 flex items-center justify-between gap-4">
      <h2 class="text-lg font-bold text-gray-800 whitespace-nowrap m-0">Permintaan Masuk</h2>
      
      <!-- Tombol dikunci paksa dengan modifier ! (important) Tailwind -->
      <button 
        @click="fetchAvailableTasks" 
        class="!w-10 !h-10 !min-w-[40px] !max-w-[40px] !flex-none !flex !items-center !justify-center bg-gray-50 hover:bg-gray-100 active:bg-gray-200 !rounded-full shadow-sm border border-gray-200 !p-0 !m-0 !outline-none"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          class="!w-5 !h-5 !shrink-0 transition-colors" 
          :class="{'animate-spin text-blue-600': loading, 'text-gray-700': !loading}"
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor" 
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </header>
    
    <div class="p-4">
      <div v-if="loading" class="flex flex-col items-center justify-center py-16">
        <div class="inline-block animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full mb-3"></div>
        <p class="text-gray-500 text-sm font-medium">Mencari tugas baru...</p>
      </div>
      
      <div v-else-if="availableTasks.length === 0" class="flex flex-col items-center justify-center bg-white px-6 py-12 rounded-2xl shadow-sm border border-gray-100 mt-2 text-center">
        <div class="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
          </svg>
        </div>
        <p class="text-gray-800 font-bold text-base">Kolam Tugas Kosong</p>
        <p class="text-gray-500 text-sm mt-1">Belum ada pengiriman baru dari gudang saat ini.</p>
      </div>

      <div v-else class="flex flex-col gap-3">
        <CardOrderDelivery 
          v-for="task in availableTasks" 
          :key="task.id" 
          :task="task" 
          @claim="claimTask" 
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useKurir } from '../composables/useKurir'
import CardOrderDelivery from '../components/CardOrderDelivery.vue'

const { availableTasks, loading, fetchAvailableTasks, claimTask } = useKurir()

onMounted(() => {
  fetchAvailableTasks()
})
</script>