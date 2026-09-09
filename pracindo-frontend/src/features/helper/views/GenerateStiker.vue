<template>
    <div class="flex gap-6 h-full p-6 bg-slate-50/50">
        
        <!-- ========================================== -->
        <!-- SISI KIRI: PEMILIHAN JENIS & DAFTAR FILE   -->
        <!-- ========================================== -->
        <div class="w-1/4 flex flex-col gap-5">
            <!-- 1. Dropdown Jenis -->
            <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 flex flex-col gap-3">
                <label class="text-xs font-extrabold text-slate-500 uppercase tracking-widest">Pilih Jenis</label>
                <Dropdown 
                    v-model="form.jenis" 
                    :options="opsiJenis" 
                    optionLabel="label" 
                    optionValue="value" 
                    placeholder="Pilih Jenis..." 
                    class="w-full"
                    @change="resetPilihan"
                />
            </div>

            <!-- 2. Daftar File -->
            <div v-if="form.jenis" class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 flex-1 overflow-y-auto custom-scrollbar">
                <label class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-4 block">Opsi Template</label>
                <div class="flex flex-col gap-3">
                    <button 
                        v-for="file in daftarFileAktif" 
                        :key="file.id"
                        @click="pilihFile(file)"
                        class="p-4 text-left rounded-xl border-2 transition-all w-full flex flex-col gap-1 group"
                        :class="fileTerpilih?.id === file.id ? 'border-slate-800 bg-slate-50' : 'border-slate-100 bg-white hover:border-slate-300'"
                    >
                        <span class="font-bold text-sm transition-colors" :class="fileTerpilih?.id === file.id ? 'text-slate-900' : 'text-slate-600 group-hover:text-slate-900'">
                            {{ file.nama_file }}
                        </span>
                        <span class="text-xs font-semibold" :class="fileTerpilih?.id === file.id ? 'text-slate-600' : 'text-slate-400'">
                            Pola: {{ file.pola }}
                        </span>
                    </button>
                </div>
            </div>
        </div>

        <!-- ========================================== -->
        <!-- SISI KANAN: AREA INPUT (ACTIVITY)          -->
        <!-- ========================================== -->
        <div class="w-3/4 flex flex-col">
            <div class="bg-white p-8 rounded-3xl shadow-sm border border-slate-200 flex flex-col h-full">
                
                <!-- State Kosong -->
                <div v-if="!fileTerpilih" class="flex-1 flex flex-col items-center justify-center text-slate-400">
                    <div class="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                        <i class="pi pi-file-edit text-3xl text-slate-400"></i>
                    </div>
                    <h3 class="font-bold text-slate-600 mb-1">Belum Ada Template Terpilih</h3>
                    <p class="text-sm">Silakan pilih jenis dan template di panel sebelah kiri.</p>
                </div>

                <!-- State Aktif (Formulir Dinamis) -->
                <div v-else class="flex flex-col h-full">
                    
                    <!-- Header -->
                    <div class="border-b border-slate-200 pb-5 mb-6 flex justify-between items-start">
                        <div>
                            <h2 class="text-2xl font-black text-slate-800 tracking-tight mb-1">Input Data Stiker</h2>
                            <div class="flex items-center gap-2 text-sm">
                                <span class="font-semibold text-slate-600">{{ fileTerpilih.nama_file }}</span>
                                <span class="text-slate-300">•</span>
                                <span class="text-slate-500">Pola <span class="font-bold text-slate-700">{{ fileTerpilih.pola }}</span></span>
                            </div>
                        </div>
                        <div class="bg-indigo-50 border border-indigo-100 text-indigo-700 px-4 py-2 rounded-xl flex items-center gap-2 font-bold text-sm">
                            <i class="pi pi-info-circle"></i>
                            Butuh {{ form.items.length }} Input
                        </div>
                    </div>

                    <!-- Area Input -->
                    <div class="flex-1 overflow-y-auto pr-4 custom-scrollbar flex flex-col gap-6">
                        <div 
                            v-for="(item, index) in form.items" 
                            :key="index"
                            class="p-6 rounded-2xl border border-slate-200 bg-white shadow-sm flex flex-col gap-5 hover:border-slate-300 transition-colors"
                        >
                            <!-- Header Label per Blok -->
                            <div class="flex items-center gap-3 border-b border-slate-100 pb-4">
                                <div class="w-8 h-8 bg-slate-800 text-white rounded-full flex items-center justify-center font-black text-sm shadow-sm">
                                    {{ index + 1 }}
                                </div>
                                <h3 class="font-bold text-slate-700 tracking-wide text-sm uppercase">Grup Input {{ index + 1 }}</h3>
                            </div>
                            
                            <!-- Form Grid -->
                            <div class="grid grid-cols-2 gap-x-6 gap-y-5">
                                <div class="flex flex-col gap-2">
                                    <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Nama Barang</label>
                                    <InputText v-model="item.nama_item" placeholder="Misal: SUPER WHITE" class="p-3 border-slate-300 rounded-xl" />
                                </div>
                                <div class="flex flex-col gap-2">
                                    <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Tipe Barang</label>
                                    <InputText v-model="item.tipe" placeholder="Misal: SC SC" class="p-3 border-slate-300 rounded-xl" />
                                </div>
                                <div class="flex flex-col gap-2">
                                    <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Tanggal Lot</label>
                                    <Calendar v-model="item.lot" dateFormat="yy-mm-dd" placeholder="Pilih Tanggal" class="w-full" :pt="{ input: { class: 'p-3 border-slate-300 rounded-xl w-full' } }" />
                                </div>
                                <div class="flex flex-col gap-2">
                                    <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Net (KGS)</label>
                                    <InputNumber v-model="item.net" mode="decimal" :minFractionDigits="2" :maxFractionDigits="2" placeholder="0.00" class="w-full" :pt="{ input: { class: 'p-3 border-slate-300 rounded-xl w-full' } }" />
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Footer / Submit -->
                    <div class="pt-6 mt-4 border-t border-slate-200 flex justify-end">
                        <button @click="submitStiker" class="bg-slate-900 hover:bg-slate-800 text-white font-bold py-3 px-8 rounded-xl flex items-center gap-3 transition-colors shadow-md">
                            <i class="pi pi-print"></i>
                            Generate Stiker Sekarang
                        </button>
                    </div>
                </div>

            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Calendar from 'primevue/calendar'

