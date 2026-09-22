<template>
    <section class="grid grid-cols-2 xl:grid-cols-4 gap-3 sm:gap-4">
        <article
            v-for="item in items"
            :key="item.key"
            class="rounded-2xl border p-4 sm:p-5"
            :class="item.class"
        >
            <div
                class="text-[10px] sm:text-xs font-black tracking-widest uppercase"
                :class="item.labelClass"
            >
                {{ item.label }}
            </div>

            <div
                class="mt-2 text-xl sm:text-3xl lg:text-4xl font-black tabular-nums truncate"
                :class="item.valueClass"
            >
                {{ item.value }}
            </div>

            <div
                v-if="item.caption"
                class="mt-1 text-xs text-slate-500 truncate"
            >
                {{ item.caption }}
            </div>
        </article>
    </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    saldoKas: {
        type: String,
        default: 'Rp0',
    },
    jumlahTagihan: {
        type: Number,
        default: 0,
    },
    totalTagihan: {
        type: String,
        default: 'Rp0',
    },
    peringatan: {
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
        key: 'kas',
        label: 'Saldo Kas',
        value: props.saldoKas,
        caption: 'Saldo rekening kas',
        class: 'border-slate-800 bg-slate-900',
        labelClass: 'text-slate-500',
        valueClass: 'text-white',
    },
    {
        key: 'tagihan',
        label: 'Tagihan Terbuka',
        value: props.jumlahTagihan,
        caption: props.totalTagihan,
        class: 'border-slate-800 bg-slate-900',
        labelClass: 'text-slate-500',
        valueClass: 'text-white',
    },
    {
        key: 'peringatan',
        label: 'Peringatan',
        value: props.peringatan,
        caption: 'Mendekati jatuh tempo',
        class: 'border-amber-500/20 bg-amber-950/20',
        labelClass: 'text-amber-500',
        valueClass: 'text-amber-300',
    },
    {
        key: 'terlambat',
        label: 'Terlambat',
        value: props.terlambat,
        caption: 'Perlu tindak lanjut',
        class: 'border-red-500/20 bg-red-950/20',
        labelClass: 'text-red-500',
        valueClass: 'text-red-300',
    },
])
</script>