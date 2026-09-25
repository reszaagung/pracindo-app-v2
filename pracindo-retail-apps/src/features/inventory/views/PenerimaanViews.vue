<template>
    <div class="min-h-screen bg-slate-100 text-slate-800 font-sans">
        <div class="w-full max-w-[1700px] mx-auto p-4 lg:p-6">

            <header class="mb-5">
                <div class="bg-white border border-slate-200 shadow-sm">
                    <div class="px-5 py-4">
                        <div class="flex flex-col xl:flex-row xl:items-center xl:justify-between gap-4">
                            <div class="flex items-center gap-4">
                                <button
                                    type="button"
                                    @click="$router.push('/dashboard')"
                                    class="h-10 px-4 bg-slate-900 text-white flex items-center gap-2 text-sm font-semibold hover:bg-slate-800 transition"
                                >
                                    <i class="pi pi-arrow-left text-xs"></i>
                                    Dashboard
                                </button>

                                <div class="hidden sm:block h-8 w-px bg-slate-200"></div>

                                <div>
                                    <div class="flex items-center gap-2">
                                        <span class="w-2 h-2 rounded-full bg-emerald-500"></span>

                                        <span
                                            class="text-[10px] uppercase tracking-[0.2em] font-black text-slate-400"
                                        >
                                            Logistik / Inventory
                                        </span>
                                    </div>

                                    <h1 class="text-xl lg:text-2xl font-black tracking-tight text-slate-900 mt-1">
                                        Penerimaan Barang
                                    </h1>
                                </div>
                            </div>

                            <div class="grid grid-cols-2 border-b-2 border-slate-200 w-full xl:w-auto">
                                <button
                                    type="button"
                                    @click="$router.push('/stok')"
                                    class="px-5 py-2.5 text-xs font-black text-slate-400 hover:text-slate-700 transition flex items-center justify-center gap-2"
                                >
                                    <i class="pi pi-box text-[10px]"></i>
                                    Stok
                                </button>

                                <button
                                    type="button"
                                    class="px-5 py-2.5 -mb-[2px] border-b-2 border-emerald-500 text-xs font-black text-emerald-600 flex items-center justify-center gap-2"
                                >
                                    <i class="pi pi-truck text-[10px]"></i>
                                    Terima Barang
                                </button>
                            </div>
                        </div>

                        <div class="flex justify-end mt-4">
                            <button
                                type="button"
                                @click="refreshData"
                                :disabled="isLoading"
                                class="h-10 px-4 border border-slate-200 text-slate-600 text-sm font-bold hover:bg-slate-50 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                            >
                                <i
                                    :class="isLoading ? 'pi pi-spin pi-spinner' : 'pi pi-refresh'"
                                ></i>
                                Refresh Data
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            <div
                v-if="errorPesan"
                class="mb-5 bg-rose-50 border border-rose-200 px-4 py-3 flex items-start justify-between gap-4"
            >
                <div class="flex items-start gap-3 text-sm text-rose-700">
                    <i class="pi pi-exclamation-circle mt-0.5"></i>
                    <span>{{ errorPesan }}</span>
                </div>

                <button
                    type="button"
                    @click="errorPesan = ''"
                    class="text-rose-400 hover:text-rose-700 transition"
                >
                    <i class="pi pi-times text-xs"></i>
                </button>
            </div>

            <div class="grid grid-cols-1 xl:grid-cols-[380px_minmax(0,1fr)] gap-5">

                <section
                    class="bg-white border border-slate-200 shadow-sm flex flex-col xl:h-[calc(100vh-190px)]"
                >
                    <div class="px-5 py-4 border-b border-slate-200">
                        <div class="flex items-center justify-between gap-3">
                            <div>
                                <p class="text-[10px] uppercase tracking-[0.18em] font-black text-slate-400">
                                    Incoming Delivery
                                </p>

                                <h2 class="text-lg font-black text-slate-900 mt-1">
                                    Kiriman Pending
                                </h2>
                            </div>

                            <span
                                class="min-w-8 h-8 px-2 bg-orange-50 text-orange-600 flex items-center justify-center text-xs font-black"
                            >
                                {{ doList.length }}
                            </span>
                        </div>
                    </div>

                    <div class="flex-1 overflow-y-auto custom-scrollbar">
                        <div
                            v-if="isLoading && doList.length === 0"
                            class="min-h-[400px] flex items-center justify-center"
                        >
                            <div class="text-center">
                                <i class="pi pi-spin pi-spinner text-2xl text-emerald-600"></i>

                                <p class="mt-3 text-sm text-slate-400 font-medium">
                                    Memuat data penerimaan...
                                </p>
                            </div>
                        </div>

                        <div
                            v-else-if="doList.length === 0"
                            class="min-h-[400px] flex items-center justify-center px-6"
                        >
                            <div class="text-center">
                                <div
                                    class="w-16 h-16 mx-auto mb-4 border border-dashed border-slate-300 flex items-center justify-center"
                                >
                                    <i class="pi pi-inbox text-xl text-slate-300"></i>
                                </div>

                                <p class="text-sm font-bold text-slate-600">
                                    Tidak ada kiriman baru
                                </p>

                                <p class="text-xs text-slate-400 mt-1">
                                    Semua surat jalan sudah diproses.
                                </p>
                            </div>
                        </div>

                        <div v-else class="divide-y divide-slate-200">
                            <button
                                v-for="kiriman in doList"
                                :key="kiriman.id"
                                type="button"
                                @click="pilihDO(kiriman)"
                                :class="
                                    selectedDO?.id === kiriman.id
                                        ? 'bg-emerald-50 border-l-4 border-l-emerald-500'
                                        : 'bg-white border-l-4 border-l-transparent hover:bg-slate-50'
                                "
                                class="w-full text-left p-5 transition"
                            >
                                <div class="flex items-start justify-between gap-3">
                                    <div class="min-w-0">
                                        <p class="text-sm font-black text-slate-900 truncate">
                                            {{ kiriman.nomor_penerimaan }}
                                        </p>

                                        <p class="text-xs text-slate-400 mt-1">
                                            {{ kiriman.tanggal_kirim }}
                                        </p>
                                    </div>

                                    <span
                                        class="shrink-0 px-2 py-1 text-[9px] uppercase font-black"
                                        :class="
                                            kiriman.status === 'SELESAI'
                                                ? 'bg-emerald-100 text-emerald-700'
                                                : 'bg-orange-100 text-orange-700'
                                        "
                                    >
                                        {{ kiriman.status }}
                                    </span>
                                </div>

                                <div class="mt-4 flex items-center justify-between gap-3">
                                    <span class="text-[10px] uppercase tracking-wider font-bold text-slate-400">
                                        Surat Jalan
                                    </span>

                                    <span class="text-xs font-bold text-slate-600 truncate">
                                        {{ kiriman.referensi_logistik || '-' }}
                                    </span>
                                </div>

                                <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between">
                                    <span class="text-[10px] text-slate-400">
                                        {{ kiriman.items?.length || 0 }} item
                                    </span>

                                    <span
                                        class="text-[10px] font-bold"
                                        :class="
                                            selectedDO?.id === kiriman.id
                                                ? 'text-emerald-600'
                                                : 'text-slate-400'
                                        "
                                    >
                                        {{
                                            selectedDO?.id === kiriman.id
                                                ? 'Dipilih'
                                                : 'Pilih'
                                        }}
                                    </span>
                                </div>
                            </button>
                        </div>
                    </div>
                </section>

                <section
                    class="bg-white border border-slate-200 shadow-sm flex flex-col xl:h-[calc(100vh-190px)]"
                >
                    <div
                        v-if="!selectedDO"
                        class="flex-1 min-h-[500px] flex items-center justify-center px-6"
                    >
                        <div class="text-center max-w-md">
                            <div
                                class="w-20 h-20 mx-auto mb-5 border border-dashed border-slate-300 flex items-center justify-center"
                            >
                                <i class="pi pi-list-check text-3xl text-slate-300"></i>
                            </div>

                            <h3 class="text-lg font-black text-slate-700">
                                Pilih Surat Jalan
                            </h3>

                            <p class="text-sm text-slate-400 mt-2 leading-relaxed">
                                Pilih salah satu kiriman pada panel kiri untuk melakukan pengecekan jumlah barang yang diterima.
                            </p>
                        </div>
                    </div>

                    <template v-else>
                        <div class="px-5 py-4 border-b border-slate-200">
                            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                                <div>
                                    <p class="text-[10px] uppercase tracking-[0.18em] font-black text-emerald-600">
                                        Pengecekan Fisik
                                    </p>

                                    <h2 class="text-lg font-black text-slate-900 mt-1">
                                        {{ selectedDO.nomor_penerimaan }}
                                    </h2>

                                    <p class="text-xs text-slate-400 mt-1">
                                        Surat Jalan:
                                        {{ selectedDO.referensi_logistik || '-' }}
                                    </p>
                                </div>

                                <div class="flex items-center gap-4">
                                    <div class="text-right">
                                        <p class="text-[10px] uppercase tracking-wider font-bold text-slate-400">
                                            Total Item
                                        </p>

                                        <p class="text-lg font-black text-slate-900">
                                            {{ checklistItems.length }}
                                        </p>
                                    </div>

                                    <div
                                        class="w-10 h-10 border border-slate-200 flex items-center justify-center text-slate-400"
                                    >
                                        <i class="pi pi-box"></i>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="flex-1 overflow-y-auto custom-scrollbar">
                            <div
                                v-if="checklistItems.length === 0"
                                class="min-h-[400px] flex items-center justify-center px-6"
                            >
                                <div class="text-center">
                                    <i class="pi pi-box text-3xl text-slate-300"></i>

                                    <p class="text-sm font-bold text-slate-500 mt-3">
                                        Tidak ada item
                                    </p>
                                </div>
                            </div>

                            <div v-else class="overflow-x-auto">
                                <table class="w-full min-w-[720px]">
                                    <thead class="bg-slate-50 border-b border-slate-200">
                                        <tr>
                                            <th class="px-5 py-3 text-left text-[10px] uppercase tracking-wider font-black text-slate-400">
                                                Produk
                                            </th>

                                            <th class="px-5 py-3 text-center text-[10px] uppercase tracking-wider font-black text-slate-400 w-32">
                                                Dikirim
                                            </th>

                                            <th class="px-5 py-3 text-center text-[10px] uppercase tracking-wider font-black text-emerald-600 w-40">
                                                Diterima
                                            </th>

                                            <th class="px-5 py-3 text-center text-[10px] uppercase tracking-wider font-black text-slate-400 w-32">
                                                Selisih
                                            </th>
                                        </tr>
                                    </thead>

                                    <tbody class="divide-y divide-slate-100">
                                        <tr
                                            v-for="item in checklistItems"
                                            :key="item.id"
                                            class="hover:bg-slate-50 transition"
                                        >
                                            <td class="px-5 py-4">
                                                <p class="text-sm font-bold text-slate-800">
                                                    {{ item.nama_produk }}
                                                </p>

                                                <p class="text-xs text-slate-400 mt-1">
                                                    {{ item.kemasan || '-' }}
                                                </p>

                                                <p
                                                    v-if="item.kode_produk"
                                                    class="text-[10px] font-mono text-slate-300 mt-1"
                                                >
                                                    {{ item.kode_produk }}
                                                </p>
                                            </td>

                                            <td class="px-5 py-4 text-center bg-slate-50/70">
                                                <span class="text-sm font-black text-slate-600">
                                                    {{ item.qty_kirim }}
                                                </span>
                                            </td>

                                            <td class="px-5 py-4">
                                                <div class="flex justify-center">
                                                    <input
                                                        type="number"
                                                        min="0"
                                                        step="1"
                                                        v-model.number="item.qty_terima"
                                                        @input="normalizeQty(item)"
                                                        class="w-28 bg-transparent border-0 border-b-2 text-center py-2 outline-none font-black transition"
                                                        :class="
                                                            Number(item.qty_terima) === Number(item.qty_kirim)
                                                                ? 'border-emerald-300 text-emerald-700 focus:border-emerald-500'
                                                                : 'border-orange-300 text-orange-700 focus:border-orange-500'
                                                        "
                                                    />
                                                </div>
                                            </td>

                                            <td class="px-5 py-4 text-center">
                                                <span
                                                    v-if="Number(item.qty_terima) === Number(item.qty_kirim)"
                                                    class="text-xs font-bold text-emerald-600"
                                                >
                                                    Sesuai
                                                </span>

                                                <span
                                                    v-else
                                                    class="text-xs font-bold text-orange-600"
                                                >
                                                    {{ Number(item.qty_terima || 0) - Number(item.qty_kirim || 0) }}
                                                </span>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <div class="border-t border-slate-200 bg-white">
                            <div
                                v-if="adaSelisih"
                                class="mx-5 mt-5 p-4 border border-orange-200 bg-orange-50 flex items-start gap-3"
                            >
                                <i class="pi pi-exclamation-triangle text-orange-500 mt-0.5"></i>

                                <div>
                                    <p class="text-sm font-bold text-orange-800">
                                        Terdapat selisih barang
                                    </p>

                                    <p class="text-xs text-orange-700 mt-1 leading-relaxed">
                                        Jumlah fisik yang diterima berbeda dengan jumlah yang dikirim. Sistem akan mencatat selisih tersebut.
                                    </p>
                                </div>
                            </div>

                            <div class="p-5">
                                <button
                                    type="button"
                                    @click="submitPenerimaan"
                                    :disabled="
                                        isLoading ||
                                        selectedDO?.status === 'SELESAI' ||
                                        checklistItems.length === 0
                                    "
                                    class="w-full h-14 bg-emerald-600 text-white font-black text-sm tracking-wide flex items-center justify-center gap-2 hover:bg-emerald-700 transition disabled:opacity-40 disabled:cursor-not-allowed"
                                >
                                    <i
                                        v-if="isLoading"
                                        class="pi pi-spin pi-spinner"
                                    ></i>

                                    <i
                                        v-else
                                        class="pi pi-check-circle"
                                    ></i>

                                    {{
                                        selectedDO?.status === 'SELESAI'
                                            ? 'SUDAH DITERIMA'
                                            : isLoading
                                                ? 'MEMPROSES...'
                                                : 'KONFIRMASI BARANG DITERIMA'
                                    }}
                                </button>
                            </div>
                        </div>
                    </template>
                </section>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { usePenerimaan } from '../composables/usePenerimaanBarang'

