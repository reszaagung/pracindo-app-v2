<template>
  <div class="flex flex-col gap-3 w-full max-w-xs mx-auto">
    <button
      v-for="(huruf, posisi) in pola.split('')"
      :key="posisi"
      type="button"
      @click="$emit('pilih-huruf', huruf)"
      :aria-label="`Isi data untuk huruf ${huruf}`"
      class="relative h-16 rounded-2xl flex items-center justify-center font-black text-2xl text-white shadow-md transition-transform active:scale-95"
      :style="{ background: warnaHuruf[huruf] || warnaDefault }"
    >
      {{ huruf }}
      <span
        v-if="statusTersimpan(huruf)"
        class="absolute -top-2 -right-2 w-7 h-7 bg-white rounded-full border-2 border-emerald-500 flex items-center justify-center shadow"
      >
        <i class="pi pi-check text-emerald-500 text-sm"></i>
      </span>
    </button>
  </div>
</template>

<script setup>
// `hurufUnik` adalah daftar huruf unik sesuai urutan kemunculan pertama di `pola`
// (mis. "AABC" -> ['A','B','C']). Urutan ini HARUS sama dengan urutan
// `form.items` dibuat di GenerateStiker.vue, supaya index item cocok dengan huruf.
const props = defineProps({
  pola: { type: String, required: true },
  hurufUnik: { type: Array, required: true },
  items: { type: Array, required: true } // tiap item punya field is_saved
})
defineEmits(['pilih-huruf'])

const warnaHuruf = {
  A: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  B: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  C: 'linear-gradient(135deg, #ff9966 0%, #ff5e62 100%)',
  D: 'linear-gradient(135deg, #b224ef 0%, #7579ff 100%)',
}
const warnaDefault = 'linear-gradient(135deg, #94a3b8 0%, #64748b 100%)'

const statusTersimpan = (huruf) => {
  const idx = props.hurufUnik.indexOf(huruf)
  return idx !== -1 && !!props.items[idx]?.is_saved
}
</script>