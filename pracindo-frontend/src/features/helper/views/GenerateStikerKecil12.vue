<template>
  <div class="p-4 sm:p-6 max-w-7xl mx-auto">
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-6">
      <h2 class="text-xl sm:text-2xl font-bold text-gray-800">Generate Stiker Kecil (12 Slot)</h2>
      <button
        @click="submitStiker"
        :disabled="isSubmitting || !polaValid"
        class="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2.5 rounded-xl shadow-md transition-colors disabled:bg-blue-400"
      >
        {{ isSubmitting ? 'Memproses...' : 'Generate & Download Stiker' }}
      </button>
    </div>

    <div class="mb-8 bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col md:flex-row gap-6">
      <div class="w-full md:w-1/2">
        <label class="block text-gray-700 font-bold mb-3">Jenis Stiker:</label>
        <select v-model="jenisTerpilih" class="w-full p-3 border border-gray-300 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500">
          <option v-for="opsi in opsiJenis" :key="opsi.value" :value="opsi.value">{{ opsi.label }}</option>
        </select>
      </div>

      <div class="w-full md:w-1/2">
        <label class="block text-gray-700 font-bold mb-3">Pola Stiker:</label>
        <div v-if="sedangMuatPola" class="text-sm text-gray-400 py-3">Memuat pola...</div>
        <div v-else-if="daftarPolaTersedia.length === 0" class="text-sm text-gray-400 py-3">
          Belum ada template terdaftar untuk jenis ini.
        </div>
        <div v-else class="flex flex-wrap gap-2">
          <button
            v-for="item in daftarPolaTersedia"
            :key="item.id"
            type="button"
            @click="pilihPola(item)"
            class="px-4 py-2 rounded-lg border-2 text-sm font-mono transition-colors"
            :class="polaTerpilihId === item.id ? 'border-blue-600 bg-blue-50 text-blue-700 font-bold' : 'border-gray-300 bg-gray-50 text-gray-600 hover:border-gray-400'"
          >
            {{ item.kode }}
          </button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start" v-if="polaValid">
      <div class="lg:col-span-4 flex justify-center bg-gray-50 py-8 rounded-3xl border border-gray-200 shadow-inner">
        <GridPreviewKecil12 :pola="polaTerpilih" :form-data="formData" @pilih-huruf="setHurufAktif" />
      </div>

      <div class="lg:col-span-8 w-full flex flex-col gap-6">
        <FormGenerateStikerKecil12 v-if="!isMobile" />

        <div v-if="!hurufAktif" class="flex flex-col items-center justify-center h-full min-h-[220px] sm:min-h-[300px] p-8 sm:p-12 bg-white rounded-2xl border-2 border-dashed border-gray-300 text-gray-400">
          <p class="text-base sm:text-lg font-semibold text-center">Ketuk salah satu kotak stiker</p>
          <p class="text-sm text-center">untuk mulai mengisi data barang pada slot tersebut.</p>
        </div>

        <div v-if="adaDataTersimpan" class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-gray-100">
          <h4 class="text-base sm:text-lg font-bold text-gray-800 mb-4">Ringkasan Data Tersimpan:</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="huruf in hurufDipakai" :key="huruf">
              <div v-if="formData[huruf].is_saved" class="p-4 bg-green-50 border border-green-200 rounded-xl flex flex-col gap-1 relative overflow-hidden">
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
          <div class="relative w-full max-h-[85vh] overflow-y-auto">
            <div class="w-10 h-1.5 bg-slate-300 rounded-full mx-auto my-2"></div>
            <FormGenerateStikerKecil12 />
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import api from '../api'
import { useStikerKecil12 } from '../composables/useStikerKecil12'
import FormGenerateStikerKecil12 from './FormGenerateStikerKecil12.vue'
import GridPreviewKecil12 from '../components/GridPreviewKecil12.vue'

const toast = useToast()
const { formData, resetData, hurufAktif, tutupForm, setHurufAktif, namaTampil } = useStikerKecil12()
const isSubmitting = ref(false)

const opsiJenis = [
  { label: 'Polos Kecil', value: 'polos_kecil' },
  { label: 'CV Kecil', value: 'cv_kecil' },
  { label: 'PT Kecil', value: 'pt_kecil' },
]
const jenisTerpilih = ref(opsiJenis[0].value)

const daftarPolaTersedia = ref([])
const polaTerpilihId = ref(null)
const sedangMuatPola = ref(false)

const muatDaftarPola = async () => {
  sedangMuatPola.value = true
  polaTerpilihId.value = null
  daftarPolaTersedia.value = []
  resetData()
  try {
    const { data } = await api.get('fitur/template-stiker-kecil-12/', {
      params: { jenis: jenisTerpilih.value }
    })
    daftarPolaTersedia.value = data
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Tidak bisa memuat daftar pola dari server', life: 4000 })
  } finally {
    sedangMuatPola.value = false
  }
}

onMounted(muatDaftarPola)
watch(jenisTerpilih, muatDaftarPola)

const pilihPola = (item) => {
  polaTerpilihId.value = item.id
  resetData()
}

const isMobile = ref(typeof window !== 'undefined' ? window.innerWidth < 1024 : false)
const cekLebarLayar = () => { isMobile.value = window.innerWidth < 1024 }
onMounted(() => {
  cekLebarLayar()
  window.addEventListener('resize', cekLebarLayar)
})
onUnmounted(() => window.removeEventListener('resize', cekLebarLayar))

const polaTerpilih = computed(() => {
  const dipilih = daftarPolaTersedia.value.find(p => p.id === polaTerpilihId.value)
  return dipilih ? dipilih.pola : ''
})
const polaValid = computed(() => !!polaTerpilihId.value)

const hurufDipakai = computed(() => polaValid.value ? [...new Set(polaTerpilih.value)] : [])
const adaDataTersimpan = computed(() => Object.values(formData).some(d => d.is_saved))

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
    } catch { return null }
  }
  return err?.response?.data?.detail || null
}

const submitStiker = async () => {
  if (!polaValid.value) {
    toast.add({ severity: 'warn', summary: 'Peringatan', detail: 'Pilih pola terlebih dahulu!', life: 3000 })
    return
  }
  isSubmitting.value = true

  const itemsArray = hurufDipakai.value
    .filter(h => formData[h].nama_item !== null)
    .map(h => ({
      nama_item: formData[h].nama_item,
      tipe: formData[h].tipe,
      lot: formatTanggalLokal(formData[h].lot),
      net: formData[h].net
    }))

  if (itemsArray.length !== hurufDipakai.value.length) {
    toast.add({ severity: 'warn', summary: 'Belum Lengkap', detail: 'Isi semua grup sebelum generate!', life: 3000 })
    isSubmitting.value = false
    return
  }

  const payload = { jenis: jenisTerpilih.value, pola: polaTerpilih.value, items: itemsArray }

  try {
    const response = await api.post('fitur/generate-stiker-kecil-12/', payload, { responseType: 'blob' })
    const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
    const link = document.createElement('a')
    link.href = window.URL.createObjectURL(blob)
    link.download = `StikerKecil12_${jenisTerpilih.value}_${polaTerpilih.value}.docx`
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