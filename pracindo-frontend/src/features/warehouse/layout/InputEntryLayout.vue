<template>
    <component :is="layoutAktif" />
</template>

<script setup>
import { shallowRef, onMounted, onUnmounted } from 'vue'

import DesktopInputEntryLayout from './DesktopInputEntryLayout.vue'
import MobileInputEntryLayout from './MobileInputEntryLayout.vue'

const layoutAktif = shallowRef(DesktopInputEntryLayout)

let mediaQuery = null

const cekLayar = () => {
    layoutAktif.value =
        window.innerWidth < 1024
            ? MobileInputEntryLayout
            : DesktopInputEntryLayout
}

onMounted(() => {
    mediaQuery = window.matchMedia('(max-width: 1023px)')

    cekLayar()

    mediaQuery.addEventListener(
        'change',
        cekLayar
    )
})

onUnmounted(() => {
    mediaQuery?.removeEventListener(
        'change',
        cekLayar
    )

    mediaQuery = null
})
</script>
