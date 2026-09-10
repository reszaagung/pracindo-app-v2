<script setup>
import { ref, onMounted } from 'vue'
import { BOTTOM_NAV_MENU } from '@/features/kurir/uiConfigKurir'

// Awal dikosongkan/pakai placeholder netral, bukan dummy spesifik
const namaUser = ref('Memuat...')
const tipeKurir = ref('')
const jabatanUser = ref('')

onMounted(() => {
  try {
    // Menarik murni dari data sesi login user di browser
    const userData = JSON.parse(localStorage.getItem('user'))
    if (userData) {
      namaUser.value = userData.nama || userData.username || 'Pengguna'
      tipeKurir.value = userData.tipe || 'KURIR INTERNAL'
      jabatanUser.value = userData.jabatan || 'Staff'
    } else {
      namaUser.value = 'Pengguna'
      tipeKurir.value = 'KURIR INTERNAL'
      jabatanUser.value = 'Staff'
    }
  } catch (e) {
    namaUser.value = 'Pengguna'
  }
})
</script>

<template>
  <div class="h-[100dvh] bg-[#f0f4f8] font-sans text-slate-800 flex flex-col relative max-w-md mx-auto shadow-2xl border-x border-slate-200 overflow-hidden">
    
    <!-- Header: Rata Tengah, Nama Putih, Tombol Kanan Dihapus -->
    <header class="bg-[#111827] rounded-b-[2rem] pt-10 pb-8 px-6 shadow-md relative z-10 shrink-0">
      <div class="flex items-center">
        
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-full border-2 border-emerald-500 flex items-center justify-center bg-slate-800 shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <div class="flex flex-col justify-center">
            <p class="text-[10px] font-bold text-slate-400 tracking-wider uppercase leading-none mb-1.5">{{ tipeKurir }}</p>
            <h1 class="text-xl font-bold !text-white leading-none capitalize mb-1">{{ namaUser }}</h1>
            <p class="text-xs text-slate-400 leading-none capitalize">{{ jabatanUser }}</p>
          </div>
        </div>

      </div>
    </header>

    <main class="flex-1 overflow-y-auto px-5 pt-8 pb-8">
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