<template>
    <div
        class="relative flex h-screen w-full overflow-hidden bg-[#F8FAFC] font-sans text-slate-700"
    >
        <header
            class="fixed inset-x-0 top-0 z-[999] flex h-16 items-center justify-between border-b border-slate-100 bg-white/95 px-4 shadow-[0_4px_20px_rgba(15,23,42,0.04)] backdrop-blur-xl"
        >
            <div class="flex min-w-0 items-center gap-3">
                <button
                    ref="menuTrigger"
                    type="button"
                    @click="toggleSidebar"
                    :aria-expanded="sidebarAktif"
                    aria-controls="input-entry-sidebar"
                    :aria-label="
                        sidebarAktif
                            ? 'Tutup menu navigasi'
                            : 'Buka menu navigasi'
                    "
                    class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-50 text-slate-600 shadow-sm transition-all duration-200 hover:bg-slate-100 hover:text-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95"
                >
                    <i
                        :class="
                            sidebarAktif
                                ? 'pi pi-times'
                                : 'pi pi-bars'
                        "
                        class="text-lg"
                        aria-hidden="true"
                    ></i>
                </button>

                <div class="min-w-0">
                    <p
                        class="text-[9px] font-extrabold uppercase tracking-[0.14em] text-slate-400"
                    >
                        Warehouse
                    </p>

                    <span
                        class="block truncate text-[15px] font-extrabold tracking-tight text-slate-800"
                    >
                        Input Entry
                    </span>
                </div>
            </div>

            <button
                type="button"
                @click="keDashboard"
                :disabled="isLoggingOut"
                aria-label="Ke Dashboard"
                title="Dashboard"
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-white shadow-md shadow-slate-900/10 transition-all duration-200 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50"
            >
                <i
                    class="pi pi-home text-sm"
                    aria-hidden="true"
                ></i>
            </button>
        </header>

        <Transition name="overlay">
            <button
                v-if="sidebarAktif"
                type="button"
                @click="tutupDiMobile"
                aria-label="Tutup menu navigasi"
                class="fixed inset-0 z-[998] cursor-default bg-slate-950/45 backdrop-blur-[3px]"
            ></button>
        </Transition>

        <aside
            ref="sidebarRef"
            id="input-entry-sidebar"
            class="fixed bottom-2 left-2 top-2 z-[999] flex w-[88px] flex-col items-center justify-between rounded-[28px] border border-slate-100 bg-white/95 py-6 shadow-[0_12px_40px_rgba(15,23,42,0.08)] backdrop-blur-xl transition-transform duration-300 ease-out"
            :class="
                sidebarAktif
                    ? 'translate-x-0'
                    : '-translate-x-[150%]'
            "
            role="dialog"
            aria-modal="true"
            aria-labelledby="input-entry-sidebar-title"
            :aria-hidden="sidebarAktif ? 'false' : 'true'"
        >
            <h2
                id="input-entry-sidebar-title"
                class="sr-only"
            >
                Navigasi Input Entry Warehouse
            </h2>

            <div class="flex w-full flex-col items-center">
                <div class="mb-5 w-full px-4">
                    <button
                        type="button"
                        @click="tutupDiMobile"
                        aria-label="Tutup menu navigasi"
                        title="Tutup"
                        class="flex h-10 w-full items-center justify-center rounded-xl bg-slate-100 text-slate-500 transition-all duration-200 hover:bg-slate-200 hover:text-slate-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95"
                    >
                        <i
                            class="pi pi-times text-sm"
                            aria-hidden="true"
                        ></i>
                    </button>
                </div>

                <div class="mb-5 group relative">
                    <button
                        type="button"
                        @click="keDashboard"
                        :disabled="isLoggingOut"
                        aria-label="Ke Dashboard"
                        title="Dashboard"
                        class="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-900 text-white shadow-md shadow-slate-900/10 transition-all duration-200 hover:-translate-y-0.5 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        <i
                            class="pi pi-home text-lg"
                            aria-hidden="true"
                        ></i>
                    </button>

                    <span
                        class="pointer-events-none absolute left-16 top-1/2 z-50 -translate-y-1/2 translate-x-1 whitespace-nowrap rounded-lg bg-slate-800 px-3 py-1.5 text-[11px] font-semibold text-white opacity-0 shadow-lg transition-all duration-200 group-hover:translate-x-0 group-hover:opacity-100"
                        aria-hidden="true"
                    >
                        Ke Dashboard
                    </span>
                </div>

                <nav
                    class="flex w-full flex-col gap-3 px-4"
                    aria-label="Navigasi Input Entry Warehouse"
                >
                    <button
                        v-for="menu in menus"
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
                        class="group relative mx-auto flex h-12 w-12 items-center justify-center rounded-2xl transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 disabled:cursor-not-allowed"
                        :class="
                            menu.activate
                                ? aktif(menu.rute)
                                    ? 'bg-slate-900 text-white shadow-md shadow-slate-900/15'
                                    : 'text-slate-400 hover:bg-slate-50 hover:text-slate-700'
                                : 'cursor-default text-slate-300'
                        "
                    >
                        <i
                            :class="[
                                'pi',
                                menu.ikon,
                                'text-lg transition-transform duration-200',
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

            <div class="group relative">
                <button
                    type="button"
                    @click="keluar"
                    :disabled="isLoggingOut"
                    :aria-busy="isLoggingOut"
                    aria-label="Keluar dari aplikasi"
                    title="Keluar"
                    class="flex h-11 w-11 items-center justify-center rounded-2xl border border-rose-100 bg-white text-rose-400 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-rose-200 hover:bg-rose-50 hover:text-rose-600 hover:shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-500 focus-visible:ring-offset-2 active:scale-95 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    <i
                        v-if="!isLoggingOut"
                        class="pi pi-power-off text-sm"
                        aria-hidden="true"
                    ></i>

                    <i
                        v-else
                        class="pi pi-spin pi-spinner text-sm"
                        aria-hidden="true"
                    ></i>
                </button>

                <span
                    class="pointer-events-none absolute bottom-1/2 left-16 z-50 translate-y-1/2 translate-x-1 whitespace-nowrap rounded-xl bg-rose-600 px-3 py-2 text-[11px] font-semibold text-white opacity-0 shadow-xl transition-all duration-200 group-hover:translate-x-0 group-hover:opacity-100"
                    aria-hidden="true"
                >
                    {{ isLoggingOut ? 'Keluar...' : 'Keluar' }}
                </span>
            </div>
        </aside>

        <main
            class="custom-scrollbar min-w-0 flex-1 overflow-y-auto px-4 pb-6 pt-20 md:px-6 md:pt-24"
        >
            <div class="mx-auto min-h-full w-full">
                <router-view v-slot="{ Component, route }">
                    <transition
                        name="fade"
                        mode="out-in"
                    >
                        <div
                            :key="route.fullPath"
                            class="w-full"
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
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { useLayout } from '@/composables/useLayout'

