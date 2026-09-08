<template>
    <component :is="isMobile ? MobileHelperLayout : HelperLayout" />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import HelperLayout from './HelperLayout.vue'
import MobileHelperLayout from './MobileHelperLayout.vue'

const isMobile = ref(false)

const checkScreen = () => {
    isMobile.value = window.innerWidth < 1024
}

onMounted(() => {
    checkScreen()
    window.addEventListener('resize', checkScreen)
})

onUnmounted(() => {
    window.removeEventListener('resize', checkScreen)
})
</script>