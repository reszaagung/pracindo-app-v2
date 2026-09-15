<template>
  <div class="p-6 max-w-4xl mx-auto space-y-6">
    <header class="border-b border-slate-200 pb-4">
      <h1 class="text-2xl font-bold text-slate-800">Manajemen Cabang Franchise</h1>
      <p class="text-sm text-slate-500">Daftarkan cabang toko baru beserta akun login operasional ke dalam sistem.</p>
    </header>

    <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
      <form @submit.prevent="submitCabang" class="space-y-5">
        
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
                class="w-full border border-slate-300 rounded-lg px-4 py-2 focus:border-blue-500 outline-none"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">Password</label>
              <input 
                v-model="form.password" 
                type="password" 
                required
                placeholder="••••••••" 
                class="w-full border border-slate-300 rounded-lg px-4 py-2 focus:border-blue-500 outline-none"
              />
            </div>
          </div>
        </div>

        <hr class="border-slate-100 my-4" />

        <!-- Seksi Profil Fisik Cabang -->
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
                class="w-full border border-slate-300 rounded-lg px-4 py-2 focus:border-blue-500 outline-none"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">Nama Cabang</label>
              <input 
                v-model="form.nama" 
                type="text" 
                required
                placeholder="Contoh: Pracindo Cabang Surabaya" 
                class="w-full border border-slate-300 rounded-lg px-4 py-2 focus:border-blue-500 outline-none"
              />
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
import { retailApi } from '../api'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoading = ref(false)

const form = ref({
  username: '',
  password: '',
  kode: '',
  nama: '',
  alamat: '',
  aktif: true
})

const submitCabang = async () => {
  isLoading.value = true
  try {
    await retailApi.createCabang(form.value)
    alert('Cabang dan akun login berhasil didaftarkan!')
    
    form.value = { username: '', password: '', kode: '', nama: '', alamat: '', aktif: true }
    router.push('/retail')
  } catch (error) {
    console.error("Gagal menyimpan cabang:", error)
    alert("Terjadi kesalahan sistem. Pastikan Username atau Kode Cabang belum digunakan.")
  } finally {
    isLoading.value = false
  }
}
</script>