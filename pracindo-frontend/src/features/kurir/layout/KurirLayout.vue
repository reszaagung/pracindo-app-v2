<script setup>
import { BOTTOM_NAV_MENU } from '@/features/kurir/uiConfigKurir'
import { useAuth } from '@/composables/useAuth'

// Tarik data profil (kartu) langsung dari composable auth lu
const { kartu } = useAuth()
</script>

<template>
  <div class="h-[100dvh] bg-[#f0f4f8] font-sans text-slate-800 flex flex-col relative max-w-md mx-auto shadow-2xl border-x border-slate-200 overflow-hidden">
    
    <header class="bg-[#111827] rounded-b-3xl pt-8 pb-5 px-5 shadow-md relative z-20 shrink-0">
      <div class="flex items-center gap-3.5">
        <div class="w-11 h-11 rounded-full border border-emerald-500 flex items-center justify-center text-slate-300 bg-slate-800 shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <div class="flex flex-col justify-center">
          <span class="text-[9px] font-bold text-slate-400 tracking-widest uppercase mb-0.5">KURIR INTERNAL</span>
          
          <!-- Gunakan kartu?.nama dan kartu?.role_display dari useAuth lu -->
          <h1 class="text-lg font-bold !text-white leading-tight capitalize mb-0.5">{{ kartu?.nama || 'Pengguna' }}</h1>
          <span class="text-[10px] text-slate-400 capitalize">{{ kartu?.role_display || 'Staff' }}</span>
        </div>
      </div>
    </header>

    <main class="flex-1 overflow-y-auto px-5 pt-6 pb-8">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <nav class="shrink-0 w-full bg-white border-t border-slate-200 flex justify-around items-center h-[70px] px-2 z-50 rounded-t-2xl shadow-[0_-10px_20px_-10px_rgba(0,0,0,0.1)]">
      <router-link
        v-for="menu in BOTTOM_NAV_MENU"
        :key="menu.path"
        :to="menu.path"
        class="flex-1 flex flex-col items-center justify-center gap-1 h-full text-slate-400 hover:text-emerald-600 transition-colors relative"
        active-class="!text-emerald-600"
      >
        <span v-if="menu.hasBadge" class="absolute top-2 right-4 w-2 h-2 bg-red-500 rounded-full border border-white"></span>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="menu.iconPath" />
        </svg>
        <span class="text-[10px] font-bold">{{ menu.name }}</span>
      </router-link>
    </nav>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(5px);
}
</style>