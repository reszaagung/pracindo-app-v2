<template>
    <div class="flex flex-col w-full animate-fade-in bg-slate-50 min-h-screen p-6">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 border-b-2 border-slate-200 pb-5 gap-4">
            <div>
                <p class="text-xs text-slate-400 mb-1">
                    <span class="hover:text-slate-700 transition-colors">Logistics</span> /
                    <span class="text-slate-600 font-semibold">Delivery Order</span>
                </p>
                <h1 class="text-2xl md:text-3xl font-bold text-slate-800 tracking-tight">Delivery Request Order</h1>
                <p class="text-sm text-slate-500 mt-1">
                    {{ activeTab === 'DISTRIBUSI' ? 'Permintaan pengiriman stok internal ke cabang retail.' : 'Permintaan pengiriman B2C langsung ke kustomer (SO).' }}
                </p>
            </div>
            
            <div class="flex border-2 border-slate-800 bg-white shadow-sm rounded-lg overflow-hidden w-full md:w-auto">
                <button type="button" @click="activeTab = 'DISTRIBUSI'" 
                    :class="activeTab === 'DISTRIBUSI' ? 'bg-slate-800 text-white' : 'text-slate-800 hover:bg-slate-100'"
                    class="flex-1 md:flex-none px-8 py-3 text-sm font-bold uppercase transition-colors border-r-2 border-slate-800 outline-none">
                    Distribusi (Retail)
                </button>
                <button type="button" @click="activeTab = 'DELIVERY'"
                    :class="activeTab === 'DELIVERY' ? 'bg-slate-800 text-white' : 'text-slate-800 hover:bg-slate-100'"
                    class="flex-1 md:flex-none px-8 py-3 text-sm font-bold uppercase transition-colors outline-none">
                    Delivery (B2C)
                </button>
            </div>
        </div>

        <div class="w-full bg-white border border-slate-200 rounded-2xl shadow-sm p-6">
            <DistribusiCreate v-if="activeTab === 'DISTRIBUSI'" />
            
            <DeliveryCreate v-if="activeTab === 'DELIVERY'" />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import DistribusiCreate from './DistribusiCreate.vue'
import DeliveryCreate from './DeliveryCreate.vue'

const activeTab = ref('DISTRIBUSI')
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>