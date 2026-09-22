<template>
    <header
        class="grid grid-cols-1 lg:grid-cols-[1fr_auto_1fr] items-center gap-4 mb-5"
    >
        <div>
            <div
                class="text-[10px] sm:text-xs font-black tracking-[0.25em] text-slate-500 uppercase"
            >
                PT PRACINDO JAYA MANDIRI
            </div>

            <h1
                class="mt-1 text-2xl sm:text-3xl lg:text-4xl font-black tracking-tight"
            >
                ACCOUNTING IDS
            </h1>

            <div
                class="mt-1 text-xs sm:text-sm text-slate-400"
            >
                INFORMATION DISPLAY SYSTEM
            </div>
        </div>

        <div class="text-center order-first lg:order-none">
            <div
                class="text-3xl sm:text-4xl lg:text-5xl font-black tabular-nums tracking-tight"
            >
                {{ waktu }}
            </div>

            <div
                class="mt-1 text-xs sm:text-sm font-semibold text-slate-400 capitalize"
            >
                {{ tanggal }}
            </div>
        </div>

        <div class="flex lg:justify-end items-center gap-2">
            <div
                class="flex items-center gap-2 px-3 py-2 rounded-xl border border-slate-800 bg-slate-900"
            >
                <span
                    class="w-2.5 h-2.5 rounded-full"
                    :class="
                        memuat
                            ? 'bg-amber-400 animate-pulse'
                            : 'bg-emerald-400'
                    "
                />

                <span class="text-xs font-bold text-slate-300">
                    {{ memuat ? 'SYNC' : 'ONLINE' }}
                </span>
            </div>

            <button
                type="button"
                @click="$emit('toggle-auto-refresh')"
                class="px-3 py-2 rounded-xl border border-slate-800 bg-slate-900 text-xs font-bold"
            >
                AUTO {{ autoRefresh ? 'ON' : 'OFF' }}
            </button>

            <button
                type="button"
                @click="$emit('refresh')"
                :disabled="memuat"
                class="px-3 py-2 rounded-xl bg-white text-slate-950 text-xs font-black disabled:opacity-50"
            >
                REFRESH
            </button>
        </div>
    </header>
</template>

<script setup>
defineProps({
    waktu: {
        type: String,
        default: '--:--:--',
    },
    tanggal: {
        type: String,
        default: '',
    },
    memuat: {
        type: Boolean,
        default: false,
    },
    autoRefresh: {
        type: Boolean,
        default: true,
    },
})

defineEmits([
    'refresh',
    'toggle-auto-refresh',
])
</script>