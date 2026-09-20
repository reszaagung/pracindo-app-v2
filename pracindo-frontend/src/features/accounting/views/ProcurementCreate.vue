<template>
    <div class="flex flex-col w-full relative">
        <!-- Header -->
        <div class="mb-4 flex justify-between items-center gap-2 border-b border-slate-100 pb-4">
            <span class="bg-slate-100 text-slate-600 text-[10px] font-bold px-2.5 py-1 rounded-full tracking-wide">
                DRAFT
            </span>

            <div class="flex items-center gap-2">
                <button type="button" @click="showModalProduct = true"
                    class="px-3 py-1.5 border border-blue-200 bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-semibold rounded-lg transition-colors flex items-center gap-1.5">
                    <i class="pi pi-box text-xs"></i>
                    <span class="hidden sm:inline">Produk Baru</span><span class="sm:hidden">Produk</span>
                </button>

                <button type="button" @click="showModalSupplier = true"
                    class="px-3 py-1.5 border border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-semibold rounded-lg transition-colors flex items-center gap-1.5">
                    <i class="pi pi-users text-xs"></i>
                    <span class="hidden sm:inline">Suplier Baru</span><span class="sm:hidden">Suplier</span>
                </button>
            </div>
        </div>

        <!-- Toggle Jenis PO -->
        <div class="inline-flex items-center gap-1 p-1 mb-5 bg-slate-100 border border-slate-200 rounded-xl w-full sm:w-max">
            <button type="button" @click="jenisPo = 'BAHAN_BAKU'"
                :class="['flex-1 sm:flex-none justify-center px-4 py-1.5 text-xs font-semibold rounded-lg transition-all duration-200 flex items-center gap-1.5',
                    jenisPo === 'BAHAN_BAKU'
                        ? 'bg-white text-teal-700 shadow-sm border border-slate-200'
                        : 'text-slate-500 hover:text-slate-700']">
                <i class="pi pi-box text-xs"></i> Bahan Baku
            </button>
            <button type="button" @click="jenisPo = 'KEMASAN'"
                :class="['flex-1 sm:flex-none justify-center px-4 py-1.5 text-xs font-semibold rounded-lg transition-all duration-200 flex items-center gap-1.5',
                    jenisPo === 'KEMASAN'
                        ? 'bg-white text-blue-700 shadow-sm border border-slate-200'
                        : 'text-slate-500 hover:text-slate-700']">
                <i class="pi pi-shopping-bag text-xs"></i> Kemasan
            </button>
        </div>

        <div v-if="pesanError"
            class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-xs text-red-600 font-medium flex items-start gap-2">
            <i class="pi pi-exclamation-triangle mt-0.5 text-xs"></i>
            <span>{{ pesanError }}</span>
        </div>

        <form @submit.prevent="kirim" class="w-full">
            <!-- Entitas Pembeli -->
            <div class="flex flex-row items-center justify-between mb-5 border-b border-slate-100 pb-4 gap-2">
                <h3 class="text-sm font-bold text-slate-800">Entitas Pembeli</h3>
                <div class="inline-flex flex-wrap items-center bg-slate-100 p-1 rounded-xl border border-slate-200">
                    <button v-for="ent in listEntitas" :key="ent.id" type="button" @click="draf.entitas_id = ent.id"
                        :class="['px-3.5 py-1 text-xs font-semibold rounded-lg transition-all duration-200 text-center',
                            draf.entitas_id === ent.id
                                ? 'bg-white text-slate-800 shadow-sm border border-slate-200'
                                : 'text-slate-400 hover:text-slate-600']">
                        {{ ent.kode }}
                    </button>
                </div>
            </div>

            <!-- Baris field utama -->
            <div class="grid grid-cols-1 md:grid-cols-[1fr_0.8fr_1.3fr] gap-4 mb-6">
                <div class="flex flex-col gap-1.5">
                    <label class="text-xs font-semibold text-slate-600">No. PO (Preview)</label>
                    <input :value="previewNomor" type="text" readonly
                        class="w-full h-10 px-3 bg-slate-100 border border-slate-200 rounded-lg text-sm text-slate-500 font-medium cursor-not-allowed focus:outline-none" />
                </div>

                <div class="flex flex-col gap-1.5">
                    <label class="text-xs font-semibold text-slate-600">Tanggal PO</label>
                    <input v-model="draf.tanggal" type="date" required
                        class="w-full h-10 px-3 bg-white border border-slate-300 rounded-lg text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-teal-500/30 focus:border-teal-500 transition" />
                </div>

                <div class="flex flex-col gap-1.5">
                    <label class="text-xs font-semibold text-slate-600">Pilih Supplier</label>
                    <Select
                        v-model="draf.suplier_id"
                        :options="listSupplier"
                        optionLabel="nama"
                        optionValue="id"
                        filter
                        appendTo="body"
                        placeholder="-- Pilih Supplier --"
                        class="w-full"
                        :pt="{
                            root: { class: 'h-10 bg-white border border-slate-300 rounded-lg flex items-center w-full' },
                            input: { class: 'text-sm px-3 text-slate-700' },
                            trigger: { class: 'w-9 flex items-center justify-center text-slate-400' }
                        }">
                        <template #empty>
                            <div class="p-2 text-center text-slate-500 text-xs">Supplier tidak ditemukan.</div>
                        </template>
                    </Select>
                </div>
            </div>

            <!-- Item Pesanan -->
            <div class="w-full mb-6">
                <div class="flex justify-between items-center mb-3">
                    <h3 class="text-sm font-bold text-slate-800">
                        Item Pesanan
                        <span class="text-slate-400 font-normal">({{ jenisPo === 'BAHAN_BAKU' ? 'Bahan' : 'Kemasan' }})</span>
                    </h3>
                    <button type="button" @click="tambahItem"
                        class="px-3 py-1.5 border border-teal-200 bg-teal-50 hover:bg-teal-100 text-teal-700 text-xs font-semibold rounded-lg transition-colors flex items-center gap-1.5">
                        <i class="pi pi-plus text-xs"></i> Tambah
                    </button>
                </div>

                <!-- MOBILE -->
                <div class="block md:hidden space-y-3">
                    <div v-for="(item, index) in draf.items" :key="'m-' + index"
                        class="p-3 bg-slate-50 border border-slate-200 rounded-xl relative flex flex-col gap-3">

                        <div class="flex justify-between items-center border-b border-slate-200 pb-2">
                            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Item #{{ index + 1 }}</span>
                            <button type="button" @click="hapusItem(index)" :disabled="draf.items.length === 1"
                                class="text-red-500 hover:text-red-700 text-xs font-semibold disabled:opacity-30 flex items-center gap-1">
                                <i class="pi pi-trash text-xs"></i> Hapus
                            </button>
                        </div>

                        <div class="flex flex-col gap-1.5">
                            <label class="text-xs font-semibold text-slate-600">
                                {{ jenisPo === 'BAHAN_BAKU' ? 'Bahan Baku' : 'Kemasan' }}
                            </label>
                            <Dropdown v-model="item.produk" :options="produkBerdasarkanSuplier" optionLabel="label"
                                appendTo="body"
                                :placeholder="draf.suplier_id ? 'Pilih produk...' : 'Pilih supplier dulu'"
                                class="w-full" :disabled="!draf.suplier_id" filter :loading="loadingProduk"
                                :pt="{
                                    root: { class: 'w-full h-10 bg-white border border-slate-300 rounded-lg flex items-center' },
                                    input: { class: 'text-sm px-3 text-slate-700' },
                                    trigger: { class: 'w-9 flex items-center justify-center text-slate-400' }
                                }">
                            </Dropdown>
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                            <div class="flex flex-col gap-1.5">
                                <label class="text-xs font-semibold text-slate-600">
                                    {{ jenisPo === 'BAHAN_BAKU' ? 'Qty (Kg)' : 'Qty (Pcs)' }}
                                </label>
                                <input v-model.number="item.qty" type="number" min="0" step="0.01" required
                                    class="w-full h-10 px-3 bg-white border border-slate-300 rounded-lg text-sm text-right text-slate-800 font-medium focus:outline-none focus:ring-2 focus:ring-teal-500/30 focus:border-teal-500"
                                    placeholder="0" />
                            </div>
                            <div class="flex flex-col gap-1.5">
                                <label class="text-xs font-semibold text-slate-600">Harga Satuan</label>
                                <div class="relative h-10">
                                    <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 font-semibold text-xs">Rp</span>
                                    <input v-model.number="item.harga_per_kg" type="number" min="0" step="1"
                                        class="w-full h-full pl-8 pr-3 bg-white border border-slate-300 rounded-lg text-sm text-right text-slate-800 font-medium focus:outline-none focus:ring-2 focus:ring-teal-500/30 focus:border-teal-500"
                                        placeholder="0" />
                                </div>
                            </div>
                        </div>

                        <div class="flex justify-between items-center pt-2 border-t border-slate-200">
                            <span class="text-xs font-semibold text-slate-500">Subtotal Item:</span>
                            <span class="font-bold text-teal-700 text-sm">
                                Rp {{ (subtotal(item)).toLocaleString('id-ID') }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- DESKTOP (Tabel) -->
                <div class="hidden md:block overflow-x-auto custom-scrollbar rounded-xl border border-slate-200">
                    <table class="w-full text-left text-sm min-w-[680px]">
                        <thead class="text-slate-500 bg-slate-50 border-b border-slate-200">
                            <tr>
                                <th style="width: 44%;" class="py-2.5 px-3 font-semibold text-[11px] uppercase tracking-wide">
                                    {{ jenisPo === 'BAHAN_BAKU' ? 'Bahan Baku' : 'Kemasan' }}
                                </th>
                                <th style="width: 15%;" class="py-2.5 px-3 font-semibold text-right text-[11px] uppercase tracking-wide">
                                    {{ jenisPo === 'BAHAN_BAKU' ? 'Qty (Kg)' : 'Qty (Pcs)' }}
                                </th>
                                <th style="width: 18%;" class="py-2.5 px-3 font-semibold text-right text-[11px] uppercase tracking-wide">Harga</th>
                                <th style="width: 18%;" class="py-2.5 px-3 font-semibold text-right text-[11px] uppercase tracking-wide">Subtotal</th>
                                <th style="width: 5%;" class="py-2.5 px-3 font-semibold text-center text-[11px] uppercase tracking-wide">Aksi</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in draf.items" :key="'d-' + index"
                                class="bg-white border-b border-slate-100 last:border-0 hover:bg-slate-50/60 transition-colors">

                                <td class="py-2 px-3 align-middle">
                                    <Dropdown v-model="item.produk" :options="produkBerdasarkanSuplier" optionLabel="label"
                                        appendTo="body"
                                        :placeholder="draf.suplier_id ? 'Pilih produk...' : 'Pilih supplier'"
                                        class="w-full" :disabled="!draf.suplier_id" filter :loading="loadingProduk"
                                        :pt="{
                                            root: { class: 'w-full h-10 bg-white border border-slate-300 rounded-lg flex items-center' },
                                            input: { class: 'text-sm px-3 text-slate-700' },
                                            trigger: { class: 'w-9 flex items-center justify-center text-slate-400' }
                                        }">
                                    </Dropdown>
                                </td>

                                <td class="py-2 px-3 align-middle">
                                    <input v-model.number="item.qty" type="number" min="0" step="0.01" required
                                        class="w-full h-10 px-3 bg-white border border-slate-300 rounded-lg text-sm text-right text-slate-800 focus:outline-none focus:ring-2 focus:ring-teal-500/30 focus:border-teal-500"
                                        placeholder="0" />
                                </td>

                                <td class="py-2 px-3 align-middle">
                                    <div class="relative h-10">
                                        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 font-semibold text-xs">Rp</span>
                                        <input v-model.number="item.harga_per_kg" type="number" min="0" step="1"
                                            class="w-full h-full pl-8 pr-3 bg-white border border-slate-300 rounded-lg text-sm text-right text-slate-800 focus:outline-none focus:ring-2 focus:ring-teal-500/30 focus:border-teal-500"
                                            placeholder="0" />
                                    </div>
                                </td>

                                <td class="py-2 px-3 text-right align-middle">
                                    <span class="font-bold text-slate-800 text-sm">
                                        Rp {{ (subtotal(item)).toLocaleString('id-ID') }}
                                    </span>
                                </td>

                                <td class="py-2 px-3 text-center align-middle">
                                    <button type="button" @click="hapusItem(index)" :disabled="draf.items.length === 1"
                                        class="w-8 h-8 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 disabled:opacity-30 disabled:hover:bg-transparent transition-colors flex items-center justify-center mx-auto"
                                        title="Hapus">
                                        <i class="pi pi-times text-xs"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Footer / Total -->
            <div class="flex flex-col md:flex-row justify-between items-start gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
                <div class="flex items-center gap-2 w-full md:w-auto">
                    <input type="checkbox" id="pakaiPpn" :true-value="11" :false-value="0" v-model="draf.ppn_persen"
                        class="w-4 h-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500 cursor-pointer">
                    <label for="pakaiPpn" class="text-xs font-semibold text-slate-700 cursor-pointer select-none">
                        Kenakan PPN 11%
                    </label>
                </div>

                <div class="flex flex-col w-full md:w-64 gap-2 border-t md:border-none border-slate-200 pt-4 md:pt-0">
                    <div class="flex justify-between items-center text-xs">
                        <span class="font-semibold text-slate-500">Subtotal</span>
                        <span class="font-bold text-slate-700">Rp {{ (subtotalSemua).toLocaleString('id-ID') }}</span>
                    </div>

                    <div v-if="draf.ppn_persen > 0" class="flex justify-between items-center text-xs">
                        <span class="font-semibold text-teal-600">PPN (11%)</span>
                        <span class="font-bold text-teal-700">Rp {{ (ppnNominal).toLocaleString('id-ID') }}</span>
                    </div>

                    <div class="flex justify-between items-end mt-1 pt-2 border-t border-slate-200">
                        <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-0.5">Grand Total</span>
                        <span class="text-xl font-black text-slate-800">Rp {{ (grandTotal).toLocaleString('id-ID') }}</span>
                    </div>

                    <div class="flex gap-2 mt-3 w-full">
                        <button type="button" @click="$emit('close')"
                            class="flex-1 py-2.5 bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 font-semibold rounded-lg text-xs transition-all">
                            Batal
                        </button>
                        <button type="submit" :disabled="sedangProses || periodeDitutup"
                            class="flex-1 py-2.5 bg-teal-600 hover:bg-teal-700 disabled:bg-slate-400 text-white font-bold rounded-lg text-xs shadow-sm transition-all flex justify-center items-center gap-1.5 cursor-pointer disabled:cursor-not-allowed">
                            <i class="pi text-xs" :class="sedangProses ? 'pi-spin pi-spinner' : 'pi-check-circle'"></i>
                            Simpan
                        </button>
                    </div>
                </div>
            </div>
        </form>

        <SupplierForm v-if="showModalSupplier" @close="showModalSupplier = false" @saved="handleSupplierSaved" />
        <ProductEntry v-if="showModalProduct" @close="showModalProduct = false" @saved="handleProductSaved" />
    </div>
