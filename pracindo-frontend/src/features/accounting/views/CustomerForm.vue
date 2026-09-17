<template>
    <div class="fixed inset-0 z-[9999] flex items-end sm:items-center justify-center bg-slate-900/60 backdrop-blur-sm sm:p-6 animate-fade-in">
        <div class="bg-white w-full max-w-3xl rounded-t-[24px] sm:rounded-[32px] rounded-b-none sm:rounded-b-[32px] shadow-2xl relative flex flex-col max-h-[90vh] overflow-hidden animate-fade-in-up">
            <button @click="tutupForm" class="absolute top-4 right-4 sm:top-6 sm:right-6 w-8 h-8 sm:w-10 sm:h-10 bg-slate-100 hover:bg-red-100 text-slate-500 hover:text-red-600 rounded-full flex items-center justify-center transition-colors z-10">
                <i class="pi pi-times text-sm sm:text-base"></i>
            </button>
            <div class="p-5 sm:p-8 overflow-y-auto custom-scrollbar">
                <h2 class="text-xl sm:text-3xl font-extrabold text-slate-800 mb-1 sm:mb-2 pr-10">Tambah Pelanggan Baru</h2>
                <p class="text-xs sm:text-sm text-slate-500 mb-6 sm:mb-8">Mendaftarkan data customer atau pelanggan baru ke dalam sistem.</p>
                <form @submit.prevent="simpanPelanggan" class="flex flex-col gap-4 sm:gap-6">
                    <div>
                        <label class="block text-sm font-bold text-slate-700 mb-2">Nama Pelanggan / Perusahaan</label>
                        <div class="relative">
                            <i class="pi pi-building absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                            <input v-model="formPelanggan.nama" type="text" required placeholder="Contoh: PT. Maju Mundur" class="w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all font-medium text-slate-700">
                        </div>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-2">NPWP (Opsional)</label>
                            <div class="relative">
                                <i class="pi pi-id-card absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                                <input v-model="formPelanggan.npwp" type="text" placeholder="Nomor NPWP..." class="w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all font-medium text-slate-700">
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-2">Nomor HP / Telepon</label>
                            <div class="relative">
                                <i class="pi pi-phone absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                                <input v-model="formPelanggan.kontak_hp" type="text" placeholder="Contoh: 0812345..." class="w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all font-medium text-slate-700">
                            </div>
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-700 mb-2">Nama Kontak (PIC)</label>
                        <div class="relative">
                            <i class="pi pi-user absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                            <input v-model="formPelanggan.kontak_nama" type="text" placeholder="Nama orang yang bisa dihubungi..." class="w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all font-medium text-slate-700">
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-700 mb-2">Alamat Lengkap</label>
                        <div class="relative">
                            <i class="pi pi-map-marker absolute left-4 top-4 text-slate-400"></i>
                            <textarea v-model="formPelanggan.alamat" required rows="3" placeholder="Alamat pengiriman / tagihan..." class="w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all font-medium text-slate-700 resize-none"></textarea>
                        </div>
                    </div>
                    <div class="flex justify-end items-center gap-4 mt-2 sm:mt-4 pt-4 sm:pt-6 border-t border-slate-100">
                        <button type="button" @click="tutupForm" :disabled="isSubmitting" class="px-6 py-3 font-bold text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-xl transition-all">
                            Batal
                        </button>
                        <button type="submit" :disabled="isSubmitting" class="px-8 py-3 rounded-xl font-bold bg-blue-600 text-white hover:bg-blue-700 transition-all shadow-md flex items-center gap-2">
                            <i class="pi" :class="isSubmitting ? 'pi-spin pi-spinner' : 'pi-save'"></i>
                            {{ isSubmitting ? 'Menyimpan...' : 'Simpan Pelanggan' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import api from '@/utils/api'

const emit = defineEmits(['close', 'saved'])
const isSubmitting = ref(false)

const formPelanggan = reactive({
    nama: '',
    npwp: '',
    kontak_nama: '',
    kontak_hp: '',
    alamat: ''
})

const tutupForm = () => emit('close')

const simpanPelanggan = async () => {
    isSubmitting.value = true
    try {
        await api.post('master/pelanggan/', {
            nama: formPelanggan.nama,
            npwp: formPelanggan.npwp,
            kontak_nama: formPelanggan.kontak_nama,
            kontak_hp: formPelanggan.kontak_hp,
            alamat: formPelanggan.alamat,
            aktif: true
        })
        emit('saved')
    } catch (error) {
        alert("Gagal menyimpan data pelanggan: " + (error.response?.data?.detail || error.message))
    } finally {
        isSubmitting.value = false
    }
}
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
.animate-fade-in-up { animation: fadeInUp 0.4s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 10px; }
</style>