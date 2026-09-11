<template>
  <div class="p-6 max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Generate Stiker</h2>
      <button 
        @click="submitStiker" 
        :disabled="isSubmitting" 
        class="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2 rounded-xl shadow-md transition-colors disabled:bg-blue-400"
      >
        {{ isSubmitting ? 'Memproses...' : 'Generate & Download Stiker' }}
      </button>
    </div>

    <div class="mb-8 bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col md:flex-row gap-6">
      <div class="w-full md:w-1/2">
        <label class="block text-gray-700 font-bold mb-3">Jenis Stiker:</label>
        <select 
          v-model="jenisTerpilih" 
          class="w-full p-3 border border-gray-300 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500"
        >
          <option value="Polos Besar">Polos Besar</option>
          <option value="CV Besar">CV Besar</option>
        </select>
      </div>

      <div class="w-full md:w-1/2">
        <label class="block text-gray-700 font-bold mb-3">Pola Stiker:</label>
        <select 
          v-model="polaTerpilih" 
          @change="resetData" 
          class="w-full p-3 border border-gray-300 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500"
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

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start" v-if="polaTerpilih">
      <div class="lg:col-span-4 flex justify-center bg-gray-50 py-8 rounded-3xl border border-gray-200 shadow-inner">
        <component :is="komponenPreviewAktif" />
      </div>

      <div class="lg:col-span-8 w-full flex flex-col gap-6">
        <FormGenerateStiker />
        
        <div v-if="!hurufAktif" class="flex flex-col items-center justify-center h-full min-h-[300px] p-12 bg-white rounded-2xl border-2 border-dashed border-gray-300 text-gray-400">
            <svg class="w-16 h-16 mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path></svg>
            <p class="text-lg font-semibold">Klik salah satu kotak stiker di samping</p>
            <p class="text-sm">untuk mulai mengisi data barang pada slot tersebut.</p>
        </div>

        <div v-if="adaDataTersimpan" class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h4 class="text-lg font-bold text-gray-800 mb-4">Ringkasan Data Tersimpan:</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-for="huruf in ['A', 'B', 'C', 'D']" :key="huruf">
                    <div v-if="formData[huruf].is_saved" class="p-4 bg-green-50 border border-green-200 rounded-xl flex flex-col gap-1 relative overflow-hidden">
                        <div class="absolute top-0 right-0 bg-green-500 text-white px-3 py-1 rounded-bl-lg text-xs font-bold">Grup {{ huruf }}</div>
                        <p class="font-bold text-gray-800 mt-2">{{ formData[huruf].nama_item || '(Tanpa Nama)' }}</p>
                        <p class="text-sm text-gray-600">Tipe: {{ formData[huruf].tipe || '-' }}</p>
                        <p class="text-sm text-gray-600">Lot: {{ formData[huruf].lot || '-' }} | Net: {{ formData[huruf].net || '-' }}</p>
                    </div>
                </div>
            </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
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
const { formData, resetData, hurufAktif } = useStiker() 
const isSubmitting = ref(false)

const jenisTerpilih = ref('Polos Besar')
const polaTerpilih = ref(null)

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

const submitStiker = async () => {
    if (!polaTerpilih.value) {
        toast.add({ severity: 'warn', summary: 'Peringatan', detail: 'Pilih pola stiker terlebih dahulu!', life: 3000 })
        return
    }

    isSubmitting.value = true
    
    const itemsArray = Object.keys(formData)
        .filter(key => formData[key].nama_item !== '')
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
        link.download = `Stiker_${jenisTerpilih.value.replace(' ', '_')}_${polaTerpilih.value}.docx`
        
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)

        toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Stiker berhasil diunduh!', life: 3000 })
    } catch (err) {
        toast.add({ severity: 'error', summary: 'Gagal', detail: 'Terjadi kesalahan pada server saat merender dokumen', life: 4000 })
    } finally {
        isSubmitting.value = false
    }
}
</script>