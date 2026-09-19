<template>
  <div class="p-4 sm:p-6 max-w-7xl mx-auto min-h-full flex flex-col pb-40 transition-all duration-300">
    
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-6 shrink-0">
      <h2 class="text-xl sm:text-2xl font-bold text-gray-800">Generate Stiker</h2>
      <button 
        @click="submitStiker" 
        :disabled="isSubmitting" 
        class="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2.5 rounded-xl shadow-md transition-colors disabled:bg-blue-400"
      >
        {{ isSubmitting ? 'Memproses...' : 'Generate & Download Stiker' }}
      </button>
    </div>

    <div class="mb-8 bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col md:flex-row gap-6 shrink-0">
      <div class="w-full md:w-1/2 flex flex-col gap-2">
        <label class="text-gray-700 font-bold">Jenis Stiker:</label>
        <select 
          v-model="jenisTerpilih" 
          class="w-full p-3 border border-gray-300 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500 transition-shadow"
        >
          <option v-for="opsi in opsiJenis" :key="opsi.value" :value="opsi.value">{{ opsi.label }}</option>
        </select>
      </div>

      <div class="w-full md:w-1/2 flex flex-col gap-2">
        <label class="text-gray-700 font-bold">Pola Stiker:</label>
        <select 
          v-model="polaTerpilih" 
          @change="resetData" 
          class="w-full p-3 border border-gray-300 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500 transition-shadow"
        >
          <option :value="null" disabled>-- Pilih Pola --</option>
          <option value="AAAA">Pola (AAAA)</option>
          <option value="AAAB">Pola (AAAB)</option>
          <option value="AABB">Pola (AABB)</option>
          <option value="AABC">Pola (AABC)</option>
          <option value="ABCD">Pola (ABCD)</option>
        </select>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start flex-grow" v-if="polaTerpilih">
      
      <div class="lg:col-span-4 flex justify-center bg-gray-50 py-8 rounded-3xl border border-gray-200 shadow-inner lg:sticky lg:top-4 transition-all">
        <component :is="komponenPreviewAktif" />
      </div>

      <div class="lg:col-span-8 w-full flex flex-col gap-6">
        <FormGenerateStiker v-if="!isMobile" />

        <div v-if="!hurufAktif" class="flex flex-col items-center justify-center h-full min-h-[220px] sm:min-h-[300px] p-8 sm:p-12 bg-white rounded-2xl border-2 border-dashed border-gray-300 text-gray-400 transition-all hover:bg-gray-50">
            <svg class="w-16 h-16 mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path></svg>
            <p class="text-base sm:text-lg font-semibold text-center">Ketuk salah satu kotak stiker</p>
            <p class="text-sm text-center">untuk mulai mengisi data barang pada slot tersebut.</p>
        </div>

        <div v-if="adaDataTersimpan" class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-gray-100 mt-auto">
            <h4 class="text-base sm:text-lg font-bold text-gray-800 mb-4">Ringkasan Data Tersimpan:</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-for="huruf in ['A', 'B', 'C', 'D']" :key="huruf">
                    <div v-if="formData[huruf].is_saved" class="p-4 bg-green-50 border border-green-200 rounded-xl flex flex-col gap-1 relative overflow-hidden transition-all hover:shadow-md">
                        <div class="absolute top-0 right-0 bg-green-500 text-white px-3 py-1 rounded-bl-lg text-xs font-bold">Grup {{ huruf }}</div>
                        <p class="font-bold text-gray-800 mt-2">{{ namaTampil(formData[huruf].nama_item) }}</p>
                        <p class="text-sm text-gray-600">Tipe: {{ formData[huruf].tipe || '-' }}</p>
                        <p class="text-sm text-gray-600">Lot: {{ formData[huruf].lot || '-' }} | Net: {{ formData[huruf].net || '-' }}</p>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>

    <Teleport to="body">
      <Transition name="sheet">
        <div v-if="isMobile && hurufAktif" class="fixed inset-0 z-[60] flex items-end">
          <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" @click="tutupForm"></div>
          
          <div class="relative w-full max-h-[85vh] overflow-y-auto pb-32 bg-slate-50 rounded-t-3xl shadow-[0_-10px_40px_rgba(0,0,0,0.1)]">
            <div class="sticky top-0 bg-slate-50/90 backdrop-blur-md z-10 pt-4 pb-3 flex justify-center border-b border-slate-200/50">
                <div class="w-12 h-1.5 bg-slate-300 rounded-full"></div>
            </div>
            <div class="p-4">
                <FormGenerateStiker />
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import api from '../api' 
import { useStiker } from '../composables/useStiker'
import FormGenerateStiker from './FormGenerateStiker.vue'

