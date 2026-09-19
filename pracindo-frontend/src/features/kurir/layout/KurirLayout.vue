<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 relative">
    
    <!-- Main Content Area -->
    <!-- pb-20 (padding-bottom 80px) sangat penting agar konten paling bawah 
         tidak tertutup oleh bottom navigation yang fix -->
    <main class="pb-20">
      <!-- Transisi halus saat pindah halaman antar menu -->
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Bottom Navigation Bar -->
    <nav class="fixed bottom-0 w-full max-w-md mx-auto inset-x-0 bg-white border-t border-gray-200 flex justify-between items-center h-16 px-6 pb-safe-area z-50 shadow-[0_-2px_10px_rgba(0,0,0,0.02)]">
      
      <!-- Menu 1: Permintaan (RequestDelivery) -->
      <router-link
        to="/kurir/permintaan"
        class="flex flex-col items-center justify-center w-16 h-full text-gray-400 transition-colors"
        active-class="text-blue-600 font-bold"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" :class="{'fill-blue-50': $route.path.includes('/kurir/permintaan')}">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <span class="text-[10px] tracking-wide">Permintaan</span>
      </router-link>

      <!-- Menu 2: Tugas Saya (TaskOwn) -->
      <router-link
        to="/kurir/tugas-saya"
        class="flex flex-col items-center justify-center w-16 h-full text-gray-400 transition-colors"
        active-class="text-blue-600 font-bold"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" :class="{'fill-blue-50': $route.path.includes('/kurir/tugas-saya')}">
          <path d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
        </svg>
        <span class="text-[10px] tracking-wide">Tugas Saya</span>
      </router-link>

      <!-- Menu 3: Profil / Akun -->
      <router-link
        to="/kurir/profil"
        class="flex flex-col items-center justify-center w-16 h-full text-gray-400 transition-colors"
        active-class="text-blue-600 font-bold"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" :class="{'fill-blue-50': $route.path.includes('/kurir/profil')}">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span class="text-[10px] tracking-wide">Profil</span>
      </router-link>
      
    </nav>
  </div>
</template>

<script setup>
// Layout ini murni untuk UI wrapper, tidak butuh logic khusus
</script>

<style scoped>
/* Transisi mulus ala aplikasi native saat ganti tab */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Penyesuaian padding untuk iPhone yang punya garis bawah layar (Home Indicator) */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .pb-safe-area {
    padding-bottom: env(safe-area-inset-bottom);
  }
}
</style>