<script setup>
import { BOTTOM_NAV_MENU } from '@/features/kurir/uiConfigKurir'
</script>

<template>
  <div class="min-h-screen bg-[#f0f4f8] font-sans text-slate-800 relative max-w-md mx-auto shadow-xl">

    <!-- HEADER GELAP (Tanpa Kartu Absen) -->
    <header class="bg-[#111827] rounded-b-[2rem] pt-10 pb-10 px-6 shadow-md relative z-10">
      <div class="flex justify-between items-start">
        <!-- Info Profil -->
        <div class="flex items-center gap-4">
          <!-- Avatar dengan Ring Hijau -->
          <div class="w-12 h-12 rounded-full border-2 border-emerald-500 flex items-center justify-center bg-slate-800">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <!-- Teks Profil -->
          <div>
            <p class="text-[10px] font-bold text-slate-400 tracking-wider">KURIR INTERNAL</p>
            <h1 class="text-xl font-bold text-white leading-tight mt-0.5">resza</h1>
            <p class="text-xs text-slate-400 mt-0.5">Supervisor</p>
          </div>
        </div>

        <!-- Tombol Notifikasi Putih -->
        <button class="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </button>
      </div>
    </header>

    <!-- AREA KONTEN (Menampilkan Halaman Child) -->
    <main class="px-5 pt-8 pb-24 min-h-[70vh]">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- BOTTOM NAVBAR -->
    <nav class="fixed bottom-0 w-full max-w-md mx-auto bg-white border-t border-slate-200 flex justify-around items-center h-16 px-2 z-50 shadow-[0_-5px_15px_-5px_rgba(0,0,0,0.05)] rounded-t-2xl">
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