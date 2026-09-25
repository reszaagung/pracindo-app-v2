```vue
<template>
    <component :is="layoutAktif" />
</template>

<script setup>
import { shallowRef, onMounted, onUnmounted } from 'vue'
import DesktopWarehouseMainLayout from './DesktopWarehouseMainLayout.vue'
import MobileWarehouseMainLayout from './MobileWarehouseMainLayout.vue'

const layoutAktif = shallowRef(DesktopWarehouseMainLayout)

let mediaQuery = null

const cekLayar = () => {
    layoutAktif.value = window.innerWidth < 1024
        ? MobileWarehouseMainLayout
        : DesktopWarehouseMainLayout
}

onMounted(() => {
    mediaQuery = window.matchMedia('(max-width: 1023px)')
    cekLayar()
    mediaQuery.addEventListener('change', cekLayar)
})

onUnmounted(() => {
    mediaQuery?.removeEventListener('change', cekLayar)
    mediaQuery = null
})
</script>
```
