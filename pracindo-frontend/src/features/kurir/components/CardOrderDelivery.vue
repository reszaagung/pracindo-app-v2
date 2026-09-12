<template>
  <div class="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden flex flex-col p-5 gap-4">
    <div class="flex justify-between items-start">
      <div class="flex flex-col gap-1">
        <span class="w-max px-2.5 py-1 bg-blue-50 text-blue-600 text-[10px] font-bold rounded-lg flex items-center gap-1">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
          Destinasi #{{ stop.urutan }}
        </span>
        <span class="text-xs font-bold text-slate-400 mt-1">DO: {{ stop.nomor_distribusi }}</span>
      </div>
      <span 
        :class="{
          'bg-emerald-100 text-emerald-700': stop.status === 'DITERIMA',
          'bg-orange-100 text-orange-700': stop.status === 'MENUNGGU',
          'bg-blue-100 text-blue-700': stop.status === 'SAMPAI',
          'bg-red-100 text-red-700': stop.status === 'DIRETUR'
        }"
        class="px-2.5 py-1 text-[10px] font-bold rounded-lg uppercase tracking-wider"
      >
        {{ stop.status }}
      </span>
    </div>

    <div>
      <h3 class="font-black text-slate-800 text-base mb-1">{{ stop.pelanggan_nama }}</h3>
      <p class="text-xs text-slate-500 leading-relaxed">{{ stop.alamat || 'Alamat tidak tersedia' }}</p>
      
      <div v-if="stop.berat_kg" class="flex items-center gap-2 mt-3">
        <span class="flex items-center gap-1 px-2 py-1 bg-slate-100 text-slate-600 text-[10px] font-bold rounded-md">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"></path></svg>
          {{ stop.berat_kg }} Kg
        </span>
      </div>
    </div>

    <button 
      @click="isExpanded = !isExpanded"
      class="flex justify-between items-center w-full py-2.5 mt-1 border-t border-slate-100 text-xs font-bold text-slate-500 hover:text-slate-700 transition-colors"
    >
      <span class="flex items-center gap-1.5">
        <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
        {{ isExpanded ? 'Tutup Rincian Muatan' : 'Lihat Rincian Muatan' }}
      </span>
      <svg 
        :class="{'rotate-180': isExpanded}" 
        class="w-4 h-4 text-slate-400 transition-transform duration-300" 
        fill="none" stroke="currentColor" viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
      </svg>
    </button>

    <div v-show="isExpanded" class="bg-slate-50 rounded-2xl p-3.5 flex flex-col gap-2 border border-slate-100">
      <div class="flex justify-between items-center">
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Rincian Barang</p>
        <span v-if="stop.baris && stop.baris.length > 0" class="text-[10px] font-bold text-slate-400">
          {{ stop.baris.length }} Item
        </span>
      </div>
      
      <div v-if="!stop.baris || stop.baris.length === 0" class="text-xs text-slate-400 italic mt-1">
        Tidak ada rincian item.
      </div>

      <div v-else class="flex flex-col gap-2 mt-1">
        <div v-for="(item, idx) in stop.baris" :key="idx" class="flex justify-between items-center text-xs py-1.5 border-b border-slate-200/60 last:border-none">
          <div class="flex flex-col w-2/3">
            <span 
              class="font-bold text-slate-700 truncate" 
              :title="item.produk_nama && item.produk_nama !== '-' ? item.produk_nama : 'Produk Tidak Diketahui'"
            >
              {{ item.produk_nama && item.produk_nama !== '-' ? item.produk_nama : 'Produk Tidak Diketahui' }}
            </span>
            <span v-if="item.stiker && item.stiker !== '-'" class="text-[10px] text-slate-400 truncate">
              Stiker: {{ item.stiker }}
            </span>
          </div>
          <span class="font-black text-slate-900 bg-white px-2 py-1 rounded-lg border border-slate-200 shadow-sm whitespace-nowrap">
            {{ item.qty }} {{ item.unit }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="$slots.actions" class="mt-2">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  stop: {
    type: Object,
    required: true
  }
})

const isExpanded = ref(false)
</script>