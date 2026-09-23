<template>
    <section
        class="relative z-10 mx-4 -mt-8 overflow-hidden rounded-2xl border border-slate-200 bg-white p-3 shadow-[0_10px_30px_rgba(15,23,42,0.08)] sm:p-4"
        aria-label="Ringkasan aktivitas kurir"
        :aria-busy="loading"
    >
        <div
            class="grid grid-cols-1 min-[360px]:grid-cols-2 min-[360px]:divide-x min-[360px]:divide-slate-200"
        >
            <div
                class="flex min-w-0 items-center gap-3 px-2 py-2 min-[360px]:pr-3 sm:px-0 sm:pr-4"
            >
                <template v-if="loading">
                    <div
                        class="h-11 w-11 shrink-0 animate-pulse rounded-xl bg-slate-200"
                        aria-hidden="true"
                    ></div>

                    <div class="min-w-0 flex-1 space-y-2">
                        <div
                            class="h-2.5 w-16 animate-pulse rounded bg-slate-200"
                            aria-hidden="true"
                        ></div>

                        <div
                            class="h-5 w-20 animate-pulse rounded bg-slate-200"
                            aria-hidden="true"
                        ></div>
                    </div>
                </template>

                <template v-else>
                    <div
                        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600"
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
                                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                        </svg>
                    </div>

                    <div class="min-w-0">
                        <p
                            class="truncate text-[10px] font-bold uppercase tracking-[0.1em] text-slate-400"
                        >
                            Selesai
                        </p>

                        <p class="mt-0.5 flex flex-wrap items-baseline gap-x-1">
                            <span
                                class="text-xl font-extrabold tracking-tight text-slate-800 sm:text-2xl"
                            >
                                {{ selesai }}
                            </span>

                            <span class="text-xs font-medium text-slate-400">
                                tugas
                            </span>
                        </p>
                    </div>
                </template>
            </div>

            <div
                class="flex min-w-0 items-center gap-3 border-t border-slate-100 px-2 py-2 min-[360px]:border-t-0 min-[360px]:pl-3 sm:px-0 sm:pl-4"
            >
                <template v-if="loading">
                    <div
                        class="h-11 w-11 shrink-0 animate-pulse rounded-xl bg-slate-200"
                        aria-hidden="true"
                    ></div>

                    <div class="min-w-0 flex-1 space-y-2">
                        <div
                            class="h-2.5 w-12 animate-pulse rounded bg-slate-200"
                            aria-hidden="true"
                        ></div>

                        <div
                            class="h-5 w-20 animate-pulse rounded bg-slate-200"
                            aria-hidden="true"
                        ></div>
                    </div>
                </template>

                <template v-else>
                    <div
                        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-orange-50 text-orange-600"
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
                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                        </svg>
                    </div>

                    <div class="min-w-0">
                        <p
                            class="flex items-center gap-1.5 truncate text-[10px] font-bold uppercase tracking-[0.1em] text-slate-400"
                        >
                            Aktif

                            <span
                                v-if="aktif > 0"
                                class="h-1.5 w-1.5 animate-pulse rounded-full bg-orange-500"
                                aria-hidden="true"
                            ></span>
                        </p>

                        <p class="mt-0.5 flex flex-wrap items-baseline gap-x-1">
                            <span
                                class="text-xl font-extrabold tracking-tight text-slate-800 sm:text-2xl"
                            >
                                {{ aktif }}
                            </span>

                            <span class="text-xs font-medium text-slate-400">
                                jalan
                            </span>
                        </p>
                    </div>
                </template>
            </div>
        </div>
    </section>
</template>

<script setup>
defineProps({
    selesai: {
        type: Number,
        default: 0
    },
    aktif: {
        type: Number,
        default: 0
    },
    loading: {
        type: Boolean,
        default: false
    }
})
</script>
