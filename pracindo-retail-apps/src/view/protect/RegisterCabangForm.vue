<template>
    <div class="register-wrapper">
        <div class="register-box">
            <div class="header-text">
                <h1 class="title">Registrasi Cabang</h1>
                <p class="subtitle">Daftarkan cabang ritel baru Anda</p>
            </div>

            <form @submit.prevent="handleRegister" class="register-form">
                
                <div class="input-group">
                    <label>Nama Cabang</label>
                    <div class="input-wrapper">
                        <i class="pi pi-shop input-icon"></i>
                        <input v-model="form.nama_cabang" type="text" placeholder="Contoh: Cabang Arob" required :disabled="sedangProses" class="form-input" />
                    </div>
                </div>

                <div class="input-group">
                    <label>Alamat Lengkap</label>
                    <div class="input-wrapper">
                        <i class="pi pi-map-marker input-icon"></i>
                        <textarea v-model="form.alamat_lengkap" placeholder="Masukkan alamat lengkap cabang" required :disabled="sedangProses" class="form-input textarea"></textarea>
                    </div>
                </div>

                <div class="input-group">
                    <label>Username (Untuk Login)</label>
                    <div class="input-wrapper">
                        <i class="pi pi-user input-icon"></i>
                        <input v-model="form.username" type="text" placeholder="Buat username cabang" required :disabled="sedangProses" class="form-input" />
                    </div>
                </div>

                <div class="input-group">
                    <label>Kata Sandi</label>
                    <div class="input-wrapper">
                        <i class="pi pi-lock input-icon"></i>
                        <input v-model="form.password" type="password" placeholder="Minimal 6 karakter" required :disabled="sedangProses" class="form-input" />
                    </div>
                </div>

                <!-- Notifikasi Error atau Sukses -->
                <div v-if="pesanError" class="alert-box error">
                    <i class="pi pi-exclamation-circle"></i> {{ pesanError }}
                </div>
                
                <div v-if="pesanSukses" class="alert-box success">
                    <i class="pi pi-check-circle"></i> {{ pesanSukses }}
                </div>

                <button type="submit" class="btn-submit" :disabled="sedangProses">
                    <i v-if="sedangProses" class="pi pi-spin pi-spinner"></i>
                    <i v-else class="pi pi-save"></i>
                    {{ sedangProses ? 'Mendaftarkan...' : 'Daftarkan Cabang' }}
                </button>

                <div class="back-link">
                    <router-link to="/login" class="link">
                        <i class="pi pi-arrow-left"></i> Kembali ke Halaman Login
                    </router-link>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

import { apiCabang } from '@/services/apiRetail'

const router = useRouter()
const sedangProses = ref(false)
const pesanError = ref('')
const pesanSukses = ref('')

const form = reactive({
    nama_cabang: '',
    alamat_lengkap: '',
    username: '',
    password: ''
})

const handleRegister = async () => {
    pesanError.value = ''
    pesanSukses.value = ''
    sedangProses.value = true

    try {
        const response = await apiCabang.buat({
            nama: form.nama_cabang,      
            alamat: form.alamat_lengkap, 
            username: form.username,
            password: form.password
        })

        pesanSukses.value = `Mantap! Cabang ${form.nama_cabang} berhasil didaftarkan dengan kode ${response.kode}.`
        
        form.nama_cabang = ''
        form.alamat_lengkap = ''
        form.username = ''
        form.password = ''



    } catch (error) {
        if (error.response && error.response.data) {
            if (error.response.data.username) {
                pesanError.value = error.response.data.username[0]
            } else {
                pesanError.value = error.response.data.detail || 'Gagal mendaftar. Periksa kembali data Anda.'
            }
        } else {
            pesanError.value = 'Terjadi kesalahan koneksi ke server.'
        }
    } finally {
        sedangProses.value = false
    }
}
</script>

<style scoped>
* { box-sizing: border-box; }
.register-wrapper { 
    min-height: 100vh; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    background: #f8fafc; 
    padding: 2rem; 
    font-family: 'Inter', system-ui, sans-serif; 
}
.register-box { 
    width: 100%; 
    max-width: 480px; 
    background: #ffffff; 
    padding: 2.5rem; 
    border-radius: 1.25rem; 
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.1); 
    border: 1px solid #e2e8f0; 
}
.header-text { margin-bottom: 2rem; text-align: center; }
.title { font-size: 1.75rem; font-weight: 800; color: #1e293b; margin: 0 0 0.5rem 0; letter-spacing: -0.025em; }
.subtitle { font-size: 0.95rem; color: #64748b; margin: 0; }

.register-form { display: flex; flex-direction: column; gap: 1.25rem; }
.input-group { display: flex; flex-direction: column; gap: 0.5rem; }
.input-group label { font-size: 0.875rem; font-weight: 600; color: #334155; }
.input-wrapper { position: relative; }
.input-icon { 
    position: absolute; 
    left: 1rem; 
    top: 1rem; 
    color: #94a3b8; 
    pointer-events: none; 
}
.form-input { 
    width: 100%; 
    padding: 0.875rem 1rem 0.875rem 2.75rem; 
    border: 1px solid #cbd5e1; 
    border-radius: 0.75rem; 
    font-size: 0.95rem; 
    color: #1e293b; 
    background: #f8fafc; 
    transition: all 0.2s; 
    outline: none; 
}
.form-input:focus { 
    border-color: #3b82f6; 
    background: #ffffff; 
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15); 
}
.textarea { min-height: 80px; resize: vertical; }

.alert-box { 
    padding: 0.875rem 1rem; 
    border-radius: 0.75rem; 
    font-size: 0.875rem; 
    display: flex; 
    align-items: center; 
    gap: 0.5rem; 
    line-height: 1.4; 
}
.alert-box.error { background: #fef2f2; border: 1px solid #fca5a5; color: #b91c1c; }
.alert-box.success { background: #f0fdf4; border: 1px solid #86efac; color: #15803d; font-weight: 600; }

.btn-submit { 
    width: 100%; 
    padding: 1rem; 
    border: none; 
    border-radius: 0.75rem; 
    background: #2563eb; 
    color: #ffffff; 
    font-size: 1rem; 
    font-weight: 700; 
    cursor: pointer; 
    transition: background 0.2s; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    gap: 0.5rem; 
}
.btn-submit:hover:not(:disabled) { background: #1d4ed8; }
.btn-submit:disabled { opacity: 0.7; cursor: not-allowed; }

.back-link { text-align: center; margin-top: 1rem; }
.link { 
    color: #64748b; 
    text-decoration: none; 
    font-size: 0.875rem; 
    font-weight: 600; 
    display: inline-flex; 
    align-items: center; 
    gap: 0.25rem; 
    transition: color 0.2s; 
}
.link:hover { color: #1e293b; }
</style>