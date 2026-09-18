<template>
  <div class="space-y-6 relative">
    <div class="flex flex-col md:flex-row md:justify-between md:items-end gap-4 mb-8">
      <div>
        <div class="text-xs font-semibold text-slate-400 mb-1 tracking-wider uppercase">Distribution / Status Armada</div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-800">Pantau Armada</h1>
        <p class="text-slate-500 text-sm mt-1">Ketersediaan truk dan kendaraan saat ini.</p>
      </div>
      <button @click="bukaModal" class="bg-slate-900 hover:bg-slate-800 text-white px-6 py-2.5 rounded-xl font-medium transition-colors flex items-center gap-2 shadow-md">
        <i class="pi pi-plus text-sm"></i>
        <span>Registrasi Armada</span>
      </button>
    </div>

    <div v-if="memuat" class="flex justify-center items-center py-12">
      <i class="pi pi-spin pi-spinner text-3xl text-emerald-500"></i>
    </div>

    <div v-else-if="galat" class="bg-rose-50 border border-rose-200 text-rose-700 p-4 rounded-xl flex items-start gap-3">
      <i class="pi pi-exclamation-triangle mt-0.5"></i>
      <p class="text-sm">{{ galat }}</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-if="armadaList.length === 0" class="col-span-full bg-slate-50 border border-slate-200 rounded-2xl p-12 text-center">
        <div class="w-16 h-16 bg-slate-200 rounded-full flex items-center justify-center mx-auto mb-4">
          <i class="pi pi-truck text-2xl text-slate-400"></i>
        </div>
        <h3 class="text-slate-700 font-bold mb-1">Tidak Ada Armada</h3>
        <p class="text-slate-500 text-sm">Belum ada data kendaraan yang terdaftar di sistem.</p>
      </div>

      <div v-for="truk in armadaList" :key="truk.id"
           class="bg-white border rounded-2xl p-6 transition-all duration-300 hover:shadow-lg"
           :class="truk.aktif !== false ? 'border-slate-200' : 'border-rose-100 bg-rose-50/30'">
        <div class="flex justify-between items-start mb-6">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full flex items-center justify-center"
                 :class="truk.aktif !== false ? 'bg-slate-100 text-slate-600' : 'bg-rose-100 text-rose-500'">
              <i class="pi pi-truck"></i>
            </div>
            <div>
              <h3 class="text-slate-800 font-bold text-lg leading-tight">
                {{ truk.plat_nomor || truk.kode }}
              </h3>
              <p class="text-slate-500 text-xs">{{ truk.nama }}</p>
            </div>
          </div>
          <span class="px-3 py-1 rounded-full text-[10px] font-bold tracking-wider"
                :class="truk.aktif !== false
                  ? 'bg-emerald-100 text-emerald-700 border border-emerald-200'
                  : 'bg-rose-100 text-rose-700 border border-rose-200'">
            {{ truk.aktif !== false ? 'TERSEDIA' : 'NONAKTIF' }}
          </span>
        </div>

        <div class="bg-slate-50 rounded-xl p-4 mb-6 border border-slate-100">
          <p class="text-[10px] font-bold text-slate-400 mb-1 uppercase tracking-wider">Informasi Kendaraan</p>
          <div class="flex items-center gap-2">
            <i class="pi pi-id-card text-slate-400"></i>
            <span class="text-slate-700 text-sm font-medium">Kode: {{ truk.kode || '-' }}</span>
          </div>
        </div>

        <div class="flex items-end justify-between pt-4 border-t border-slate-100">
          <div>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-0.5">Kapasitas Maks</p>
            <p class="text-slate-700 font-bold">
              {{ formatKapasitas(truk.kapasitas_kg) }}
            </p>
          </div>
          <button class="text-blue-600 hover:text-blue-700 text-sm font-semibold flex items-center gap-1 group">
            Detail
            <i class="pi pi-arrow-right text-xs transition-transform group-hover:translate-x-1"></i>
          </button>
        </div>
      </div>
    </div>

    <div v-if="tampilModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm transition-opacity">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-fade-in">
        <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h2 class="font-bold text-slate-800 text-lg">Registrasi Armada Baru</h2>
          <button @click="tutupModal" class="text-slate-400 hover:text-rose-500 transition-colors">
            <i class="pi pi-times text-lg"></i>
          </button>
        </div>
        
        <form @submit="tanganiSubmit" class="p-6 flex flex-col gap-5">
          <div v-if="formGalat" class="p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-600 font-medium flex items-start gap-2">
            <i class="pi pi-exclamation-triangle mt-0.5"></i>
            <span>{{ formGalat }}</span>
          </div>
          
          <div class="flex flex-col gap-1.5">
            <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Plat Nomor *</label>
            <input type="text" v-model="form.plat_nomor" required placeholder="Contoh: B 1234 CD"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800 font-medium uppercase" />
          </div>

          <div class="flex flex-col gap-1.5">
            <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Nama Kendaraan</label>
            <input type="text" v-model="form.nama" placeholder="Contoh: Truk Engkel Box"
                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800 font-medium" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Kode Internal</label>
              <input type="text" v-model="form.kode" placeholder="T-001"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800 font-medium uppercase" />
            </div>
            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Kapasitas (KG) *</label>
              <input type="number" v-model="form.kapasitas_kg" required min="1" placeholder="2000"
                  class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800 font-medium" />
            </div>
          </div>

          <div class="flex justify-end gap-3 mt-4">
            <button type="button" @click="tutupModal" class="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-bold rounded-xl transition-colors">
              Batal
            </button>
            <button type="submit" class="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold rounded-xl transition-all shadow-md flex items-center gap-2">
              <i class="pi pi-save text-xs"></i>
              <span>Simpan Armada</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { apiDistribusi } from '../api.js'