</template>

<script setup>
import { reactive, computed, ref, watch, onMounted } from 'vue'
import Dropdown from 'primevue/dropdown'
import Select from 'primevue/select'
import SupplierForm from '@/features/master/views/SupplierForm.vue'
import ProductEntry from '@/features/master/views/ProductEntry.vue'
import { usePurchaseOrder } from '@/features/accounting/composables/usePurchaseOrder'
import api from '@/utils/api'

const emit = defineEmits(['close', 'saved'])

const {
    listEntitas, listSupplier, sedangProses, pesanError, previewNomor,
    periodeDitutup, muatDataMaster, muatPreviewNomor, simpanPO, cekStatusPeriode
} = usePurchaseOrder()

const showModalSupplier = ref(false)
const showModalProduct = ref(false)
const produkBerdasarkanSuplier = ref([])
const loadingProduk = ref(false)
const jenisPo = ref('BAHAN_BAKU')

const hariIni = () => {
    const t = new Date(Date.now() - new Date().getTimezoneOffset() * 60_000)
    return t.toISOString().slice(0, 10)
}

const itemKosong = () => ({ produk: null, qty: null, harga_per_kg: null })

const draf = reactive({
    entitas_id: '',
    suplier_id: '',
    tanggal: hariIni(),
    tanggal_kirim_diminta: '',
    catatan: '',
    ppn_persen: 0,
    items: [itemKosong()],
})

