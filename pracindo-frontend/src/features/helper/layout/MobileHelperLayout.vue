<template>
    <div class="flex flex-col h-screen bg-[#F8FAFC] font-sans text-slate-700 overflow-hidden relative">
        <header class="flex-shrink-0 h-16 bg-white shadow-sm z-30 flex items-center justify-between px-4 border-b border-slate-100">
            <div class="flex items-center gap-3">
                <button @click="toggleSidebar" class="p-2 rounded-xl bg-slate-50 text-slate-600 hover:bg-slate-100 active:bg-slate-200 transition-colors">
                    <i class="pi pi-bars text-xl"></i>
                </button>
                <span class="font-bold text-slate-800 text-base">Helper System</span>
            </div>
            <button @click="kembali" class="w-9 h-9 bg-slate-900 rounded-xl flex items-center justify-center shadow-md active:scale-95 transition-transform">
                <i class="pi pi-arrow-left text-white text-sm"></i>
            </button>
        </header>

        <div v-if="sidebarAktif" @click="toggleSidebar" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-40 transition-opacity"></div>

        <aside :class="['fixed top-0 left-0 bottom-0 w-64 bg-white z-50 shadow-xl transition-transform duration-300 ease-in-out flex flex-col', sidebarAktif ? 'translate-x-0' : '-translate-x-full']">
            <div class="p-4 border-b border-slate-100 flex justify-between items-center">
                <span class="font-bold text-slate-800">Menu Helper</span>
                <button @click="toggleSidebar" class="w-8 h-8 flex items-center justify-center rounded-lg bg-slate-50 text-slate-500 hover:bg-slate-100">
                    <i class="pi pi-times"></i>
                </button>
            </div>
            <nav class="p-4 flex flex-col gap-2 flex-1">
                <button v-for="item in menu" :key="item.id" @click="klikMenu(item)" class="flex items-center gap-3 w-full p-3 rounded-xl transition-colors text-left" :class="aktif(item.rute) ? 'bg-slate-900 text-white shadow-md' : 'text-slate-600 hover:bg-slate-50'">
                    <i :class="['pi', item.ikon]"></i>
                    <span class="text-sm font-semibold">{{ item.label }}</span>
                </button>
            </nav>
        </aside>

        <main class="flex-1 overflow-y-auto p-4 custom-scrollbar relative">
            <router-view v-slot="{ Component, route }">
                <transition name="fade" mode="out-in">
                    <div :key="route.fullPath" class="w-full h-full">
                        <component :is="Component" />
                    </div>
                </transition>
            </router-view>
        </main>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useNavHelper } from '../composables/useNavHelper'

const router = useRouter()
const { menuHelper: menu, aktif } = useNavHelper()
const sidebarAktif = ref(false)

const kembali = () => {
    router.push('/')
}

const toggleSidebar = () => {
    sidebarAktif.value = !sidebarAktif.value
}

const klikMenu = (item) => {
    if (!item.activate) return
    router.push(item.rute)
    sidebarAktif.value = false
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