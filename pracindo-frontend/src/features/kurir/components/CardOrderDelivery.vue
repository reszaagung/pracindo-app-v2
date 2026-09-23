<template>
    <article
        class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
        :class="{ 'pointer-events-none opacity-70': disabled }"
        :aria-label="`Permintaan pengiriman ${task.nomor || 'baru'}`"
    >
        <div
            class="flex items-center justify-between gap-3 border-b border-slate-100 bg-gradient-to-r from-slate-50 to-white px-4 py-3"
        >
            <div class="min-w-0">
                <p class="text-[10px] font-semibold uppercase tracking-[0.1em] text-slate-400">
                    Permintaan Pengiriman
                </p>

                <h2
                    class="mt-0.5 truncate text-sm font-extrabold text-slate-800 sm:text-base"
                >
                    {{ task.nomor || 'Nomor tidak tersedia' }}
                </h2>
            </div>

            <span
                class="inline-flex shrink-0 items-center gap-1.5 rounded-full border border-blue-100 bg-blue-50 px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-wide text-blue-700"
            >
                <span
                    class="h-1.5 w-1.5 rounded-full bg-blue-500"
                    aria-hidden="true"
                ></span>

                Baru
            </span>
        </div>

        <div class="px-4 py-4">
            <div class="rounded-xl border border-slate-100 bg-slate-50/70 p-3.5">
                <div class="flex items-start gap-3">
                    <div
                        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-slate-500 shadow-sm"
                        aria-hidden="true"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-5 w-5"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            stroke-width="1.8"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                            />
                        </svg>
                    </div>

                    <div class="min-w-0 flex-1">
                        <p class="text-[10px] font-bold uppercase tracking-[0.1em] text-slate-400">
                            Tanggal Dibuat
                        </p>

                        <p class="mt-1 text-sm font-bold text-slate-800">
                            {{ task.tanggal || 'Tanggal tidak tersedia' }}
                        </p>

                        <p class="mt-1 text-[11px] leading-5 text-slate-400">
                            Permintaan ini tersedia untuk segera diambil.
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <div class="border-t border-slate-100 bg-white px-4 pb-4">
            <button
                type="button"
                :disabled="disabled || claiming"
                :aria-busy="claiming"
                :aria-label="
                    claiming
                        ? `Sedang mengambil pengiriman ${task.nomor || ''}`
                        : `Ambil pengiriman ${task.nomor || ''}`
                "
                class="flex w-full items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-extrabold text-white shadow-sm transition focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed"
                :class="
                    claiming
                        ? 'bg-blue-500'
                        : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'
                "
                @click="emit('claim', task.id)"
            >
                <svg
                    v-if="claiming"
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 animate-spin"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                    aria-hidden="true"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M12 3v3m6.36-.36l-2.12 2.12M21 12h-3m.36 6.36l-2.12-2.12M12 21v-3m-6.36-.36l2.12-2.12M3 12h3m-.36-6.36l2.12 2.12"
                    />
                </svg>

                <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="1.8"
                    aria-hidden="true"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
                    />
                </svg>

                <span>
                    {{ claiming ? 'Mengambil Pengiriman...' : 'Ambil Pengiriman' }}
                </span>
            </button>
        </div>
    </article>
</template>

<script setup>
defineProps({
    task: {
        type: Object,
        required: true
    },
    claiming: {
        type: Boolean,
        default: false
    },
    disabled: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['claim'])
</script>