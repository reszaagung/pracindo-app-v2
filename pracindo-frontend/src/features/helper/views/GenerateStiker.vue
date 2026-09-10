<template>
    <div class="flex gap-6 h-full p-6 bg-slate-50/50">
        <div class="w-1/4 flex flex-col gap-5">
            <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 flex flex-col gap-3">
                <label class="text-xs font-extrabold text-slate-500 uppercase tracking-widest">Pilih Jenis</label>
                <Dropdown :options="opsiJenis" @change="resetPilihan" class="w-full" optionLabel="label" optionValue="value" placeholder="Pilih Jenis..." v-model="form.jenis"/>
            </div>
            <div v-if="form.jenis" class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 flex-1 overflow-y-auto custom-scrollbar">
                <label class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-4 block">Opsi Template</label>
                <div class="flex flex-col gap-3">
                    <button 
                        v-for="file in daftarFileAktif" 
                        :key="file.id"
                        @click="pilihFile(file)"
                        class="w-full p-4 text-left rounded-xl border-2 transition-all flex flex-col gap-1 group"
                        :class="fileTerpilih?.id === file.id ? 'border-slate-800 bg-slate-50' : 'border-slate-100 bg-white hover:border-slate-300'"
                    >
                        <div class="font-bold text-base transition-colors" :class="fileTerpilih?.id === file.id ? 'text-slate-900' : 'text-slate-700 group-hover:text-slate-900'">
                            Pola: {{ file.pola }}
                        </div>
                        <div class="text-xs truncate transition-colors" :class="fileTerpilih?.id === file.id ? 'text-slate-500' : 'text-slate-400'">
                            {{ file.nama_file }}
                        </div>
                    </button>
                </div>
            </div>
        </div>

        <div class="w-3/4 flex flex-col">
            <div class="bg-white p-8 rounded-3xl shadow-sm border border-slate-200 flex flex-col h-full min-h-0">
                <div v-if="!fileTerpilih" class="flex-1 flex flex-col items-center justify-center text-slate-400">
                    <div class="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                        <i class="pi pi-file-edit text-3xl text-slate-400"></i>
                    </div>
                    <h3 class="font-bold text-slate-600 mb-1">Belum Ada Template Terpilih</h3>
                    <p class="text-sm">Silakan pilih jenis dan template di panel sebelah kiri.</p>
                </div>
                <div v-else class="flex gap-6 h-full min-h-0">
                    <div class="flex-1 flex flex-col h-full min-h-0">
                        <div class="border-b border-slate-200 pb-5 mb-6 flex justify-between items-start flex-shrink-0">
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
                        <div class="flex-1 overflow-y-auto pr-4 custom-scrollbar flex flex-col gap-6">
                            <div 
                                v-for="(item, index) in form.items" 
                                :key="index"
                                class="p-6 rounded-2xl border border-slate-200 bg-white shadow-sm flex flex-col gap-5 hover:border-slate-300 transition-colors"
                            >
                                <div class="flex items-center gap-3 border-b border-slate-100 pb-4">
                                    <div class="w-8 h-8 bg-slate-800 text-white rounded-full flex items-center justify-center font-black text-sm shadow-sm">
                                        {{ index + 1 }}
                                    </div>
                                    <h3 class="font-bold text-slate-700 tracking-wide text-sm uppercase">Grup Input {{ index + 1 }}</h3>
                                </div>
                                <div class="grid grid-cols-2 gap-x-6 gap-y-5">
                                    <div class="flex flex-col gap-2">
                                        <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Nama Barang</label>
                                        <InputText class="p-3 border-slate-300 rounded-xl" placeholder="Misal: SUPER WHITE" v-model="item.nama_item"/>
                                    </div>
                                    <div class="flex flex-col gap-2">
                                        <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Tipe Barang</label>
                                        <InputText class="p-3 border-slate-300 rounded-xl" placeholder="Misal: SC SC" v-model="item.tipe"/>
                                    </div>
                                    <div class="flex flex-col gap-2">
                                        <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Tanggal Lot</label>
                                        <Calendar :pt="{ input: { class: 'p-3 border-slate-300 rounded-xl w-full' } }" class="w-full" dateFormat="yy-mm-dd" placeholder="Pilih Tanggal" v-model="item.lot"/>
                                    </div>
                                    <div class="flex flex-col gap-2">
                                        <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Net (KGS)</label>
                                        <InputNumber :maxFractionDigits="2" :minFractionDigits="2" :pt="{ input: { class: 'p-3 border-slate-300 rounded-xl w-full' } }" class="w-full" mode="decimal" placeholder="0.00" v-model="item.net"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="pt-6 mt-4 border-t border-slate-200 flex justify-end flex-shrink-0">
                            <button 
                                @click="submitStiker" 
                                :disabled="isSubmitting"
                                class="bg-slate-900 hover:bg-slate-800 disabled:bg-slate-400 disabled:cursor-not-allowed text-white font-bold py-3 px-8 rounded-xl flex items-center gap-3 transition-colors shadow-md"
                            >
                                <i :class="isSubmitting ? 'pi pi-spin pi-spinner' : 'pi pi-print'"></i>
                                {{ isSubmitting ? 'Memproses...' : 'Generate Stiker Sekarang' }}
                            </button>
                        </div>
                    </div>
                    <div class="w-80 bg-slate-50/80 p-5 rounded-2xl border border-slate-200 flex flex-col min-h-0">
                        <div class="text-xs font-extrabold text-slate-500 uppercase tracking-widest mb-4 flex-shrink-0">Petunjuk Visual</div>
                        <div class="flex-1 border-2 border-dashed border-slate-200 rounded-xl bg-white p-4 overflow-y-auto custom-scrollbar min-h-0 flex flex-col">
                            <div class="m-auto w-full flex items-center justify-center">
                                <component :is="PreviewComponent" v-if="fileTerpilih" :form="form" class="w-full" />
                                <div v-else class="text-slate-400 text-xs text-center">Pilih template untuk melihat preview.</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed, shallowRef, defineAsyncComponent } from 'vue'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Calendar from 'primevue/calendar'
