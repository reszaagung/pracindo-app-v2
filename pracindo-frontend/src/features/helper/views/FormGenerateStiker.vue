<template>
  <div v-if="hurufAktif" id="form-input-stiker" class="p-6 bg-white border border-gray-200 shadow-xl rounded-2xl transition-all duration-300">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-2xl font-bold text-gray-800 flex items-center gap-3">
        Isi Data Grup <span class="text-blue-600">{{ hurufAktif }}</span>
        <span v-if="formData[hurufAktif].is_saved" class="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full border border-green-200">
          ✓ Tersimpan
        </span>
      </h3>
      <button @click="tutupForm" class="p-2 text-gray-400 hover:text-red-500 rounded-full hover:bg-red-50 transition-colors">
        <i class="pi pi-times text-xl"></i>
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="flex flex-col gap-2">
        <label class="font-semibold text-gray-700">Nama Item</label>
        <input type="text" v-model="formData[hurufAktif].nama_item" :disabled="formData[hurufAktif].is_saved" class="p-3 border rounded-lg disabled:bg-gray-100 disabled:text-gray-400" />
      </div>
      
      <div class="flex flex-col gap-2">
        <label class="font-semibold text-gray-700">Tipe</label>
        <input type="text" v-model="formData[hurufAktif].tipe" :disabled="formData[hurufAktif].is_saved" class="p-3 border rounded-lg disabled:bg-gray-100 disabled:text-gray-400" />
      </div>

      <div class="flex flex-col gap-2">
        <label class="font-semibold text-gray-700">Tanggal Lot</label>
        <input type="date" v-model="formData[hurufAktif].lot" :disabled="formData[hurufAktif].is_saved" class="p-3 border rounded-lg disabled:bg-gray-100 disabled:text-gray-400" />
      </div>

      <div class="flex flex-col gap-2">
        <label class="font-semibold text-gray-700">Net Weight</label>
        <select v-model="formData[hurufAktif].net" :disabled="formData[hurufAktif].is_saved" class="p-3 border rounded-lg disabled:bg-gray-100 disabled:text-gray-400 bg-white">
          <option :value="null" disabled>Pilih Net Weight...</option>
          <option v-for="net in netOptions" :key="net" :value="net">{{ net }}</option>
        </select>
      </div>
    </div>

    <div class="mt-8 flex justify-end">
      <button v-if="!formData[hurufAktif].is_saved" @click="simpanGrup" class="px-6 py-3 font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-md transition-colors">
        Simpan Grup {{ hurufAktif }}
      </button>
      <button v-else @click="editGrup" class="px-6 py-3 font-bold text-blue-600 bg-blue-50 border border-blue-200 hover:bg-blue-100 rounded-xl shadow-sm transition-colors">
        Edit Data Grup {{ hurufAktif }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { useStiker } from '../composables/useStiker'

const { hurufAktif, formData, tutupForm } = useStiker()

const netOptions = [1, 5, 10, 15, 20, 25, 30]

const simpanGrup = () => {
    formData[hurufAktif.value].is_saved = true
}

const editGrup = () => {
    formData[hurufAktif.value].is_saved = false
}
</script>