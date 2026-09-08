<template>
    <div class="p-6 max-w-7xl mx-auto">
        <div class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-2xl font-bold text-slate-800">Master Data Retail</h1>
                <p class="text-slate-500 text-sm">Kelola identitas dan jaringan cabang toko retail.</p>
            </div>
            <button @click="bukaFormTambah" class="bg-slate-900 hover:bg-slate-800 text-white px-5 py-2.5 rounded-xl font-semibold flex items-center gap-2 transition-colors">
                <i class="pi pi-plus"></i> Daftarkan Retail Baru
            </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            <div v-for="toko in daftarToko" :key="toko.id" 
                 class="relative bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow group">
                
                <div class="bg-gradient-to-r from-slate-800 to-slate-900 px-4 py-2 flex justify-between items-center">
                    <span class="text-white text-xs font-bold tracking-widest uppercase">Retail Identity Card</span>
                    <span class="text-slate-300 text-xs font-mono">{{ toko.kode_cabang }}</span>
                </div>

                <div class="p-5 flex gap-4">
                    <div class="w-20 h-24 bg-slate-100 rounded-lg border-2 border-dashed border-slate-300 flex flex-col items-center justify-center flex-shrink-0">
                        <i class="pi pi-building text-2xl text-slate-400 mb-1"></i>
                        <span class="text-[10px] text-slate-400 font-semibold uppercase">Cabang</span>
                    </div>

                    <div class="flex-1 space-y-2">
                        <div>
                            <p class="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Nama Identitas</p>
                            <p class="text-sm font-bold text-slate-900 leading-tight">{{ toko.nama }}</p>
                        </div>
                        
                        <div>
                            <p class="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Alamat Lengkap</p>
                            <p class="text-xs text-slate-700 leading-snug">{{ toko.alamat }}</p>
                        </div>

                        <div class="flex justify-between items-end pt-1">
                            <div>
                                <p class="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Penanggung Jawab</p>
                                <p class="text-xs font-semibold text-slate-800">{{ toko.pic || 'Belum Ditunjuk' }}</p>
                            </div>
                            <span :class="toko.aktif ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" 
                                  class="text-[10px] px-2 py-0.5 rounded-full font-bold uppercase">
                                {{ toko.aktif ? 'Aktif' : 'Tutup' }}
                            </span>
                        </div>
                    </div>
                </div>

                <div class="absolute top-12 right-2 flex flex-col gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button class="w-8 h-8 bg-white border border-slate-200 shadow-sm rounded-full flex items-center justify-center text-blue-600 hover:bg-blue-50">
                        <i class="pi pi-pencil text-xs"></i>
                    </button>
                    <button class="w-8 h-8 bg-white border border-slate-200 shadow-sm rounded-full flex items-center justify-center text-red-600 hover:bg-red-50">
                        <i class="pi pi-trash text-xs"></i>
                    </button>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCabangRetail } from '../composables/useCabangRetail'

const { 
    daftarToko, 
    isLoading, 
    error, 
    muatDaftarToko 
} = useCabangRetail()

onMounted(() => {
    muatDaftarToko()
})

const bukaFormTambah = () => {
    alert("Siap bikin KTP Retail baru!")
}
</script>