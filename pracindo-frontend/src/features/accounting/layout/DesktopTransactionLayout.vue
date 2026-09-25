<template>
    <div
        class="relative flex h-screen w-full overflow-hidden bg-[#F8FAFC] font-sans text-slate-700"
    >
        <aside
            class="relative z-20 m-4 flex h-[calc(100vh-2rem)] w-[88px] flex-shrink-0 flex-col items-center justify-between rounded-3xl border border-slate-100 bg-white/95 py-6 shadow-[0_8px_30px_rgb(15,23,42,0.04)] backdrop-blur-xl"
        >
            <div class="flex w-full flex-col items-center gap-8">
                <nav
                    class="flex w-full flex-col gap-3 px-4"
                    aria-label="Navigasi transaksi akunting"
                >
                    <button
                        v-for="menu in transaksi"
                        :key="menu.id"
                        type="button"
                        :disabled="!menu.activate || isLoggingOut"
                        :aria-current="
                            aktif(menu.rute)
                                ? 'page'
                                : undefined
                        "
                        :aria-label="
                            menu.activate
                                ? menu.label
                                : `${menu.label} - Segera`
                        "
                        :title="
                            menu.activate
                                ? menu.label
                                : `${menu.label} - Segera`
                        "
                        @click="klikMenu(menu)"
                        class="group relative mx-auto flex h-12 w-12 items-center justify-center rounded-2xl transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2"
                        :class="
                            menu.activate
                                ? aktif(menu.rute)
                                    ? 'bg-slate-900 text-white shadow-md shadow-slate-900/15'
                                    : 'text-slate-400 hover:-translate-y-0.5 hover:bg-slate-50 hover:text-slate-700'
                                : 'cursor-default text-slate-300'
                        "
                    >
                        <span
                            class="absolute -left-1 top-1/2 h-6 w-1 -translate-y-1/2 rounded-full transition-all duration-200"
                            :class="
                                aktif(menu.rute)
                                    ? 'bg-slate-900 opacity-100'
                                    : 'bg-transparent opacity-0'
                            "
                            aria-hidden="true"
                        ></span>

                        <i
                            :class="[
                                'pi',
                                menu.ikon,
                                'text-xl',
                                'transition-transform duration-200',
                                menu.activate
                                    ? 'group-hover:scale-110'
                                    : ''
                            ]"
                            aria-hidden="true"
                        ></i>

                        <span
                            class="pointer-events-none absolute left-16 top-1/2 z-50 -translate-y-1/2 translate-x-1 whitespace-nowrap rounded-xl bg-slate-900 px-3 py-2 text-[10px] font-bold text-white opacity-0 shadow-xl shadow-slate-900/10 transition-all duration-200 group-hover:translate-x-0 group-hover:opacity-100"
                            aria-hidden="true"
                        >
                            {{ menu.label }}
                            <template v-if="!menu.activate">
                                · segera
                            </template>
                        </span>
                    </button>
                </nav>
            </div>

            <div class="flex flex-col items-center gap-4">
                <div class="group relative flex flex-col items-center">
                    <button
                        type="button"
                        @click="keDashboard"
                        :disabled="isLoggingOut"
                        aria-label="Kembali ke Dashboard"
                        title="Dashboard"
                        class="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-slate-400 hover:bg-slate-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        <i
                            class="pi pi-home text-slate-400 transition-colors duration-200 group-hover:text-slate-600"
                            aria-hidden="true"
                        ></i>
                    </button>

                    <span
                        class="pointer-events-none absolute -top-10 z-50 whitespace-nowrap rounded-lg bg-slate-800 px-2.5 py-1.5 text-[11px] font-semibold text-white opacity-0 shadow-lg transition-opacity duration-200 group-hover:opacity-100"
                        aria-hidden="true"
                    >
                        Ke Dashboard
                    </span>
                </div>

                <div class="group relative flex flex-col items-center">
                    <button
                        type="button"
                        @click="keluar"
                        :disabled="isLoggingOut"
                        :aria-busy="isLoggingOut"
                        aria-label="Keluar dari aplikasi"
                        title="Keluar"
                        class="flex h-10 w-10 items-center justify-center rounded-xl border border-rose-100 bg-white shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-rose-400 hover:bg-rose-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-500 focus-visible:ring-offset-2 active:scale-95 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                        <i
                            v-if="!isLoggingOut"
                            class="pi pi-power-off text-rose-400 transition-colors duration-200 group-hover:text-rose-600"
                            aria-hidden="true"
                        ></i>

                        <i
                            v-else
                            class="pi pi-spin pi-spinner text-rose-500"
                            aria-hidden="true"
                        ></i>
                    </button>

                    <span
                        class="pointer-events-none absolute -top-10 z-50 whitespace-nowrap rounded-lg bg-rose-600 px-2.5 py-1.5 text-[11px] font-semibold text-white opacity-0 shadow-lg transition-opacity duration-200 group-hover:opacity-100"
                        aria-hidden="true"
                    >
                        {{ isLoggingOut ? 'Keluar...' : 'Keluar' }}
                    </span>
                </div>
            </div>
        </aside>

        <main class="custom-scrollbar min-w-0 flex-1 overflow-y-auto p-8">
            <div class="mx-auto min-h-full w-full max-w-[1480px]">
                <router-view v-slot="{ Component }">
                    <transition
                        name="fade"
                        mode="out-in"
                    >
                        <div
                            :key="$route.fullPath"
                            class="min-h-full w-full"
                        >
                            <component :is="Component" />
                        </div>
                    </transition>
                </router-view>
            </div>
        </main>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { useNavTransaksi } from '@/features/accounting/composables/useNavTransaction'

const route = useRoute()
const router = useRouter()

const { logout } = useAuth()
const { transaksi, aktif } = useNavTransaksi()

const isLoggingOut = ref(false)

const kembali = () => {
    if (isLoggingOut.value) return

    if (window.history.length > 2) {
        router.back()
    } else {
        router.push('/accounting')
    }
}

const keDashboard = () => {
    if (isLoggingOut.value) return
    router.push('/')
}

const klikMenu = (menu) => {
    if (
        !menu?.activate ||
        !menu?.rute ||
        isLoggingOut.value
    ) {
        return
    }

    if (route.path === menu.rute) {
        return
    }

    router.push(menu.rute)
}

const keluar = async () => {
    if (isLoggingOut.value) return

    isLoggingOut.value = true

    try {
        await logout()
        await router.push('/login')
    } finally {
        isLoggingOut.value = false
    }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition:
        opacity 0.2s ease,
        transform 0.2s ease;
}

.fade-enter-from {
    opacity: 0;
    transform: translateY(6px);
}

.fade-leave-to {
    opacity: 0;
    transform: translateY(-6px);
}

.custom-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 transparent;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 999px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

@media (prefers-reduced-motion: reduce) {
    .fade-enter-active,
    .fade-leave-active,
    .transition-all,
    .transition-colors,
    .transition-transform,
    .transition-opacity {
        animation: none !important;
        transition: none !important;
    }
}
</style>