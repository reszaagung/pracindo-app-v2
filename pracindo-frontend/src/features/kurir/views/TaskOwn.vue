<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    
    <header class="sticky top-0 z-10 bg-white border-b border-gray-100 shadow-sm px-4 py-3 flex items-center justify-between gap-4">
      <h2 class="text-lg font-bold text-gray-800 whitespace-nowrap m-0">Tugas Saya</h2>
      
      <button 
        @click="fetchMyDeliveries" 
        class="!w-10 !h-10 !min-w-[40px] !max-w-[40px] !flex-none !flex !items-center !justify-center bg-gray-50 hover:bg-gray-100 active:bg-gray-200 !rounded-full shadow-sm border border-gray-200 !p-0 !m-0 !outline-none"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          class="!w-5 !h-5 !shrink-0 transition-colors" 
          :class="{'animate-spin text-blue-600': loading, 'text-gray-700': !loading}"
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor" 
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </header>

    <div class="p-4">
      <div v-if="loading" class="flex flex-col items-center justify-center py-16">
        <div class="inline-block animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full mb-3"></div>
        <p class="text-gray-500 text-sm font-medium">Memuat tugas...</p>
      </div>

      <div v-else-if="myDeliveries.length === 0" class="flex flex-col items-center justify-center bg-white px-6 py-12 rounded-2xl shadow-sm border border-gray-100 mt-2 text-center">
        <p class="text-gray-800 font-bold text-base">Belum Ada Tugas</p>
        <p class="text-gray-500 text-sm mt-1">Silakan klaim permintaan dari tab sebelah.</p>
      </div>

      <div v-else class="flex flex-col gap-4">
        <div v-for="delivery in myDeliveries" :key="delivery.id" class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden flex flex-col">
          
          <div class="px-4 py-3 border-b border-gray-50 flex justify-between items-center bg-gray-50/50">
            <h3 class="font-bold text-gray-800 text-sm truncate">{{ delivery.nomor }}</h3>
            <!-- Badge warna juga sudah dibuat dinamis mengikuti status perhentian -->
            <span :class="getBadgeClass(cekStatusSampai(delivery) ? 'SAMPAI' : delivery.status)" class="px-2 py-1 text-[10px] uppercase font-bold tracking-wider rounded whitespace-nowrap ml-2">
              {{ cekStatusSampai(delivery) ? 'SAMPAI' : delivery.status }}
            </span>
          </div>

          <div class="p-4">
            
            <div v-if="delivery.status === 'DISIAPKAN' || delivery.status === 'SIAP_KIRIM'">
              <p class="text-sm text-gray-600 mb-3">Barang sudah siap dibawa. Silakan mulai perjalanan.</p>
              <button @click="startDelivery(delivery.id)" class="w-full flex justify-center items-center gap-2 bg-blue-600 text-white px-4 py-3 rounded-lg font-bold hover:bg-blue-700 active:bg-blue-800 text-sm">
                Mulai Perjalanan 🚀
              </button>
            </div>

            <!-- PERBAIKAN: Mengecek status SAMPAI DULU sebelum mengecek BERANGKAT -->
            <div v-else-if="cekStatusSampai(delivery)">
              <p class="text-sm text-gray-600 mb-3 font-medium text-orange-600">Barang sudah sampai! Silakan unggah bukti surat jalan.</p>
              
              <div class="flex gap-2">
                <input type="file" :id="`upload-${delivery.id}`" class="hidden" accept="image/*" @change="(e) => handleUpload(e, delivery)" />
                <label :for="`upload-${delivery.id}`" class="flex-1 flex justify-center items-center gap-2 bg-emerald-600 text-white px-4 py-3 rounded-lg font-bold hover:bg-emerald-700 cursor-pointer text-sm">
                  📸 Upload Bukti
                </label>
                
                <button @click="handleRetur(delivery)" class="flex-1 flex justify-center items-center gap-2 bg-rose-100 text-rose-700 px-4 py-3 rounded-lg font-bold border border-rose-200 text-sm">
                  Retur
                </button>
              </div>
            </div>

            <div v-else-if="delivery.status === 'BERANGKAT'">
              <p class="text-sm text-gray-600 mb-3">Sedang dalam perjalanan menuju tujuan.</p>
              <!-- Menggunakan fungsi pintar untuk mencari ID perhentian -->
              <button @click="markArrived(delivery.id, dapatkanIdPerhentian(delivery))" class="w-full flex justify-center items-center gap-2 bg-purple-600 text-white px-4 py-3 rounded-lg font-bold hover:bg-purple-700 text-sm">
                Tandai Sudah Sampai 📍
              </button>
            </div>

            <div v-else-if="delivery.status === 'SELESAI'">
              <div class="flex items-center gap-2 text-emerald-600 bg-emerald-50 p-3 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <span class="text-sm font-bold">Pengiriman Selesai!</span>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useKurir } from '../composables/useKurir'

const { myDeliveries, loading, fetchMyDeliveries, startDelivery, markArrived, uploadProof } = useKurir()

onMounted(() => {
  fetchMyDeliveries()
})

// === HELPER PINTAR BARU ===
// Fungsi untuk mengecek apakah titik perhentian saat ini statusnya SAMPAI
const cekStatusSampai = (delivery) => {
  if (delivery.perhentian && Array.isArray(delivery.perhentian)) {
    // Mengecek apakah ada perhentian di dalam pengiriman ini yang berstatus SAMPAI
    return delivery.perhentian.some(p => p.status === 'SAMPAI')
  }
  return false
}

// Fungsi untuk mendapatkan ID perhentian yang tepat untuk aksi saat ini
const dapatkanIdPerhentian = (delivery) => {
  if (delivery.perhentian && Array.isArray(delivery.perhentian) && delivery.perhentian.length > 0) {
    const aktif = delivery.perhentian.find(p => p.status === 'MENUNGGU' || p.status === 'SAMPAI')
    if (aktif) return aktif.id
    return delivery.perhentian[0].id
  }
  return delivery.perhentian_id || delivery.id
}
// =========================

const getBadgeClass = (status) => {
  const warna = {
    'MENUNGGU': 'bg-slate-100 text-slate-600',
    'DISIAPKAN': 'bg-orange-100 text-orange-700',
    'SIAP_KIRIM': 'bg-orange-100 text-orange-700',
    'BERANGKAT': 'bg-blue-100 text-blue-700',
    'SAMPAI': 'bg-purple-100 text-purple-700', 
    'SELESAI': 'bg-emerald-100 text-emerald-700',
    'RETUR': 'bg-rose-100 text-rose-700'
  }
  return warna[status] || 'bg-gray-100 text-gray-800'
}

const handleUpload = async (event, delivery) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('foto', file) 
  
  const perhentianId = dapatkanIdPerhentian(delivery) 

  try {
    await uploadProof(delivery.id, perhentianId, formData)
    alert('Bukti berhasil diunggah! Pengiriman selesai.')
  } catch (error) {
    const pesanDetail = error.response?.data?.foto?.[0] || error.response?.data?.detail || error.message
    alert('Gagal mengunggah bukti: ' + pesanDetail)
  }
}
const handleRetur = (delivery) => {
  alert(`Buka form retur untuk pengiriman ${delivery.nomor}`)
}
</script>