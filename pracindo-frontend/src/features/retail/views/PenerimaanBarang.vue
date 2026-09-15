<template>
  <div class="penerimaan-stok p-6 max-w-7xl mx-auto space-y-6">
    <header class="flex justify-between items-end border-b border-slate-200 pb-4">
      <div>
        <p class="text-sm text-slate-500 mb-1">Logistik Cabang</p>
        <h1 class="text-2xl font-bold text-slate-800">Penerimaan Barang (DO)</h1>
      </div>
    </header>

    <!-- Tabel Daftar Dokumen Pengiriman (GET) -->
    <div v-if="!dokumenAktif" class="bg-white rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden">
      <table class="min-w-full divide-y divide-slate-200">
        <thead class="bg-slate-50">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase">Nomor DO</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase">Status</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase">Tanggal Kirim</th>
            <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-if="daftarPenerimaan.length === 0">
            <td colspan="4" class="px-6 py-8 text-center text-slate-400">Belum ada dokumen pengiriman dari logistik.</td>
          </tr>
          <tr v-for="dokumen in daftarPenerimaan" :key="dokumen.id" class="hover:bg-slate-50 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-blue-600">{{ dokumen.nomor_penerimaan }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <span :class="dokumen.status === 'SELESAI' ? 'bg-emerald-100 text-emerald-700' : 'bg-orange-100 text-orange-700'" class="px-3 py-1 rounded-md text-xs font-bold">
                {{ dokumen.status }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-700">{{ formatTanggal(dokumen.tanggal_kirim) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-center">
              <button 
                v-if="dokumen.status !== 'SELESAI'" 
                @click="bukaDokumen(dokumen)"
                class="bg-slate-900 text-white px-4 py-2 rounded-lg text-xs font-bold hover:bg-slate-800 transition-colors"
              >
                Proses Terima
              </button>
              <span v-else class="text-xs font-semibold text-slate-400">Selesai</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Form Cek Fisik Barang (POST Proses) -->
    <div v-else class="bg-white rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 p-6 space-y-6">
      <div class="flex justify-between items-center border-b border-slate-100 pb-4">
        <div>
          <button @click="dokumenAktif = null" class="text-sm font-semibold text-blue-600 hover:underline mb-1 block">← Kembali ke Daftar</button>
          <h2 class="text-lg font-bold text-slate-800">DO: {{ dokumenAktif.nomor_penerimaan }}</h2>
        </div>
        <p class="text-sm text-slate-500">Referensi: <span class="font-semibold text-slate-700">{{ dokumenAktif.referensi_logistik || '-' }}</span></p>
      </div>

      <table class="min-w-full divide-y divide-slate-200">
        <thead class="bg-slate-50">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase">Nama Barang</th>
            <th class="px-6 py-4 text-left text-xs font-bold text-slate-500 uppercase">Kemasan</th>
            <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase">Unit Dikirim</th>
            <th class="px-6 py-4 text-center text-xs font-bold text-slate-500 uppercase w-48">Unit Diterima (Fisik)</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="(item, index) in dokumenAktif.items" :key="item.id" class="hover:bg-slate-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-slate-800">{{ item.produk_nama }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">{{ item.kemasan_nama || item.kemasan }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-center font-semibold text-slate-700">{{ item.unit_dikirim }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-center">
              <input 
                type="number" 
                v-model.number="dokumenAktif.items[index].unit_diterima" 
                min="0" 
                class="w-full text-center border border-slate-300 rounded-lg py-2 px-3 font-bold text-slate-800 outline-none focus:border-blue-500"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <div class="flex justify-end gap-3 pt-4 border-t border-slate-100">
        <button @click="dokumenAktif = null" class="bg-slate-100 text-slate-600 font-bold px-6 py-2.5 rounded-xl hover:bg-slate-200 transition-colors">Batal</button>
        <button @click="submitPenerimaan" :disabled="isLoading" class="bg-emerald-600 text-white font-bold px-6 py-2.5 rounded-xl hover:bg-emerald-700 transition-colors shadow-md flex items-center">
          <i v-if="isLoading" class="pi pi-spinner pi-spin mr-2"></i>
          <span>Simpan & Masukkan ke Stok</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { retailApi } from '../api'

const daftarPenerimaan = ref([])
const dokumenAktif = ref(null)
const isLoading = ref(false)

const fetchPenerimaan = async () => {
  try {
    const data = await retailApi.getPenerimaan()
    daftarPenerimaan.value = data.results || data
  } catch (error) {
    console.error("Gagal memuat data penerimaan:", error)
  }
}

onMounted(() => {
  fetchPenerimaan()
})

const formatTanggal = (isoString) => {
  if (!isoString) return '-'
  return new Date(isoString).toLocaleDateString('id-ID', {
    day: '2-digit', month: 'short', year: 'numeric'
  })
}

const bukaDokumen = (dokumen) => {
  dokumenAktif.value = JSON.parse(JSON.stringify(dokumen))
  dokumenAktif.value.items.forEach(item => {
    if (item.unit_diterima === 0) {
      item.unit_diterima = item.unit_dikirim
    }
  })
}

const submitPenerimaan = async () => {
  const adaMinus = dokumenAktif.value.items.some(item => item.unit_diterima < 0)
  if (adaMinus) {
    alert("Jumlah barang diterima tidak boleh kurang dari 0.")
    return
  }

  isLoading.value = true
  try {
    const payload = {
      items: dokumenAktif.value.items.map(item => ({
        id: item.id,
        unit_diterima: item.unit_diterima
      }))
    }

    await retailApi.prosesPenerimaan(dokumenAktif.value.id, payload)
    alert('Penerimaan berhasil disimpan dan stok cabang telah bertambah!')
    dokumenAktif.value = null
    fetchPenerimaan()
  } catch (error) {
    console.error("Gagal memproses penerimaan:", error)
    alert("Terjadi kesalahan saat menyimpan data ke server.")
  } finally {
    isLoading.value = false
  }
}
</script>