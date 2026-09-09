<template>
    <div class="flex flex-col w-full animate-fade-in bg-slate-50 min-h-screen p-6">
        
        <!-- HEADER & TABS -->
        <div class="flex justify-between items-center mb-6 border-b-2 border-slate-200 pb-4">
            <div>
                <h1 class="text-2xl font-bold text-slate-800 tracking-tight">Form Pengiriman</h1>
                <p class="text-sm text-slate-500 mt-1">
                    {{ activeTab === 'DISTRIBUSI' ? 'Tarik barang dari stok pabrik ke cabang retail.' : 'Pilih antrean reguler untuk dinaikkan ke armada.' }}
                </p>
            </div>
            
            <!-- TOMBOL TAB KOTAK TEGAS (Override Global CSS) -->
            <div class="flex border-2 border-slate-800 bg-white shadow-sm">
                <button type="button" @click="activeTab = 'DISTRIBUSI'" 
                    :class="activeTab === 'DISTRIBUSI' ? '!bg-slate-800 !text-white' : '!text-slate-800 hover:!bg-slate-100'"
                    class="px-10 py-3 text-sm font-bold uppercase transition-colors border-r-2 border-slate-800 !rounded-none !outline-none">
                    DISTRIBUSI
                </button>
                <button type="button" @click="activeTab = 'DELIVERY'"
                    :class="activeTab === 'DELIVERY' ? '!bg-slate-800 !text-white' : '!text-slate-800 hover:!bg-slate-100'"
                    class="px-10 py-3 text-sm font-bold uppercase transition-colors !rounded-none !outline-none">
                    DELIVERY
                </button>
            </div>
        </div>

        <div class="w-full">
            <DistribusiCreate v-if="activeTab === 'DISTRIBUSI'" />
            <DeliveryCreate v-if="activeTab === 'DELIVERY'" />
        </div>

    </div>
</template>

<script setup>
import { ref } from 'vue'
import DistribusiCreate from './DistribusiCreate.vue'
import DeliveryCreate from './DeliveryCreate.vue'

// Tentukan tab awal yang terbuka
const activeTab = ref('DISTRIBUSI')
</script>