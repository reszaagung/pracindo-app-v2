<template>
    <div class="min-h-screen bg-slate-100 flex items-center justify-center p-4 font-sans">
        <div class="max-w-md w-full bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-200">
            <div class="p-8 sm:p-10">
                <div class="text-center mb-8">
                    <div class="w-16 h-16 bg-emerald-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                        <i class="pi pi-store text-3xl text-emerald-600"></i>
                    </div>
                    <h1 class="text-2xl font-black text-slate-800 tracking-tight">Registrasi Cabang</h1>
                    <p class="text-slate-500 mt-2 text-sm font-medium">Daftarkan cabang ritel baru Anda</p>
                </div>

                <form @submit.prevent="handleRegister" class="space-y-4">
                    <div>
                        <label class="block text-sm font-bold text-slate-700 mb-1.5">Nama Cabang</label>
                        <div class="relative">
                            <i class="pi pi-shop absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400"></i>
                            <input v-model="form.nama_cabang" type="text"
                                class="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-50 outline-none transition-all text-sm font-medium"
                                placeholder="Contoh: Cabang Sudirman" required>
                        </div>
                    </div>

                    <div>
                        <label class="block text-sm font-bold text-slate-700 mb-1.5">Alamat Lengkap</label>
                        <div class="relative">
                            <i
                                class="pi pi-map-marker absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400"></i>
                            <input v-model="form.alamat" type="text"
                                class="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-50 outline-none transition-all text-sm font-medium"
                                placeholder="Alamat cabang..." required>
                        </div>
                    </div>

                    <div class="pt-4 border-t border-slate-100 mt-2">
                        <p class="text-xs font-bold text-slate-500 mb-3 uppercase tracking-wider">Buat Akun Admin Cabang
                        </p>

                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1.5">Username</label>
                                <div class="relative">
                                    <i
                                        class="pi pi-user absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400"></i>
                                    <input v-model="form.username" type="text"
                                        class="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-50 outline-none transition-all text-sm font-medium"
                                        placeholder="Buat username..." required>
                                </div>
                            </div>

                            <div>
                                <label class="block text-sm font-bold text-slate-700 mb-1.5">Password</label>
                                <div class="relative">
                                    <i
                                        class="pi pi-lock absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400"></i>
                                    <input v-model="form.password" type="password"
                                        class="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-200 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-50 outline-none transition-all text-sm font-medium"
                                        placeholder="Buat password..." required>
                                </div>
                            </div>
                        </div>
                    </div>

                    <button type="submit"
                        class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3.5 rounded-xl transition-all shadow-lg shadow-emerald-200 mt-6 flex items-center justify-center gap-2 active:scale-[0.98]">
                        <i class="pi pi-check-circle"></i> Daftarkan Cabang
                    </button>

                    <div class="text-center mt-4">
                        <router-link to="/login"
                            class="text-sm font-bold text-slate-500 hover:text-emerald-600 transition-colors">
                            Sudah punya akun? Kembali ke Login
                        </router-link>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
    nama_cabang: '',
    alamat: '',
    username: '',
    password: ''
})

const handleRegister = () => {
    alert(`Simulasi: Cabang ${form.nama_cabang} berhasil didaftarkan!`)
    router.push('/login')
}
</script>