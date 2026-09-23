<template>
    <div class="min-h-screen bg-slate-50 pb-24 text-slate-900">
        <header
            class="sticky top-0 z-20 border-b border-slate-200/80 bg-white/95 px-4 py-3.5 backdrop-blur-xl"
        >
            <div class="mx-auto flex max-w-md items-center justify-center">
                <h1 class="text-base font-extrabold tracking-tight text-slate-800">
                    Profil Saya
                </h1>
            </div>
        </header>

        <main class="mx-auto flex max-w-md flex-col gap-4 px-4 pt-5">
            <section
                class="relative overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-[0_10px_30px_rgba(15,23,42,0.06)]"
            >
                <div
                    class="absolute inset-x-0 top-0 h-28 bg-gradient-to-br from-blue-600 via-blue-500 to-cyan-500"
                ></div>

                <div
                    class="absolute -right-10 -top-12 h-32 w-32 rounded-full bg-white/10 blur-sm"
                ></div>

                <div
                    class="relative flex flex-col items-center px-6 pb-6 pt-12 text-center"
                >
                    <div
                        class="flex h-24 w-24 items-center justify-center rounded-full border-4 border-white bg-blue-50 text-3xl font-extrabold text-blue-600 shadow-[0_12px_30px_rgba(15,23,42,0.16)]"
                        aria-hidden="true"
                    >
                        {{ userInitial }}
                    </div>

                    <h2 class="mt-4 text-xl font-extrabold tracking-tight text-slate-800">
                        {{ userName }}
                    </h2>

                    <p class="mt-1 text-sm font-medium text-slate-500">
                        Tim Ekspedisi / Kurir
                    </p>

                    <div
                        class="mt-4 inline-flex items-center gap-2 rounded-full border border-emerald-100 bg-emerald-50 px-3.5 py-2 text-xs font-bold text-emerald-700"
                    >
                        <span class="relative flex h-2.5 w-2.5">
                            <span
                                class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60"
                            ></span>
                            <span
                                class="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500"
                            ></span>
                        </span>

                        Aktif Bertugas
                    </div>
                </div>
            </section>

            <section
                class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
                aria-label="Menu profil"
            >
                <button
                    type="button"
                    class="flex w-full items-center justify-between border-b border-slate-100 px-5 py-4 text-left transition hover:bg-slate-50 focus:outline-none focus-visible:bg-slate-50 focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-blue-500 active:bg-slate-100"
                    aria-label="Buka riwayat pengiriman"
                    @click="bukaRiwayat"
                >
                    <div class="flex min-w-0 items-center gap-3.5">
                        <div
                            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600"
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
                            <span
                                class="block truncate text-sm font-bold text-slate-700"
                            >
                                Riwayat Pengiriman
                            </span>

                            <span class="mt-0.5 block text-xs text-slate-400">
                                Lihat perjalanan yang sudah selesai
                            </span>
                        </div>
                    </div>

                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4 shrink-0 text-slate-300"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                        aria-hidden="true"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M9 5l7 7-7 7"
                        />
                    </svg>
                </button>

                <button
                    type="button"
                    class="flex w-full items-center justify-between px-5 py-4 text-left transition hover:bg-rose-50 focus:outline-none focus-visible:bg-rose-50 focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-rose-500 active:bg-rose-100 disabled:cursor-not-allowed disabled:opacity-60"
                    :disabled="isLoggingOut"
                    :aria-busy="isLoggingOut"
                    aria-label="Keluar dari aplikasi"
                    @click="handleLogout"
                >
                    <div class="flex items-center gap-3.5">
                        <div
                            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-rose-50 text-rose-600"
                            aria-hidden="true"
                        >
                            <svg
                                v-if="!isLoggingOut"
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
                                    d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                                />
                            </svg>

                            <svg
                                v-else
                                xmlns="http://www.w3.org/2000/svg"
                                class="h-5 w-5 animate-spin"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                stroke-width="2"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    d="M12 3v3m6.36-.36l-2.12 2.12M21 12h-3m.36 6.36l-2.12-2.12M12 21v-3m-6.36-.36l2.12-2.12M3 12h3m-.36-6.36l2.12 2.12"
                                />
                            </svg>
                        </div>

                        <div>
                            <span class="block text-sm font-bold text-rose-600">
                                {{ isLoggingOut ? 'Keluar...' : 'Keluar' }}
                            </span>

                            <span class="mt-0.5 block text-xs text-rose-300">
                                {{
                                    isLoggingOut
                                        ? 'Membersihkan sesi aplikasi'
                                        : 'Keluar dari akun kurir'
                                }}
                            </span>
                        </div>
                    </div>

                    <svg
                        v-if="!isLoggingOut"
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-4 w-4 text-rose-200"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                        aria-hidden="true"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M9 5l7 7-7 7"
                        />
                    </svg>
                </button>
            </section>

            <section
                class="rounded-2xl border border-slate-200 bg-white px-5 py-4 shadow-sm"
            >
                <div class="flex items-center justify-between gap-4">
                    <div>
                        <p class="text-xs font-semibold uppercase tracking-[0.12em] text-slate-400">
                            Aplikasi
                        </p>

                        <p class="mt-1 text-sm font-bold text-slate-700">
                            Pracindo Kurir
                        </p>
                    </div>

                    <div
                        class="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-bold text-slate-500"
                    >
                        v2.0
                    </div>
                </div>
            </section>

            <p class="pb-2 text-center text-[11px] font-medium text-slate-400">
                Pracindo Kurir App
            </p>
        </main>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggingOut = ref(false)

const loadUserData = () => {
    try {
        return JSON.parse(
            localStorage.getItem('user') ||
            localStorage.getItem('retail_user') ||
            '{}'
        )
    } catch {
        return {}
    }
}

const userData = loadUserData()

const userName = ref(
    userData.nama ||
    userData.username ||
    'Kurir Internal'
)

const userInitial = computed(() => {
    const name = userName.value?.trim()

    if (!name) {
        return 'K'
    }

    return name.charAt(0).toUpperCase()
})

const bukaRiwayat = () => {
    router.push('/kurir/riwayat')
}

const clearAuthStorage = () => {
    const authKeys = [
        'token',
        'user',
        'retail_token',
        'retail_user'
    ]

    authKeys.forEach((key) => {
        localStorage.removeItem(key)
        sessionStorage.removeItem(key)
    })
}

const handleLogout = async () => {
    if (isLoggingOut.value) {
        return
    }

    const confirmLogout = window.confirm(
        'Apakah Anda yakin ingin keluar dari aplikasi?'
    )

    if (!confirmLogout) {
        return
    }

    isLoggingOut.value = true

    try {
        clearAuthStorage()
    } finally {
        await router.replace({
            path: '/login',
            query: {
                logged_out: '1'
            }
        })
    }
}
</script>
