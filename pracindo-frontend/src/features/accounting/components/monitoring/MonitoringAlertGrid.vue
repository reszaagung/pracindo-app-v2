<template>
    <section class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <article
            v-for="item in items"
            :key="item.label"
            class="rounded-2xl border p-4"
            :class="item.panel"
        >
            <div
                class="text-[10px] font-black tracking-widest"
                :class="item.labelClass"
            >
                {{ item.label }}
            </div>

            <div
                class="mt-1 text-2xl font-black"
                :class="item.valueClass"
            >
                {{ item.value }}
            </div>
        </article>
    </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    normal: {
        type: Number,
        default: 0,
    },
    peringatan: {
        type: Number,
        default: 0,
    },
    jatuhTempo: {
        type: Number,
        default: 0,
    },
    terlambat: {
        type: Number,
        default: 0,
    },
})

const items = computed(() => [
    {
        label: 'NORMAL',
        value: props.normal,
        panel: 'border-emerald-500/10 bg-emerald-950/10',
        labelClass: 'text-emerald-500',
        valueClass: 'text-emerald-300',
    },
    {
        label: 'PERINGATAN',
        value: props.peringatan,
        panel: 'border-amber-500/10 bg-amber-950/10',
        labelClass: 'text-amber-500',
        valueClass: 'text-amber-300',
    },
    {
        label: 'JATUH TEMPO',
        value: props.jatuhTempo,
        panel: 'border-orange-500/10 bg-orange-950/10',
        labelClass: 'text-orange-500',
        valueClass: 'text-orange-300',
    },
    {
        label: 'TERLAMBAT',
        value: props.terlambat,
        panel: 'border-red-500/10 bg-red-950/10',
        labelClass: 'text-red-500',
        valueClass: 'text-red-300',
    },
])
</script>