<template>
  <div class="relative" ref="wrapperRef">
    <input
      type="text"
      v-model="teksCari"
      @input="onInput"
      @focus="tampilkanSaran = true"
      :disabled="disabled"
      placeholder="Ketik minimal 2 huruf buat cari produk..."
      class="p-3 border rounded-lg disabled:bg-gray-100 disabled:text-gray-400 w-full"
      autocomplete="off"
    />
    <div
      v-if="tampilkanSaran && sedangCari"
      class="absolute z-20 mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg px-3 py-2 text-sm text-gray-400"
    >
      Mencari...
    </div>
    <div
      v-else-if="tampilkanSaran && hasilCari.length > 0"
      class="absolute z-20 mt-1 w-full max-h-56 overflow-y-auto bg-white border border-gray-200 rounded-lg shadow-lg"
    >
      <button
        v-for="produk in hasilCari"
        :key="produk.id"
        type="button"
        @click="pilihProduk(produk)"
        class="w-full text-left px-3 py-2 hover:bg-blue-50 text-sm border-b border-gray-100 last:border-b-0"
      >
        {{ produk.nama_item }}
      </button>
    </div>
    <div
      v-else-if="tampilkanSaran && teksCari.trim().length >= 2 && hasilCari.length === 0 && !sedangCari"
      class="absolute z-20 mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-lg px-3 py-2 text-sm text-gray-400"
    >
      Tidak ada produk yang cocok
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import api from '../api'

const props = defineProps({
  modelValue: { type: [Number, String, null], default: null },
  disabled: { type: Boolean, default: false }
})
const emit = defineEmits(['update:modelValue', 'produk-terpilih'])

const teksCari = ref('')
const tampilkanSaran = ref(false)
const hasilCari = ref([])
const sedangCari = ref(false)
const wrapperRef = ref(null)
let timerDebounce = null

watch(() => props.modelValue, (id) => {
  if (id === null) teksCari.value = ''
})

// Dikonfirmasi dari MasterProdukViewSet: filter_backends = [SearchFilter],
// parameter otomatisnya "search", field yang dicari termasuk "nama_item".
const cariKeServer = async (q) => {
  sedangCari.value = true
  try {
    const { data } = await api.get('master/master-produk/', {
      params: { search: q, aktif: true }
    })
    hasilCari.value = (data.results ?? data).slice(0, 20)
  } catch {
    hasilCari.value = []
  } finally {
    sedangCari.value = false
  }
}

const onInput = () => {
  tampilkanSaran.value = true
  emit('update:modelValue', null)
  clearTimeout(timerDebounce)

  const q = teksCari.value.trim()
  if (q.length < 2) {
    hasilCari.value = []
    return
  }
  timerDebounce = setTimeout(() => cariKeServer(q), 300)
}

const pilihProduk = (produk) => {
  teksCari.value = produk.nama_item
  tampilkanSaran.value = false
  hasilCari.value = []
  emit('update:modelValue', produk.id)
  emit('produk-terpilih', produk)
}

const tutupKalauKlikLuar = (event) => {
  if (wrapperRef.value && !wrapperRef.value.contains(event.target)) {
    tampilkanSaran.value = false
  }
}
onMounted(() => document.addEventListener('click', tutupKalauKlikLuar))
onUnmounted(() => document.removeEventListener('click', tutupKalauKlikLuar))
</script>