<template>
    <section
        class="rounded-3xl border p-4 sm:p-5 lg:p-6 mb-5"
        :class="panelClass"
    >
        <div
            class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3"
        >
            <div>
                <div
                    class="text-[10px] sm:text-xs font-black tracking-[0.25em] text-slate-500"
                >
                    STATUS KEUANGAN OPERASIONAL
                </div>

                <div class="mt-1 flex items-center gap-3">
                    <span
                        class="w-3 h-3 rounded-full"
                        :class="dotClass"
                    />

                    <span
                        class="text-2xl sm:text-3xl font-black"
                    >
                        {{ status?.label || 'KONDISI NORMAL' }}
                    </span>
                </div>
            </div>

            <div
                class="text-left sm:text-right text-xs text-slate-500"
            >
                DATA TERAKHIR

                <div
                    class="mt-1 text-slate-300 font-bold"
                >
                    {{ terakhirDiperbarui }}
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    status: {
        type: Object,
        default: () => ({
            key: 'NORMAL',
            label: 'KONDISI NORMAL',
        }),
    },
    terakhirDiperbarui: {
        type: String,
        default: '-',
    },
})

const panelClass = computed(() => {
    switch (props.status?.key) {
        case 'KRITIS':
            return 'border-red-500/30 bg-red-950/30'

        case 'JATUH_TEMPO':
            return 'border-orange-500/30 bg-orange-950/20'

        case 'PERINGATAN':
            return 'border-amber-500/30 bg-amber-950/20'

        default:
            return 'border-emerald-500/20 bg-emerald-950/10'
    }
})

const dotClass = computed(() => {
    switch (props.status?.key) {
        case 'KRITIS':
            return 'bg-red-400 animate-pulse'

        case 'JATUH_TEMPO':
            return 'bg-orange-400 animate-pulse'

        case 'PERINGATAN':
            return 'bg-amber-400 animate-pulse'

        default:
            return 'bg-emerald-400'
    }
})
</script>