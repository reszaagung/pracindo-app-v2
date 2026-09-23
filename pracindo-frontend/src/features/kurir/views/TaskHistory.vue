<template>
    <div class="min-h-screen bg-slate-50 pb-24 text-slate-900">
        <header
            class="sticky top-0 z-20 border-b border-slate-200/80 bg-white/95 px-4 py-3.5 shadow-sm backdrop-blur-xl"
        >
            <div class="mx-auto flex max-w-md items-center justify-between gap-3">
                <div class="min-w-0">
                    <p class="text-[10px] font-extrabold uppercase tracking-[0.14em] text-blue-600">
                        Aktivitas
                    </p>

                    <h1 class="mt-0.5 truncate text-lg font-extrabold tracking-tight text-slate-800">
                        Riwayat Tugas
                    </h1>
                </div>

                <div class="flex shrink-0 items-center gap-2">
                    <div
                        v-if="isRefreshing"
                        class="hidden items-center gap-1.5 rounded-full border border-blue-100 bg-blue-50 px-2.5 py-1.5 text-[10px] font-bold text-blue-600 sm:flex"
                        role="status"
                        aria-live="polite"
                    >
                        <span
                            class="h-1.5 w-1.5 animate-pulse rounded-full bg-blue-500"
                            aria-hidden="true"
                        ></span>
                        Memperbarui...
                    </div>

                    <button
                        type="button"
                        :disabled="loadingHistory"
                        :aria-busy="loadingHistory"
                        :aria-label="
                            isRefreshing
                                ? 'Sedang memperbarui riwayat tugas'
                                : 'Muat ulang riwayat tugas'
                        "
                        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-slate-200 bg-slate-50 text-slate-600 shadow-sm transition hover:bg-slate-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
                        @click="fetchHistory"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-5 w-5"
                            :class="{
                                'animate-spin text-blue-600': loadingHistory,
                                'text-slate-600': !loadingHistory
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
            </div>

            <div
                v-if="isRefreshing"
                class="mx-auto mt-2 flex max-w-md items-center gap-2 text-[11px] font-medium text-blue-600 sm:hidden"
                role="status"
                aria-live="polite"
            >
                <span
                    class="h-1.5 w-1.5 animate-pulse rounded-full bg-blue-500"
                    aria-hidden="true"
                ></span>
                Memperbarui riwayat tugas...
            </div>
        </header>

        <main class="mx-auto flex max-w-md flex-col gap-4 px-4 pt-5">
            <section
                v-if="!initialLoading && historyDeliveries.length > 0"
                class="flex items-center justify-between rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm"
                aria-label="Ringkasan riwayat"
            >
                <div class="flex items-center gap-3">
                    <div
                        class="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-100 text-slate-600"
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

                    <div>
                        <p class="text-[10px] font-semibold uppercase tracking-[0.1em] text-slate-400">
                            Riwayat
                        </p>

                        <p class="text-sm font-extrabold text-slate-800">
                            {{ historyDeliveries.length }} tugas
                        </p>
                    </div>
                </div>

                <span
                    class="rounded-full bg-slate-100 px-2.5 py-1 text-[10px] font-bold text-slate-500"
                >
                    {{ isRefreshing ? 'Sinkronisasi' : 'Tersimpan' }}
                </span>
            </section>

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
                    Memuat riwayat
                </h2>

                <p class="mt-1 text-xs leading-5 text-slate-400">
                    Mengambil data tugas yang telah selesai atau dibatalkan.
                </p>
            </section>

            <section
                v-else-if="error && historyDeliveries.length === 0"
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
                    Riwayat belum dapat dimuat
                </h2>

                <p class="mx-auto mt-1 max-w-xs text-xs leading-5 text-slate-400">
                    {{ error }}
                </p>

                <button
                    type="button"
                    class="mt-5 inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-xs font-bold text-white shadow-sm transition hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-blue-800"
                    @click="fetchHistory"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4"
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

                    Coba Lagi
                </button>
            </section>

            <section
                v-else-if="historyDeliveries.length === 0"
                class="rounded-3xl border border-slate-200 bg-white px-6 py-12 text-center shadow-sm"
                aria-live="polite"
            >
                <div
                    class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-slate-100 text-slate-400"
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
                            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                    </svg>
                </div>

                <h2 class="mt-5 text-base font-extrabold text-slate-800">
                    Belum Ada Riwayat
                </h2>

                <p class="mx-auto mt-1 max-w-xs text-sm leading-6 text-slate-400">
                    Tugas yang sudah selesai atau dibatalkan akan muncul di sini.
                </p>

                <button
                    type="button"
                    :disabled="loadingHistory"
                    class="mt-5 inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-700 shadow-sm transition hover:bg-slate-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
                    @click="fetchHistory"
                >
                    <span
                        v-if="isRefreshing"
                        class="h-3.5 w-3.5 animate-spin rounded-full border-2 border-slate-300 border-t-blue-600"
                        aria-hidden="true"
                    ></span>

                    <svg
                        v-else
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4"
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

                    {{ isRefreshing ? 'Memperbarui...' : 'Periksa Lagi' }}
                </button>
            </section>

            <section
                v-else
                class="flex flex-col gap-3"
                aria-label="Daftar riwayat pengiriman"
                aria-live="polite"
            >
                <div
                    v-if="isRefreshing"
                    class="flex items-center gap-2 rounded-xl border border-blue-100 bg-blue-50 px-3 py-2 text-[11px] font-semibold text-blue-600"
                    role="status"
                >
                    <span
                        class="h-3.5 w-3.5 animate-spin rounded-full border-2 border-blue-200 border-t-blue-600"
                        aria-hidden="true"
                    ></span>

                    Menyegarkan riwayat tanpa menghilangkan data saat ini...
                </div>

                <div
                    class="flex flex-col gap-3 transition-opacity duration-200"
                    :class="{ 'opacity-60': isRefreshing }"
                >
                    <article
                        v-for="delivery in historyDeliveries"
                        :key="delivery.id"
                        class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition-all hover:shadow-md"
                    >
                        <div
                            class="flex items-center justify-between gap-3 border-b border-slate-100 bg-slate-50/80 px-4 py-3"
                        >
                            <div class="min-w-0">
                                <h2
                                    class="truncate text-sm font-extrabold text-slate-800"
                                >
                                    {{ delivery.nomor || 'Pengiriman' }}
                                </h2>

                                <p class="mt-0.5 text-[10px] font-medium text-slate-500">
                                    {{ delivery.tanggal || 'Tanggal tidak tersedia' }}
                                </p>
                            </div>

                            <span
                                class="shrink-0 rounded-full px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-wide"
                                :class="
                                    delivery.status === 'SELESAI'
                                        ? 'bg-emerald-100 text-emerald-700'
                                        : 'bg-rose-100 text-rose-700'
                                "
                            >
                                {{ delivery.status }}
                            </span>
                        </div>

                        <div class="p-4">
                            <div
                                v-if="delivery.status === 'BATAL'"
                                class="mb-3 rounded-xl border border-rose-100 bg-rose-50 p-3"
                            >
                                <div class="flex items-start gap-2">
                                    <div
                                        class="mt-0.5 text-rose-500"
                                        aria-hidden="true"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            class="h-4 w-4"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke="currentColor"
                                            stroke-width="2"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                d="M12 9v4m0 4h.01M10.29 3.86l-7.82 13.5A2 2 0 004.2 20.5h15.6a2 2 0 001.73-3.14l-7.82-13.5a2 2 0 00-3.42 0z"
                                            />
                                        </svg>
                                    </div>

                                    <div>
                                        <p class="text-[10px] font-extrabold uppercase tracking-[0.08em] text-rose-500">
                                            Alasan Pembatalan
                                        </p>

                                        <p class="mt-1 text-xs font-medium leading-5 text-rose-700">
                                            {{ extractBatalReason(delivery.catatan) }}
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <button
                                type="button"
                                :aria-expanded="expandedId === delivery.id"
                                :aria-controls="`history-detail-${delivery.id}`"
                                class="flex w-full items-center justify-between gap-3 rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-3 text-left transition hover:bg-slate-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-slate-200"
                                @click="toggleDetail(delivery.id)"
                            >
                                <div class="flex min-w-0 items-center gap-3">
                                    <div
                                        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white text-slate-500 shadow-sm"
                                        aria-hidden="true"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            class="h-4.5 w-4.5"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                            stroke="currentColor"
                                            stroke-width="1.8"
                                        >
                                            <path
                                                stroke-linecap="round"
                                                stroke-linejoin="round"
                                                d="M9 20l-5-2V6l5 2 6-2 5 2v12l-5-2-6 2zm0-12v12m6-14v12"
                                            />
                                        </svg>
                                    </div>

                                    <div class="min-w-0">
                                        <span class="block text-xs font-extrabold text-slate-700">
                                            {{
                                                expandedId === delivery.id
                                                    ? 'Tutup detail rute'
                                                    : 'Lihat muatan & alamat tujuan'
                                            }}
                                        </span>

                                        <span
                                            v-if="delivery.perhentian?.length"
                                            class="mt-0.5 block text-[10px] text-slate-400"
                                        >
                                            {{ delivery.perhentian.length }}
                                            perhentian
                                        </span>
                                    </div>
                                </div>

                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    class="h-4 w-4 shrink-0 text-slate-400 transition-transform duration-200"
                                    :class="{
                                        'rotate-180': expandedId === delivery.id
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
                                        d="M19 9l-7 7-7-7"
                                    />
                                </svg>
                            </button>

                            <div
                                v-if="expandedId === delivery.id"
                                :id="`history-detail-${delivery.id}`"
                                class="mt-4 border-t border-slate-100 pt-4"
                            >
                                <div
                                    v-if="delivery.perhentian?.length"
                                    class="relative ml-2 border-l-2 border-slate-200"
                                >
                                    <div
                                        v-for="(stop, index) in delivery.perhentian"
                                        :key="stop.id"
                                        class="relative pb-4 pl-5 last:pb-0"
                                    >
                                        <span
                                            class="absolute -left-[7px] top-1.5 h-3 w-3 rounded-full border-2 border-white bg-slate-400 shadow-sm"
                                            aria-hidden="true"
                                        ></span>

                                        <div
                                            class="rounded-xl border border-slate-200 bg-white p-3 shadow-sm"
                                        >
                                            <div class="mb-2 flex items-start justify-between gap-3">
                                                <div class="min-w-0">
                                                    <p class="text-[10px] font-bold uppercase tracking-[0.08em] text-slate-400">
                                                        Tujuan {{ index + 1 }}
                                                    </p>

                                                    <h3 class="mt-0.5 text-sm font-extrabold leading-5 text-slate-700">
                                                        {{
                                                            stop.pelanggan_nama ||
                                                            `Tujuan ${index + 1}`
                                                        }}
                                                    </h3>
                                                </div>

                                                <span
                                                    class="shrink-0 rounded-full px-2 py-1 text-[9px] font-extrabold uppercase tracking-wide"
                                                    :class="
                                                        stop.status === 'DITERIMA'
                                                            ? 'bg-emerald-100 text-emerald-700'
                                                            : stop.status === 'DIRETUR'
                                                              ? 'bg-rose-100 text-rose-700'
                                                              : 'bg-slate-100 text-slate-600'
                                                    "
                                                >
                                                    {{ stop.status || 'PENDING' }}
                                                </span>
                                            </div>

                                            <div class="space-y-2.5">
                                                <div class="flex items-start gap-2.5">
                                                    <div
                                                        class="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-blue-50 text-blue-600"
                                                        aria-hidden="true"
                                                    >
                                                        <svg
                                                            xmlns="http://www.w3.org/2000/svg"
                                                            class="h-3.5 w-3.5"
                                                            fill="none"
                                                            viewBox="0 0 24 24"
                                                            stroke="currentColor"
                                                            stroke-width="1.8"
                                                        >
                                                            <path
                                                                stroke-linecap="round"
                                                                stroke-linejoin="round"
                                                                d="M12 21s7-6.16 7-12a7 7 0 10-14 0c0 5.84 7 12 7 12z"
                                                            />
                                                            <circle
                                                                cx="12"
                                                                cy="9"
                                                                r="2.2"
                                                            />
                                                        </svg>
                                                    </div>

                                                    <div class="min-w-0">
                                                        <p class="text-[9px] font-bold uppercase tracking-[0.08em] text-slate-400">
                                                            Alamat
                                                        </p>

                                                        <p class="mt-0.5 text-xs leading-5 text-slate-600">
                                                            {{
                                                                stop.alamat ||
                                                                'Alamat tidak tersedia'
                                                            }}
                                                        </p>
                                                    </div>
                                                </div>

                                                <div class="flex items-center gap-2.5">
                                                    <div
                                                        class="flex h-6 w-6 shrink-0 items-center justify-center rounded-lg bg-amber-50 text-amber-600"
                                                        aria-hidden="true"
                                                    >
                                                        <svg
                                                            xmlns="http://www.w3.org/2000/svg"
                                                            class="h-3.5 w-3.5"
                                                            fill="none"
                                                            viewBox="0 0 24 24"
                                                            stroke="currentColor"
                                                            stroke-width="1.8"
                                                        >
                                                            <path
                                                                stroke-linecap="round"
                                                                stroke-linejoin="round"
                                                                d="M20 7l-8-4-8 4m16 0v10l-8 4-8-4V7m16 0l-8 4m-8-4l8 4m0 0v10"
                                                            />
                                                        </svg>
                                                    </div>

                                                    <div class="min-w-0">
                                                        <p class="text-[9px] font-bold uppercase tracking-[0.08em] text-slate-400">
                                                            Delivery Order
                                                        </p>

                                                        <p class="mt-0.5 text-xs font-bold text-slate-600">
                                                            {{ stop.nomor_distribusi || 'N/A' }}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div
                                    v-else
                                    class="rounded-xl border border-dashed border-slate-200 bg-slate-50 px-4 py-6 text-center"
                                >
                                    <p class="text-xs font-semibold text-slate-500">
                                        Detail perhentian belum tersedia.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </article>
                </div>
            </section>
        </main>
    </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useKurir } from '../composables/useKurir'

const {
    historyDeliveries,
    loadingHistory,
    error,
    fetchHistory
} = useKurir()

const expandedId = ref(null)

const initialLoading = computed(() => {
    return loadingHistory.value && historyDeliveries.value.length === 0
})

const isRefreshing = computed(() => {
    return loadingHistory.value && historyDeliveries.value.length > 0
})

const toggleDetail = (id) => {
    expandedId.value = expandedId.value === id ? null : id
}

const extractBatalReason = (catatan) => {
    if (!catatan) {
        return 'Dibatalkan oleh sistem/admin.'
    }

    const text = String(catatan)
    const match = text.match(/\[BATAL\](.*)/)

    return match ? match[1].trim() : text
}

onMounted(() => {
    fetchHistory()
})
</script>