onMounted(async () => {
    await muatDataMaster()
    previewNomor.value = 'Pilih entitas & tanggal'

    if (listEntitas.value.length > 0) {
        draf.entitas_id = listEntitas.value[0].id
    }
})

const handleSupplierSaved = async () => {
    showModalSupplier.value = false
    await muatDataMaster()
}

const handleProductSaved = async (produkBaru) => {
    showModalProduct.value = false
    if (draf.suplier_id) {
        await tarikProdukDariAPI(draf.suplier_id)

        const produkTerpilih = produkBerdasarkanSuplier.value.find(p => p.id === produkBaru.id)
        if (produkTerpilih) {
            const barisTerakhir = draf.items[draf.items.length - 1]
            if (!barisTerakhir.produk) {
                barisTerakhir.produk = produkTerpilih
            }
        }
    }
}

watch([() => draf.entitas_id, () => draf.tanggal], async ([entitas, tanggal]) => {
    if (entitas && tanggal) {
        await Promise.all([
            muatPreviewNomor(entitas, tanggal),
            cekStatusPeriode(entitas, tanggal)
        ])
    } else {
        previewNomor.value = 'Pilih entitas & tanggal'
        periodeDitutup.value = false
    }
})

const tarikProdukDariAPI = async (idSuplier) => {
    if (!idSuplier) {
        produkBerdasarkanSuplier.value = []
        return
    }

    loadingProduk.value = true
    try {
        const response = await api.get('master/produk/', {
            params: {
                suplier: idSuplier,
                jenis: jenisPo.value,
                aktif: true,
                ringkas: 1
            }
        })
        const hasil = response.data?.results || response.data || []

        produkBerdasarkanSuplier.value = hasil.map(p => ({ ...p, label: `${p.kode} - ${p.nama}` }))
    } catch (err) {
        console.error("Gagal menarik produk:", err)
    } finally {
        loadingProduk.value = false
    }
}

