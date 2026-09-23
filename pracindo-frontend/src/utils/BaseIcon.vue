<template>
    <i
        v-if="isPrimeIcon"
        class="pi"
        :class="primeIconClass"
        :style="iconStyle"
        aria-hidden="true"
    ></i>

    <svg
        v-else
        :width="ukuran"
        :height="ukuran"
        :viewBox="viewBox"
        :fill="fill"
        :stroke="stroke"
        :stroke-width="strokeWidth"
        :stroke-linecap="strokeLinecap"
        :stroke-linejoin="strokeLinejoin"
        aria-hidden="true"
    >
        <g v-html="pathIcon"></g>
    </svg>
</template>

<script setup>
import { computed } from 'vue'
import { IKON } from '@/config/modules'

const props = defineProps({
    nama: {
        type: String,
        default: '',
    },
    ukuran: {
        type: [String, Number],
        default: 20,
    },
    warna: {
        type: String,
        default: 'currentColor',
    },
    fill: {
        type: String,
        default: 'none',
    },
    stroke: {
        type: String,
        default: 'currentColor',
    },
    strokeWidth: {
        type: [String, Number],
        default: 1.8,
    },
    strokeLinecap: {
        type: String,
        default: 'round',
    },
    strokeLinejoin: {
        type: String,
        default: 'round',
    },
})

const primeIcons = {
    home: 'pi-home',
    dashboard: 'pi-home',
    search: 'pi-search',
    user: 'pi-user',
    users: 'pi-users',
    settings: 'pi-cog',
    cog: 'pi-cog',
    menu: 'pi-bars',
    close: 'pi-times',
    back: 'pi-arrow-left',
    forward: 'pi-arrow-right',
    plus: 'pi-plus',
    tambah: 'pi-plus',
    trash: 'pi-trash',
    edit: 'pi-pencil',
    check: 'pi-check',
    warning: 'pi-exclamation-triangle',
    info: 'pi-info-circle',
    lock: 'pi-lock',
    logout: 'pi-sign-out',
    refresh: 'pi-refresh',
    download: 'pi-download',
    upload: 'pi-upload',
    box: 'pi-box',
    database: 'pi-database',
    truck: 'pi-truck',
    calendar: 'pi-calendar',
    clock: 'pi-clock',
    history: 'pi-history',
    chart: 'pi-chart-line',
    chartPie: 'pi-chart-pie',
}

const namaNormal = computed(() =>
    String(props.nama || '')
        .trim()
        .replace(/^pi\s+/, '')
        .replace(/^pi-/, '')
)

const isPrimeIcon = computed(() => {
    const value = String(props.nama || '').trim()

    if (value.startsWith('pi pi-')) {
        return true
    }

    if (value.startsWith('pi-')) {
        return true
    }

    return Boolean(primeIcons[namaNormal.value])
})

const primeIconClass = computed(() => {
    const value = String(props.nama || '').trim()

    if (value.startsWith('pi pi-')) {
        return value.replace(/^pi\s+/, '')
    }

    if (value.startsWith('pi-')) {
        return value
    }

    return primeIcons[namaNormal.value] || ''
})

const pathIcon = computed(() => IKON[namaNormal.value] || '')

const viewBox = '0 0 24 24'

const iconStyle = computed(() => ({
    fontSize: `${props.ukuran}px`,
    width: `${props.ukuran}px`,
    height: `${props.ukuran}px`,
    color: props.warna,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
}))
</script>