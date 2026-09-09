<template>
    <div class="w-full p-4 flex flex-col gap-4 pb-24 bg-slate-50 min-h-screen">
        <div class="flex justify-between items-end mb-2">
            <div>
                <h1 class="text-xl font-bold text-slate-800">On-Go Delivery</h1>
                <p class="text-xs text-slate-500">Eksekusi pengiriman aktif Anda</p>
            </div>
            <button @click="loadDeliveries" class="text-blue-600 font-bold text-xs bg-blue-100 px-3 py-1.5 rounded-lg">
                Refresh
            </button>
        </div>

        <div v-if="isLoading" class="text-center py-10 text-slate-500 font-bold animate-pulse">
            Memuat data...
        </div>

        <div v-else-if="deliveries.length === 0" class="bg-white border-2 border-slate-200 rounded-2xl p-10 text-center">
            <span class="text-4xl">🏁</span>
            <p class="font-bold text-slate-700 mt-3">Tidak Ada Tugas Aktif</p>
            <p class="text-xs text-slate-500">Ambil tugas baru di Order Pool.</p>
        </div>

        <div v-else class="flex flex-col gap-6">
            <div v-for="delivery in deliveries" :key="delivery.id" class="bg-white border-2 border-blue-200 rounded-2xl p-4 shadow-sm relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
                
                <div class="flex justify-between items-center border-b border-slate-100 pb-3 mb-3">
                    <div>
                        <span class="text-[10px] font-bold bg-blue-100 text-blue-700 px-2 py-1 rounded">{{ delivery.nomor }}</span>
                        <p class="text-xs text-slate-500 mt-1">Status: <span class="font-bold">{{ delivery.status_label }}</span></p>
                    </div>
                    <button v-if="delivery.status === 'DISIAPKAN'" @click="startDelivery(delivery.id)"
                        class="px-4 py-2 bg-emerald-600 text-white font-bold text-xs rounded-xl">
                        MULAI JALAN
                    </button>
                </div>

                <!-- Daftar Tujuan -->
                <div class="flex flex-col gap-4">
                    <div v-for="stop in delivery.perhentian" :key="stop.id" class="bg-slate-50 rounded-xl p-3 border border-slate-200">
                        <div class="flex justify-between items-start">
                            <div>
                                <h3 class="text-sm font-bold text-slate-800">{{ stop.urutan }}. {{ stop.pelanggan_nama }}</h3>
                                <p class="text-xs text-slate-500 line-clamp-2">{{ stop.alamat }}</p>
                            </div>
                            <span class="text-[10px] font-bold uppercase" :class="stop.status === 'SELESAI' ? 'text-emerald-600' : 'text-orange-500'">
                                {{ stop.status }}
                            </span>
                        </div>

                        <!-- Tombol Aksi Upload -->
                        <div v-if="delivery.status === 'BERANGKAT'" class="grid grid-cols-2 gap-2 mt-4 pt-3 border-t border-slate-200">
                            
                            <button v-if="stop.status === 'MENUNGGU'" @click="markArrived(delivery.id, stop.id)"
                                class="col-span-2 py-2 bg-blue-600 text-white font-bold text-xs rounded-xl text-center">
                                Tiba di Lokasi
                            </button>

                            <template v-if="stop.status === 'SAMPAY' || stop.status === 'SELESAI'">
                                <!-- Upload Surat Jalan / Foto Barang -->
                                <label class="flex items-center justify-center gap-1.5 bg-white border-2 border-slate-200 hover:bg-slate-50 text-slate-700 text-[11px] font-bold py-2 rounded-xl cursor-pointer">
                                    <span>📸</span> Surat Jalan
                                    <input type="file" accept="image/*" class="hidden" @change="(e) => handleUpload(delivery.id, stop.id, 'surat_jalan', e)" />
                                </label>
                                
                                <!-- Upload Struk / Bon Pembayaran -->
                                <label class="flex items-center justify-center gap-1.5 bg-emerald-50 border-2 border-emerald-200 text-emerald-700 hover:bg-emerald-100 text-[11px] font-bold py-2 rounded-xl cursor-pointer">
                                    <span>📄</span> Struk / Bon
                                    <input type="file" accept="image/*,application/pdf" class="hidden" @change="(e) => handleUpload(delivery.id, stop.id, 'struk_bon', e)" />
                                </label>
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useMyDeliveries } from '@/features/kurir/composables/useMyDeliveries'

const { deliveries, isLoading, loadDeliveries, startDelivery, markArrived, uploadProof } = useMyDeliveries()

const handleUpload = async (deliveryId, stopId, jenisDokumen, event) => {
    const file = event.target.files[0]
    if (!file) return

    const success = await uploadProof(deliveryId, stopId, file, jenisDokumen)
    if (success) alert(`${jenisDokumen.replace('_', ' ').toUpperCase()} berhasil diunggah!`)
}

onMounted(() => loadDeliveries())
</script>