const errorPesan = ref('')
const selectedDO = ref(null)
const checklistItems = ref([])

const {
    doList,
    isLoading,
    fetchDO,
    prosesPenerimaan
} = usePenerimaan()

onMounted(() => {
    fetchDO()
})

const refreshData = async () => {
    errorPesan.value = ''
    await fetchDO()
}

const pilihDO = (kiriman) => {
    errorPesan.value = ''
    selectedDO.value = kiriman

    checklistItems.value = (kiriman.items || []).map(item => ({
        id: item.id,
        kode_produk: item.produk,
        nama_produk: item.produk_nama,
        kemasan: item.kemasan,
        qty_kirim: Number(item.unit_dikirim) || 0,
        qty_terima: Number(item.unit_dikirim) || 0
    }))
}

const normalizeQty = (item) => {
    const value = Number(item.qty_terima)

    item.qty_terima = Number.isFinite(value) && value >= 0
        ? Math.floor(value)
        : 0
}

const adaSelisih = computed(() => {
    return checklistItems.value.some(
        item => Number(item.qty_terima) !== Number(item.qty_kirim)
    )
})

const submitPenerimaan = async () => {
    if (!selectedDO.value) {
        return
    }

    errorPesan.value = ''

    checklistItems.value.forEach(item => {
        normalizeQty(item)
    })

    const payloadItems = checklistItems.value.map(item => ({
        id: item.id,
        unit_diterima: item.qty_terima
    }))

    const result = await prosesPenerimaan(
        selectedDO.value.id,
        payloadItems
    )

    if (result?.status === 'sukses') {
        selectedDO.value = null
        checklistItems.value = []
        await fetchDO()
        return
    }

    errorPesan.value =
        result?.pesan ||
        'Gagal memproses penerimaan.'
}
</script>

<style scoped>
.custom-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 transparent;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}
</style>
