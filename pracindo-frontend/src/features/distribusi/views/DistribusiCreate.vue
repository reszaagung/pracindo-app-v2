<template>
    <div class="w-full">
        <form @submit.prevent="simpanDistribusi" class="flex flex-col gap-6">

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="flex flex-col gap-4">
                    <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col">
                        <label class="text-[10px] font-bold text-slate-500 uppercase mb-2">Perusahaan (PT/CV) <span class="text-red-500">*</span></label>
                        <select v-model="form.entitas_id" @change="pilihEntitas" required
                            class="w-full text-sm font-bold text-slate-800 bg-white border border-slate-300 rounded-sm px-3 py-2 focus:ring-1 focus:ring-blue-500 focus:outline-none cursor-pointer transition-all">
                            <option value="" disabled>-- Pilih Perusahaan --</option>
                            <option v-for="entitas in daftarEntitas" :key="entitas.id" :value="entitas.id">
                                {{ entitas.nama }} ({{ entitas.kode }})
                            </option>
                        </select>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col">
                        <label class="text-[10px] font-bold text-slate-500 uppercase mb-2">Tanggal Distribusi <span class="text-red-500">*</span></label>
                        <input type="date" v-model="form.tanggal" required
                            class="w-full text-sm font-bold text-slate-800 bg-white border border-slate-300 rounded-sm px-3 py-2 focus:ring-1 focus:ring-blue-500 focus:outline-none transition-all" />
                    </div>
                    <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col">
                        <label class="text-[10px] font-bold text-slate-500 uppercase mb-2">Tujuan (Cabang Retail) <span class="text-red-500">*</span></label>
                        <select v-model="form.tujuan_toko_id" required
                            class="w-full text-sm font-bold text-slate-800 bg-white border border-slate-300 rounded-sm px-3 py-2 focus:ring-1 focus:ring-blue-500 focus:outline-none cursor-pointer transition-all">
                            <option value="" disabled>-- Pilih Cabang Retail --</option>
                            <option v-for="toko in daftarToko" :key="toko.id" :value="toko.id">
                                {{ toko.nama }} ({{ toko.kode }})
                            </option>
                        </select>
                    </div>
                </div>
                <div class="flex flex-col gap-4">
                    <div class="bg-blue-50 border border-blue-200 p-4 rounded-xl shadow-sm flex flex-col justify-center min-h-[90px]">
                        <label class="text-[10px] font-bold text-blue-500 uppercase mb-1">No Surat Jalan (DO)</label>
                        <input type="text" :value="previewNomor" readonly
                            class="w-full text-sm font-bold text-blue-700 bg-transparent focus:outline-none cursor-not-allowed" />
                    </div>
                    <div class="bg-slate-50 border border-slate-200 p-4 rounded-xl shadow-sm flex flex-col">
                        <label class="text-[10px] font-bold text-slate-500 uppercase mb-2">Armada / Kendaraan</label>
                        <select v-model="form.kendaraan_id"
                            class="w-full text-sm font-bold text-slate-800 bg-white border border-slate-300 rounded-sm px-3 py-2 focus:ring-1 focus:ring-blue-500 focus:outline-none cursor-pointer transition-all">
                            <option value="">-- Bebas (Ditentukan Kemudian) --</option>
                            <option v-for="armada in daftarArmada" :key="armada.id" :value="armada.id">
                                {{ armada.plat_nomor }} - {{ armada.nama }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="bg-white border border-slate-200 rounded-xl shadow-sm mt-2 relative animate-fade-in">
                
                <div v-if="sedangMuatStok" class="absolute inset-0 bg-white/70 backdrop-blur-sm z-10 flex items-center justify-center rounded-xl">
                    <div class="flex flex-col items-center gap-2">
                        <i class="pi pi-spin pi-spinner text-3xl text-blue-600"></i>
                        <span class="text-xs font-bold text-slate-500">Memuat Stok...</span>
                    </div>
                </div>
                
                <div class="overflow-x-auto rounded-t-xl">
                    <table class="w-full text-left border-collapse min-w-[750px]">
                        <thead>
                            <tr class="bg-slate-100 border-b border-slate-200">
                                <th class="p-4 text-[11px] font-bold text-slate-500 uppercase w-10 text-center">No</th>
                                <th class="p-4 text-[11px] font-bold text-slate-500 uppercase w-48">Group / Klaim</th>
                                <th class="p-4 text-[11px] font-bold text-slate-500 uppercase min-w-[180px]">Pilih Barang</th>
                                <th class="p-4 text-[11px] font-bold text-slate-500 uppercase min-w-[180px]">Kemasan & Stok</th>
                                <th class="p-4 text-[11px] font-bold text-slate-500 uppercase w-24 text-center">Qty Kirim</th>
                                <th class="p-4 text-[11px] font-bold text-slate-500 uppercase w-24 text-right">Total Berat</th>
                                <th class="p-4 w-12 text-center">Aksi</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <tr v-for="(item, index) in form.items" :key="index" class="hover:bg-slate-50/50 transition-colors">
                                <td class="p-4 text-center font-bold text-slate-700">{{ index + 1 }}</td>
                                
                                <td class="p-3 align-top">
                                    <select v-model="item.stiker" @change="resetBarang(item)" :disabled="!form.entitas_id" required
                                        class="w-full bg-white border border-slate-300 rounded-sm px-3 py-2 text-sm font-semibold text-blue-700 focus:ring-1 focus:ring-blue-500 focus:outline-none disabled:bg-slate-100 disabled:text-slate-400 disabled:border-slate-200 disabled:cursor-not-allowed cursor-pointer transition-all">
                                        <option value="" disabled>{{ form.entitas_id ? '-- Pilih Grup --' : 'Pilih PT Dulu' }}</option>
                                        <option v-for="grup in daftarGrupUnik" :key="grup" :value="grup">{{ grup }}</option>
                                    </select>
                                </td>

                                <td class="p-3 align-top">
                                    <select v-model="item.barang_nama" @change="resetKemasan(item)" :disabled="!item.stiker" required 
                                        class="w-full bg-white border border-slate-300 rounded-sm px-3 py-2 text-sm font-semibold text-slate-800 focus:ring-1 focus:ring-blue-500 focus:outline-none disabled:bg-slate-100 disabled:text-slate-400 disabled:border-slate-200 disabled:cursor-not-allowed cursor-pointer transition-all">
                                        <option value="" disabled>{{ item.stiker ? '-- Pilih Barang --' : 'Pilih Grup Dulu ←' }}</option>
                                        <option v-for="nama in getBarangTersedia(item.stiker)" :key="nama" :value="nama">{{ nama }}</option>
                                    </select>
                                    
                                    <div v-if="item.barang_nama && item.stiker" class="text-[11px] font-medium text-emerald-600 mt-2 flex items-start gap-1">
                                        <i class="pi pi-info-circle text-[10px] mt-[2px]"></i>
                                        <span class="leading-tight">{{ getInfoStokBarang(item) }}</span>
                                    </div>
                                </td>

                                <td class="p-3 align-top">
                                    <select v-model="item.stok_terpilih" @change="hitungOtomatis(item)" :disabled="!item.barang_nama" required 
                                        class="w-full bg-white border border-slate-300 rounded-sm px-3 py-2 text-sm font-semibold text-slate-800 focus:ring-1 focus:ring-blue-500 focus:outline-none disabled:bg-slate-100 disabled:text-slate-400 disabled:border-slate-200 disabled:cursor-not-allowed cursor-pointer transition-all">
                                        <option :value="null" disabled>-- Pilih Kemasan --</option>
                                        <option v-for="(kemasan, idx) in getKemasanTersedia(item.barang_nama, item.stiker)" :key="idx" :value="kemasan">
                                            {{ kemasan.kemasan_nama || kemasan.kemasan }} (Ada: {{ kemasan.qty_unit || kemasan.qty || 0 }})
                                        </option>
                                    </select>
                                </td>
                                
                                <td class="p-3 align-top">
                                    <input type="number" v-model="item.total_unit" @input="kalkulasiBerat(item)" :max="item.stok_terpilih?.qty_unit || item.stok_terpilih?.qty" min="1" :disabled="!item.stok_terpilih" required 
                                        class="w-full text-center bg-white border border-slate-300 rounded-sm px-3 py-2 text-sm font-bold text-blue-600 focus:ring-1 focus:ring-blue-500 focus:outline-none disabled:bg-slate-100 disabled:text-slate-400 disabled:border-slate-200 disabled:cursor-not-allowed transition-all" />
                                </td>
                                
                                <td class="p-3 align-top text-right">
                                    <span class="font-bold text-slate-700 text-sm block mt-2">{{ item.total_berat ? item.total_berat + ' Kg' : '0 Kg' }}</span>
                                </td>
                                
                                <td class="p-3 align-top text-center">
                                    <button type="button" @click="hapusItem(index)" v-if="form.items.length > 1" class="w-8 h-8 mt-1 rounded-sm flex items-center justify-center text-red-500 hover:bg-red-100 border border-transparent hover:border-red-200 transition-colors mx-auto">
                                        <i class="pi pi-trash text-sm"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <div class="p-4 bg-slate-50 border-t border-slate-200 text-center rounded-b-xl">
                    <button type="button" @click="tambahItem" :disabled="!form.entitas_id" class="text-sm font-bold text-blue-600 hover:text-blue-700 disabled:text-slate-400 flex items-center justify-center gap-2 mx-auto px-4 py-2 hover:bg-blue-50 rounded-sm transition-colors">
                        <i class="pi pi-plus text-xs"></i> Tambah Baris Barang
                    </button>
                </div>
            </div>

            <div class="flex justify-end mt-4">
                <button type="submit" :disabled="sedangProses || !form.entitas_id || form.items.length === 0" class="px-8 py-3 bg-slate-900 text-white font-bold hover:bg-slate-800 disabled:bg-slate-400 transition-colors rounded-sm shadow-md flex items-center gap-2">
                    <i v-if="sedangProses" class="pi pi-spin pi-spinner text-sm"></i>
                    <i v-else class="pi pi-send text-sm"></i>
                    <span>{{ sedangProses ? 'Menyimpan...' : 'Kirim Request Distribusi' }}</span>
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDistribusiForm } from '../composables/useDistribusiForm'

const {
    sedangProses, sedangMuatStok, daftarEntitas, daftarToko, daftarArmada, 
    form, previewNomor, daftarGrupUnik, getBarangTersedia, // Tambahan export
    tambahItem, hapusItem, getKemasanTersedia, getInfoStokBarang, 
    resetBarang, resetKemasan, hitungOtomatis, kalkulasiBerat, pilihEntitas, 
    muatDataMaster, simpanDistribusi
} = useDistribusiForm()

onMounted(() => muatDataMaster())
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>