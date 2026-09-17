import { ref } from 'vue'
import api from '@/services/api'
import JSEncrypt from 'jsencrypt' // 👈 Satpamnya kita panggil ke sini

export function useRetailAuth() {
    const sedangProses = ref(false)

    const login = async (username, password) => {
        sedangProses.value = true
        
        try {
            // --- 🔐 STRICT MODE: TIDAK ADA KOMPROMI ---
            const rawPublicKey = import.meta.env.VITE_RSA_PUBLIC_KEY
            
            // 1. Cek apakah kunci ketemu di .env
            if (!rawPublicKey) {
                console.error("FATAL: VITE_RSA_PUBLIC_KEY tidak terbaca oleh Vite!")
                sedangProses.value = false
                return { success: false, message: 'Sistem Keamanan Gagal: Kunci Enkripsi Tidak Ditemukan.' }
            }

            const PUBLIC_KEY = rawPublicKey.replace(/\\n/g, '\n')
            const encryptor = new JSEncrypt()
            encryptor.setPublicKey(PUBLIC_KEY)
            
            const encryptedPassword = encryptor.encrypt(password)
            
            // 2. Cek apakah proses acak berhasil
            if (!encryptedPassword) {
                console.error("FATAL: Proses enkripsi JSEncrypt gagal!")
                sedangProses.value = false
                return { success: false, message: 'Sistem Keamanan Gagal: Gagal mengacak password.' }
            }
            // ------------------------------------------

            // 3. HANYA KIRIM JIKA PASSWORD SUDAH BERUBAH JADI KODE ACAK
            const response = await api.post('retail/login/', {
                username: username,
                password: encryptedPassword // 👈 Gembok dikirim di sini!
            })

            const token = response.data.access || response.data.token 
            const user = response.data.user || response.data.profil
            
            localStorage.setItem('retail_token', token)
            if (user) {
                localStorage.setItem('retail_user', JSON.stringify(user))
            }
            
            sedangProses.value = false
            return { success: true }

        } catch (error) {
            sedangProses.value = false
            
            let pesanError = 'Terjadi kesalahan pada server.'
            if (error.response && error.response.data) {
                pesanError = error.response.data.detail || 
                             error.response.data.message || 
                             error.response.data.non_field_errors?.[0] || 
                             'Login gagal. Periksa kembali username dan kata sandi Anda.'
            }
            
            return { success: false, message: pesanError }
        }
    }

    const logout = () => {
        localStorage.removeItem('retail_token')
        localStorage.removeItem('retail_user')
        
        window.location.href = '/login' 
    }

    return { 
        login, 
        logout, 
        sedangProses 
    }
}