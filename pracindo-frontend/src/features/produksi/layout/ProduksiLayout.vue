<!-- src/features/produksi/layout/ProduksiLayout.vue -->
<template>
  <component :is="layoutAktif" />
</template>

<script setup>
import { shallowRef, onMounted, onUnmounted } from 'vue'

import DesktopInputProduksi from './DesktopInputProduksi.vue'
import MobileInputProduksi from './MobileInputProduksi.vue'

const layoutAktif = shallowRef(DesktopInputProduksi)

const cekLayar = () => {
  if (window.innerWidth < 1024) {
    layoutAktif.value = MobileInputProduksi
  } else {
    layoutAktif.value = DesktopInputProduksi
  }
}

onMounted(() => {
  cekLayar()
  window.addEventListener('resize', cekLayar)
})

onUnmounted(() => {
  window.removeEventListener('resize', cekLayar)
})
</script>
