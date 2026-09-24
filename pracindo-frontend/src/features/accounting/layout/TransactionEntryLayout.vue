<template>
    <div
        class="relative flex h-screen w-full overflow-hidden bg-[#F8FAFC] font-sans text-slate-700"
    >
        <header
            class="fixed inset-x-0 top-0 z-[999] flex h-16 items-center justify-between border-b border-slate-100 bg-white/90 px-4 shadow-[0_4px_20px_rgba(15,23,42,0.04)] backdrop-blur-xl lg:hidden"
        >
            <div class="flex min-w-0 items-center gap-3">
                <button
                    ref="menuTrigger"
                    type="button"
                    @click="toggleSidebar"
                    :aria-expanded="sidebarAktif"
                    aria-controls="transaction-sidebar"
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
                        Akunting
                    </p>

                    <span
                        class="block truncate text-[15px] font-extrabold tracking-tight text-slate-800"
                    >
                        Input Transaksi
                    </span>
                </div>
            </div>

            <button
                type="button"
                @click="kembali"
                :disabled="isLoggingOut"
                aria-label="Kembali ke halaman utama"
                title="Halaman Utama"
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-white shadow-md shadow-slate-900/10 transition-all duration-200 hover:-translate-y-0.5 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:translate-y-0 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50"
            >
                <i
                    class="pi pi-home text-sm text-white"
                    aria-hidden="true"
                ></i>
            </button>
        </header>

        <div
            v-if="isMobile && sidebarAktif"
            @click="tutupDiMobile"
            class="fixed inset-0 z-[998] bg-slate-950/45 backdrop-blur-[2px] lg:hidden"
            role="presentation"
            aria-hidden="true"
        ></div>

        <aside
            ref="sidebarRef"
            id="transaction-sidebar"
            class="fixed bottom-2 left-2 top-2 z-[999] flex w-[88px] flex-col items-center justify-between rounded-3xl border border-slate-100 bg-white/95 py-6 shadow-[0_12px_40px_rgba(15,23,42,0.08)] backdrop-blur-xl transition-transform duration-300 ease-out lg:relative lg:bottom-auto lg:left-auto lg:top-auto lg:z-20 lg:m-4 lg:h-[calc(100vh-2rem)] lg:translate-x-0"
            :class="
                sidebarAktif
                    ? 'translate-x-0'
                    : '-translate-x-[150%] lg:translate-x-0'
            "
            :role="
                isMobile && sidebarAktif
                    ? 'dialog'
                    : undefined
            "
            :aria-modal="
                isMobile && sidebarAktif
                    ? 'true'
                    : undefined
            "
            :aria-labelledby="
                isMobile && sidebarAktif
                    ? 'transaction-sidebar-title'
                    : undefined
            "
            :aria-describedby="
                isMobile && sidebarAktif
                    ? 'transaction-sidebar-description'
                    : undefined
            "
            :aria-hidden="
                isMobile && !sidebarAktif
                    ? 'true'
                    : undefined
            "
        >
            <h2
                v-if="isMobile && sidebarAktif"
                id="transaction-sidebar-title"
                class="sr-only"
            >
                Menu Navigasi Akunting
            </h2>

            <p
                v-if="isMobile && sidebarAktif"
                id="transaction-sidebar-description"
                class="sr-only"
            >
                Gunakan menu navigasi untuk berpindah halaman transaksi akunting.
                Tekan Escape untuk menutup menu.
            </p>

            <div class="flex w-full flex-col items-center gap-7 lg:gap-8">
                <button
                    type="button"
                    @click="kembali"
                    aria-label="Kembali ke halaman utama"
                    title="Halaman Utama"
                    class="group hidden h-12 w-12 items-center justify-center rounded-2xl bg-slate-900 shadow-md shadow-slate-900/10 transition-all duration-200 hover:-translate-y-0.5 hover:scale-[1.03] hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-95 lg:flex"
                >
                    <i
                        class="pi pi-home text-xl text-white transition-transform duration-200 group-hover:scale-110"
                        aria-hidden="true"
                    ></i>
                </button>

                <nav
                    class="flex w-full flex-col gap-3 px-4 lg:gap-4"
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
                                'text-lg lg:text-xl',
                                'transition-transform duration-200',
                                menu.activate
                                    ? 'group-hover:scale-110'
                                    : ''
                            ]"
                            aria-hidden="true"
                        ></i>

                        <span
                            class="pointer-events-none absolute left-[calc(100%+0.75rem)] top-1/2 z-50 -translate-y-1/2 translate-x-1 whitespace-nowrap rounded-xl bg-slate-900 px-3 py-2 text-[10px] font-bold text-white opacity-0 shadow-xl shadow-slate-900/10 transition-all duration-200 group-hover:translate-x-0 group-hover:opacity-100"
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

            <div class="group relative mb-3 flex flex-col items-center">
                <button
                    type="button"
                    @click="keluar"
                    :disabled="isLoggingOut"
                    :aria-busy="isLoggingOut"
                    aria-label="Keluar dari aplikasi"
                    title="Keluar"
                    class="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-red-200 hover:bg-red-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2 active:scale-95 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    <i
                        v-if="!isLoggingOut"
                        class="pi pi-power-off text-slate-400 transition-colors duration-200 group-hover:text-red-500"
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
            class="custom-scrollbar h-full min-w-0 flex-1 overflow-y-auto px-4 pb-6 pt-20 md:px-6 md:pb-8 md:pt-24 lg:p-8"
        >
            <div class="mx-auto min-h-full w-full max-w-[1480px]">
                <router-view v-slot="{ Component }">
                    <transition
                        name="fade"
                        mode="out-in"
                    >
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
    </div>
