<template>
    <div class="min-h-screen bg-slate-50 flex flex-col font-sans">

        <header
            class="h-16 bg-slate-900 text-white border-b border-slate-800 flex items-center justify-between px-6 z-10 shrink-0">
            <div class="flex items-center gap-4">
                <h1 class="text-xl font-black tracking-wider"><span class="text-blue-500">POS</span> Retail</h1>
                <div
                    class="hidden md:flex items-center gap-2 px-3 py-1 bg-slate-800 rounded-lg border border-slate-700">
                    <div class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
                    <span class="text-xs font-medium text-slate-300">Shift Aktif</span>
                </div>
            </div>

            <div class="flex items-center gap-4">
                <div class="hidden md:block text-right mr-2">
                    <p class="text-sm font-bold text-white">Kasir Cabang</p>
                    <p class="text-xs text-slate-400">Toko Pusat</p>
                </div>
                <div
                    class="w-9 h-9 rounded-full bg-blue-600 flex items-center justify-center text-sm font-bold border-2 border-slate-700">
                    K
                </div>
                <button @click="prosesLogout"
                    class="flex items-center gap-2 text-sm font-bold text-rose-400 hover:text-white bg-slate-800 hover:bg-rose-500 px-3 py-2 rounded-lg transition-colors border border-slate-700 hover:border-rose-500">
                    <i class="pi pi-power-off"></i> <span class="hidden sm:inline">Tutup Shift</span>
                </button>
            </div>
        </header>

        <main class="flex-1 overflow-y-auto p-4 md:p-6 relative">
            <router-view />
        </main>

    </div>
</template>

<script setup>
import { useLayout } from '@/composables/useLayout'

const { prosesLogout } = useLayout()
</script>