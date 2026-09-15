<template>
  <div v-if="hurufAktif" id="form-input-stiker-kecil-12" class="p-4 sm:p-6 bg-white border border-gray-200 shadow-xl rounded-2xl transition-all duration-300">
    <div class="flex items-start justify-between gap-3 mb-6">
      <h3 class="text-lg sm:text-2xl font-bold text-gray-800 flex flex-wrap items-center gap-2 sm:gap-3">
        Isi Data Grup <span class="text-blue-600">{{ hurufAktif }}</span>
        <span v-if="formData[hurufAktif].is_saved" class="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full border border-green-200 whitespace-nowrap">
          ✓ Tersimpan
        </span>
      </h3>
      <button
        v-if="!formData[hurufAktif].is_saved"
        type="button"
        @click="tutupForm"
        class="text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors"
        style="flex-shrink: 0; flex-grow: 0; width: 36px; height: 36px; min-width: 36px; padding: 0; border: none; border-radius: 9999px; display: flex; align-items: center; justify-content: center; background-color: transparent;"
      >
        <i class="pi pi-times text-lg"></i>
      </button>
      <button
        v-else
        type="button"
        @click="tutupForm"
        class="text-white font-bold hover:opacity-90 transition-opacity"
        style="flex-shrink: 0; flex-grow: 0; padding: 8px 20px; border: none; border-radius: 9999px; background-color: #16a34a; white-space: nowrap;"
      >
        Selesai
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="flex flex-col gap-2">
        <label class="font-semibold text-gray-700">Nama Item</label>
        <SugestionInputForm
          v-model="formData[hurufAktif].nama_item"
          @produk-terpilih="simpanNamaTampil($event.id, $event.nama)"
          :disabled="formData[hurufAktif].is_saved"
        />
      </div>

      <div class="flex flex-col gap-2">
        <label class="font-semibold text-gray-700">Tipe</label>
        <input type="text" v-model="formData[hurufAktif].tipe" :disabled="formData[hurufAktif].is_saved" class="p-3 border rounded-lg disabled:bg-gray-100 disabled:text-gray-400 w-full" />
      </div>

      <div class="flex flex-col gap-2">
        <label class="font-semibold text-gray-700">Tanggal Lot</label>
        <input type="date" v-model="formData[hurufAktif].lot" :disabled="formData[hurufAktif].is_saved" class="p-3 border rounded-lg disabled:bg-gray-100 disabled:text-gray-400 w-full" />
      </div>

      <div class="flex flex-col gap-2">
        <label class="font-semibold text-gray-700">Net Weight</label>
        <select v-model="formData[hurufAktif].net" :disabled="formData[hurufAktif].is_saved" class="p-3 border rounded-lg disabled:bg-gray-100 disabled:text-gray-400 bg-white w-full">
          <option :value="null" disabled>Pilih Net Weight...</option>
          <option v-for="net in netOptions" :key="net" :value="net">{{ net }}</option>
        </select>
      </div>
    </div>

    <div class="mt-6 sm:mt-8 flex justify-center sm:justify-end">
      <button v-if="!formData[hurufAktif].is_saved" @click="simpanGrup" class="w-full sm:w-auto px-6 py-3 font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-md transition-colors">
        Simpan Grup {{ hurufAktif }}
      </button>
      <button v-else @click="editGrup" class="w-full sm:w-auto px-6 py-3 font-bold text-blue-600 bg-blue-50 border border-blue-200 hover:bg-blue-100 rounded-xl shadow-sm transition-colors">
        Edit Data Grup {{ hurufAktif }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { useStikerKecil12 } from '../composables/useStikerKecil12'
import SugestionInputForm from '../components/SugestionInputForm.vue'

const { hurufAktif, formData, tutupForm, simpanNamaTampil } = useStikerKecil12()

const netOptions = [1, 5, 10, 15, 20, 25, 30]

const simpanGrup = () => { formData[hurufAktif.value].is_saved = true }
const editGrup = () => { formData[hurufAktif.value].is_saved = false }
</script>