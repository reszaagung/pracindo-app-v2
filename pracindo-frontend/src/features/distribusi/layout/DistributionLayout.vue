<template>
    <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-700 overflow-hidden relative w-full">
        
        <!-- HEADER MOBILE (Hanya Tampil di HP) -->
        <header class="flex lg:hidden fixed top-0 left-0 right-0 h-14 bg-white/95 backdrop-blur-md shadow-sm z-[999] items-center justify-between px-4 border-b border-slate-100">
            <span class="font-extrabold text-slate-800 text-[15px] tracking-tight">
                Distribution
            </span>
            <button @click="kembali" aria-label="Dashboard Utama" class="w-9 h-9 bg-slate-900 hover:bg-slate-800 rounded-xl flex items-center justify-center shadow-md active:scale-95 transition-all">
                <i class="pi pi-home text-white text-sm"></i>
            </button>
        </header>

        <!-- SIDEBAR DESKTOP (Hanya Tampil di Laptop/PC) -->
        <aside class="hidden lg:flex bg-white rounded-3xl shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 flex-col items-center py-6 flex-shrink-0 justify-between relative w-[88px] h-[calc(100vh-2rem)] m-4 z-[999]">
            <div class="flex flex-col items-center w-full gap-8">
                <div @click="kembali" title="Kembali ke Dashboard Utama" class="mb-2 cursor-pointer">
                    <div class="w-12 h-12 bg-slate-900 rounded-2xl flex items-center justify-center shadow-md hover:scale-105 transition-transform group">
                        <i class="pi pi-home text-white text-xl group-hover:-translate-y-1 transition-transform"></i>
                    </div>
                </div>

                <nav class="flex flex-col gap-4 w-full px-4">
                    <button v-for="item in menu" :key="item.id" :disabled="!item.activate" @click="klikMenu(item)"
                        class="w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300 relative mx-auto group"
                        :class="item.activate ? (aktif(item.rute) ? 'bg-slate-900 text-white shadow-md' : 'text-slate-400 hover:bg-slate-50 hover:text-slate-600') : 'text-slate-300 cursor-default'">
                        <i :class="['pi', item.ikon, 'text-xl', 'transition-transform', item.activate ? 'group-hover:scale-110' : '']"></i>
                        <span class="absolute left-16 bg-slate-800 text-white text-xs font-bold px-3 py-1.5 rounded-lg opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-50 shadow-lg transition-opacity">
                            {{ item.label }}<template v-if="!item.activate"> - Segera</template>
                        </span>
                    </button>
                </nav>
            </div>

            <div class="mt-auto flex flex-col items-center group relative mb-4">
                <button @click="keluar" type="button" aria-label="Keluar Aplikasi" class="w-10 h-10 rounded-xl overflow-hidden cursor-pointer border border-slate-200 hover:border-red-500 bg-white hover:bg-red-50 transition-all shadow-sm flex items-center justify-center">
                    <i class="pi pi-power-off text-slate-400 group-hover:text-red-500 transition-colors"></i>
                </button>
                <span class="absolute -top-10 bg-slate-800 text-white text-[11px] font-bold px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50 shadow-lg">
                    Keluar
                </span>
            </div>
        </aside>

        <!-- MAIN CONTENT -->
        <main class="flex-1 overflow-y-auto w-full h-full p-4 pt-20 pb-28 lg:p-8 custom-scrollbar relative z-10">
            <div class="mx-auto w-full h-full max-w-7xl">
                <router-view v-slot="{ Component, route }">
                    <transition name="fade" mode="out-in">
                        <div :key="route.fullPath" class="w-full h-full">
                            <component :is="Component" />
                        </div>
                    </transition>
                </router-view>
            </div>
        </main>

        <!-- BOTTOM NAVIGATION (Hanya Tampil di HP) -->
        <nav class="flex lg:hidden fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-lg border-t border-slate-200 items-center justify-around px-2 pt-2.5 pb-[calc(env(safe-area-inset-bottom)+0.75rem)] z-[999] shadow-[0_-10px_30px_rgba(0,0,0,0.05)]">
            <button v-for="item in menu" :key="item.id" :disabled="!item.activate" @click="klikMenu(item)"
                class="flex flex-col items-center justify-center w-[22%] relative transition-all duration-300 gap-1"
                :class="item.activate ? (aktif(item.rute) ? 'text-slate-900' : 'text-slate-400 active:scale-95') : 'text-slate-300 opacity-50'">
                
                <i :class="['pi', item.ikon, 'text-[22px] transition-transform duration-300', aktif(item.rute) ? 'font-bold scale-110 -translate-y-0.5' : '']"></i>
                <span class="text-[9px] font-extrabold tracking-wide truncate w-full text-center transition-opacity" :class="aktif(item.rute) ? 'opacity-100' : 'opacity-70'">
                    {{ item.label }}
                </span>
            </button>
        </nav>

    </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { useNavDistribution } from '../composables/useNavDistribution'

const route = useRoute()
const router = useRouter()
const { logout } = useAuth()
const { menu, aktif } = useNavDistribution()

const kembali = () => router.push('/')

const klikMenu = (item) => {
    if (!item.activate) return
    router.push(item.rute)
}

const keluar = async () => {
    await logout()
    router.push('/login')
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active { transition: opacity 0.25s ease-out, transform 0.25s ease-out; }
.fade-enter-from { opacity: 0; transform: translateY(10px); }
.fade-leave-to { opacity: 0; transform: translateY(-10px); }

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 999px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

@media (prefers-reduced-motion: reduce) {
    .fade-enter-active,
    .fade-leave-active { transition: none; }
}

@supports (padding-bottom: env(safe-area-inset-bottom)) {
    nav {
        padding-bottom: calc(env(safe-area-inset-bottom) + 0.75rem);
    }
}
</style>