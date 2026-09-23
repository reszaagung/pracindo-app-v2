<template>
    <div class="min-h-screen bg-slate-50 pb-24 text-slate-900">
        <header
            class="sticky top-0 z-20 border-b border-slate-200/80 bg-white/95 px-4 py-3.5 shadow-sm backdrop-blur-xl"
        >
            <div class="mx-auto flex max-w-md items-center justify-between gap-3">
                <div class="min-w-0">
                    <p class="text-[10px] font-extrabold uppercase tracking-[0.14em] text-blue-600">
                        Operasional
                    </p>

                    <h1 class="mt-0.5 truncate text-lg font-extrabold tracking-tight text-slate-800">
                        Tugas Saya
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
                        :disabled="loading"
                        :aria-busy="loading"
                        :aria-label="
                            isRefreshing
                                ? 'Sedang memperbarui tugas saya'
                                : 'Muat ulang tugas saya'
                        "
                        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-slate-200 bg-slate-50 text-slate-600 shadow-sm transition hover:bg-slate-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
                        @click="fetchMyDeliveries"
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
                Memperbarui tugas saya...
            </div>
        </header>

        <main class="mx-auto flex max-w-md flex-col gap-4 px-4 pt-5">
            <section
                v-if="!initialLoading && myDeliveries.length > 0"
                class="flex items-center justify-between rounded-2xl border border-blue-100 bg-gradient-to-r from-blue-50 to-cyan-50 px-4 py-3"
                aria-label="Ringkasan tugas"
            >
                <div class="flex items-center gap-3">
                    <div
                        class="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-blue-600 shadow-sm"
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
                                d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"
                            />
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a2 2 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0"
                            />
                        </svg>
                    </div>

                    <div>
                        <p class="text-[11px] font-semibold uppercase tracking-[0.1em] text-blue-500">
                            Aktif
                        </p>

                        <p class="text-sm font-extrabold text-slate-800">
                            {{ myDeliveries.length }} tugas
                        </p>
                    </div>
                </div>

                <span
                    class="rounded-full bg-white px-2.5 py-1 text-[10px] font-bold text-blue-600 shadow-sm"
                >
                    {{ isRefreshing ? 'Sinkronisasi' : 'Berjalan' }}
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
                    Memuat tugas
                </h2>

                <p class="mt-1 text-xs leading-5 text-slate-400">
                    Mengambil daftar pengiriman yang sedang Anda tangani.
                </p>
            </section>

            <section
                v-else-if="error && myDeliveries.length === 0"
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
                    Tugas belum dapat dimuat
                </h2>

                <p class="mx-auto mt-1 max-w-xs text-xs leading-5 text-slate-400">
                    {{ error }}
                </p>

                <button
                    type="button"
                    class="mt-5 inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-xs font-bold text-white shadow-sm transition hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-blue-800"
                    @click="fetchMyDeliveries"
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
                v-else-if="myDeliveries.length === 0"
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
                            d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"
                        />
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a2 2 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0"
                        />
                    </svg>
                </div>

                <h2 class="mt-5 text-base font-extrabold text-slate-800">
                    Belum Ada Tugas
                </h2>

                <p class="mx-auto mt-1 max-w-xs text-sm leading-6 text-slate-400">
                    Silakan klaim permintaan dari tab Permintaan untuk mulai bertugas.
                </p>

                <button
                    type="button"
                    :disabled="loading"
                    class="mt-5 inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-700 shadow-sm transition hover:bg-slate-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-60"
                    @click="fetchMyDeliveries"
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
                aria-label="Daftar tugas kurir"
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

                    Menyegarkan tugas tanpa menghilangkan data saat ini...
                </div>

                <div
                    class="flex flex-col gap-3 transition-opacity duration-200"
                    :class="{ 'opacity-60': isRefreshing }"
                >
                    <article
                        v-for="delivery in myDeliveries"
                        :key="delivery.id"
                        class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
                    >
                        <div
                            class="flex items-center justify-between gap-3 border-b border-slate-100 bg-slate-50/80 px-4 py-3"
                        >
                            <div class="min-w-0">
                                <p class="text-[10px] font-semibold uppercase tracking-[0.08em] text-slate-400">
                                    Pengiriman
                                </p>

                                <h2 class="mt-0.5 truncate text-sm font-extrabold text-slate-800">
                                    {{ delivery.nomor || 'Nomor tidak tersedia' }}
                                </h2>
                            </div>

                            <span
                                class="shrink-0 rounded-full px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-wide"
                                :class="getBadgeClass(cekStatusSampai(delivery) ? 'SAMPAI' : delivery.status)"
                            >
                                {{ cekStatusSampai(delivery) ? 'SAMPAI' : delivery.status }}
                            </span>
                        </div>

                        <div class="p-4">
                            <div
                                v-if="delivery.status === 'DISIAPKAN' || delivery.status === 'SIAP_KIRIM'"
                                class="rounded-2xl border border-orange-100 bg-orange-50 p-4"
                            >
                                <div class="flex items-start gap-3">
                                    <div
                                        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-orange-600 shadow-sm"
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
                                                d="M3 7h11v10H3zM14 10h3l4 4v3h-7zM5 17a2 2 0 104 0m9 0a2 2 0 104 0"
                                            />
                                        </svg>
                                    </div>

                                    <div class="min-w-0 flex-1">
                                        <p class="text-sm font-extrabold text-orange-800">
                                            Siap Dibawa
                                        </p>

                                        <p class="mt-1 text-xs leading-5 text-orange-700">
                                            Barang sudah siap dibawa. Silakan mulai perjalanan.
                                        </p>
                                    </div>
                                </div>

                                <button
                                    type="button"
                                    class="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-blue-800"
                                    @click="startDelivery(delivery.id)"
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
                                            d="M5 12h14M13 6l6 6-6 6"
                                        />
                                    </svg>

                                    Mulai Perjalanan
                                </button>
                            </div>

                            <div
                                v-else-if="cekStatusSampai(delivery)"
                                class="rounded-2xl border border-emerald-100 bg-emerald-50 p-4"
                            >
                                <div class="flex items-start gap-3">
                                    <div
                                        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-emerald-600 shadow-sm"
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
                                                d="M12 21s7-6.16 7-12a7 7 0 10-14 0c0 5.84 7 12 7 12z"
                                            />
                                            <circle
                                                cx="12"
                                                cy="9"
                                                r="2.2"
                                            />
                                        </svg>
                                    </div>

                                    <div>
                                        <p class="text-sm font-extrabold text-emerald-800">
                                            Sudah Sampai
                                        </p>

                                        <p class="mt-1 text-xs leading-5 text-emerald-700">
                                            Silakan unggah bukti surat jalan atau proses retur.
                                        </p>
                                    </div>
                                </div>

                                <div class="mt-4 grid grid-cols-2 gap-2">
                                    <input
                                        :id="`upload-${delivery.id}`"
                                        type="file"
                                        class="hidden"
                                        accept="image/*"
                                        @change="(event) => handleUpload(event, delivery)"
                                    />

                                    <label
                                        :for="`upload-${delivery.id}`"
                                        class="flex cursor-pointer items-center justify-center gap-2 rounded-xl bg-emerald-600 px-3 py-3 text-xs font-bold text-white transition hover:bg-emerald-700 focus-within:ring-2 focus-within:ring-emerald-500 focus-within:ring-offset-2"
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
                                                d="M3 7h4l2-2h6l2 2h4v12H3z"
                                            />
                                            <circle
                                                cx="12"
                                                cy="13"
                                                r="3"
                                            />
                                        </svg>

                                        Upload Bukti
                                    </label>

                                    <button
                                        type="button"
                                        class="flex items-center justify-center gap-2 rounded-xl border border-rose-200 bg-rose-50 px-3 py-3 text-xs font-bold text-rose-700 transition hover:bg-rose-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-500 focus-visible:ring-offset-2 active:bg-rose-200"
                                        @click="handleRetur(delivery)"
                                    >
                                        Retur
                                    </button>
                                </div>
                            </div>

                            <div
                                v-else-if="delivery.status === 'BERANGKAT'"
                                class="rounded-2xl border border-blue-100 bg-blue-50 p-4"
                            >
                                <div class="flex items-start gap-3">
                                    <div
                                        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-blue-600 shadow-sm"
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
                                                d="M3 7h11v10H3zM14 10h3l4 4v3h-7zM5 17a2 2 0 104 0m9 0a2 2 0 104 0"
                                            />
                                        </svg>
                                    </div>

                                    <div>
                                        <p class="text-sm font-extrabold text-blue-800">
                                            Dalam Perjalanan
                                        </p>

                                        <p class="mt-1 text-xs leading-5 text-blue-700">
                                            Sedang menuju tujuan berikutnya.
                                        </p>
                                    </div>
                                </div>

                                <button
                                    type="button"
                                    class="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-purple-600 px-4 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-purple-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-purple-500 focus-visible:ring-offset-2 active:bg-purple-800"
                                    @click="markArrived(delivery.id, dapatkanIdPerhentian(delivery))"
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
                                            d="M12 21s7-6.16 7-12a7 7 0 10-14 0c0 5.84 7 12 7 12z"
                                        />
                                        <circle
                                            cx="12"
                                            cy="9"
                                            r="2.2"
                                        />
                                    </svg>

                                    Tandai Sudah Sampai
                                </button>
                            </div>

                            <div
                                v-else-if="delivery.status === 'SELESAI'"
                                class="flex items-center gap-3 rounded-2xl border border-emerald-100 bg-emerald-50 p-4"
                            >
                                <div
                                    class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-white text-emerald-600 shadow-sm"
                                    aria-hidden="true"
                                >
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        class="h-5 w-5"
                                        viewBox="0 0 20 20"
                                        fill="currentColor"
                                    >
                                        <path
                                            fill-rule="evenodd"
                                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                            clip-rule="evenodd"
                                        />
                                    </svg>
                                </div>

                                <div>
                                    <p class="text-sm font-extrabold text-emerald-800">
                                        Pengiriman Selesai
                                    </p>

                                    <p class="mt-0.5 text-xs text-emerald-700">
                                        Tugas ini telah diselesaikan.
                                    </p>
                                </div>
                            </div>

                            <button
                                type="button"
                                :aria-expanded="expandedId === delivery.id"
                                :aria-controls="`delivery-detail-${delivery.id}`"
                                class="mt-4 flex w-full items-center justify-between gap-3 rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-3 text-left transition hover:bg-slate-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:bg-slate-200"
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
                                :id="`delivery-detail-${delivery.id}`"
                                class="mt-4 border-t border-slate-100 pt-4"
                            >
                                <div
                                    v-if="delivery.perhentian?.length"
                                    class="relative ml-2 border-l-2 border-blue-200"
                                >
                                    <div
                                        v-for="(stop, index) in delivery.perhentian"
                                        :key="stop.id"
                                        class="relative pb-4 pl-5 last:pb-0"
                                    >
                                        <span
                                            class="absolute -left-[7px] top-1.5 h-3 w-3 rounded-full border-2 border-white"
                                            :class="
                                                stop.status === 'SAMPAI' ||
                                                stop.status === 'DITERIMA'
                                                    ? 'bg-emerald-500'
                                                    : 'bg-blue-500'
                                            "
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
                                                    :class="getBadgeClass(stop.status)"
                                                >
                                                    {{ stop.status || 'MENUNGGU' }}
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
    myDeliveries,
    loading,
    error,
    fetchMyDeliveries,
    startDelivery,
    markArrived,
    uploadProof
} = useKurir()

