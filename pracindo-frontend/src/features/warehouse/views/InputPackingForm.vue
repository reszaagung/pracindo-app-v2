<template>
  <div class="p-6 bg-white rounded-lg shadow max-w-4xl mx-auto">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-slate-800">Input Eksekusi Packing</h2>
      <button @click="$router.back()" class="px-4 py-2 border border-slate-200 rounded-lg text-slate-600 hover:bg-slate-50 transition-colors text-sm font-medium shadow-sm">
        Kembali
      </button>
    </div>

    <div v-if="errorFetch" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600 flex items-start gap-3">
      <i class="pi pi-exclamation-triangle mt-0.5"></i>
      <div>
        <strong>Gagal Memuat Data Referensi:</strong>
        <p>{{ errorFetch }}</p>
      </div>
    </div>

    <div v-if="error" class="mb-6 p-4 bg-rose-50 border border-rose-200 rounded-xl text-sm text-rose-600">
      {{ error }}
    </div>

    <form @submit.prevent="submitForm" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        
        <div>
          <label class="block text-sm font-medium text-slate-600 mb-1">Grup Kepemilikan</label>
          <select v-model="form.grup" required class="w-full border border-slate-200 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-400 outline-none transition-all text-slate-700 bg-slate-50" :disabled="isLoadingData">
            <option value="">{{ isLoadingData ? 'Memuat Grup...' : '-- Pilih Grup --' }}</option>
            <option v-for="g in grupList" :key="g.id" :value="g.id">
              {{ g.nama || g.kode }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-slate-600 mb-1">Tangki Sumber (WIP)</label>
          <select v-model="form.tangki" required class="w-full border border-slate-200 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-400 outline-none transition-all text-slate-700 bg-slate-50" :disabled="isLoadingData">
            <option value="">{{ isLoadingData ? 'Memuat Tangki...' : '-- Pilih Tangki --' }}</option>
            <option v-for="t in tangkis" :key="t.id" :value="t.id">
              {{ t.kode }} - {{ t.nama || 'Tangki' }}
              <template v-if="t.loadingSaldo"> (Memuat saldo...)</template>
              <template v-else-if="hitungSaldo(t.saldo) === 0"> (Kosong)</template>
              <template v-else> 
                (Isi: {{ hitungSaldo(t.saldo).toLocaleString('id-ID', {minimumFractionDigits: 0, maximumFractionDigits: 3}) }} Kg)
              </template>
            </option>
          </select>
          
          <p v-if="tangkiTerpilih" class="text-xs mt-1 font-semibold" :class="tangkiTerpilih.isi_kg > 0 ? 'text-emerald-600' : 'text-rose-500'">
            <i class="pi" :class="tangkiTerpilih.isi_kg > 0 ? 'pi-check-circle' : 'pi-times-circle'"></i> 
            Cairan tersedia: {{ tangkiTerpilih.isi_kg.toLocaleString('id-ID', {minimumFractionDigits: 0, maximumFractionDigits: 3}) }} Kg
          </p>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-600 mb-1">Barang Jadi (Produk Output)</label>
          <div class="relative" ref="produkWrapperRef">
            <input
              type="text"
              :value="produkQuery"
              @input="onProdukInput"
              @focus="onProdukFocus"
              @keydown.down.prevent="highlightNext"
              @keydown.up.prevent="highlightPrev"
              @keydown.enter.prevent="selectHighlighted"
              @keydown.esc="showProdukSuggestions = false"
              required
              autocomplete="off"
              role="combobox"
              aria-autocomplete="list"
              aria-controls="produk-listbox"
              :aria-expanded="showProdukSuggestions"
              class="w-full border border-slate-200 p-2.5 pr-9 rounded-lg focus:ring-2 focus:ring-emerald-100 focus:border-emerald-400 outline-none transition-all text-slate-700 bg-slate-50"
              placeholder="Ketik minimal 2-3 huruf nama barang jadi..."
            />
            <button
              v-if="form.produk"
              type="button"
              @click="clearProduk"
              tabindex="-1"
              class="absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-rose-500 transition-colors"
            >
              <i class="pi pi-times-circle"></i>
            </button>
            <i v-else-if="isSearchingProduk" class="pi pi-spin pi-spinner absolute right-3 top-1/2 -translate-y-1/2 text-slate-300 text-sm pointer-events-none"></i>
            <i v-else class="pi pi-search absolute right-3 top-1/2 -translate-y-1/2 text-slate-300 text-sm pointer-events-none"></i>

            <ul
              v-if="showProdukSuggestions"
              id="produk-listbox"
              role="listbox"
              class="absolute z-20 mt-1 w-full max-h-56 overflow-auto bg-white border border-slate-200 rounded-lg shadow-lg py-1"
            >
              <li v-if="isSearchingProduk" class="px-3 py-2 text-sm text-slate-400 italic flex items-center gap-2">
                <i class="pi pi-spin pi-spinner"></i> Mencari produk...
              </li>
              <template v-else>
                <li v-if="produkSearchError" class="px-3 py-2 text-sm text-rose-500">
                  {{ produkSearchError }}
                </li>
                <li v-else-if="produkOptions.length === 0" class="px-3 py-2 text-sm text-slate-400 italic">
                  Produk tidak ditemukan
                </li>
                <li
                  v-for="(p, idx) in produkOptions"
                  :key="p.id"
                  role="option"
                  :aria-selected="idx === highlightedIndex"
                  @click="pilihProduk(p)"
                  @mouseenter="highlightedIndex = idx"
                  class="px-3 py-2 text-sm cursor-pointer transition-colors"
                  :class="idx === highlightedIndex ? 'bg-emerald-50 text-emerald-700' : 'text-slate-700 hover:bg-slate-50'"
                >
                  {{ p.nama_item }}
                </li>
              </template>
            </ul>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-slate-600 mb-1">Total Qty Packing (Kg)</label>
          <select v-model="form.qty_kg" required class="w-full border border-slate-200 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-100 focus:border-blue-400 outline-none transition-all text-slate-700 bg-slate-50">
             <option value="">-- Pilih Qty --</option>
             <option v-for="n in nettopPack" :key="n" :value="n">{{ n }}</option>
          </select>
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
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { warehouseApi } from '../api' 
import { usePacking } from '../composables/usePacking'

const router = useRouter()
const { createPacking, isLoading, error, tangkis, fetchTangkisWithSaldo } = usePacking()

const grupList = ref([])
const kemasanLuarList = ref([])
const kemasanDalamList = ref([])

const isLoadingData = ref(true)
const errorFetch = ref('')
const butuhKemasanDalam = ref(false)

const form = reactive({
  grup: '',
  tangki: '',
  produk: '',
  qty_kg: '',
  kemasan: '',
  total_unit: '',
  kemasan_dalam: '',
  qty_kemasan_dalam: ''
})

const nettopPack = [30, 25, 20, 12, 5, 1]

const produkQuery = ref('')
const showProdukSuggestions = ref(false)
const highlightedIndex = ref(-1)
const produkWrapperRef = ref(null)
const produkOptions = ref([])
const isSearchingProduk = ref(false)
const produkSearchError = ref('')

let produkDebounceTimer = null
let produkRequestSeq = 0
const PRODUK_DEBOUNCE_MS = 350

const hitungSaldo = (saldoData) => {
  if (!saldoData) return 0
  if (Array.isArray(saldoData)) return saldoData.reduce((sum, b) => sum + Number(b.sisa_qty || b.saldo_qty || 0), 0)
  if (typeof saldoData === 'object') return Number(saldoData.sisa_qty || saldoData.saldo_qty || saldoData.qty || 0)
  return 0
}

const tangkiTerpilih = computed(() => {
  if (!form.tangki) return null
  const t = tangkis.value.find(x => x.id === form.tangki)
  if (!t) return null
  const isi_kg = hitungSaldo(t.saldo)
  return { ...t, isi_kg }
})

const cariBarangJadi = async (query) => {
  const seq = ++produkRequestSeq
  isSearchingProduk.value = true
  produkSearchError.value = ''
  try {
    const res = await warehouseApi.getMasterProduk({ search: query })
    if (seq !== produkRequestSeq) return 
    produkOptions.value = res.data?.results || res.data || []
  } catch (err) {
    if (seq !== produkRequestSeq) return
    produkOptions.value = []
    produkSearchError.value = err.response?.data?.pesan || err.message || 'Gagal mencari produk.'
  } finally {
    if (seq === produkRequestSeq) {
      isSearchingProduk.value = false
    }
  }
}

const onProdukFocus = () => {
  showProdukSuggestions.value = true
  if (produkOptions.value.length === 0 && !isSearchingProduk.value) {
    cariBarangJadi(produkQuery.value.trim())
  }
}

const onProdukInput = (event) => {
  produkQuery.value = event.target.value
  showProdukSuggestions.value = true
  highlightedIndex.value = -1
  if (form.produk) {
    form.produk = ''
  }

  clearTimeout(produkDebounceTimer)
  produkDebounceTimer = setTimeout(() => {
    cariBarangJadi(produkQuery.value.trim())
  }, PRODUK_DEBOUNCE_MS)
}

const pilihProduk = (p) => {
  form.produk = p.id
  produkQuery.value = p.nama_item
  showProdukSuggestions.value = false
  highlightedIndex.value = -1
}

const clearProduk = () => {
  form.produk = ''
  produkQuery.value = ''
  showProdukSuggestions.value = false
  highlightedIndex.value = -1
  produkOptions.value = []
}

const highlightNext = () => {
  if (!showProdukSuggestions.value) {
    showProdukSuggestions.value = true
    return
  }
  if (highlightedIndex.value < produkOptions.value.length - 1) {
    highlightedIndex.value++
  }
}

const highlightPrev = () => {
  if (highlightedIndex.value > 0) {
    highlightedIndex.value--
  }
}

const selectHighlighted = () => {
  const target = produkOptions.value[highlightedIndex.value]
  if (target) {
    pilihProduk(target)
  }
}

const handleClickOutsideProduk = (event) => {
  if (produkWrapperRef.value && !produkWrapperRef.value.contains(event.target)) {
    showProdukSuggestions.value = false
  }
}

const fetchData = async () => {
  isLoadingData.value = true
  errorFetch.value = ''
  
  try {
    const [resGrup, resKemasan] = await Promise.all([
      warehouseApi.getGrupAktif(),
      warehouseApi.getKemasanAktif(),
      fetchTangkisWithSaldo() 
    ])

    grupList.value = resGrup.data?.results || resGrup.data || []
    kemasanLuarList.value = resKemasan.data?.results || resKemasan.data || []
    kemasanDalamList.value = resKemasan.data?.results || resKemasan.data || []
    
  } catch (err) {
    errorFetch.value = err.response?.data?.pesan || err.message || 'Gagal memuat opsi pilihan dari server.'
  } finally {
    isLoadingData.value = false
  }
}

onMounted(() => {
  fetchData()
  document.addEventListener('click', handleClickOutsideProduk)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutsideProduk)
  clearTimeout(produkDebounceTimer)
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
    const dataSaldo = tangkiTerpilih.value?.saldo;
    const batchList = dataSaldo?.batches || (Array.isArray(dataSaldo) ? dataSaldo : []);
    
    if (!dataSaldo || batchList.length === 0) {
      alert("Tangki ini kosong! Tidak ada cairan batch yang bisa di-packing.");
      return;
    }

    const targetBatch = batchList[0];
    const batchId = targetBatch.id || targetBatch.batch_id || targetBatch.batch || targetBatch.pk;

    if (!form.produk) {
      alert("Pilih Barang Jadi terlebih dahulu!");
      return;
    }
    if (!batchId) {
      alert("Gagal membaca Batch ID dari tangki! Struktur data tidak sesuai.");
      return;
    }

    const hitungTotalKg = parseFloat(form.qty_kg) * parseInt(form.total_unit);

    const payload = {
      qty_kg: hitungTotalKg, 
      total_unit: form.total_unit,
      kemasan: form.kemasan,
      entitas: form.grup,
      batch: batchId,
      produk: form.produk,
      kemasan_dalam: butuhKemasanDalam.value ? form.kemasan_dalam : null,
      qty_kemasan_dalam: butuhKemasanDalam.value ? form.qty_kemasan_dalam : 0,
      status: 'POSTED'
    }
    
    await createPacking(payload)
    router.push({ name: 'InputPackingList' })
  } catch (err) {
    const pesanError = err?.response?.data || err?.data || err?.message || err;
    alert("Error Server: " + JSON.stringify(pesanError));
  }
}
</script>