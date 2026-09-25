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
                    aria-controls="warehouse-sidebar"
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
                        Modul Gudang
                    </span>
                </div>
            </div>

            <button
                type="button"
                @click="kembali"
                aria-label="Kembali ke halaman sebelumnya"
                title="Kembali"
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-white shadow-md shadow-slate-900/10 transition-all duration-200 hover:-translate-y-0.5 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95"
            >
                <i
                    class="pi pi-arrow-left text-sm"
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
            id="warehouse-sidebar"
            class="fixed bottom-2 left-2 top-2 z-[999] flex w-[88px] flex-col items-center justify-between rounded-[28px] border border-slate-100 bg-white/95 py-6 shadow-[0_12px_40px_rgba(15,23,42,0.08)] backdrop-blur-xl transition-transform duration-300 ease-out"
            :class="
                sidebarAktif
                    ? 'translate-x-0'
                    : '-translate-x-[150%]'
            "
            role="dialog"
            aria-modal="true"
            aria-labelledby="warehouse-sidebar-title"
            :aria-hidden="sidebarAktif ? 'false' : 'true'"
        >
            <h2
                id="warehouse-sidebar-title"
                class="sr-only"
            >
                Menu Modul Gudang
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

                <nav
                    class="flex w-full flex-col gap-3 px-4"
                    aria-label="Navigasi Modul Gudang"
                >
                    <router-link
                        to="/warehouse"
                        exact-active-class="bg-slate-900 text-white shadow-[0_7px_18px_rgba(15,23,42,0.18)]"
                        @click="tutupDiMobile"
                        aria-label="Posisi Gudang"
                        title="Posisi Gudang"
                        class="group relative mx-auto flex h-12 w-12 items-center justify-center rounded-2xl text-slate-400 transition-all duration-200 hover:bg-slate-50 hover:text-slate-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95"
                    >
                        <i
                            class="pi pi-box text-lg transition-transform duration-200 group-hover:scale-110"
                            aria-hidden="true"
                        ></i>

                        <span
                            class="pointer-events-none absolute left-16 top-1/2 z-50 -translate-y-1/2 translate-x-1 whitespace-nowrap rounded-xl bg-slate-900 px-3 py-2 text-[11px] font-semibold text-white opacity-0 shadow-xl transition-all duration-200 group-hover:translate-x-0 group-hover:opacity-100"
                            aria-hidden="true"
                        >
                            Posisi Gudang
                        </span>
                    </router-link>

                    <router-link
                        to="/warehouse/selisih"
                        active-class="bg-slate-900 text-white shadow-[0_7px_18px_rgba(15,23,42,0.18)]"
                        @click="tutupDiMobile"
                        aria-label="Selisih dan Retur"
                        title="Selisih dan Retur"
                        class="group relative mx-auto flex h-12 w-12 items-center justify-center rounded-2xl text-slate-400 transition-all duration-200 hover:bg-slate-50 hover:text-slate-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95"
                    >
                        <i
                            class="pi pi-exclamation-triangle text-lg transition-transform duration-200 group-hover:scale-110"
                            aria-hidden="true"
                        ></i>

                        <span
                            class="pointer-events-none absolute left-16 top-1/2 z-50 -translate-y-1/2 translate-x-1 whitespace-nowrap rounded-xl bg-slate-900 px-3 py-2 text-[11px] font-semibold text-white opacity-0 shadow-xl transition-all duration-200 group-hover:translate-x-0 group-hover:opacity-100"
                            aria-hidden="true"
                        >
                            Selisih / Retur
                        </span>
                    </router-link>
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
                        class="flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-200 bg-white text-slate-400 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-slate-300 hover:bg-slate-50 hover:text-slate-700 hover:shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95"
                    >
                        <i
                            class="pi pi-home text-sm"
                            aria-hidden="true"
                        ></i>

                        <span class="sr-only">
                            Ke Dashboard
                        </span>
                    </button>

                    <span
                        class="pointer-events-none absolute bottom-1/2 left-16 z-50 translate-y-1/2 whitespace-nowrap rounded-xl bg-slate-900 px-3 py-2 text-[11px] font-semibold text-white opacity-0 shadow-xl transition-all duration-200 group-hover:translate-x-1 group-hover:opacity-100"
                        aria-hidden="true"
                    >
                        Ke Dashboard
                    </span>
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
                        class="pointer-events-none absolute bottom-1/2 left-16 z-50 translate-y-1/2 whitespace-nowrap rounded-xl bg-rose-600 px-3 py-2 text-[11px] font-semibold text-white opacity-0 shadow-xl transition-all duration-200 group-hover:translate-x-1 group-hover:opacity-100"
                        aria-hidden="true"
                    >
                        {{ isLoggingOut ? 'Keluar...' : 'Keluar' }}
                    </span>
                </div>
            </div>
        </aside>

        <main
            class="custom-scrollbar relative min-w-0 flex-1 overflow-y-auto px-4 pb-6 pt-20"
        >
            <div class="mx-auto min-h-full w-full">
                <router-view v-slot="{ Component, route }">
                    <Transition
                        name="page"
                        mode="out-in"
                    >
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
            'button:not([disabled]), a[href]'
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

const kembali = () => {
    if (window.history.length > 2) {
        router.back()
    } else {
        router.push('/')
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
.page-enter-active,
.page-leave-active,
.overlay-enter-active,
.overlay-leave-active {
    transition:
        opacity 0.2s ease,
        transform 0.2s ease;
}

.page-enter-from {
    opacity: 0;
    transform: translateY(6px);
}

.page-leave-to {
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

button:focus-visible,
a:focus-visible {
    outline: 2px solid #0f172a;
    outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
    .page-enter-active,
    .page-leave-active,
    .overlay-enter-active,
    .overlay-leave-active {
        transition: none;
    }
}
</style>
