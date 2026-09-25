<template>
    <div
        class="flex h-screen overflow-hidden bg-[#F8FAFC] font-sans text-slate-700"
    >
        <aside
            class="relative z-20 m-4 flex h-[calc(100vh-2rem)] w-[88px] flex-shrink-0 flex-col items-center justify-between rounded-3xl border border-slate-100 bg-white py-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)]"
        >
            <div class="flex w-full flex-col items-center gap-8">
                <nav
                    class="flex w-full flex-col gap-4 px-4"
                    aria-label="Navigasi Produksi"
                >
                    <button
                        v-for="menu in menuProduksi"
                        :key="menu.id"
                        type="button"
                        :disabled="!menu.activate"
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
                        class="group relative mx-auto flex h-12 w-12 items-center justify-center rounded-2xl transition-all duration-300 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 disabled:cursor-not-allowed"
                        :class="
                            menu.activate
                                ? aktif(menu.rute)
                                    ? 'bg-slate-900 text-white shadow-md shadow-slate-900/10'
                                    : 'text-slate-400 hover:bg-slate-50 hover:text-slate-600'
                                : 'cursor-default text-slate-300'
                        "
                    >
                        <i
                            :class="[
                                'pi',
                                menu.ikon,
                                'text-lg lg:text-xl',
                                'transition-transform',
                                menu.activate
                                    ? 'group-hover:scale-110'
                                    : ''
                            ]"
                            aria-hidden="true"
                        ></i>

                        <span
                            class="pointer-events-none absolute left-16 top-1/2 z-50 -translate-y-1/2 translate-x-1 whitespace-nowrap rounded-lg bg-slate-800 px-3 py-1.5 text-xs font-semibold text-white opacity-0 shadow-lg transition-all duration-200 group-hover:translate-x-0 group-hover:opacity-100"
                            aria-hidden="true"
                        >
                            {{ menu.label }}

                            <template v-if="!menu.activate">
                                (Segera)
                            </template>
                        </span>
                    </button>
                </nav>
            </div>

            <div class="relative mb-4 mt-auto flex flex-col items-center gap-4">
                <div class="group relative flex flex-col items-center">
                    <button
                        @click="keDashboard"
                        type="button"
                        aria-label="Ke Dashboard"
                        title="Ke Dashboard"
                        class="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white shadow-sm transition-all hover:border-slate-400 hover:bg-slate-50 active:scale-95 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2"
                    >
                        <i
                            class="pi pi-home text-slate-400 transition-colors group-hover:text-slate-600"
                            aria-hidden="true"
                        ></i>
                    </button>

                    <span
                        class="pointer-events-none absolute -top-10 z-50 whitespace-nowrap rounded-lg bg-slate-800 px-2 py-1 text-[11px] font-semibold text-white opacity-0 shadow-lg transition-opacity group-hover:opacity-100"
                        aria-hidden="true"
                    >
                        Ke Dashboard
                    </span>
                </div>

                <div class="group relative flex flex-col items-center">
                    <button
                        @click="keluar"
                        type="button"
                        aria-label="Keluar"
                        title="Keluar"
                        class="flex h-10 w-10 items-center justify-center rounded-xl border border-rose-100 bg-white shadow-sm transition-all hover:border-rose-400 hover:bg-rose-50 active:scale-95 focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-500 focus-visible:ring-offset-2"
                    >
                        <i
                            class="pi pi-power-off text-rose-400 transition-colors group-hover:text-rose-600"
                            aria-hidden="true"
                        ></i>
                    </button>

                    <span
                        class="pointer-events-none absolute -top-10 z-50 whitespace-nowrap rounded-lg bg-rose-600 px-2 py-1 text-[11px] font-semibold text-white opacity-0 shadow-lg transition-opacity group-hover:opacity-100"
                        aria-hidden="true"
                    >
                        Keluar
                    </span>
                </div>
            </div>
        </aside>

        <main class="custom-scrollbar flex-1 overflow-y-auto p-8">
            <div class="mx-auto w-full max-w-7xl">
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
import { useRouter } from 'vue-router'
import { useNavProduksi } from '../composables/useNavProduksi'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { menuProduksi, aktif } = useNavProduksi()
const { logout } = useAuth()

const keDashboard = () => {
    router.push('/')
}

const klikMenu = (menu) => {
    if (!menu?.activate || !menu?.rute) return

    if (router.currentRoute.value.path === menu.rute) return

    router.push(menu.rute)
}

const keluar = async () => {
    await logout()
    router.push('/login')
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition:
        opacity 0.15s ease,
        transform 0.15s ease;
}

.fade-enter-from {
    opacity: 0;
    transform: translateY(4px);
}

.fade-leave-to {
    opacity: 0;
    transform: translateY(-4px);
}

.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
}

button:focus-visible {
    outline: 2px solid #0f172a;
    outline-offset: 2px;
}
</style>

