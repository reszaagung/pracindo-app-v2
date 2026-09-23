<template>
    <div
        class="flex h-screen bg-[#F8FAFC] font-sans text-slate-700 overflow-hidden relative"
    >
        <header
            class="lg:hidden fixed top-0 left-0 right-0 h-16 bg-white/95 backdrop-blur-md shadow-sm z-30 flex items-center justify-between px-4 border-b border-slate-100"
        >
            <div class="flex items-center gap-3 min-w-0">
                <button
                    type="button"
                    @click="toggleSidebar"
                    class="w-10 h-10 rounded-xl bg-slate-50 text-slate-600 hover:bg-slate-100 active:bg-slate-200 transition-colors flex items-center justify-center shrink-0"
                    aria-label="Buka menu"
                >
                    <i class="pi pi-bars text-lg"></i>
                </button>

                <div class="min-w-0">
                    <p class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">
                        Akunting
                    </p>

                    <span class="block font-bold text-slate-800 text-base truncate">
                        Input Transaksi
                    </span>
                </div>
            </div>

            <button
                type="button"
                @click="kembali"
                class="w-10 h-10 bg-slate-900 rounded-xl flex items-center justify-center shadow-md hover:bg-slate-800 active:scale-95 transition-all shrink-0"
                aria-label="Kembali ke dashboard"
            >
                <i class="pi pi-arrow-left text-white text-sm"></i>
            </button>
        </header>

        <div
            v-if="isMobile && sidebarAktif"
            @click="tutupDiMobile"
            class="fixed inset-0 bg-slate-950/45 backdrop-blur-[2px] z-40 lg:hidden"
        ></div>

        <aside
            class="bg-white/95 backdrop-blur-md rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 flex flex-col items-center py-6 flex-shrink-0 justify-between transition-transform duration-300 ease-in-out"
            :class="[
                'lg:relative lg:translate-x-0 lg:w-[88px] lg:h-[calc(100vh-2rem)] lg:m-4 lg:z-20',
                'fixed top-2 bottom-2 left-2 w-[88px] z-50',
                sidebarAktif ? 'translate-x-0' : '-translate-x-[150%]'
            ]"
        >
            <div class="flex flex-col items-center w-full gap-6 lg:gap-8">
                <button
                    type="button"
                    @click="kembali"
                    class="mb-2 cursor-pointer hidden lg:flex w-12 h-12 bg-slate-900 rounded-2xl items-center justify-center shadow-md hover:bg-slate-800 hover:scale-105 transition-all"
                    aria-label="Kembali ke dashboard"
                >
                    <i class="pi pi-arrow-left text-white text-xl"></i>
                </button>

                <nav class="flex flex-col gap-3 lg:gap-4 w-full px-4">
                    <button
                        v-for="menu in transaksi"
                        :key="menu.id"
                        type="button"
                        :disabled="!menu.activate"
                        @click="klikMenu(menu)"
                        class="w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300 relative mx-auto group"
                        :class="
                            menu.activate
                                ? aktif(menu.rute)
                                    ? 'bg-slate-900 text-white shadow-md shadow-slate-900/10'
                                    : 'text-slate-400 hover:bg-slate-50 hover:text-slate-700'
                                : 'text-slate-300 cursor-default'
                        "
                        :aria-label="menu.label"
                    >
                        <i
                            :class="[
                                'pi',
                                menu.ikon,
                                'text-lg lg:text-xl',
                                'transition-transform duration-300',
                                menu.activate
                                    ? 'group-hover:scale-110'
                                    : ''
                            ]"
                        ></i>

                        <span
                            class="absolute left-16 top-1/2 -translate-y-1/2 bg-slate-800 text-white text-[11px] lg:text-xs font-semibold px-3 py-1.5 rounded-lg opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-50 shadow-lg transition-opacity duration-200"
                        >
                            {{ menu.label }}
                            <template v-if="!menu.activate">
                                · segera
                            </template>
                        </span>
                    </button>
                </nav>
            </div>

            <div
                class="mt-auto flex flex-col items-center group relative mb-4"
            >
                <button
                    type="button"
                    @click="keluar"
                    class="w-10 h-10 rounded-xl overflow-hidden cursor-pointer border border-slate-200 hover:border-red-200 bg-white hover:bg-red-50 transition-all shadow-sm flex items-center justify-center active:scale-95"
                    aria-label="Keluar"
                >
                    <i
                        class="pi pi-power-off text-slate-400 group-hover:text-red-500 transition-colors"
                    ></i>
                </button>

                <span
                    class="absolute -top-10 bg-slate-800 text-white text-[11px] font-semibold px-2 py-1 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50 shadow-lg"
                >
                    Keluar
                </span>
            </div>
        </aside>

        <main
            class="flex-1 min-w-0 overflow-y-auto p-4 pt-20 md:p-6 md:pt-24 lg:p-8 custom-scrollbar"
        >
            <div class="mx-auto w-full max-w-[1480px] min-h-full">
                <router-view v-slot="{ Component }">
                    <transition
                        name="fade"
                        mode="out-in"
                    >
                        <component
                            :is="Component"
                            :key="route.fullPath"
                        />
                    </transition>
                </router-view>
            </div>
        </main>
    </div>
</template>

<script setup>
import { watch } from 'vue'
import {
    useRoute,
    useRouter
} from 'vue-router'

import { useAuth } from '@/composables/useAuth'
import { useLayout } from '@/composables/useLayout'
import { useNavTransaksi } from '@/features/accounting/composables/useNavTransaction'

const route = useRoute()
const router = useRouter()

const { logout } = useAuth()

const {
    sidebarAktif,
    isMobile,
    toggleSidebar,
    tutupDiMobile
} = useLayout()

const {
    transaksi,
    aktif
} = useNavTransaksi()

const kembali = () => {
    router.push('/')
}

const klikMenu = (
    menu
) => {
    if (
        !menu?.activate ||
        !menu?.rute
    ) {
        return
    }

    router.push(menu.rute)
    tutupDiMobile()
}

const keluar = async () => {
    await logout()
    router.push('/login')
}

watch(
    () => route.fullPath,
    () => {
        if (isMobile.value) {
            tutupDiMobile()
        }
    }
)
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition:
        opacity 0.18s ease,
        transform 0.18s ease;
}

.fade-enter-from {
    opacity: 0;
    transform: translateY(4px);
}

.fade-leave-to {
    opacity: 0;
    transform: translateY(-4px);
}

.custom-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 transparent;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
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
    .fade-leave-active {
        transition: none;
    }

    .transition-all,
    .transition-colors,
    .transition-transform,
    .transition-opacity {
        transition: none !important;
    }
}
</style>    