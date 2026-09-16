import { ref } from 'vue'
import api from '@/services/api' // Import Axios interceptor buatan lu

export function useRetailAuth() {
    const sedangProses = ref(false)

    const login = async (username, password) => {
        sedangProses.value = true
        
        try {
            // Tembak endpoint yang ada 'retail/'-nya agar sesuai dengan PUBLIK
            const response = await api.post('retail/login/', {
                username: username,
                password: password
            })

            // Ambil token (JWT) dan data user
            // Sesuaikan .access / .token dengan response asli dari Django lu
            const token = response.data.access || response.data.token 
            const user = response.data.user || response.data.profil
            
            // Simpan pakai nama key khusus RETAIL (sesuai rules di api.js lu)
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

    return { 
        login, 
        sedangProses 
    }
}