import PreviewAAAA from '../components/stiker_besar/stiker_besar_AAAA.vue'
import PreviewAAAB from '../components/stiker_besar/stiker_besar_AAAB.vue'
import PreviewAABB from '../components/stiker_besar/stiker_besar_AABB.vue'
import PreviewAABC from '../components/stiker_besar/stiker_besar_AABC.vue'
import PreviewABCD from '../components/stiker_besar/stiker_besar_ABCD.vue'

const toast = useToast()
const { formData, resetData, hurufAktif, tutupForm, namaTampil } = useStiker() 
const isSubmitting = ref(false)

const opsiJenis = [
  { label: 'Polos Besar', value: 'polos_besar' },
  { label: 'CV Besar', value: 'cv_besar' },
  { label: 'PT Besar', value: 'pt_besar' },
]

const jenisTerpilih = ref(opsiJenis[0].value)
const polaTerpilih = ref(null)

const isMobile = ref(typeof window !== 'undefined' ? window.innerWidth < 1024 : false)
const cekLebarLayar = () => { isMobile.value = window.innerWidth < 1024 }
onMounted(() => {
    cekLebarLayar()
    window.addEventListener('resize', cekLebarLayar)
})
onUnmounted(() => {
    window.removeEventListener('resize', cekLebarLayar)
})

const komponenPreviewAktif = computed(() => {
    switch (polaTerpilih.value) {
        case 'AAAA': return PreviewAAAA
        case 'AAAB': return PreviewAAAB
        case 'AABB': return PreviewAABB
        case 'AABC': return PreviewAABC
        case 'ABCD': return PreviewABCD
        default: return null
    }
})

const adaDataTersimpan = computed(() => {
    return Object.values(formData).some(data => data.is_saved)
})

const formatTanggalLokal = (date) => {
    if (!date) return null
    const d = new Date(date)
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const bacaPesanErrorBlob = async (err) => {
    const data = err?.response?.data
    if (data instanceof Blob) {
        try {
            const teks = await data.text()
            const json = JSON.parse(teks)
            return json.detail || Object.values(json)?.[0]?.[0] || teks
        } catch {
            return null
        }
    }
    return err?.response?.data?.detail || null
}

const submitStiker = async () => {
    if (!polaTerpilih.value) {
        toast.add({ severity: 'warn', summary: 'Peringatan', detail: 'Pilih pola stiker terlebih dahulu!', life: 3000 })
        return
    }

    isSubmitting.value = true
    
    const itemsArray = Object.keys(formData)
        .filter(key => formData[key].nama_item !== null)
        .map(key => ({
            nama_item: formData[key].nama_item,
            tipe: formData[key].tipe,
            lot: formatTanggalLokal(formData[key].lot),
            net: formData[key].net
        }))

    if (itemsArray.length === 0) {
        toast.add({ severity: 'warn', summary: 'Kosong', detail: 'Isi minimal satu barang sebelum generate!', life: 3000 })
        isSubmitting.value = false
        return
    }

    const payload = {
        jenis: jenisTerpilih.value,
        pola: polaTerpilih.value,
        items: itemsArray
    }

    try {
        const response = await api.post('fitur/generate-stiker/', payload, {
            responseType: 'blob'
        })
        
        const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = `Stiker_${jenisTerpilih.value}_${polaTerpilih.value}.docx`
        
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)

        toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Stiker berhasil diunduh!', life: 3000 })
    } catch (err) {
        const pesanDetail = await bacaPesanErrorBlob(err)
        toast.add({ severity: 'error', summary: 'Gagal', detail: pesanDetail || 'Terjadi kesalahan pada server saat merender dokumen', life: 4000 })
    } finally {
        isSubmitting.value = false
    }
}
</script>

<style scoped>
.sheet-enter-active, .sheet-leave-active { transition: opacity 0.22s ease; }
.sheet-enter-from, .sheet-leave-to { opacity: 0; }
.sheet-enter-active .relative, .sheet-leave-active .relative { transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1); }
.sheet-enter-from .relative, .sheet-leave-to .relative { transform: translateY(24px); }
</style>