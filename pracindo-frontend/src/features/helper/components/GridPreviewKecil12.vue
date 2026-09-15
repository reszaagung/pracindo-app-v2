<template>
  <div class="grid grid-cols-3 gap-3 w-full max-w-sm mx-auto">
    <div
      v-for="(huruf, posisi) in pola.split('')"
      :key="posisi"
      class="relative aspect-square rounded-xl flex items-center justify-center font-black text-xl text-white shadow-md cursor-pointer transition-transform active:scale-95"
      :style="{ background: warnaHuruf(huruf) }"
      @click="$emit('pilih-huruf', huruf)"
    >
      {{ huruf }}
      <span v-if="formData[huruf]?.is_saved" class="absolute -top-1.5 -right-1.5 w-6 h-6 bg-white rounded-full border-2 border-emerald-500 flex items-center justify-center shadow">
        <i class="pi pi-check text-emerald-500 text-xs"></i>
      </span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  pola: { type: String, required: true },
  formData: { type: Object, required: true }
})
defineEmits(['pilih-huruf'])

const PALET = [
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(135deg, #ff9966 0%, #ff5e62 100%)',
  'linear-gradient(135deg, #b224ef 0%, #7579ff 100%)',
  'linear-gradient(135deg, #f6d365 0%, #fda085 100%)',
  'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)',
  'linear-gradient(135deg, #ff6a88 0%, #ff9a8b 100%)',
  'linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)',
  'linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)',
  'linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%)',
  'linear-gradient(135deg, #fddb92 0%, #d1fdff 100%)',
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
]
const DAFTAR_HURUF = ['A','B','C','D','E','F','G','H','I','J','K','L']
const warnaHuruf = (huruf) => PALET[DAFTAR_HURUF.indexOf(huruf)] || '#94a3b8'
</script>