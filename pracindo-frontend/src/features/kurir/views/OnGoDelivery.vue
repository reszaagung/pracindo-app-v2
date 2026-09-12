<template>
  <div class="flex flex-col gap-6 pb-24">
    
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-xl font-bold text-slate-800">Tugas Aktif</h1>
        <p class="text-xs text-slate-500">Eksekusi pengiriman Anda hari ini</p>
      </div>
      <button @click="loadDeliveries" :disabled="isLoading" class="text-emerald-600 p-2 hover:bg-emerald-50 rounded-full transition-colors">
        <svg :class="{'animate-spin': isLoading}" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-10 text-slate-500 font-bold animate-pulse">
        Memuat data tugas...
    </div>

    <!-- Empty State -->
    <div v-else-if="deliveries.length === 0" class="bg-white border border-slate-100 rounded-3xl p-10 text-center shadow-sm">
        <span class="text-5xl">🛵</span>
        <p class="font-bold text-slate-700 mt-4 text-lg">Semua Selesai!</p>
        <p class="text-xs text-slate-500 mt-1">Anda tidak memiliki pengiriman yang sedang berjalan.</p>
    </div>

    <!-- Delivery List -->
    <div v-else class="flex flex-col gap-8">
      <div v-for="delivery in deliveries" :key="delivery.id" class="flex flex-col gap-4">
        
        <!-- Header Grup Pengiriman -->
        <div class="flex justify-between items-end border-b border-slate-200 pb-2">
            <div>
                <span class="text-[10px] font-bold bg-slate-800 text-white px-2 py-1 rounded">{{ delivery.nomor }}</span>
                <p class="text-xs font-bold text-slate-500 mt-2">{{ delivery.jumlah_perhentian }} Destinasi Tersisa</p>
            </div>
            <!-- Tombol Mulai Jalan (Jika Masih Disiapkan) -->
            <button v-if="delivery.status === 'DISIAPKAN'" @click="startDelivery(delivery.id)"
                class="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs rounded-xl shadow-md active:scale-95 transition-all">
                Mulai Perjalanan
            </button>
        </div>

        <!-- Render Card Destinasi menggunakan CardOrderDelivery.vue -->
        <CardOrderDelivery 
          v-for="stop in delivery.perhentian" 
          :key="stop.id" 
          :stop="stop"
        >
          <!-- Mengisi slot aksi dengan tombol-tombol fungsional Kurir -->
          <template #actions v-if="delivery.status === 'BERANGKAT'">
            
            <button v-if="stop.status === 'MENUNGGU'" @click="markArrived(delivery.id, stop.id)"
                class="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl text-center shadow-md active:scale-95 transition-all">
                Tiba di Lokasi
            </button>

            <div v-else-if="stop.status === 'SAMPAI'" class="grid grid-cols-2 gap-2 mt-2">
                <label class="flex items-center justify-center gap-1.5 bg-emerald-50 border-2 border-emerald-200 text-emerald-700 hover:bg-emerald-100 text-[11px] font-bold py-2.5 rounded-xl cursor-pointer transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                    Foto Bukti
                    <input type="file" accept="image/*" class="hidden" @change="(e) => handleUpload(delivery.id, stop.id, 'bukti_terima', e)" />
                </label>
                
                <label class="flex items-center justify-center gap-1.5 bg-red-50 border-2 border-red-200 text-red-700 hover:bg-red-100 text-[11px] font-bold py-2.5 rounded-xl cursor-pointer transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    Barang Diretur
                    <!-- Sementara pakai upload foto retur. Idealnya modal form retur -->
                    <input type="file" accept="image/*" class="hidden" @change="(e) => handleUpload(delivery.id, stop.id, 'retur', e)" />
                </label>
            </div>
            
          </template>
        </CardOrderDelivery>

      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import CardOrderDelivery from '@/features/kurir/components/CardOrderDelivery.vue'
import { useMyDeliveries } from '@/features/kurir/composables/useMyDeliveries'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const { deliveries, isLoading, loadDeliveries, startDelivery, markArrived, uploadProof } = useMyDeliveries()

const handleUpload = async (deliveryId, stopId, jenisAksi, event) => {
    const file = event.target.files[0]
    if (!file) return

    const success = await uploadProof(deliveryId, stopId, file, jenisAksi)
    if (success) {
      toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Dokumen terkirim ke server!', life: 3000 })
    }
}

onMounted(() => {
  loadDeliveries()
})
</script>