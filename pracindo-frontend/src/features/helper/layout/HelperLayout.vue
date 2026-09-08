<template>
    <div class="flex h-screen bg-[#F8FAFC] font-sans text-slate-700 overflow-hidden relative">
        <aside class="bg-white rounded-3xl shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col items-center py-6 flex-shrink-0 justify-between relative w-[88px] h-[calc(100vh-2rem)] m-4 z-20">
            <div class="flex flex-col items-center w-full gap-8">
                <div @click="kembali" class="mb-2 cursor-pointer">
                    <div class="w-12 h-12 bg-slate-900 rounded-2xl flex items-center justify-center shadow-md hover:scale-105 transition-transform">
                        <i class="pi pi-arrow-left text-white text-xl"></i>
                    </div>
                </div>
                <nav class="flex flex-col gap-4 w-full px-4">
                    <button v-for="item in menu" :key="item.id" :disabled="!item.activate" @click="klikMenu(item)" class="w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300 relative mx-auto group" :class="[item.activate ? (aktif(item.rute) ? 'bg-slate-900 text-white shadow-md' : 'text-slate-400 hover:bg-slate-50 hover:text-slate-600') : 'text-slate-300 cursor-default']">
                        <i :class="['pi', item.ikon, 'text-xl transition-transform', item.activate ? 'group-hover:scale-110' : '']"></i>
                        <span class="absolute left-16 bg-slate-800 text-white text-xs font-semibold px-3 py-1.5 rounded-lg opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-50 shadow-lg transition-opacity">
                            {{ item.label }}
                        </span>
                    </button>
                </nav>
            </div>
        </aside>

        <main class="flex-1 overflow-y-auto p-8 custom-scrollbar relative">
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
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useNavHelperLayout } from '../composables/useNavHelperLayout'

const router = useRouter()
const { menu, aktif } = useNavHelperLayout()

const kembali = () => {
    router.push('/')
}

const klikMenu = (item) => {
    if (!item.activate) return
    router.push(item.rute)
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease-out, transform 0.25s ease-out; }
.fade-enter-from { opacity: 0; transform: translateY(10px); }
.fade-leave-to { opacity: 0; transform: translateY(-10px); }

.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 999px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>