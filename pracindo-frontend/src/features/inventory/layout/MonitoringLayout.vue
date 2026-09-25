<template>
    <component :is="layoutAktif" />
</template>

<script setup>
import { shallowRef, onMounted, onUnmounted } from 'vue'
import DesktopMonitorLayout from './DesktopMonitorLayout.vue'
import MobileMonitorLayout from './MobileMonitorLayout.vue'

const layoutAktif = shallowRef(DesktopMonitorLayout)

const cekLayar = () => {
    layoutAktif.value =
        window.innerWidth < 1024
            ? MobileMonitorLayout
            : DesktopMonitorLayout
}

onMounted(() => {
    cekLayar()
    window.addEventListener('resize', cekLayar)
})

onUnmounted(() => {
    window.removeEventListener('resize', cekLayar)
})
</script>