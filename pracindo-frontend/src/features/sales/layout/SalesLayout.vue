<!-- src/features/sales/layout/SalesLayout.vue -->
<template>
    <div class="flex h-screen bg-slate-50 overflow-hidden font-sans relative">
        
        <div v-if="isMobileMenuOpen" @click="isMobileMenuOpen = false" 
             class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-20 md:hidden transition-opacity">
        </div>

        <aside :class="[
                isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full',
                'md:translate-x-0'
            ]" 
            class="fixed md:relative w-64 h-full bg-white border-r border-slate-200 flex flex-col shadow-2xl md:shadow-sm z-30 transition-transform duration-300 ease-in-out">
            
            <div class="h-16 flex items-center justify-between px-6 border-b border-slate-100">
                <span class="text-xl font-black text-teal-600 tracking-tight flex items-center gap-2">
                    <i class="pi pi-chart-line"></i> Modul Sales
                </span>
                <button @click="isMobileMenuOpen = false" class="md:hidden text-slate-400 hover:text-red-500">
                    <i class="pi pi-times text-lg"></i>
                </button>
            </div>
            
            <nav class="flex-1 overflow-y-auto p-4 space-y-2">
                <router-link 
                    v-for="(menu, index) in salesMenu" 
                    :key="index" 
                    :to="menu.to"
                    @click="isMobileMenuOpen = false"
                    class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold text-slate-600 hover:bg-teal-50 hover:text-teal-700 transition-all"
                    active-class="bg-teal-50 text-teal-700 shadow-sm border border-teal-100"
                >
                    <i :class="menu.icon"></i> {{ menu.label }}
                </router-link>
            </nav>
        </aside>

        <div class="flex-1 flex flex-col h-screen overflow-hidden">
            <header class="h-16 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-4 md:px-6 z-10">
                
                <button @click="isMobileMenuOpen = true" class="md:hidden p-2 text-slate-500 hover:text-slate-800 bg-slate-100 rounded-lg">
                    <i class="pi pi-bars text-xl"></i>
                </button>

                <div class="flex items-center gap-3 ml-auto">
                    <div class="w-8 h-8 rounded-full bg-teal-600 text-white flex items-center justify-center font-bold text-sm shadow-md">
                        S
                    </div>
                </div>
            </header>

            <main class="flex-1 overflow-y-auto p-4 md:p-6">
                <router-view v-slot="{ Component }">
                    <transition name="fade" mode="out-in">
                        <component :is="Component" />
                    </transition>
                </router-view>
            </main>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { salesMenu } from '../uiConfigSales'

const isMobileMenuOpen = ref(false)
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
    opacity: 0;
    transform: translateY(5px);
}
</style>