const expandedId = ref(null)

const initialLoading = computed(() => {
    return loading.value && myDeliveries.value.length === 0
})

const isRefreshing = computed(() => {
    return loading.value && myDeliveries.value.length > 0
})

const toggleDetail = (id) => {
    expandedId.value = expandedId.value === id ? null : id
}

const cekStatusSampai = (delivery) => {
    if (!Array.isArray(delivery?.perhentian)) {
        return false
    }

    return delivery.perhentian.some(
        (perhentian) => perhentian.status === 'SAMPAI'
    )
}

const dapatkanIdPerhentian = (delivery) => {
    if (
        Array.isArray(delivery?.perhentian) &&
        delivery.perhentian.length > 0
    ) {
        const aktif = delivery.perhentian.find(
            (perhentian) =>
                perhentian.status === 'MENUNGGU' ||
                perhentian.status === 'SAMPAI'
        )

        if (aktif) {
            return aktif.id
        }

        return delivery.perhentian[0].id
    }

    return delivery?.perhentian_id || delivery?.id
}

const getBadgeClass = (status) => {
    const warna = {
        MENUNGGU: 'bg-slate-100 text-slate-600',
        DISIAPKAN: 'bg-orange-100 text-orange-700',
        SIAP_KIRIM: 'bg-orange-100 text-orange-700',
        BERANGKAT: 'bg-blue-100 text-blue-700',
        SAMPAI: 'bg-purple-100 text-purple-700',
        DITERIMA: 'bg-emerald-100 text-emerald-700',
        SELESAI: 'bg-emerald-100 text-emerald-700',
        RETUR: 'bg-rose-100 text-rose-700',
        DIRETUR: 'bg-rose-100 text-rose-700'
    }

    return warna[status] || 'bg-slate-100 text-slate-600'
}

const handleUpload = async (event, delivery) => {
    const file = event.target.files?.[0]

    if (!file) {
        return
    }

    const formData = new FormData()
    formData.append('foto', file)

    const perhentianId = dapatkanIdPerhentian(delivery)

    try {
        await uploadProof(
            delivery.id,
            perhentianId,
            formData
        )

        window.alert(
            'Bukti berhasil diunggah! Pengiriman selesai.'
        )
    } catch (error) {
        const pesanDetail =
            error?.response?.data?.foto?.[0] ||
            error?.response?.data?.detail ||
            error?.message ||
            'Gagal mengunggah bukti.'

        window.alert(
            'Gagal mengunggah bukti: ' + pesanDetail
        )
    } finally {
        event.target.value = ''
    }
}

const handleRetur = (delivery) => {
    window.alert(
        `Buka form retur untuk pengiriman ${delivery.nomor}`
    )
}

onMounted(() => {
    fetchMyDeliveries()
})
</script>
