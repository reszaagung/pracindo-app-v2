<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-xl md:text-2xl font-bold text-slate-800">Riwayat Batch Produksi</h1>
        <p class="text-sm text-slate-500 mt-1">Daftar seluruh batch mixing &amp; blending yang tercatat.</p>
      </div>
      <router-link
        :to="{ name: 'produksi-batch-buat' }"
        class="inline-flex items-center gap-2 bg-white border border-slate-200 text-slate-700 text-sm font-bold px-4 py-2.5 rounded-xl shadow-sm hover:bg-slate-50 active:scale-95 transition-all self-start sm:self-auto"
      >
        <i class="pi pi-plus text-sm text-slate-500"></i>
        Input Baru
      </router-link>
    </div>

    <p v-if="errorMsg" class="text-sm bg-red-50 text-red-600 border border-red-100 rounded-xl px-4 py-2.5">
      {{ errorMsg }}
    </p>

    <!-- FILTER PENCARIAN -->
    <div class="bg-white rounded-2xl border border-slate-100 shadow-[0_4px_20px_rgb(0,0,0,0.03)] p-4">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
       <div class="relative lg:col-span-2">
          <i class="pi pi-search absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm pointer-events-none"></i>
          <input
            v-model="filter.search"
            type="text"
            placeholder="Cari nomor batch / nama hasil..."
            class="w-full pl-10 pr-3 py-2.5 rounded-xl border border-slate-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-300"
            @input="cariDenganDebounce"
          />
        </div>

        <select
          v-model="filter.jenis"
          class="w-full py-2.5 px-3 rounded-xl border border-slate-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10"
          @change="muatUlang"
        >
          <option v-for="opt in JENIS_BATCH_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
        </select>
      </div>
    </div>

    <div class="bg-white rounded-2xl border border-slate-100 shadow-[0_4px_20px_rgb(0,0,0,0.03)] overflow-hidden">
      <!-- Tampilan Desktop -->
      <div v-if="!isMobile" class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-100">
              <th class="px-4 py-3 font-semibold text-slate-500 text-xs uppercase tracking-wide text-left">Nomor Batch</th>
              <th class="px-4 py-3 font-semibold text-slate-500 text-xs uppercase tracking-wide text-left">Tangki Tujuan</th>
              <th class="px-4 py-3 font-semibold text-slate-500 text-xs uppercase tracking-wide text-left">Nama Hasil</th>
              <th class="px-4 py-3 font-semibold text-slate-500 text-xs uppercase tracking-wide text-right">Qty Hasil (Kg)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-if="loading">
              <td colspan="4" class="px-4 py-10 text-center text-slate-400">
                <i class="pi pi-spin pi-spinner mr-2"></i>Memuat data...
              </td>
            </tr>
            <tr v-else-if="baris.length === 0">
              <td colspan="4" class="px-4 py-10 text-center text-slate-400">
                Belum ada batch produksi yang cocok dengan filter.
              </td>
            </tr>
            <tr v-for="row in baris" :key="row.id" class="hover:bg-slate-50/70 transition-colors">
              <td class="px-4 py-4 font-mono font-bold text-slate-800">{{ row.nomor || row.batch }}</td>
              <td class="px-4 py-4 text-slate-700">{{ row.tangki_kode || row.tangki_tujuan_nama || row.tangki || '-' }}</td>
              <td class="px-4 py-4 font-semibold text-blue-700">{{ row.nama_hasil }}</td>
              <td class="px-4 py-4 text-right font-black text-emerald-600">{{ formatAngka(row.qty_hasil) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="flex flex-col gap-4 p-4 bg-slate-50">
        <div v-if="loading" class="text-center text-slate-400 py-10">
          <i class="pi pi-spin pi-spinner mr-2"></i>Memuat data...
        </div>
        <div v-else-if="baris.length === 0" class="text-center text-slate-400 py-10">
          Belum ada batch produksi yang cocok dengan filter.
        </div>
        <div v-for="row in baris" :key="row.id" class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm flex flex-col gap-3">
          <div class="flex justify-between items-start border-b border-slate-100 pb-3">
            <div>
              <h3 class="font-mono font-bold text-slate-800">{{ row.nomor || row.batch }}</h3>
              <p class="text-xs text-slate-500 mt-1">{{ formatTanggal(row.tanggal || row.waktu) }}</p>
            </div>
            <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[10px] font-bold bg-slate-100 text-slate-600 border border-slate-200">
               {{ row.tangki_kode || row.tangki_tujuan_nama || row.tangki || '-' }}
            </span>
          </div>

          <div class="grid grid-cols-2 gap-2 text-xs">
             <div class="flex flex-col gap-1">
              <span class="text-slate-400 font-semibold uppercase">Nama Hasil</span>
              <span class="text-blue-700 font-bold">{{ row.nama_hasil }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-slate-400 font-semibold uppercase">Jenis</span>
              <span class="text-slate-700">{{ JENIS_BATCH_LABELS[row.jenis] || row.jenis }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-slate-400 font-semibold uppercase">Yield Output</span>
              <span class="text-emerald-600 font-black">{{ formatAngka(row.qty_hasil) }} Kg</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Paginasi -->
      <div
        v-if="!loading && baris.length > 0"
        class="flex items-center justify-between px-4 py-3 border-t border-slate-100 text-sm text-slate-500 bg-white"
      >
        <span>Halaman {{ halaman }}{{ totalHalaman ? ` dari ${totalHalaman}` : '' }}</span>
        <div class="flex gap-2">
          <button
            class="px-3 py-1.5 rounded-lg border border-slate-200 disabled:opacity-40 hover:bg-slate-50 transition-colors"
            :disabled="halaman <= 1 || loading"
            @click="gantiHalaman(halaman - 1)"
          >
            <i class="pi pi-chevron-left text-xs"></i>
          </button>
          <button
            class="px-3 py-1.5 rounded-lg border border-slate-200 disabled:opacity-40 hover:bg-slate-50 transition-colors"
            :disabled="!adaHalamanBerikut || loading"
            @click="gantiHalaman(halaman + 1)"
          >
            <i class="pi pi-chevron-right text-xs"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiBatch } from '../api'
import { useLayout } from '@/composables/useLayout'

// Impor config dipertahankan hanya untuk filter jenis
import { JENIS_BATCH_OPTIONS, JENIS_BATCH_LABELS } from '../uiConfigProduksi'

const router = useRouter()
const { isMobile } = useLayout()
const baris = ref([])
const loading = ref(false)
const errorMsg = ref('')
const filter = reactive({ jenis: '', search: '' })
const halaman = ref(1)
const totalHalaman = ref(0)
const adaHalamanBerikut = ref(false)
let timerDebounce = null

function formatTanggal(v) {
  if (!v) return '-'
  const d = new Date(v)
  if (isNaN(d)) return v
  return (
    d.toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' }) +
    ' ' +
    d.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })
  )
}

function formatAngka(v) {
  return Number(v || 0).toLocaleString('id-ID', { minimumFractionDigits: 3, maximumFractionDigits: 3 })
}

function formatRupiah(v) {
  return `Rp ${Number(v || 0).toLocaleString('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

async function muatData() {
  loading.value = true
  errorMsg.value = ''
  try {
    const params = { page: halaman.value }
    if (filter.jenis) params.jenis = filter.jenis
    if (filter.search) params.search = filter.search
    
    const res = await apiBatch.daftar(params)

    if (Array.isArray(res)) {
      baris.value = res
      totalHalaman.value = 0
      adaHalamanBerikut.value = false
    } else {
      baris.value = res?.results ?? []
      adaHalamanBerikut.value = Boolean(res?.next)
      const pageSize = baris.value.length || 1
      totalHalaman.value = res?.count ? Math.ceil(res.count / pageSize) : 0
    }
  } catch {
    errorMsg.value = 'Gagal memuat daftar batch produksi'
    baris.value = []
  } finally {
    loading.value = false
  }
}

function muatUlang() {
  halaman.value = 1
  muatData()
}

function cariDenganDebounce() {
  clearTimeout(timerDebounce)
  timerDebounce = setTimeout(muatUlang, 400)
}

function gantiHalaman(h) {
  if (h < 1) return
  halaman.value = h
  muatData()
}

onMounted(muatData)
</script>