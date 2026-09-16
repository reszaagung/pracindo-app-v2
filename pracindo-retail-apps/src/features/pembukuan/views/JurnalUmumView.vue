<template>
    <div class="max-w-7xl mx-auto pb-10 space-y-6 font-sans">

        <!-- HEADER -->
        <header class="flex justify-between items-end border-b border-slate-200 pb-4">
            <div>
                <p class="text-sm text-slate-500 mb-1">Akuntansi & Keuangan</p>
                <h1 class="text-2xl font-bold text-slate-800">Jurnal Umum</h1>
            </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

            <!-- ==========================================
           KIRI: FORM INPUT JURNAL BARU (Bisa nambah baris)
      =========================================== -->
            <div
                class="lg:col-span-2 bg-white rounded-[20px] shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 overflow-hidden flex flex-col">
                <div class="p-4 md:p-5 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                    <h2 class="font-bold text-slate-700">Buat Entri Jurnal Baru</h2>
                    <button @click="tambahBaris"
                        class="text-xs font-bold bg-blue-100 text-blue-700 px-3 py-1.5 rounded-lg hover:bg-blue-200 transition-colors">
                        + Tambah Baris Akun
                    </button>
                </div>

                <div class="p-4 md:p-5 space-y-4">
                    <!-- Info Dasar Jurnal -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-bold text-slate-600 mb-1">Referensi Dokumen
                                (Opsional)</label>
                            <input v-model="form.referensi" type="text" placeholder="Contoh: INV-001 / BKK-09"
                                class="w-full border border-slate-200 rounded-xl px-3 py-2 text-sm outline-none focus:border-blue-500 bg-white">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-600 mb-1">Keterangan Transaksi <span
                                    class="text-rose-500">*</span></label>
                            <input v-model="form.keterangan" type="text" placeholder="Catatan transaksi..."
                                class="w-full border border-slate-200 rounded-xl px-3 py-2 text-sm outline-none focus:border-blue-500 bg-white">
                        </div>
                    </div>

                    <!-- Tabel Input Debit/Kredit -->
                    <div class="border border-slate-200 rounded-xl overflow-hidden mt-4">
                        <table class="min-w-full">
                            <thead class="bg-slate-50 border-b border-slate-200">
                                <tr>
                                    <th class="px-4 py-2 text-left text-xs font-bold text-slate-500 w-1/2">Akun Buku
                                        Besar</th>
                                    <th class="px-4 py-2 text-right text-xs font-bold text-slate-500 w-1/4">Debit (Rp)
                                    </th>
                                    <th class="px-4 py-2 text-right text-xs font-bold text-slate-500 w-1/4">Kredit (Rp)
                                    </th>
                                    <th class="px-2 py-2 w-10"></th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                <tr v-for="(baris, index) in form.items" :key="index" class="hover:bg-slate-50/50">
                                    <td class="px-4 py-2">
                                        <select v-model="baris.akun_id"
                                            class="w-full border border-slate-200 rounded-lg px-2 py-1.5 text-sm outline-none focus:border-blue-500 bg-white">
                                            <option :value="null" disabled>-- Pilih Akun --</option>
                                            <option v-for="akun in akunList" :key="akun.id" :value="akun.id">
                                                {{ akun.kode }} - {{ akun.nama }}
                                            </option>
                                        </select>
                                    </td>
                                    <td class="px-4 py-2">
                                        <input v-model.number="baris.debit" @input="baris.kredit = 0" type="number"
                                            min="0"
                                            class="w-full border border-slate-200 rounded-lg px-2 py-1.5 text-sm outline-none focus:border-blue-500 text-right bg-white">
                                    </td>
                                    <td class="px-4 py-2">
                                        <input v-model.number="baris.kredit" @input="baris.debit = 0" type="number"
                                            min="0"
                                            class="w-full border border-slate-200 rounded-lg px-2 py-1.5 text-sm outline-none focus:border-blue-500 text-right bg-white">
                                    </td>
                                    <td class="px-2 py-2 text-center">
                                        <button @click="hapusBaris(index)" :disabled="form.items.length <= 2"
                                            class="text-rose-400 hover:text-rose-600 disabled:opacity-30 disabled:cursor-not-allowed">
                                            <i class="pi pi-times-circle"></i>
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                            <tfoot class="bg-slate-50 border-t border-slate-200">
                                <tr>
                                    <td class="px-4 py-3 text-right text-xs font-bold text-slate-600">TOTAL ENTRI</td>
                                    <td class="px-4 py-3 text-right font-bold text-sm"
                                        :class="totalDebit === totalKredit ? 'text-emerald-600' : 'text-slate-800'">
                                        {{ totalDebit.toLocaleString('id-ID') }}
                                    </td>
                                    <td class="px-4 py-3 text-right font-bold text-sm"
                                        :class="totalDebit === totalKredit ? 'text-emerald-600' : 'text-slate-800'">
                                        {{ totalKredit.toLocaleString('id-ID') }}
                                    </td>
                                    <td></td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>

                    <!-- Validasi Balance & Tombol Submit -->
                    <div class="flex items-center justify-between pt-4">
                        <div class="flex items-center gap-2">
                            <span v-if="selisih !== 0"
                                class="text-xs font-bold text-rose-500 bg-rose-50 px-3 py-1 rounded-md border border-rose-100">
                                <i class="pi pi-exclamation-triangle text-[10px]"></i> Selisih: Rp {{
                                    Math.abs(selisih).toLocaleString('id-ID') }} (Tidak Balance)
                            </span>
                            <span v-else-if="totalDebit > 0 && totalKredit > 0"
                                class="text-xs font-bold text-emerald-600 bg-emerald-50 px-3 py-1 rounded-md border border-emerald-100">
                                <i class="pi pi-check text-[10px]"></i> Jurnal Balance
                            </span>
                        </div>

                        <button @click="submitJurnal" :disabled="isLoading || !isFormValid"
                            class="bg-blue-600 text-white font-bold py-2.5 px-6 rounded-xl hover:bg-blue-700 transition-all shadow-md shadow-blue-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2">
                            <i v-if="isLoading" class="pi pi-spin pi-spinner"></i>
                            <i v-else class="pi pi-save"></i>
                            {{ isLoading ? 'Menyimpan...' : 'Simpan Jurnal' }}
                        </button>
                    </div>
                </div>
            </div>

            <!-- ==========================================
           KANAN: HISTORI JURNAL TERAKHIR
      =========================================== -->
            <div
                class="bg-white rounded-[20px] shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col h-[calc(100vh-200px)]">
                <div class="p-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                    <h2 class="font-bold text-slate-700">Histori Jurnal</h2>
                    <button @click="fetchJurnal" class="text-slate-400 hover:text-blue-500"><i
                            class="pi pi-refresh"></i></button>
                </div>

                <div class="flex-1 overflow-y-auto p-4 custom-scrollbar space-y-3">
                    <div v-if="jurnalList.length === 0 && !isLoading"
                        class="text-center text-slate-400 opacity-70 py-10">
                        <i class="pi pi-book text-4xl mb-2"></i>
                        <p class="text-sm">Belum ada catatan jurnal.</p>
                    </div>

                    <!-- Card Histori -->
                    <div v-for="jurnal in jurnalList" :key="jurnal.id"
                        class="border border-slate-200 rounded-xl p-3 bg-white shadow-sm hover:border-blue-300 transition-colors">
                        <div class="flex justify-between items-start mb-2">
                            <span class="font-bold text-sm text-slate-800">{{ jurnal.nomor_jurnal }}</span>
                            <span class="text-[10px] text-slate-500">{{ new
                                Date(jurnal.tanggal).toLocaleDateString('id-ID') }}</span>
                        </div>
                        <p class="text-xs text-slate-600 mb-2 truncate">{{ jurnal.keterangan }}</p>

                        <!-- Looping Detail Jurnal (Debit/Kredit) -->
                        <div class="space-y-1 bg-slate-50 p-2 rounded-lg border border-slate-100">
                            <div v-for="detail in jurnal.item_jurnal" :key="detail.id"
                                class="flex justify-between text-[11px] font-medium">
                                <span class="text-slate-600 w-32 truncate">{{ detail.akun_nama }}</span>
                                <span v-if="detail.debit > 0" class="text-emerald-600">Rp {{
                                    parseFloat(detail.debit).toLocaleString('id-ID') }} (D)</span>
                                <span v-else class="text-rose-500">Rp {{
                                    parseFloat(detail.kredit).toLocaleString('id-ID') }} (K)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import { reactive, computed, onMounted } from 'vue'