const route = useRoute()
const router = useRouter()

const { logout } = useAuth()

const {
    sidebarAktif,
    toggleSidebar,
    tutupDiMobile
} = useLayout()

const menuTrigger = ref(null)
const sidebarRef = ref(null)
const isLoggingOut = ref(false)

const getFocusableElements = () => {
    if (!sidebarRef.value) {
        return []
    }

    return Array.from(
        sidebarRef.value.querySelectorAll(
            'button:not([disabled]), a[href]:not([aria-hidden="true"])'
        )
    ).filter((element) => element.offsetParent !== null)
}

const handleKeydown = (event) => {
    if (!sidebarAktif.value) {
        return
    }

    if (event.key === 'Escape') {
        event.preventDefault()
        tutupDiMobile()
        return
    }

    if (event.key !== 'Tab') {
        return
    }

    const elements = getFocusableElements()

    if (!elements.length) {
        event.preventDefault()
        return
    }

    const first = elements[0]
    const last = elements[elements.length - 1]

    if (
        event.shiftKey &&
        document.activeElement === first
    ) {
        event.preventDefault()
        last.focus()
        return
    }

    if (
        !event.shiftKey &&
        document.activeElement === last
    ) {
        event.preventDefault()
        first.focus()
    }
}

const keDashboard = async () => {
    if (isLoggingOut.value) return

    tutupDiMobile()

    if (route.path === '/') {
        return
    }

    await router.push('/')
}

const klikMenu = async (menu) => {
    if (
        !menu?.activate ||
        !menu?.rute ||
        isLoggingOut.value
    ) {
        return
    }

    if (route.path === menu.rute) {
        tutupDiMobile()
        return
    }

    await router.push(menu.rute)
    tutupDiMobile()
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

watch(
    () => sidebarAktif.value,
    async (open) => {
        if (open) {
            await nextTick()

            const elements = getFocusableElements()

            elements[0]?.focus()

            document.addEventListener(
                'keydown',
                handleKeydown
            )
        } else {
            document.removeEventListener(
                'keydown',
                handleKeydown
            )

            await nextTick()
            menuTrigger.value?.focus()
        }
    }
)

watch(
    () => route.fullPath,
    () => {
        tutupDiMobile()
    }
)

onBeforeUnmount(() => {
    document.removeEventListener(
        'keydown',
        handleKeydown
    )

    tutupDiMobile()
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active,
.overlay-enter-active,
.overlay-leave-active {
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

.overlay-enter-from,
.overlay-leave-to {
    opacity: 0;
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

button:focus-visible,
a:focus-visible {
    outline: 2px solid #0f172a;
    outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
    .fade-enter-active,
    .fade-leave-active,
    .overlay-enter-active,
    .overlay-leave-active {
        transition: none !important;
    }
}
</style>