</template>


<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
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

const menuTrigger = ref(null)
const sidebarRef = ref(null)
const isLoggingOut = ref(false)

const getFocusableElements = () => {
    if (!sidebarRef.value) {
        return []
    }

    return Array.from(
        sidebarRef.value.querySelectorAll(
            'button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        )
    ).filter((element) => {
        return (
            element.getAttribute('aria-hidden') !== 'true' &&
            element.offsetParent !== null
        )
    })
}

const handleSidebarKeydown = (event) => {
    if (
        !isMobile.value ||
        !sidebarAktif.value
    ) {
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

    const focusableElements = getFocusableElements()

    if (focusableElements.length === 0) {
        event.preventDefault()
        sidebarRef.value?.focus()
        return
    }

    const firstElement = focusableElements[0]
    const lastElement =
        focusableElements[
            focusableElements.length - 1
        ]

    if (
        event.shiftKey &&
        document.activeElement === firstElement
    ) {
        event.preventDefault()
        lastElement.focus()
        return
    }

    if (
        !event.shiftKey &&
        document.activeElement === lastElement
    ) {
        event.preventDefault()
        firstElement.focus()
    }
}

const focusSidebar = async () => {
    await nextTick()

    if (
        !isMobile.value ||
        !sidebarAktif.value
    ) {
        return
    }

    const focusableElements = getFocusableElements()

    if (focusableElements.length > 0) {
        focusableElements[0].focus()
    }

    document.addEventListener(
        'keydown',
        handleSidebarKeydown
    )
}

const releaseSidebarFocus = async () => {
    document.removeEventListener(
        'keydown',
        handleSidebarKeydown
    )

    if (
        isMobile.value &&
        !sidebarAktif.value
    ) {
        await nextTick()
        menuTrigger.value?.focus()
    }
}

const kembali = () => {
    if (isLoggingOut.value) return

    router.back()
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
        tutupDiMobile()
        return
    }

    router.push(menu.rute)
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
    () => [
        sidebarAktif.value,
        isMobile.value
    ],
    ([sidebarOpen, mobile]) => {
        if (mobile && sidebarOpen) {
            focusSidebar()
        } else {
            releaseSidebarFocus()
        }
    }
)

watch(
    () => route.fullPath,
    () => {
        if (isMobile.value) {
            tutupDiMobile()
        }
    }
)

onBeforeUnmount(() => {
    document.removeEventListener(
        'keydown',
        handleSidebarKeydown
    )
})
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
