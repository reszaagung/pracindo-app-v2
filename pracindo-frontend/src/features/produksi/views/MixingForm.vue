<template>
  <div class="space-y-4">

    <!-- ERROR -->
    <div
      v-if="errorMsg"
      class="bg-red-50 text-red-600 border border-red-100 rounded-lg px-4 py-2.5 text-sm"
    >
      {{ errorMsg }}
    </div>

    <!-- VALIDATION ERROR -->
    <div
      v-if="validasiTangkiError"
      class="bg-amber-50 text-amber-700 border border-amber-100 rounded-lg px-4 py-2.5 text-sm"
    >
      {{ validasiTangkiError }}
    </div>

    <!-- LOADING -->
    <div
      v-if="loadingForm"
      class="flex justify-center items-center py-10 text-slate-400"
    >
      <i class="pi pi-spin pi-spinner text-3xl"></i>
    </div>

    <template v-else>

      <!-- =====================================================
           TELEMETRI PRODUKSI
      ====================================================== -->

      <div
        class="bg-white rounded-xl border border-slate-200 shadow-sm p-4 w-full overflow-hidden"
      >
        <h3
          class="font-bold text-slate-800 text-sm mb-3 pb-2 border-b border-slate-100"
        >
          Telemetri Produksi (Mixing)
        </h3>

        <div
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3"
        >

          <!-- NAMA HASIL -->
          <label
            class="flex flex-col gap-1 w-full overflow-hidden"
          >
            <span
              class="text-[11px] font-bold text-slate-500 uppercase tracking-wide"
            >
              Nama Hasil
            </span>

            <input
              v-model="form.nama_hasil"
              type="text"
              placeholder="mis. SUPER WHITE SPESIAL"
              class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
            />
          </label>

          <!-- TANGKI TUJUAN -->
          <label
            class="flex flex-col gap-1 w-full overflow-hidden"
          >
            <span
              class="text-[11px] font-bold text-slate-500 uppercase tracking-wide"
            >
              Tangki Tujuan
            </span>

            <div
              class="flex items-center gap-2 w-full flex-nowrap"
            >

              <select
                v-model="form.tangki_tujuan"
                class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
                style="flex: 1 1 auto; min-width: 0"
              >
                <option
                  value=""
                  disabled
                >
                  Pilih tangki mixing
                </option>

                <option
                  v-for="t in daftarTangkiTujuan"
                  :key="t.id"
                  :value="t.id"
                >
                  {{ t.kode }}
                  —
                  {{
                    t.nama_hasil ||
                    t.isi_saat_ini ||
                    'Kosong'
                  }}
                </option>
              </select>

              <button
                type="button"
                class="bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 rounded-lg flex items-center justify-center font-bold shadow-sm transition-colors"
                style="flex: 0 0 42px; width: 42px; height: 42px"
                title="Tambah tangki mixing baru"
                @click="tambahTangkiBaruPrompt"
              >
                +
              </button>

            </div>

            <span
              class="text-[10px] text-slate-400"
            >
              Tangki tujuan Mixing wajib menggunakan kode
              <strong>TK-MIX-*</strong>.
            </span>

          </label>

          <!-- BATCH -->
          <label
            class="flex flex-col gap-1 w-full overflow-hidden"
          >
            <span
              class="text-[11px] font-bold text-slate-500 uppercase tracking-wide"
            >
              Batch ID
            </span>

            <div
              class="flex items-center gap-2 w-full flex-nowrap"
            >
              <input
                v-model="form.batch"
                type="text"
                placeholder="PRD-MIX-0001"
                class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
                style="flex: 1 1 auto; min-width: 0"
              />

              <button
                type="button"
                class="bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 text-xs font-bold rounded-lg flex items-center justify-center shadow-sm transition-colors disabled:opacity-50"
                style="flex: 0 0 65px; width: 65px; height: 42px"
                :disabled="!tangkiTujuanValid"
                @click="generateNomorBatch"
              >
                Auto
              </button>
            </div>
          </label>

          <!-- TEKOR -->
          <label
            class="flex flex-col gap-1 w-full overflow-hidden"
          >
            <span
              class="text-[11px] font-bold text-slate-500 uppercase tracking-wide"
            >
              Tekor / Susut (Kg)
            </span>

            <input
              v-model.number="form.tekor_kg"
              type="number"
              step="0.001"
              min="0"
              class="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
            />
          </label>

        </div>
      </div>

      <!-- =====================================================
           BOM
      ====================================================== -->

      <div
        class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden w-full"
      >

        <div class="p-4 pb-3">
          <h3 class="font-bold text-slate-800 text-sm">
            Bill of Materials (BOM)
          </h3>

          <p class="text-[11px] text-slate-400 mt-1">
            Mixing menggunakan bahan baku dari pool sebagai sumber input.
          </p>
        </div>

        <div
          class="overflow-x-auto border-y border-slate-100"
        >

          <table
            class="w-full text-sm text-left whitespace-nowrap"
          >

            <thead
              class="bg-slate-50 text-slate-500 text-[11px] uppercase font-semibold"
            >
              <tr>
                <th class="px-4 py-2">
                  Bahan Baku
                </th>

                <th class="px-4 py-2">
                  Qty Terpakai (Kg)
                </th>

                <th class="px-4 py-2 text-right">
                  Saldo Pool
                </th>

                <th class="px-4 py-2 text-right">
                  Harga (IDR/Kg)
                </th>

                <th class="px-4 py-2 text-right">
                  Subtotal
                </th>

                <th class="px-4 py-2 text-center">
                  Aksi
                </th>
              </tr>
            </thead>

            <tbody
              class="divide-y divide-slate-100 text-sm"
            >

              <tr
                v-for="row in bomRows"
                :key="row._id"
                class="hover:bg-slate-50/50 transition-colors"
              >

                <!-- BAHAN -->
                <td class="px-4 py-2">

                  <select
                    v-model="row.raw"
                    @change="
                      perbaruiTelemetriBom(row);
                      cekBahanDuplikat(row)
                    "
                    class="w-full min-w-[180px] px-2 py-1.5 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                  >

                    <option
                      value=""
                      disabled
                    >
                      Pilih bahan baku
                    </option>

                    <option
                      v-for="r in daftarRaw"
                      :key="r.raw"
                      :value="r.raw"
                      :disabled="
                        bomRows.some(
                          b =>
                            String(b.raw) ===
                              String(r.raw) &&
                            b._id !== row._id
                        )
                      "
                    >
                      {{ r.produk_kode }}
                      -
                      {{ r.produk_nama }}
                      ({{
                        formatKg(
                          r.qty_kg
                        )
                      }}
                      Kg)
                    </option>

                  </select>

                </td>

                <!-- QTY -->
                <td class="px-4 py-2">

                  <input
                    v-model.number="row.qty"
                    type="number"
                    step="0.001"
                    min="0"
                    class="w-full min-w-[100px] px-2 py-1.5 bg-white border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                  />

                </td>

                <!-- SALDO -->
                <td
                  class="px-4 py-2 text-right"
                >

                  <span
                    class="font-medium"
                    :class="
                      Number(row.qty) >
                      Number(row.saldo)
                        ? 'text-red-600'
                        : 'text-slate-700'
                    "
                  >
                    {{
                      formatKg(
                        row.saldo
                      )
                    }}
                  </span>

                </td>

                <!-- HARGA -->
                <td
                  class="px-4 py-2 text-right text-slate-500"
                >
                  {{
                    formatRupiah(
                      row.harga
                    )
                  }}
                </td>

                <!-- SUBTOTAL -->
                <td
                  class="px-4 py-2 text-right font-semibold text-slate-700"
                >
                  {{
                    formatRupiah(
                      row.subtotal
                    )
                  }}
                </td>

                <!-- AKSI -->
                <td
                  class="px-4 py-2 text-center"
                >

                  <button
                    type="button"
                    class="w-7 h-7 rounded-md flex items-center justify-center text-red-400 hover:bg-red-50 hover:text-red-600 mx-auto transition-colors"
                    @click="
                      hapusBomRow(
                        row._id
                      )
                    "
                    title="Hapus baris BOM"
                  >
                    <i
                      class="pi pi-trash text-xs"
                    ></i>
                  </button>

                </td>

              </tr>

            </tbody>

          </table>

        </div>

        <div class="p-3 bg-slate-50/50">

          <button
            type="button"
            class="text-xs font-bold text-blue-600 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-lg transition-colors flex items-center gap-2"
            @click="tambahBomRow"
          >

            <i
              class="pi pi-plus text-[10px]"
            ></i>

            Tambah Baris BOM

          </button>

        </div>

      </div>

      <!-- =====================================================
           PROYEKSI
      ====================================================== -->

      <div
        class="bg-blue-50 border border-blue-100 rounded-xl p-4 flex flex-col sm:flex-row justify-between items-center gap-2 text-sm text-center sm:text-left"
      >

        <div class="text-blue-800">
          Proyeksi Yield:

          <strong class="text-blue-900 ml-1">
            {{
              formatKg(
                proyeksiYield
              )
            }}
            Kg
          </strong>
        </div>

        <div class="text-blue-800">
          Estimasi Cost Nom:

          <strong class="text-blue-900 ml-1">
            {{
              formatRupiah(
                proyeksiHargaRata
              )
            }}
            / Kg
          </strong>
        </div>

      </div>

      <!-- =====================================================
           PRATINJAU
      ====================================================== -->

      <div
        v-if="pratinjau"
        class="mb-3"
      >
        <PratinjauValuasi
          :hasil="pratinjau"
        />
      </div>

      <!-- =====================================================
           ACTION
      ====================================================== -->

      <div
        class="flex flex-col sm:flex-row justify-end gap-2.5 pt-3 border-t border-slate-100"
      >

        <button
          type="button"
          class="px-4 py-2 text-sm font-bold text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 rounded-lg transition-all disabled:opacity-50"
          @click="$emit('batal')"
          :disabled="submitting"
        >
          Batal
        </button>

        <button
          type="button"
          class="px-4 py-2 text-sm font-bold text-blue-700 bg-blue-50 border border-blue-100 hover:bg-blue-100 rounded-lg transition-all disabled:opacity-50"
          @click="tanganiPratinjau"
          :disabled="
            submitting ||
            !tangkiTujuanValid
          "
        >
          Pratinjau
        </button>

        <button
          type="button"
          class="px-5 py-2 text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm transition-all disabled:opacity-50"
          @click="tanganiSimpanDanPosting"
          :disabled="
            submitting ||
            !tangkiTujuanValid
          "
        >
          {{
            submitting
              ? 'Memproses...'
              : 'Simpan & Posting'
          }}
        </button>

      </div>

    </template>
  </div>
