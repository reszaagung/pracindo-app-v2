<template>
  <div class="p-6 bg-white rounded-lg shadow max-w-4xl mx-auto">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-slate-800">Input Eksekusi Packing</h2>
      <button @click="$router.back()" class="px-4 py-2 border border-slate-200 rounded-lg text-slate-600 hover:bg-slate-50 transition-colors text-sm font-medium shadow-sm">
        Kembali
      </button>
    </div>

    <!-- Alert jika gagal konek ke backend -->
    <div v-if="errorFetch" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600 flex items-start gap-3">
      <i class="pi pi-exclamation-triangle mt-0.5"></i>
      <div>
        <strong>Gagal Memuat Data Referensi:</strong>
        <p>{{ errorFetch }}</p>
      </div>
    </div>

    <!-- Notifikasi Sukses/Loading Submit -->
    <div v-if="error" class="mb-6 p-4 bg-rose-50 border border-rose-200 rounded-xl text-sm text-rose-600">
      {{ error }}
    </div>

    <form @submit.prevent="submitForm" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div>
          <label class="block text-sm font-medium text-slate-600 mb-1">Entitas</label>
          <select v-model="form.entitas" required class="w-full border border-slate-200 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-400 outline-none transition-all text-slate-700 bg-slate-50" :disabled="isLoadingData">
            <option value="">{{ isLoadingData ? 'Memuat Entitas...' : '-- Pilih Entitas --' }}</option>
            <!-- Deteksi otomatis nama atau kode -->
            <option v-for="ent in entitasList" :key="ent.id" :value="ent.id">
              {{ ent.nama || ent.kode || ent.entitas_kode }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-slate-600 mb-1">Batch Produksi (WIP)</label>
          <select v-model="form.batch" required class="w-full border border-slate-200 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-400 outline-none transition-all text-slate-700 bg-slate-50" :disabled="isLoadingData">
            <option value="">{{ isLoadingData ? 'Memuat Batch...' : '-- Pilih Batch --' }}</option>
            <option v-for="b in batchList" :key="b.id" :value="b.id">
              {{ b.nomor || b.batch_nomor }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-slate-600 mb-1">Total Qty Cairan (Kg)</label>
          <input type="number" step="0.001" v-model="form.qty_kg" required class="w-full border border-slate-200 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-400 outline-none transition-all text-slate-700 bg-slate-50" placeholder="0.000" />
        </div>
      </div>

      <hr class="border-slate-100" />

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div>
          <label class="block text-sm font-medium text-slate-600 mb-1">Kemasan Luar (Dus/Jerigen)</label>
          <select v-model="form.kemasan" @change="cekKemasanDalam" required class="w-full border border-slate-200 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-400 outline-none transition-all text-slate-700 bg-white" :disabled="isLoadingData">
             <option value="">{{ isLoadingData ? 'Memuat Kemasan...' : '-- Pilih Kemasan --' }}</option>
             <option v-for="k in kemasanLuarList" :key="k.id" :value="k.id">
               {{ k.produk_nama || k.nama || k.kemasan_nama }}
             </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-slate-600 mb-1">Total Unit (Kemasan Luar)</label>
          <input type="number" v-model="form.total_unit" required class="w-full border border-slate-200 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-400 outline-none transition-all text-slate-700 bg-slate-50" placeholder="0" />
        </div>
      </div>

      
      <div v-if="butuhKemasanDalam" class="bg-blue-50/50 p-5 border border-blue-100 rounded-xl grid grid-cols-1 md:grid-cols-2 gap-5 mt-4">
        <div>
          <label class="block text-sm font-bold text-blue-800 mb-1">Isi Kemasan Dalam (Botol)</label>
          <select v-model="form.kemasan_dalam" required class="w-full border border-blue-200 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-200 focus:border-blue-500 outline-none transition-all text-blue-900 bg-white">
             <option value="">-- Pilih Botol --</option>
             <option v-for="k in kemasanDalamList" :key="k.id" :value="k.id">
               {{ k.produk_nama || k.nama || k.kemasan_nama }}
             </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-bold text-blue-800 mb-1">Isi Per Dus (Pcs)</label>
          <input type="number" v-model="form.qty_kemasan_dalam" required class="w-full border border-blue-200 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-200 focus:border-blue-500 outline-none transition-all text-blue-900 bg-white" placeholder="Contoh: 12" />
        </div>
      </div>

      <div class="flex justify-end pt-4">
        <button type="submit" :disabled="isLoading || isLoadingData" class="bg-slate-900 text-white px-6 py-2.5 rounded-lg hover:bg-slate-800 font-semibold shadow-md disabled:opacity-50 transition-all flex items-center gap-2">
          <i v-if="isLoading" class="pi pi-spin pi-spinner"></i>
          {{ isLoading ? 'Mengeksekusi...' : 'Simpan & Eksekusi Packing' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { warehouseApi } from '../api' 
import { usePacking } from '../composables/usePacking'

const router = useRouter()
const { createPacking, isLoading, error } = usePacking()

const entitasList = ref([])
const batchList = ref([])
const kemasanLuarList = ref([])
const kemasanDalamList = ref([])

const isLoadingData = ref(true)
const errorFetch = ref('')
const butuhKemasanDalam = ref(false)

const form = reactive({
  entitas: '',
  batch: '',
  qty_kg: '',
  kemasan: '',
  total_unit: '',
  kemasan_dalam: '',
  qty_kemasan_dalam: ''
})

const fetchData = async () => {
  isLoadingData.value = true
  errorFetch.value = ''
  
  try {
    const [resEntitas, resKemasan, resBatch] = await Promise.all([
      warehouseApi.getEntitasAktif(),
      warehouseApi.getKemasanAktif(),
      warehouseApi.getBatchTersedia()
    ])

    entitasList.value = resEntitas.data?.results || resEntitas.data || []
    kemasanLuarList.value = resKemasan.data?.results || resKemasan.data || []
    kemasanDalamList.value = resKemasan.data?.results || resKemasan.data || []
    batchList.value = resBatch.data?.results || resBatch.data || []
    
  } catch (err) {
    console.error("Gagal mengambil master data:", err)
    errorFetch.value = err.response?.data?.pesan || err.message || 'Gagal memuat opsi pilihan dari server.'
  } finally {
    isLoadingData.value = false
  }
}

onMounted(() => {
  fetchData()
})

const cekKemasanDalam = (event) => {
  const selectedText = event.target.options[event.target.selectedIndex]?.text?.toUpperCase() || ''
  
  if (selectedText.includes('DUS') || selectedText.includes('KARTON')) {
    butuhKemasanDalam.value = true
  } else {
    butuhKemasanDalam.value = false
    form.kemasan_dalam = ''
    form.qty_kemasan_dalam = ''
  }
}

const submitForm = async () => {
  try {
    const payload = {
      ...form,
      kemasan_dalam: butuhKemasanDalam.value ? form.kemasan_dalam : null,
      qty_kemasan_dalam: butuhKemasanDalam.value ? form.qty_kemasan_dalam : 0
    }
    
    await createPacking(payload)

    router.push({ name: 'InputPackingList' })
  } catch (err) {
  }
}
</script>