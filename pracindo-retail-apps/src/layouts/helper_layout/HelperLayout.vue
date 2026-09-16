<template>
    <div class="min-h-screen bg-slate-50 flex font-sans">

        <aside class="w-64 bg-slate-900 text-white flex-col transition-all duration-300 z-50 fixed md:relative h-full"
            :class="isSidebarOpen ? 'flex' : 'hidden md:flex'">
            <div class="h-16 flex items-center px-6 border-b border-slate-800">
                <h1 class="text-xl font-black tracking-wider text-white"><span class="text-emerald-500">OPS</span>
                    Retail</h1>
            </div>

            <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
                <p class="px-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Operasional</p>

                <router-link to="/helper/stiker" @click="closeSidebar"
                    class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors text-slate-300 hover:text-white hover:bg-slate-800"
                    active-class="bg-emerald-600 text-white hover:bg-emerald-700">
                    <i class="pi pi-tags"></i>
                    <span class="text-sm font-medium">Cetak Stiker</span>
                </router-link>

                <p class="px-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mt-6 mb-2">Inventory</p>

                <router-link to="/inventory/penerimaan" @click="closeSidebar"
                    class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors text-slate-300 hover:text-white hover:bg-slate-800"
                    active-class="bg-emerald-600 text-white hover:bg-emerald-700">
                    <i class="pi pi-box"></i>
                    <span class="text-sm font-medium">Penerimaan DO</span>
                </router-link>

                <router-link to="/inventory/stok" @click="closeSidebar"
                    class="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors text-slate-300 hover:text-white hover:bg-slate-800"
                    active-class="bg-emerald-600 text-white hover:bg-emerald-700">
                    <i class="pi pi-list"></i>
                    <span class="text-sm font-medium">Monitoring Stok</span>
                </router-link>
            </nav>

            <div class="p-4 border-t border-slate-800">
                <div class="flex items-center gap-3 px-2">
                    <div class="w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center text-sm font-bold">
                        H
                    </div>
                    <div>
                        <p class="text-sm font-bold text-white">Helper Gudang</p>
                        <p class="text-xs text-slate-400">Logistik Cabang</p>
                    </div>
                </div>
            </div>
        </aside>

        <main class="flex-1 flex flex-col overflow-hidden w-full">
            <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 z-10">

                <button @click="toggleSidebar" class="md:hidden text-slate-500 hover:text-slate-700">
                    <i class="pi" :class="isSidebarOpen ? 'pi-times' : 'pi-bars'"></i>
                </button>

                <div class="flex-1 flex justify-end items-center gap-4">
                    <button @click="prosesLogout"
                        class="flex items-center gap-2 text-sm font-bold text-rose-500 hover:text-rose-700 bg-rose-50 px-3 py-1.5 rounded-lg transition-colors">
                        <i class="pi pi-sign-out"></i> Logout
                    </button>
                </div>
            </header>

            <div v-if="isSidebarOpen" @click="closeSidebar" class="fixed inset-0 bg-black/50 z-40 md:hidden"></div>

            <div class="flex-1 overflow-y-auto p-4 md:p-6 bg-slate-50 relative">
                <router-view />
            </div>
        </main>

    </div>
</template>

<script setup>
import { useLayout } from '@/composables/useLayout'

const { isSidebarOpen, toggleSidebar, closeSidebar, prosesLogout } = useLayout()
</script>