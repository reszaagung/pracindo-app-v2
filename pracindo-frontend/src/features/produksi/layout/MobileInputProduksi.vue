<template>
  <div class="flex flex-col h-screen bg-[#F8FAFC] font-sans text-slate-700 relative overflow-hidden">

        <header class="fixed top-0 left-0 right-0 h-16 bg-white shadow-sm z-30 flex items-center justify-between px-4 gap-3 border-b border-slate-100 w-full max-w-[100vw]">
            <div class="flex items-center gap-3 min-w-0">
                <a @click="keDashboard" class="p-2 shrink-0 rounded-xl bg-slate-50 text-slate-600 hover:bg-slate-100 active:bg-slate-200 transition-colors cursor-pointer">
                    <i class="pi pi-home text-xl"></i>
                </a>
                <span class="font-bold text-slate-800 text-sm md:text-base truncate">Produksi (Mixing & Blending)</span>
            </div>
            <a @click="kembali" class="w-9 h-9 shrink-0 bg-slate-900 rounded-xl flex items-center justify-center shadow-md active:scale-95 transition-transform cursor-pointer">
                <i class="pi pi-arrow-left text-white text-sm"></i>
            </a>
        </header>

    <main class="flex-1 overflow-y-auto pt-12 pb-20 custom-scrollbar">
      <div class="p-4 w-full min-h-full">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <!-- BOTTOM NAVIGATION BAR (Menu Produksi + Dashboard + Logout) -->
    <nav class="fixed bottom-0 left-0 right-0 h-16 bg-white border-t border-slate-100 shadow-[0_-4px_10px_-2px_rgba(0,0,0,0.05)] z-40 flex items-center justify-around px-1 pb-safe">


      <button
        v-for="menu in menuProduksi"
        :key="menu.id"
        @click="klikMenu(menu)"
        :disabled="!menu.activate"
        class="flex flex-col items-center justify-center w-full h-full gap-1 transition-colors relative"
        :class="aktif(menu.rute) ? 'text-slate-900' : 'text-slate-400 active:text-slate-600'"
      >
        <div
          class="flex items-center justify-center w-10 h-6 rounded-full transition-all duration-300"
          :class="aktif(menu.rute) ? 'bg-slate-100' : 'bg-transparent'"
        >
          <i :class="['pi', menu.ikon, 'text-base', aktif(menu.rute) ? 'scale-110 font-bold' : '']"></i>
        </div>
        <span class="text-[10px] font-medium truncate px-1 w-full text-center tracking-tight" :class="aktif(menu.rute) ? 'font-bold' : ''">
          {{ menu.label }}
        </span>
        <span v-if="!menu.activate" class="absolute top-1 right-2 w-1.5 h-1.5 bg-slate-300 rounded-full"></span>
      </button>

      <!-- 3. Tombol Logout (Keluar Sistem) -->
      <button @click="keluar" class="flex flex-col items-center justify-center w-full h-full gap-1 text-rose-400 active:text-rose-600 transition-colors">
        <div class="flex items-center justify-center w-8 h-6 rounded-full bg-rose-50/50">
          <i class="pi pi-power-off text-base"></i>
        </div>
        <span class="text-[10px] font-medium tracking-tight">Keluar</span>
      </button>

    </nav>

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
  if (!menu.activate) return
  router.push(menu.rute)
}

const keluar = async () => {
    await logout()
    router.push('/login')
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.custom-scrollbar::-webkit-scrollbar { display: none; }
.pb-safe { padding-bottom: env(safe-area-inset-bottom); }
</style>