const armadaList = ref([])
const memuat = ref(true)
const galat = ref(null)

const tampilModal = ref(false)
const formGalat = ref('')

const form = reactive({
  plat_nomor: '',
  nama: '',
  kode: '',
  kapasitas_kg: ''
})

const formatKapasitas = (kg) => {
  if (!kg) return 'Tidak disetel'
  const angka = parseFloat(kg)
  if (angka >= 1000) {
    return `${(angka / 1000).toLocaleString('id-ID')} Ton`
  }
  return `${angka.toLocaleString('id-ID')} Kg`
}

const muatDataArmada = async () => {
  memuat.value = true
  galat.value = null
  try {
    const data = await apiDistribusi.getArmada()
    armadaList.value = data.results || data || []
  } catch (error) {
    galat.value = "Gagal memuat daftar kendaraan dari server."
  } finally {
    memuat.value = false
  }
}

const bukaModal = () => {
  form.plat_nomor = ''
  form.nama = ''
  form.kode = ''
  form.kapasitas_kg = ''
  formGalat.value = ''
  tampilModal.value = true
}

const tutupModal = () => {
  tampilModal.value = false
}

const tanganiSubmit = (e) => {
    e.preventDefault();
    console.log("Tombol Ditekan! Data form:", { ...form });
    submitArmada();
}

const submitArmada = async () => {
  formGalat.value = 'Mencoba mengirim data...' 
  try {
    const payload = {
      plat_nomor: form.plat_nomor,
      nama: form.nama,
      kode: form.kode,
      kapasitas_kg: parseFloat(form.kapasitas_kg)
    }
    console.log("Mengirim payload:", payload);
    
    await apiDistribusi.tambahArmada(payload) 
    
    console.log("Berhasil disimpan!");
    tutupModal()
    await muatDataArmada()
  } catch (err) {
    console.error("Error aslinya bos:", err) 
    
    if (err.response?.data) {
      const data = err.response.data
      if (typeof data === 'object') {
        const errorKey = Object.keys(data)[0]
        if (Array.isArray(data[errorKey])) {
           formGalat.value = `${errorKey}: ${data[errorKey][0]}`
        } else {
           formGalat.value = data.detail || JSON.stringify(data)
        }
      } else {
        formGalat.value = err.response.data
      }
    } else {
      formGalat.value = err.message || 'Gagal menyimpan data armada. (Cek fungsi tambahArmada di api.js)'
    }
  }
}

onMounted(() => {
  muatDataArmada()
})
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.2s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>