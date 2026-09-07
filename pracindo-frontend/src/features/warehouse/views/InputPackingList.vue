<template>
  <div class="p-6 bg-white rounded-lg shadow">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Riwayat Packing</h2>
      <button @click="$router.push({ name: 'InputPackingForm' })" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 font-medium shadow-sm transition-colors">
        + Buat Packing Baru
      </button>
    </div>

    <div v-if="isLoading" class="text-center py-8 text-gray-500">
      <i class="pi pi-spin pi-spinner text-2xl mb-2"></i>
      <p>Memuat data...</p>
    </div>
    
    <div v-else-if="error" class="text-red-600 mb-4 bg-red-50 p-4 rounded-lg border border-red-200">
      {{ error }}
    </div>

    <div v-else class="overflow-x-auto w-full rounded-lg border border-slate-200 shadow-sm">
      <table class="min-w-full divide-y divide-gray-200 whitespace-nowrap">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Nomor</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Tanggal</th>
            <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Batch WIP</th>
            <th class="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">Qty (Kg)</th>
            <th class="px-6 py-3 text-center text-xs font-semibold text-gray-500 uppercase tracking-wider">Status</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="packings.length === 0">
            <td colspan="5" class="px-6 py-8 text-center text-gray-500">Belum ada riwayat packing.</td>
          </tr>
          <tr v-for="item in packings" :key="item.id" class="hover:bg-slate-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap font-bold text-slate-800">{{ item.nomor }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-slate-600">{{ item.tanggal }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-slate-600">{{ item.batch_nomor }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right font-semibold text-slate-800">{{ item.qty_kg }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-center">
               <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-50 text-emerald-600 border border-emerald-200">
                 <i class="pi pi-check-circle text-[10px]"></i> Terkirim
               </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { usePacking } from '../composables/usePacking'

const { packings, isLoading, error, fetchPackings } = usePacking()

onMounted(() => {
  fetchPackings()
})
</script>