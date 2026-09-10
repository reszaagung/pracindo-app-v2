<template>
    <Toast />
    <router-view />

    <div v-if="showGlobalLoginModal" class="fixed inset-0 z-[9999] flex items-center justify-center bg-slate-900/80 backdrop-blur-sm px-4">
        <div class="bg-white rounded-2xl p-6 w-full max-w-sm shadow-2xl relative">
            <div class="w-12 h-12 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center mb-4 mx-auto">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
            </div>
            <h2 class="text-center text-lg font-bold text-slate-800 mb-1">Sesi Kedaluwarsa!</h2>
            <p class="text-center text-xs text-slate-500 mb-5">
              Tenang, data form Anda masih aman. Login kembali untuk melanjutkan pekerjaan.
            </p>
            
            <form @submit.prevent="handleRelogin" class="flex flex-col gap-3">
                <p v-if="loginError" class="text-xs text-rose-500 text-center font-bold">{{ loginError }}</p>
                
                <input v-model="username" type="text" placeholder="Username" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2.5 text-sm focus:outline-emerald-500" required>
                <input v-model="password" type="password" placeholder="Password" class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2.5 text-sm focus:outline-emerald-500" required>
                
                <button type="submit" :disabled="isLoading" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2.5 rounded-lg text-sm mt-2 transition-colors disabled:opacity-50">
                    {{ isLoading ? 'Memverifikasi...' : 'Lanjutkan Kerja' }}
                </button>
            </form>
        </div>
    </div>
</template>

<script setup>
import Toast from 'primevue/toast'
import { ref } from 'vue'

import { showGlobalLoginModal } from '@/utils/authModalState' 
import api from '@/utils/api'

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const loginError = ref('')

const handleRelogin = async () => {
    isLoading.value = true
    loginError.value = ''
    try {
        const { data } = await api.post('auth/login/', {
            username: username.value,
            password: password.value
        })
        
        localStorage.setItem('token', data.token || data.key) 
        
        showGlobalLoginModal.value = false
        username.value = ''
        password.value = ''
        
    } catch (error) {
        loginError.value = 'Gagal verifikasi! Pastikan password Anda benar.'
    } finally {
        isLoading.value = false
    }
}
</script>