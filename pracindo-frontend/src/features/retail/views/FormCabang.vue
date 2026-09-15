<!-- src/views/FormCabang.vue -->
<template>
  <div class="p-6 max-w-4xl mx-auto space-y-6">
    <header class="border-b border-slate-200 pb-4">
      <h1 class="text-2xl font-bold text-slate-800">Manajemen Cabang Franchise</h1>
      <p class="text-sm text-slate-500">Daftarkan cabang toko baru beserta akun login operasional ke dalam sistem.</p>
    </header>

    <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
      <form @submit.prevent="handleSubmit" class="space-y-5">
        
        <div>
          <h2 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-3">Kredensial Akun Login Cabang</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">Username Login</label>
              <input 
                v-model="form.username" 
                type="text" 
                required
                placeholder="Contoh: cabang_surabaya" 
                class="w-full border rounded-lg px-4 py-2 outline-none focus:border-blue-500"
                :class="errors.username ? 'border-red-500' : 'border-slate-300'"
              />
              <p v-if="errors.username" class="text-red-500 text-xs mt-1">{{ errors.username[0] }}</p>
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">Password</label>
              <input 
                v-model="form.password" 
                type="password" 
                required
                placeholder="••••••••" 
                class="w-full border rounded-lg px-4 py-2 outline-none focus:border-blue-500"
                :class="errors.password ? 'border-red-500' : 'border-slate-300'"
              />
              <p v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password[0] }}</p>
            </div>
          </div>
        </div>

        <hr class="border-slate-100 my-4" />

        <div>
          <h2 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-3">Informasi Toko Cabang</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">Kode Cabang</label>
              <input 
                v-model="form.kode" 
                type="text" 
                required
                placeholder="Contoh: CBG-SBY-01" 
                class="w-full border rounded-lg px-4 py-2 outline-none focus:border-blue-500"
                :class="errors.kode ? 'border-red-500' : 'border-slate-300'"
              />
              <p v-if="errors.kode" class="text-red-500 text-xs mt-1">{{ errors.kode[0] }}</p>
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">Nama Cabang</label>
              <input 
                v-model="form.nama" 
                type="text" 
                required
                placeholder="Contoh: Pracindo Cabang Surabaya" 
                class="w-full border rounded-lg px-4 py-2 outline-none focus:border-blue-500"
                :class="errors.nama ? 'border-red-500' : 'border-slate-300'"
              />
              <p v-if="errors.nama" class="text-red-500 text-xs mt-1">{{ errors.nama[0] }}</p>
            </div>
          </div>
        </div>

        <div>
          <label class="block text-sm font-semibold text-slate-700 mb-1">Alamat Lengkap</label>
          <textarea 
            v-model="form.alamat" 
            rows="3" 
            placeholder="Detail alamat operasional cabang..."
            class="w-full border border-slate-300 rounded-lg px-4 py-2 focus:border-blue-500 outline-none"
          ></textarea>
        </div>

        <div class="flex items-center gap-2 pt-2">
          <input type="checkbox" v-model="form.aktif" id="statusAktif" class="w-4 h-4 text-blue-600 rounded" />
          <label for="statusAktif" class="text-sm font-semibold text-slate-700">Cabang Aktif Beroperasi</label>
        </div>

        <div class="pt-4 border-t border-slate-100 flex justify-end">
          <button 
            type="submit" 
            :disabled="isLoading" 
            class="bg-blue-600 text-white font-bold px-6 py-2.5 rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            {{ isLoading ? 'Menyimpan Data...' : 'Simpan Cabang & Akun' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCabang } from '../composables/useCabang' 

const { isLoading, errors, simpanCabang } = useCabang()

const form = ref({
  username: '',
  password: '',
  nama: '',
  alamat: '',
  aktif: true
})

const handleSubmit = async () => {
  await simpanCabang(form.value)
}
</script>