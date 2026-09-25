<template>
    <div
        class="relative flex h-screen w-full overflow-hidden bg-[#F8FAFC] font-sans text-slate-700"
    >
        <header
            class="fixed inset-x-0 top-0 z-[999] flex h-14 items-center justify-between border-b border-slate-100 bg-white/90 px-4 shadow-[0_4px_20px_rgba(15,23,42,0.04)] backdrop-blur-xl lg:hidden"
        >
            <div class="flex min-w-0 items-center gap-3">
                <div
                    class="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-slate-900 shadow-sm"
                    aria-hidden="true"
                >
                    <i class="pi pi-box text-[13px] text-white"></i>
                </div>

                <div class="min-w-0">
                    <p class="truncate text-[9px] font-bold uppercase tracking-[0.18em] text-slate-400">
                        Module
                    </p>

                    <span class="block truncate text-[14px] font-extrabold tracking-tight text-slate-800">
                        Distribution
                    </span>
                </div>
            </div>
        </header>

        <aside
            class="relative z-[999] m-4 hidden h-[calc(100vh-2rem)] w-[88px] shrink-0 flex-col items-center justify-between rounded-3xl border border-slate-100 bg-white py-6 shadow-[0_12px_40px_rgba(15,23,42,0.05)] lg:flex"
        >
            <div class="flex w-full flex-col items-center gap-8">
                <button
                    type="button"
                    @click="kembali"
                    aria-label="Kembali ke Dashboard Utama"
                    title="Dashboard Utama"
                    class="group mb-2 flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-900 shadow-md shadow-slate-900/10 transition-all duration-200 hover:-translate-y-0.5 hover:scale-[1.03] hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95"
                >
                    <i
                        class="pi pi-home text-xl text-white transition-transform duration-200 group-hover:-translate-y-0.5"
                        aria-hidden="true"
                    ></i>
                </button>

                <nav
                    class="flex w-full flex-col gap-3 px-4"
                    aria-label="Navigasi Distribution"
                >
                    <button
                        v-for="item in menu"
                        :key="item.id"
                        type="button"
                        :disabled="!item.activate"
                        :aria-current="aktif(item.rute) ? 'page' : undefined"
                        :aria-label="item.activate ? item.label : `${item.label} - Segera`"
                        :title="item.activate ? item.label : `${item.label} - Segera`"
                        @click="klikMenu(item)"
                        class="group relative mx-auto flex h-12 w-12 items-center justify-center rounded-2xl transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2"
                        :class="
                            item.activate
                                ? aktif(item.rute)
                                    ? 'bg-slate-900 text-white shadow-md shadow-slate-900/15'
                                    : 'text-slate-400 hover:-translate-y-0.5 hover:bg-slate-50 hover:text-slate-700'
                                : 'cursor-default text-slate-300'
                        "
                    >
                        <i
                            :class="[
                                'pi',
                                item.ikon,
                                'text-xl',
                                'transition-transform',
                                'duration-200',
                                item.activate
                                    ? 'group-hover:scale-110'
                                    : ''
                            ]"
                            aria-hidden="true"
                        ></i>

                        <span
                            class="pointer-events-none absolute left-[calc(100%+0.75rem)] z-50 whitespace-nowrap rounded-xl bg-slate-900 px-3 py-2 text-[11px] font-bold text-white opacity-0 shadow-xl shadow-slate-900/10 transition-all duration-200 group-hover:translate-x-0 group-hover:opacity-100"
                            :class="
                                item.activate
                                    ? 'translate-x-1'
                                    : 'translate-x-1'
                            "
                            aria-hidden="true"
                        >
                            {{ item.label }}
                            <template v-if="!item.activate">
                                - Segera
                            </template>
                        </span>
                    </button>
                </nav>
            </div>

            <div class="group relative mb-3 flex flex-col items-center">
                <button
                    type="button"
                    @click="keluar"
                    aria-label="Keluar Aplikasi"
                    title="Keluar"
                    :aria-busy="isLoggingOut"
                    :disabled="isLoggingOut"
                    class="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-red-200 hover:bg-red-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2 active:scale-95 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    <i
                        v-if="!isLoggingOut"
                        class="pi pi-power-off text-slate-400 transition-colors group-hover:text-red-500"
                        aria-hidden="true"
                    ></i>

                    <i
                        v-else
                        class="pi pi-spin pi-spinner text-red-500"
                        aria-hidden="true"
                    ></i>
                </button>

                <span
                    class="pointer-events-none absolute -top-11 whitespace-nowrap rounded-lg bg-slate-900 px-2.5 py-1.5 text-[10px] font-bold text-white opacity-0 shadow-lg transition-opacity duration-200 group-hover:opacity-100"
                    aria-hidden="true"
                >
                    {{ isLoggingOut ? 'Keluar...' : 'Keluar' }}
                </span>
            </div>
        </aside>

        <main
            class="relative z-10 h-full w-full flex-1 overflow-y-auto overscroll-contain px-4 pb-28 pt-20 sm:px-5 lg:p-8"
        >
            <div class="mx-auto h-full w-full max-w-7xl">
                <router-view v-slot="{ Component, route }">
                    <transition name="fade" mode="out-in">
                        <div
                            :key="route.fullPath"
                            class="min-h-full w-full"
                        >
                            <component :is="Component" />
                        </div>
                    </transition>
                </router-view>
            </div>
        </main>

        <nav
            class="fixed inset-x-0 bottom-0 z-[999] flex items-center justify-around border-t border-slate-200 bg-white/92 px-2 pt-2.5 shadow-[0_-10px_35px_rgba(15,23,42,0.06)] backdrop-blur-xl lg:hidden"
            :style="{
                paddingBottom:
                    'calc(env(safe-area-inset-bottom, 0px) + 0.75rem)'
            }"
            aria-label="Navigasi utama Distribution"
        >
            <button
                v-for="item in menu"
                :key="item.id"
                type="button"
                :disabled="!item.activate"
                :aria-current="aktif(item.rute) ? 'page' : undefined"
                :aria-label="item.activate ? item.label : `${item.label} - Segera`"
                @click="klikMenu(item)"
                class="relative flex w-[22%] flex-col items-center justify-center gap-1 rounded-2xl px-1 py-1.5 transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-1"
                :class="
                    item.activate
                        ? aktif(item.rute)
                            ? 'text-slate-900'
                            : 'text-slate-400 active:scale-95'
                        : 'cursor-default text-slate-300 opacity-50'
                "
            >
                <span
                    class="absolute top-0 h-1 w-7 rounded-full transition-all duration-200"
                    :class="
                        aktif(item.rute)
                            ? 'bg-slate-900 opacity-100'
                            : 'bg-transparent opacity-0'
                    "
                    aria-hidden="true"
                ></span>

                <span
                    class="flex h-8 w-10 items-center justify-center rounded-xl transition-all duration-200"
                    :class="
                        aktif(item.rute)
                            ? 'bg-slate-100'
                            : 'bg-transparent'
                    "
                >
                    <i
                        :class="[
                            'pi',
                            item.ikon,
                            'text-[21px]',
                            'transition-transform',
                            'duration-200',
                            aktif(item.rute)
                                ? 'scale-110 font-bold -translate-y-0.5'
                                : ''
                        ]"
                        aria-hidden="true"
                    ></i>
                </span>

                <span
                    class="w-full truncate text-center text-[9px] font-extrabold tracking-wide transition-opacity duration-200"
                    :class="
                        aktif(item.rute)
                            ? 'opacity-100'
                            : 'opacity-70'
                    "
                >
                    {{ item.label }}
                </span>
            </button>
        </nav>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { useNavDistribution } from '../composables/useNavDistribution'

const route = useRoute()
const router = useRouter()
const { logout } = useAuth()
const { menu, aktif } = useNavDistribution()

const isLoggingOut = ref(false)

const kembali = () => {
    router.push('/')
}

const klikMenu = (item) => {
    if (!item.activate) return
    router.push(item.rute)
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
        opacity 0.25s ease-out,
        transform 0.25s ease-out;
}

.fade-enter-from {
    opacity: 0;
    transform: translateY(10px);
}

.fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}

.custom-scrollbar::-webkit-scrollbar {
    width: 4px;
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
    * {
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
    }
}
</style>