const opsiJenis = [
    { label: 'Polos Besar', value: 'polos_besar' },
    { label: 'CV Besar', value: 'cv_besar' }
]

const masterTemplates = {
    polos_besar: [
        { id: 1, nama_file: 'stiker_polos_besar_AAAA', pola: 'AAAA', jumlah_input: 1 },
        { id: 2, nama_file: 'stiker_polos_besar_AAAB', pola: 'AAAB', jumlah_input: 2 },
        { id: 3, nama_file: 'stiker_polos_besar_AABB', pola: 'AABB', jumlah_input: 2 },
        { id: 4, nama_file: 'stiker_polos_besar_AABC', pola: 'AABC', jumlah_input: 3 },
        { id: 5, nama_file: 'stiker_polos_besar_ABCD', pola: 'ABCD', jumlah_input: 4 },
    ],
    cv_besar: [
        { id: 6, nama_file: 'stiker_cv_besar_AAAA', pola: 'AAAA', jumlah_input: 1 },
        { id: 7, nama_file: 'stiker_cv_besar_AAAC', pola: 'AAAC', jumlah_input: 2 }, 
        { id: 8, nama_file: 'stiker_cv_besar_AABB', pola: 'AABB', jumlah_input: 2 },
        { id: 9, nama_file: 'stiker_cv_besar_AABC', pola: 'AABC', jumlah_input: 3 },
        { id: 10, nama_file: 'stiker_cv_besar_ABCD', pola: 'ABCD', jumlah_input: 4 },
    ]
}

const fileTerpilih = ref(null)
const form = reactive({
    jenis: null,
    items: [] 
})

const daftarFileAktif = computed(() => {
    if (!form.jenis) return []
    return masterTemplates[form.jenis] || []
})

const resetPilihan = () => {
    fileTerpilih.value = null
    form.items = []
}

const pilihFile = (file) => {
    fileTerpilih.value = file
    form.items = Array.from({ length: file.jumlah_input }, () => ({
        nama_item: '',
        tipe: '',
        lot: null,
        net: null
    }))
}

const submitStiker = () => {
    const payload = {
        jenis: form.jenis,
        items: form.items.map(item => ({
            ...item,
            lot: item.lot ? item.lot.toISOString().split('T')[0] : null 
        }))
    }
    console.log("Payload siap dikirim ke backend:", payload)
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 8px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 999px; border: 2px solid white; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>