watch(() => jenisPo.value, async () => {
    draf.items = [itemKosong()]
    if (draf.suplier_id) {
        await tarikProdukDariAPI(draf.suplier_id)
    }
})

watch(() => draf.suplier_id, async (newVal, oldVal) => {
    if (oldVal && newVal !== oldVal) {
        draf.items = [itemKosong()]
    }
    await tarikProdukDariAPI(newVal)
}, { immediate: true })

const subtotal = (item) => (Number(item.qty) || 0) * (Number(item.harga_per_kg) || 0)
const subtotalSemua = computed(() => draf.items.reduce((s, i) => s + subtotal(i), 0))
const ppnNominal = computed(() => subtotalSemua.value * (draf.ppn_persen / 100))
const grandTotal = computed(() => subtotalSemua.value + ppnNominal.value)

const tambahItem = () => draf.items.push(itemKosong())
const hapusItem = (i) => {
    if (draf.items.length > 1) draf.items.splice(i, 1)
}

const kirim = async () => {
    if (periodeDitutup.value) return

    pesanError.value = ''
    const kosong = draf.items.some(i => !i.produk?.id || !(Number(i.qty) > 0))
    if (kosong) {
        alert('❌ Gagal: Setiap item butuh produk dan Qty minimal 1.')
        pesanError.value = 'Setiap item butuh produk (yang valid) dan Qty minimal 1.'
        return
    }

    const payload = {
        entitas_id: draf.entitas_id,
        suplier_id: draf.suplier_id,
        tanggal: draf.tanggal,
        tanggal_kirim_diminta: draf.tanggal_kirim_diminta || null,
        catatan: draf.catatan,
        pakai_ppn: draf.ppn_persen > 0,
        ppn_persen: draf.ppn_persen || 0,
        kategori_po: jenisPo.value,
        items: draf.items.map(i => {
            const idSatuan = i.produk.satuan?.id || i.produk.satuan_id || i.produk.satuan;
            return {
                produk_id: i.produk.id,
                qty_pesan: Number(i.qty) || 0,
                harga_per_kg: Number(i.harga_per_kg) || 0,
                satuan: idSatuan
            }
        }),
    }

    const hasil = await simpanPO(payload, true)

    if (hasil.success) {
        alert("✅ Berhasil! Purchase Order baru telah tersimpan.")
        emit('saved', hasil.data)
    } else {
        alert("❌ Gagal menyimpan PO:\n" + hasil.message)
        pesanError.value = hasil.message
    }
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
    height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 6px;
}
</style>