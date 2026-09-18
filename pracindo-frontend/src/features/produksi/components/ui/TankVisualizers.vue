<template>
  <div class="flex items-center gap-3">
    <div class="text-right">
      <p class="text-lg font-black" :class="persen >= 90 ? 'text-rose-600' : 'text-slate-700'">
        {{ persen }}%
      </p>
      <p class="text-[9px] font-bold text-slate-400 uppercase">Kapasitas</p>
    </div>

    <div class="relative w-10 h-14 bg-slate-100 rounded-lg border border-slate-200 overflow-hidden flex flex-col justify-end shadow-inner">
      <div 
        class="w-full transition-all duration-700 ease-in-out opacity-85"
        :class="persen >= 90 ? 'bg-rose-500' : 'bg-blue-500'"
        :style="{ height: `${persen}%` }"
      ></div>
      <div class="absolute inset-0 bg-gradient-to-tr from-transparent via-white/30 to-transparent pointer-events-none"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  volume: { type: [Number, String], required: true },
  kapasitas: { type: [Number, String], default: 300000 }
})

const persen = computed(() => {
  const maks = Number(props.kapasitas) || 300000 
  const isi = Number(props.volume) || 0
  
  const hitung = (isi / maks) * 100
  return Math.min(Math.max(hitung, 0), 100).toFixed(1)
})
</script>