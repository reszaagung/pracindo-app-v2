<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden flex flex-col">
    <!-- Header Card: Nomor & Status -->
    <div class="px-4 py-3 border-b border-gray-50 flex justify-between items-center bg-gray-50/50">
      <h3 class="font-bold text-gray-800 text-sm sm:text-base truncate">{{ task.nomor }}</h3>
      <span class="px-2 py-1 text-[10px] uppercase font-bold tracking-wider rounded bg-blue-100 text-blue-700 whitespace-nowrap ml-2">
        Baru
      </span>
    </div>

    <!-- Body Card: Info -->
    <div class="p-4 flex flex-col gap-3 text-sm text-gray-600">
      <div class="flex items-start gap-3">
        <div class="p-1.5 bg-gray-50 rounded text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <div>
          <p class="text-[11px] text-gray-400 font-medium uppercase tracking-wide">Tanggal Dibuat</p>
          <p class="font-semibold text-gray-800 mt-0.5">{{ task.tanggal }}</p>
        </div>
      </div>
    </div>

    <!-- Footer Card: Aksi -->
    <div class="px-4 pb-4">
      <button 
        @click="$emit('claim', task.id)"
        class="w-full flex items-center justify-center gap-2 bg-blue-600 text-white px-4 py-3 rounded-lg font-bold hover:bg-blue-700 active:bg-blue-800 transition shadow-sm text-sm">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
        Ambil Pengiriman
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  task: {
    type: Object,
    required: true
  }
})

defineEmits(['claim'])
</script>