import { usePembukuan } from '../composables/usePembukuan'

const { akunList, jurnalList, isLoading, fetchAkun, fetchJurnal, simpanJurnal } = usePembukuan()

// State Form (Default 2 baris karena minimal harus ada 1 Debit dan 1 Kredit)
const form = reactive({
    referensi: '',
    keterangan: '',
    items: [
        { akun_id: null, debit: 0, kredit: 0 },
        { akun_id: null, debit: 0, kredit: 0 }
    ]
})

onMounted(() => {
    fetchAkun()
    fetchJurnal()
})

// Fungsi UI
const tambahBaris = () => {
    form.items.push({ akun_id: null, debit: 0, kredit: 0 })
}

const hapusBaris = (index) => {
    if (form.items.length > 2) {
        form.items.splice(index, 1)
    }
}

// Kalkulasi Akuntansi
const totalDebit = computed(() => form.items.reduce((sum, item) => sum + (Number(item.debit) || 0), 0))
const totalKredit = computed(() => form.items.reduce((sum, item) => sum + (Number(item.kredit) || 0), 0))
const selisih = computed(() => totalDebit.value - totalKredit.value)

// Validasi Form
const isFormValid = computed(() => {
    // 1. Keterangan wajib diisi
    if (!form.keterangan.trim()) return false
    // 2. Semua baris harus punya akun
    const adaAkunKosong = form.items.some(item => !item.akun_id)
    if (adaAkunKosong) return false
    // 3. Harus Balance (Debit = Kredit) dan tidak boleh 0
    if (selisih.value !== 0 || totalDebit.value === 0) return false

    return true
})

// Eksekusi Submit
const submitJurnal = async () => {
    if (!isFormValid.value) return

    const payload = {
        referensi: form.referensi,
        keterangan: form.keterangan,
        items: form.items.map(item => ({
            akun_id: item.akun_id,
            debit: Number(item.debit) || 0,
            kredit: Number(item.kredit) || 0
        }))
    }

    const result = await simpanJurnal(payload)
    if (result.status === 'sukses') {
        alert(`Jurnal ${result.nomor_jurnal} berhasil disimpan!`)
        // Reset form
        form.referensi = ''
        form.keterangan = ''
        form.items = [
            { akun_id: null, debit: 0, kredit: 0 },
            { akun_id: null, debit: 0, kredit: 0 }
        ]
        // Refresh histori
        fetchJurnal()
    } else {
        alert(`Gagal: ${result.pesan}`)
    }
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
    width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 999px;
}
</style>