</template>

<script setup>
import {
  computed,
  onMounted
} from 'vue'

import {
  useMixingForm
} from '../composables/useMixingForm'

import PratinjauValuasi
  from '../components/PratinjauValuasi.vue'

const props = defineProps({
  batchId: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits([
  'batal',
  'sukses'
])

const {
  loadingForm,
  submitting,
  errorMsg,

  daftarTangki,
  daftarRaw,

  form,
  bomRows,
  pratinjau,

  proyeksiYield,
  proyeksiHargaRata,

  bukaFormBaru,
  bukaFormEdit,

  tambahTangkiBaru,
  generateNomorBatch,

  tambahBomRow,
  hapusBomRow,

  perbaruiTelemetriBom,

  mintaPratinjau,
  simpanDanPosting
} = useMixingForm()

// ===========================================================
// TANGKI TUJUAN MIXING
// HANYA TK-MIX-*
// ===========================================================

const daftarTangkiTujuan = computed(() => {
  return daftarTangki.value.filter(
    (tangki) => {
      const kode =
        String(
          tangki.kode ??
          tangki.nama ??
          ''
        )
          .trim()
          .toUpperCase()

      return kode.startsWith(
        'TK-MIX-'
      )
    }
  )
})

// ===========================================================
// TANGKI TUJUAN YANG SEDANG DIPILIH
// ===========================================================

const tangkiTujuan = computed(() => {
  return daftarTangki.value.find(
    (tangki) =>
      String(tangki.id) ===
      String(
        form.tangki_tujuan
      )
  )
})

// ===========================================================
// VALIDASI KODE TANGKI TUJUAN
// ===========================================================

const tangkiTujuanValid = computed(() => {
  const tangki =
    tangkiTujuan.value

  if (!tangki) {
    return false
  }

  const kode =
    String(
      tangki.kode ??
      tangki.nama ??
      ''
    )
      .trim()
      .toUpperCase()

  return kode.startsWith(
    'TK-MIX-'
  )
})

const validasiTangkiError = computed(() => {
  if (
    !form.tangki_tujuan
  ) {
    return ''
  }

  if (
    !tangkiTujuan.value
  ) {
    return 'Tangki tujuan tidak ditemukan.'
  }

  if (
    !tangkiTujuanValid.value
  ) {
    return (
      'Tangki tujuan Mixing wajib menggunakan kode TK-MIX-*.'
    )
  }

  return ''
})

// ===========================================================
// INIT
// ===========================================================

onMounted(() => {
  if (props.batchId) {
    bukaFormEdit(
      props.batchId
    )
  } else {
    bukaFormBaru()
  }
})

// ===========================================================
// FORMAT KG
// ===========================================================

function formatKg(value) {
  return Number(
    value || 0
  ).toLocaleString(
    'id-ID',
    {
      minimumFractionDigits: 3,
      maximumFractionDigits: 3
    }
  )
}

// ===========================================================
// FORMAT RUPIAH
// ===========================================================

function formatRupiah(value) {
  return `Rp ${Number(
    value || 0
  ).toLocaleString(
    'id-ID',
    {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }
  )}`
}

// ===========================================================
// TAMBAH TANGKI MIXING
// ===========================================================

async function tambahTangkiBaruPrompt() {
  const input =
    window.prompt(
      'Masukkan kode tangki Mixing baru:\n\nContoh: TK-MIX-0004'
    )

  if (!input) {
    return
  }

  const kode =
    String(input)
      .trim()
      .toUpperCase()

  if (
    !kode.startsWith(
      'TK-MIX-'
    )
  ) {
    alert(
      'Tangki tujuan Mixing wajib menggunakan kode TK-MIX-*.\n\nContoh: TK-MIX-0004'
    )

    return
  }

  const dibuat =
    await tambahTangkiBaru(
      kode
    )

  if (!dibuat) {
    return
  }

  form.tangki_tujuan =
    dibuat.id
}

// ===========================================================
// PRATINJAU
// ===========================================================

async function tanganiPratinjau() {
  if (
    !tangkiTujuanValid.value
  ) {
    return
  }

  await mintaPratinjau()
}

// ===========================================================
// SIMPAN
// ===========================================================

async function tanganiSimpanDanPosting() {
  if (
    !tangkiTujuanValid.value
  ) {
    return
  }

  const ok =
    await simpanDanPosting(
      props.batchId
    )

  if (ok) {
    emit('sukses')
  }
}

// ===========================================================
// DUPLIKAT BOM
// ===========================================================

function cekBahanDuplikat(
  row
) {
  if (!row.raw) {
    return
  }

  const jumlahMuncul =
    bomRows.value.filter(
      (item) =>
        String(
          item.raw
        ) ===
        String(
          row.raw
        )
    ).length

  if (
    jumlahMuncul > 1
  ) {
    alert(
      'Bahan baku ini sudah dipilih di baris BOM lain! Silakan gabungkan QTY-nya.'
    )

    row.raw = ''

    perbaruiTelemetriBom(
      row
    )
  }
}
</script>
