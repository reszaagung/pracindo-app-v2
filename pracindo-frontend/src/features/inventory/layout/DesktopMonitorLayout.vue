<template>
    <div
        class="flex h-screen w-full overflow-hidden bg-[#F8FAFC] font-sans text-slate-700"
    >
        <aside
            class="relative z-20 m-4 flex h-[calc(100vh-2rem)] w-[88px] flex-shrink-0 flex-col items-center justify-between rounded-[28px] border border-slate-200/80 bg-white py-5 shadow-[0_12px_40px_rgba(15,23,42,0.08)]"
        >
            <div class="flex w-full flex-col items-center">
                <div class="mb-7">
                    
                </div>

                <nav class="flex w-full flex-col gap-2.5 px-4">
                    <button
                        v-for="item in menu"
                        :key="item.id"
                        type="button"
                        :disabled="!item.activate"
                        @click="klikMenu(item)"
                        class="group relative mx-auto flex h-12 w-12 items-center justify-center rounded-2xl transition-all duration-200"
                        :class="[
                            item.activate
                                ? (
                                    aktif(item.rute)
                                        ? 'bg-slate-900 text-white shadow-[0_7px_18px_rgba(15,23,42,0.18)]'
                                        : 'text-slate-400 hover:bg-slate-50 hover:text-slate-700'
                                )
                                : 'cursor-default text-slate-300'
                        ]"
                    >
                        <span
                            v-if="item.activate && aktif(item.rute)"
                            class="absolute -left-[18px] top-1/2 h-6 w-1 -translate-y-1/2 rounded-r-full bg-emerald-500"
                        ></span>

                        <i
                            :class="[
                                'pi',
                                item.ikon,
                                'text-lg transition-transform duration-200',
                                item.activate
                                    ? 'group-hover:scale-110'
                                    : ''
                            ]"
                        ></i>

                        <span
                            class="pointer-events-none absolute left-16 top-1/2 z-50 -translate-y-1/2 whitespace-nowrap rounded-xl bg-slate-900 px-3 py-2 text-[11px] font-semibold text-white opacity-0 shadow-xl transition-all duration-200 group-hover:translate-x-1 group-hover:opacity-100"
                        >
                            {{ item.label }}

                            <template v-if="!item.activate">
                                <span class="ml-1 text-slate-400">
                                    · Segera
                                </span>
                            </template>
                        </span>

                        <span
                            v-if="item.activate && aktif(item.rute)"
                            class="pointer-events-none absolute inset-0 rounded-2xl ring-1 ring-white/10"
                        ></span>
                    </button>
                </nav>
            </div>

            <div class="flex w-full flex-col items-center gap-3 px-4">
                <div class="mb-1 h-px w-8 bg-slate-100"></div>

                <div class="group relative">
                    <button
                        type="button"
                        @click="keDashboard"
                        aria-label="Ke Dashboard"
                        title="Dashboard"
                        class="flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-200 bg-white text-slate-400 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-slate-300 hover:bg-slate-50 hover:text-slate-700 hover:shadow-md active:scale-95"
                    >
                        <i class="pi pi-home text-sm"></i>
                    </button>

                    <span
                        class="pointer-events-none absolute bottom-1/2 left-16 z-50 translate-y-1/2 whitespace-nowrap rounded-xl bg-slate-900 px-3 py-2 text-[11px] font-semibold text-white opacity-0 shadow-xl transition-all duration-200 group-hover:translate-x-1 group-hover:opacity-100"
                    >
                        Ke Dashboard
                    </span>
                </div>

                <div class="group relative">
                    <button
                        type="button"
                        @click="keluar"
                        aria-label="Keluar Aplikasi"
                        title="Keluar"
                        class="flex h-11 w-11 items-center justify-center rounded-2xl border border-rose-100 bg-white text-rose-400 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-rose-200 hover:bg-rose-50 hover:text-rose-600 hover:shadow-md active:scale-95"
                    >
                        <i class="pi pi-power-off text-sm"></i>
                    </button>

                    <span
                        class="pointer-events-none absolute bottom-1/2 left-16 z-50 translate-y-1/2 whitespace-nowrap rounded-xl bg-rose-600 px-3 py-2 text-[11px] font-semibold text-white opacity-0 shadow-xl transition-all duration-200 group-hover:translate-x-1 group-hover:opacity-100"
                    >
                        Keluar
                    </span>
                </div>
            </div>
        </aside>

        <main class="custom-scrollbar relative flex-1 overflow-y-auto px-8 py-8">
            <div class="mx-auto min-h-full w-full max-w-[1480px]">
                <router-view v-slot="{ Component, route }">
                    <Transition name="page" mode="out-in">
                        <div
                            :key="route.fullPath"
                            class="w-full"
                        >
                            <component :is="Component" />
                        </div>
                    </Transition>
                </router-view>
            </div>
        </main>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { useNavMonitorLayout } from '../composables/useNavMonitorLayout'

const router = useRouter()

const { logout } = useAuth()

const {
    menu,
    aktif
} = useNavMonitorLayout()

const keDashboard = () => {
    router.push('/')
}

const klikMenu = (item) => {
    if (!item?.activate || !item?.rute) {
        return
    }

    if (router.currentRoute.value.path === item.rute) {
        return
    }

    router.push(item.rute)
}

const keluar = async () => {
    await logout()
    router.push('/login')
}
</script>

<style scoped>
.page-enter-active,
.page-leave-active {
    transition:
        opacity 0.25s ease-out,
        transform 0.25s ease-out;
}

.page-enter-from {
    opacity: 0;
    transform: translateY(8px);
}

.page-leave-to {
    opacity: 0;
    transform: translateY(-6px);
}

.custom-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 transparent;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 7px;
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

button:focus-visible {
    outline: 2px solid #10b981;
    outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
    .page-enter-active,
    .page-leave-active {
        transition: none;
    }

    *,
    *::before,
    *::after {
        scroll-behavior: auto !important;
    }
}
</style>
