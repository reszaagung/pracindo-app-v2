<template>
    <div class="min-h-screen bg-slate-50 pb-24 text-slate-900">
        <header
            class="sticky top-0 z-20 border-b border-slate-200/80 bg-white/95 px-4 py-3.5 shadow-sm backdrop-blur-xl"
        >
            <div class="mx-auto flex max-w-md items-center justify-between gap-3">
                <div class="min-w-0">
                    <p class="text-[10px] font-extrabold uppercase tracking-[0.14em] text-blue-600">
                        Kurir
                    </p>

                    <h1 class="mt-0.5 truncate text-lg font-extrabold tracking-tight text-slate-800">
                        Permintaan Masuk
                    </h1>
                </div>

                <button
                    type="button"
                    :disabled="loading || isClaiming"
                    :aria-busy="loading || isClaiming"
                    aria-label="Muat ulang daftar permintaan"
                    class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-slate-200 bg-slate-50 text-slate-600 shadow-sm transition hover:bg-slate-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
                    @click="fetchAvailableTasks"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5"
                        :class="{
                            'animate-spin text-blue-600': loading,
                            'text-slate-600': !loading
                        }"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                        aria-hidden="true"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581a8.003 8.003 0 01-15.357-2m15.357 2H15"
                        />
                    </svg>
                </button>
            </div>
        </header>

        <main class="mx-auto flex max-w-md flex-col gap-4 px-4 pt-5">
            <section
                v-if="initialLoading"
                class="rounded-3xl border border-slate-200 bg-white px-6 py-16 text-center shadow-sm"
                aria-live="polite"
                aria-busy="true"
            >
                <div
                    class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-blue-50"
                    aria-hidden="true"
                >
                    <div
                        class="h-8 w-8 animate-spin rounded-full border-[3px] border-blue-200 border-t-blue-600"
                    ></div>
                </div>

                <h2 class="mt-5 text-sm font-extrabold text-slate-800">
                    Memuat permintaan
                </h2>

                <p class="mt-1 text-xs leading-5 text-slate-400">
                    Sedang mengambil daftar pengiriman yang tersedia.
                </p>
            </section>

            <section
                v-else-if="error && availableTasks.length === 0"
                class="rounded-3xl border border-rose-100 bg-white px-6 py-10 text-center shadow-sm"
                role="alert"
            >
                <div
                    class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-rose-50 text-rose-500"
                    aria-hidden="true"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-8 w-8"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="1.8"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M12 9v4m0 4h.01M10.29 3.86l-7.82 13.5A2 2 0 004.2 20.5h15.6a2 2 0 001.73-3.14l-7.82-13.5a2 2 0 00-3.42 0z"
                        />
                    </svg>
                </div>

                <h2 class="mt-5 text-sm font-extrabold text-slate-800">
                    Permintaan belum dapat dimuat
                </h2>

                <p class="mx-auto mt-1 max-w-xs text-xs leading-5 text-slate-400">
                    {{ error }}
                </p>

                <button
                    type="button"
                    class="mt-5 inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-xs font-bold text-white shadow-sm transition hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-blue-800"
                    @click="fetchAvailableTasks"
                >
                    Coba Lagi
                </button>
            </section>

            <section
                v-else-if="availableTasks.length === 0"
                class="rounded-3xl border border-slate-200 bg-white px-6 py-12 text-center shadow-sm"
                aria-live="polite"
            >
                <div
                    class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-blue-50 text-blue-400"
                    aria-hidden="true"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-8 w-8"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="1.8"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
                        />
                    </svg>
                </div>

                <h2 class="mt-5 text-base font-extrabold text-slate-800">
                    Belum Ada Permintaan
                </h2>

                <p class="mx-auto mt-1 max-w-xs text-sm leading-6 text-slate-400">
                    Belum ada pengiriman baru dari gudang saat ini.
                </p>

                <button
                    type="button"
                    :disabled="loading || isClaiming"
                    class="mt-5 inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-700 shadow-sm transition hover:bg-slate-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
                    @click="fetchAvailableTasks"
                >
                    Periksa Lagi
                </button>
            </section>

            <section
                v-else
                class="flex flex-col gap-3"
                aria-label="Daftar permintaan pengiriman"
                aria-live="polite"
            >
                <div
                    v-if="isClaiming"
                    class="flex items-center gap-2 rounded-xl border border-amber-100 bg-amber-50 px-3 py-2 text-[11px] font-semibold text-amber-700"
                    role="status"
                    aria-live="polite"
                >
                    <span
                        class="h-3.5 w-3.5 animate-spin rounded-full border-2 border-amber-200 border-t-amber-600"
                        aria-hidden="true"
                    ></span>

                    Sedang mengambil pengiriman...
                </div>

                <div
                    class="flex flex-col gap-3 transition-opacity duration-200"
                    :class="{ 'opacity-60': isClaiming }"
                >
                    <CardOrderDelivery
                        v-for="task in availableTasks"
                        :key="task.id"
                        :task="task"
                        :claiming="claimingTaskId === task.id"
                        :disabled="isClaiming && claimingTaskId !== task.id"
                        @claim="handleClaim"
                    />
                </div>
            </section>
        </main>
    </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useKurir } from '../composables/useKurir'
import CardOrderDelivery from '../components/CardOrderDelivery.vue'

const {
    availableTasks,
    loading,
    error,
    fetchAvailableTasks,
    claimTask
} = useKurir()

const claimingTaskId = ref(null)

const initialLoading = computed(() => {
    return loading.value && availableTasks.value.length === 0
})

const isClaiming = computed(() => {
    return claimingTaskId.value !== null
})

const handleClaim = async (taskId) => {
    if (claimingTaskId.value !== null) {
        return
    }

    claimingTaskId.value = taskId

    try {
        const result = await claimTask(taskId)

        if (result?.success === false) {
            window.alert(
                result.message || 'Gagal mengambil pengiriman.'
            )
        }
    } catch (err) {
        window.alert(
            err?.response?.data?.detail ||
            err?.response?.data?.message ||
            err?.message ||
            'Gagal mengambil pengiriman.'
        )
    } finally {
        claimingTaskId.value = null
    }
}

onMounted(() => {
    fetchAvailableTasks()
})
</script>