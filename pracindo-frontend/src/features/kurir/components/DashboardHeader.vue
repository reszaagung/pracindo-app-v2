<template>
    <div class="min-h-screen bg-slate-50 font-sans pb-24 text-slate-800">
        
        <!-- HEADER BACKGROUND (ALa Gojek Hijau) -->
        <div class="bg-emerald-600 rounded-b-[2.5rem] pt-8 pb-16 px-5 shadow-sm">
            <!-- Profil & Notifikasi -->
            <div class="flex justify-between items-center text-white">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center text-emerald-600 font-bold text-xl shadow-inner">
                        {{ inisialNama }}
                    </div>
                    <div>
                        <p class="text-xs font-medium text-emerald-100">Selamat bekerja,</p>
                        <h1 class="text-lg font-bold">{{ namaKurir }}</h1>
                    </div>
                </div>
                <button class="p-2 bg-white/20 rounded-full hover:bg-white/30 transition">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                    </svg>
                </button>
            </div>
            
            <!-- Banner Internal (Pengganti GoCar Murah) -->
            <div class="mt-6 flex justify-between items-center bg-emerald-700/50 rounded-xl p-3 border border-emerald-500/30">
                <div>
                    <p class="text-white text-xs font-bold">INFO GUDANG</p>
                    <p class="text-emerald-100 text-xs mt-0.5">Jaga jarak aman & gunakan helm SNI.</p>
                </div>
                <span class="text-2xl">🛵</span>
            </div>
        </div>

        <!-- KOTAK STATUS (Pengganti Saldo GoPay) - Menggunakan negative margin agar tumpang tindih -->
        <div class="mx-5 -mt-8 bg-white rounded-2xl shadow-md p-4 flex items-center justify-between border-2 border-slate-100 z-10 relative">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>
                <div>
                    <p class="text-xs text-slate-500 font-semibold">Selesai Hari Ini</p>
                    <p class="text-lg font-bold text-slate-800">4 <span class="text-sm font-normal text-slate-500">Tugas</span></p>
                </div>
            </div>
            
            <div class="h-10 w-px bg-slate-200"></div> <!-- Divider -->
            
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center text-orange-600">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>
                <div>
                    <p class="text-xs text-slate-500 font-semibold">Tugas Aktif</p>
                    <p class="text-lg font-bold text-slate-800">1 <span class="text-sm font-normal text-slate-500">Jalan</span></p>
                </div>
            </div>
        </div>

        <!-- MENU UTAMA (Grid Ala Gojek) -->
        <div class="mt-8 mx-5 grid grid-cols-4 gap-y-6 gap-x-2">
            
            <!-- Menu 1: Kolam Tugas -->
            <button @click="$router.push('/kurir/available-tasks')" class="flex flex-col items-center gap-2 group">
                <div class="w-14 h-14 bg-emerald-100 group-hover:bg-emerald-200 transition-colors rounded-2xl flex items-center justify-center relative shadow-sm border border-emerald-200">
                    <!-- Badge Notification Ala Gojek -->
                    <div class="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full border-2 border-white z-10">3</div>
                    <span class="text-2xl">📦</span>
                </div>
                <span class="text-[11px] font-semibold text-slate-700 text-center leading-tight">Kolam<br>Tugas</span>
            </button>

            <!-- Menu 2: Tugas Saya -->
            <button @click="$router.push('/kurir/my-deliveries')" class="flex flex-col items-center gap-2 group">
                <div class="w-14 h-14 bg-blue-100 group-hover:bg-blue-200 transition-colors rounded-2xl flex items-center justify-center shadow-sm border border-blue-200">
                    <span class="text-2xl">🚚</span>
                </div>
                <span class="text-[11px] font-semibold text-slate-700 text-center leading-tight">Tugas<br>Saya</span>
            </button>

            <!-- Menu 3: Riwayat -->
            <button class="flex flex-col items-center gap-2 group">
                <div class="w-14 h-14 bg-purple-100 group-hover:bg-purple-200 transition-colors rounded-2xl flex items-center justify-center shadow-sm border border-purple-200">
                    <span class="text-2xl">📜</span>
                </div>
                <span class="text-[11px] font-semibold text-slate-700 text-center leading-tight">Riwayat<br>Tugas</span>
            </button>

            <!-- Menu 4: Cek Armada -->
            <button class="flex flex-col items-center gap-2 group">
                <div class="w-14 h-14 bg-orange-100 group-hover:bg-orange-200 transition-colors rounded-2xl flex items-center justify-center shadow-sm border border-orange-200">
                    <span class="text-2xl">🚐</span>
                </div>
                <span class="text-[11px] font-semibold text-slate-700 text-center leading-tight">Cek<br>Armada</span>
            </button>

            <!-- Menu 5: Retur -->
            <button class="flex flex-col items-center gap-2 group">
                <div class="w-14 h-14 bg-rose-100 group-hover:bg-rose-200 transition-colors rounded-2xl flex items-center justify-center shadow-sm border border-rose-200">
                    <span class="text-2xl">↩️</span>
                </div>
                <span class="text-[11px] font-semibold text-slate-700 text-center leading-tight">Barang<br>Retur</span>
            </button>

            <!-- Menu 6: Bantuan -->
            <button class="flex flex-col items-center gap-2 group">
                <div class="w-14 h-14 bg-slate-200 group-hover:bg-slate-300 transition-colors rounded-2xl flex items-center justify-center shadow-sm border border-slate-300">
                    <span class="text-2xl">🎧</span>
                </div>
                <span class="text-[11px] font-semibold text-slate-700 text-center leading-tight">Pusat<br>Bantuan</span>
            </button>
        </div>

        <!-- BANNER PROMO / INFO (Ala "Beli Paket GoRide") -->
        <div class="mx-5 mt-8 bg-gradient-to-r from-emerald-600 to-teal-500 rounded-2xl p-4 shadow-md text-white relative overflow-hidden">
            <!-- Ornamen Lingkaran BG -->
            <div class="absolute -right-8 -top-8 w-24 h-24 bg-white/20 rounded-full blur-xl"></div>
            
            <div class="relative z-10 w-3/4">
                <h3 class="font-bold text-sm mb-1">Target Insentif Minggu Ini!</h3>
                <p class="text-xs text-emerald-100">Selesaikan 20 pengiriman tanpa retur untuk dapatkan bonus tambahan.</p>
                <button class="mt-3 bg-white text-emerald-700 text-xs font-bold px-4 py-1.5 rounded-full shadow-sm">
                    Cek Detail
                </button>
            </div>
            
            <!-- Gambar Ilustrasi -->
            <div class="absolute -right-2 bottom-0 text-6xl">
                🎁
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Data dummy (nanti bisa diisi dari Vuex/Pinia atau API User lu)
const namaKurir = ref('Ahmad Driver')

// Komputasi inisial nama (Ahmad Driver -> AD)
const inisialNama = computed(() => {
    const names = namaKurir.value.split(' ')
    if (names.length >= 2) {
        return names[0][0] + names[1][0]
    }
    return names[0][0]
})
</script>