import { useToast } from 'primevue/usetoast'
import api from '@/utils/api'

const toast = useToast()

const opsiJenis = [
    { label: 'Polos Besar', value: 'polos_besar' },
    { label: 'CV Besar', value: 'cv' }
]

const masterTemplates = {
    polos_besar: [
        { id: 1, nama_file: 'stiker_polos_besar_AAAA', pola: 'AAAA', jumlah_input: 1 },
        { id: 2, nama_file: 'stiker_polos_besar_AAAB', pola: 'AAAB', jumlah_input: 2 },
        { id: 3, nama_file: 'stiker_polos_besar_AABB', pola: 'AABB', jumlah_input: 2 },
        { id: 4, nama_file: 'stiker_polos_besar_AABC', pola: 'AABC', jumlah_input: 3 },
        { id: 5, nama_file: 'stiker_polos_besar_ABCD', pola: 'ABCD', jumlah_input: 4 },
    ],
    cv: [
        { id: 6, nama_file: 'stiker_cv_besar_AAAA', pola: 'AAAA', jumlah_input: 1 },
        { id: 7, nama_file: 'stiker_cv_besar_AAAC', pola: 'AAAC', jumlah_input: 2 }, 
        { id: 8, nama_file: 'stiker_cv_besar_AABB', pola: 'AABB', jumlah_input: 2 },
        { id: 9, nama_file: 'stiker_cv_besar_AABC', pola: 'AABC', jumlah_input: 3 },
        { id: 10, nama_file: 'stiker_cv_besar_ABCD', pola: 'ABCD', jumlah_input: 4 },
    ]
}

const fileTerpilih = ref(null)
const isSubmitting = ref(false)
const PreviewComponent = shallowRef(null)

const form = reactive({
    jenis: null,
    items: [] 
})

const getPolaFromFilename = (filename) => {
    const cleanName = filename.replace('.docx', '')
    const parts = cleanName.split('_')
    return parts[parts.length - 1].toUpperCase()
}

const daftarFileAktif = computed(() => {
    if (!form.jenis) return []
    return (masterTemplates[form.jenis] || []).map(file => ({
        ...file,
        pola: file.pola || getPolaFromFilename(file.nama_file)
    }))
})

const resetPilihan = () => {
    fileTerpilih.value = null
    form.items = []
    PreviewComponent.value = null
}

const pilihFile = (file) => {
    fileTerpilih.value = file
    form.items = Array.from({ length: file.jumlah_input }, () => ({
        nama_item: '',
        tipe: '',
        lot: null,
        net: null
    }))

    let folderJenis = form.jenis === 'cv' ? 'cv_besar' : form.jenis
    const namaKomponen = `${folderJenis}_${file.pola}`

    PreviewComponent.value = defineAsyncComponent(() =>
        import(`../components/stiker_${folderJenis}/${namaKomponen}.vue`)
            .catch(() => ({ template: '<div class="text-slate-400 text-xs text-center p-4">Preview belum tersedia.</div>' }))
    )
}

const formatTanggalLokal = (date) => {
    if (!date) return null
    const tahun = date.getFullYear()
    const bulan = String(date.getMonth() + 1).padStart(2, '0')
    const hari = String(date.getDate()).padStart(2, '0')
    return `${tahun}-${bulan}-${hari}`
}

const validasiForm = () => {
    for (const [idx, item] of form.items.entries()) {
        const netKosong = item.net === null || item.net === undefined
        if (!item.nama_item?.trim() || !item.tipe?.trim() || !item.lot || netKosong) {
            toast.add({
                severity: 'warn',
                summary: 'Data belum lengkap',
                detail: `Grup Input ${idx + 1} masih ada field yang kosong`,
                life: 3000
            })
            return false
        }
    }
    return true
}

const submitStiker = async () => {
    if (!fileTerpilih.value || isSubmitting.value) return
    if (!validasiForm()) return

    const payload = {
        jenis: form.jenis,
        items: form.items.map(item => ({
            nama_item: item.nama_item,
            tipe: item.tipe,
            lot: formatTanggalLokal(item.lot),
            net: item.net
        }))
    }

    isSubmitting.value = true
    try {
        const response = await api.post('fitur/generate-stiker/', payload)
        const stikerId = response.data.id

        await api.post(`fitur/generate-stiker/${stikerId}/cetak/`)

        toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Perintah cetak stiker masuk antrean!', life: 3000 })
        
        resetPilihan()
        form.jenis = null
    } catch (err) {
        console.error('Gagal generate stiker:', err)
        toast.add({
            severity: 'error',
            summary: 'Gagal membuat stiker',
            detail: err?.response?.data?.detail || 'Terjadi kesalahan pada server',
            life: 4000
        })
    } finally {
        isSubmitting.value = false
    }
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 8px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 999px; border: 2px solid white; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>