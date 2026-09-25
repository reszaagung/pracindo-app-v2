<template>
    <component :is="layoutAktif" />
</template>

<script setup>
import { shallowRef, onMounted, onUnmounted } from 'vue'

import DesktopTransactionLayout from './DesktopTransactionLayout.vue'
import MobileTransactionLayout from './MobileTransactionLayout.vue'

const layoutAktif = shallowRef(DesktopTransactionLayout)

const cekLayar = () => {
    layoutAktif.value =
        window.innerWidth < 1024
            ? MobileTransactionLayout
            : DesktopTransactionLayout
}

onMounted(() => {
    cekLayar()
    window.addEventListener('resize', cekLayar)
})

onUnmounted(() => {
    window.removeEventListener('resize', cekLayar)
})
</script>