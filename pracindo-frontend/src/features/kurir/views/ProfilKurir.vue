<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <header class="sticky top-0 z-10 bg-white border-b border-gray-100 shadow-sm px-4 py-3.5 flex items-center justify-center">
      <h2 class="text-base font-bold text-gray-800">Profil Saya</h2>
    </header>

    <div class="p-4 flex flex-col gap-4 mt-2">
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center">
        <div class="w-24 h-24 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center text-4xl font-bold mb-4 border-4 border-white shadow-md">
          {{ userInitial }}
        </div>
        
        <h3 class="text-xl font-bold text-gray-800">{{ userName }}</h3>
        <p class="text-sm text-gray-500 font-medium mt-1">Tim Ekspedisi / Kurir</p>
        
        <div class="mt-4 px-4 py-1.5 bg-emerald-50 text-emerald-600 text-xs font-bold rounded-full border border-emerald-100 flex items-center gap-2">
          <div class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
          Status: Aktif Bertugas
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mt-2">
        
        <button class="w-full px-5 py-4 flex items-center justify-between border-b border-gray-50 hover:bg-gray-50 active:bg-gray-100 transition">
          <div class="flex items-center gap-3 text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="font-medium text-sm">Riwayat Pengiriman</span>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>

        <button @click="handleLogout" class="w-full px-5 py-4 flex items-center gap-3 text-rose-600 hover:bg-rose-50 active:bg-rose-100 transition">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span class="font-bold text-sm">Keluar (Logout)</span>
        </button>
      </div>
      
      <!-- Versi App -->
      <p class="text-center text-xs text-gray-400 mt-4 font-medium">Pracindo Kurir App v2.0</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const userData = JSON.parse(localStorage.getItem('user') || localStorage.getItem('retail_user') || '{}')
const userName = ref(userData.nama || userData.username || 'Kurir Internal')

const userInitial = computed(() => {
  return userName.value.charAt(0).toUpperCase() || 'K'
})

const handleLogout = () => {
  const confirmLogout = confirm('Apakah Anda yakin ingin keluar dari aplikasi?')
  
  if (confirmLogout) {
    // Hapus semua token yang mungkin dipakai
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('retail_token')
    localStorage.removeItem('retail_user')
    
    // Redirect ke halaman login
    router.push('/login')
  }
}
</script>