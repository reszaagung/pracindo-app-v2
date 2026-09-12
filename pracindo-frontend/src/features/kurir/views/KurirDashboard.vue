<template>
  <div class="flex flex-col gap-6">
    <div class="grid grid-cols-2 gap-4">
      <div class="bg-white rounded-3xl p-5 shadow-sm border border-slate-100 flex flex-col gap-2 relative overflow-hidden">
        <div class="absolute -right-4 -top-4 w-16 h-16 bg-emerald-50 rounded-full opacity-50"></div>
        <div class="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mb-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
        </div>
        <h3 class="text-2xl font-black text-slate-800">{{ totalPerhentian }}</h3>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Total Tujuan</p>
      </div>

      <div class="bg-white rounded-3xl p-5 shadow-sm border border-slate-100 flex flex-col gap-2 relative overflow-hidden">
        <div class="absolute -right-4 -top-4 w-16 h-16 bg-blue-50 rounded-full opacity-50"></div>
        <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center mb-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path></svg>
        </div>
        <h3 class="text-2xl font-black text-slate-800">{{ totalJarak }} <span class="text-sm font-bold text-slate-500">km</span></h3>
        <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Total Jarak</p>
      </div>
    </div>

    <div>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-sm font-bold text-slate-800">Daftar Tujuan Pengiriman</h2>
        <button @click="loadDeliveries" :disabled="isLoading" class="text-emerald-600 p-1 hover:bg-emerald-50 rounded-full transition-colors">
          <svg :class="{'animate-spin': isLoading}" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
        </button>
      </div>

      <div v-if="isLoading" class="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm flex flex-col items-center justify-center gap-3">
        <div class="w-8 h-8 border-4 border-slate-200 border-t-emerald-500 rounded-full animate-spin"></div>
        <p class="text-xs font-bold text-slate-400">Sinkronisasi data...</p>
      </div>

      <div v-else-if="deliveries.length === 0" class="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm flex flex-col items-center justify-center text-center gap-4">
        <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-2">
          <svg class="w-10 h-10 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
        </div>
        <div>
          <h3 class="text-base font-bold text-slate-700">Waktunya Ngopi! ☕</h3>
          <p class="text-xs text-slate-500 mt-1.5 leading-relaxed">Belum ada tugas pengiriman yang ditugaskan kepada Anda saat ini.</p>
        </div>
        <button @click="router.push('/kurir/pool')" class="mt-2 px-6 py-2.5 bg-slate-800 text-white text-xs font-bold rounded-full hover:bg-slate-700 active:scale-95 transition-all">
          Cari Tugas di Pool
        </button>
      </div>

      <div v-else class="flex flex-col gap-4">
        <template v-for="item in deliveries" :key="item.id">
          
          <div v-if="item.status === 'DISIAPKAN'" class="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden flex flex-col p-5">
            <div class="flex justify-between items-start mb-3">
              <span class="px-3 py-1 bg-slate-100 text-slate-600 text-[10px] font-bold rounded-lg tracking-wider">{{ item.nomor }}</span>
              <span class="px-3 py-1 bg-orange-100 text-orange-700 text-[10px] font-bold rounded-lg tracking-wider">MENUNGGU ACC</span>
            </div>
            <h3 class="font-bold text-slate-800 mb-2">{{ item.jumlah_perhentian }} Lokasi Tujuan</h3>
            <p class="text-xs text-slate-500 mb-4 flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
              {{ formatTanggal(item.tanggal) }}
            </p>
            <button 
              @click="accPengiriman(item.id)"
              :disabled="isSubmitting"
              class="w-full py-3.5 bg-emerald-500 text-white font-bold text-sm rounded-2xl shadow-[0_8px_16px_-6px_rgba(16,185,129,0.4)] active:scale-[0.98] transition-all flex justify-center items-center gap-2"
            >
              <span v-if="isSubmitting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
              {{ isSubmitting ? 'Memproses...' : 'ACC & Mulai Perjalanan' }}
            </button>
          </div>

          <div v-for="stop in item.perhentian" :key="stop.id" class="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden flex flex-col p-5">
            <div class="flex justify-between items-start mb-2">
              <span class="px-2.5 py-1 bg-blue-50 text-blue-600 text-[10px] font-bold rounded-lg">Destinasi #{{ stop.urutan }}</span>
              <span 
                :class="{
                  'bg-emerald-100 text-emerald-700': stop.status === 'DITERIMA',
                  'bg-orange-100 text-orange-700': stop.status === 'MENUNGGU',
                  'bg-blue-100 text-blue-700': stop.status === 'SAMPAI'
                }"
                class="px-2.5 py-1 text-[10px] font-bold rounded-lg"
              >
                {{ stop.status }}
              </span>
            </div>

            <h3 class="font-black text-slate-800 text-base mb-1">{{ stop.pelanggan_nama || stop.nomor_distribusi }}</h3>
            <p class="text-xs text-slate-500 mb-4 leading-relaxed">{{ stop.alamat || 'Alamat tidak tersedia' }}</p>

            <div class="pt-3 border-t border-slate-50 flex items-center justify-between">
              <span class="text-[11px] font-bold text-slate-400">DO: {{ stop.nomor_distribusi }}</span>
              <button 
                @click="router.push('/kurir/on-go-delivery')"
                class="px-4 py-2 bg-slate-900 text-white text-xs font-bold rounded-xl hover:bg-slate-800 active:scale-95 transition-all flex items-center gap-1.5"
              >
                <span>Kelola</span>
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"></path></svg>
              </button>
            </div>
          </div>

        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useMyDeliveries } from '@/features/kurir/composables/useMyDeliveries'

const router = useRouter()
const toast = useToast()
const { deliveries, isLoading, loadDeliveries, startDelivery } = useMyDeliveries()
const isSubmitting = ref(false)

const totalJarak = computed(() => {
  return deliveries.value.reduce((total, item) => total + Number(item.jarak_total_km || 0), 0).toFixed(1)
})

const totalPerhentian = computed(() => {
  return deliveries.value.reduce((total, item) => total + (item.jumlah_perhentian || item.perhentian?.length || 0), 0)
})

const formatTanggal = (dateString) => {
  if (!dateString) return '-'
  const d = new Date(dateString)
  return d.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })
}

const accPengiriman = async (id) => {
  isSubmitting.value = true
  try {
    await startDelivery(id)
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  loadDeliveries()
})
</script>