<template>
    <div class="flex flex-col w-full animate-fade-in relative">
        <!-- HEADER -->
        <div class="mb-4 md:mb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4 md:gap-0">
            <div>
                <p class="text-xs text-slate-400 mb-1.5">
                    <router-link to="/" class="hover:text-slate-700 transition-colors">Dashboard</router-link> ›
                    <router-link to="/accounting/input/so" class="hover:text-slate-700 transition-colors">Input Entry</router-link> › Buat SO
                </p>
                <div class="flex items-center gap-3">
                    <h2 class="text-xl md:text-2xl font-black text-slate-800 tracking-tight">Create Sales Order</h2>
                    <span class="bg-blue-100 text-blue-700 text-[10px] font-bold px-2.5 py-1 rounded-md tracking-wide">PENJUALAN</span>
                </div>
            </div>
            <div class="flex flex-wrap items-center gap-2 w-full md:w-auto">
                <button type="button" @click="showModalCustomer = true" class="w-full md:w-auto justify-center px-4 py-2.5 md:py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition-colors flex items-center gap-2">
                    <i class="pi pi-user-plus text-sm"></i> Pelanggan Baru
                </button>
            </div>
        </div>

        <div v-if="pesanError" class="mb-5 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600 font-medium flex items-start gap-3 shadow-sm">
            <i class="pi pi-exclamation-triangle mt-0.5 text-lg"></i>
            <span>{{ pesanError }}</span>
        </div>

        <form @submit.prevent="kirim" class="bg-white border border-slate-200 rounded-[24px] p-4 md:p-8 shadow-[0_4px_20px_rgba(0,0,0,0.02)] w-full">
            
            <!-- Entitas -->
            <div class="flex flex-col md:flex-row md:items-center justify-between mb-6 border-b border-slate-100 pb-5 gap-4">
                <h3 class="text-sm md:text-base font-bold text-slate-800 flex items-center gap-2">
                    <i class="pi pi-building text-slate-400"></i> Entitas Penjual
                </h3>
                <div class="flex items-center bg-slate-100/80 p-1 rounded-xl border border-slate-200/60 w-full md:w-auto">
                    <button v-for="ent in listEntitas" :key="ent.id" type="button" @click="draf.entitas_id = ent.id" 
                        :class="['px-6 py-2.5 md:py-2 text-xs font-bold rounded-lg transition-all duration-300 flex-1 md:flex-none text-center', 
                        draf.entitas_id === ent.id ? 'bg-white text-blue-700 shadow-[0_2px_8px_rgba(0,0,0,0.08)] border border-slate-100' : 'text-slate-500 hover:text-slate-700 hover:bg-slate-200/50']">
                        {{ ent.kode }}
                    </button>
                </div>
            </div>

            <!-- Form Info -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-5 md:gap-6 mb-6">
                <div class="flex flex-col gap-2">
                    <label class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">No. SO (Preview)</label>
                    <input :value="previewNomor" type="text" readonly class="px-4 py-3 md:py-2.5 bg-slate-100/70 border border-slate-200 rounded-xl focus:outline-none text-sm text-slate-500 font-bold cursor-not-allowed" />
                </div>
                <div class="flex flex-col gap-2">
                    <label class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Tanggal Transaksi</label>
                    <input v-model="draf.tanggal" type="date" required class="px-4 py-3 md:py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-sm text-slate-800 font-medium transition-all" />
                </div>
                <div class="flex flex-col gap-2">
                    <label class="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Pelanggan</label>
                    <div class="relative">
                        <select v-model.number="draf.pelanggan_id" required class="w-full px-4 py-3 md:py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-sm text-slate-800 font-medium appearance-none transition-all">
                            <option value="" disabled>-- Pilih Pelanggan --</option>
                            <option v-for="plg in listPelanggan" :key="plg.id" :value="plg.id">
                                {{ plg.nama }}{{ plg.kota ? ` — ${plg.kota}` : '' }}
                            </option>
                        </select>
                        <i class="pi pi-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 text-xs pointer-events-none"></i>
                    </div>
                </div>
            </div>

            <!-- TABEL PEMBELIAN -->
            <div class="w-full mb-8">
                <div class="flex justify-between items-center mb-4 pb-3 mt-8 border-b border-slate-100">
                    <h3 class="text-sm md:text-base font-bold text-slate-800 flex items-center gap-2">
                        <i class="pi pi-box text-slate-400"></i> Rincian Pesanan
                    </h3>
                    <button type="button" @click="tambahItem" class="px-3 py-2 md:px-4 md:py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-bold rounded-xl transition-colors flex items-center gap-2 border border-blue-100">
                        <i class="pi pi-plus"></i> Tambah Item
                    </button>
                </div>

                <!-- 1. TAMPILAN DESKTOP (Tabel 100% Lurus & Rapih) -->
                <div class="hidden md:block w-full overflow-x-auto bg-slate-50/30 border border-slate-100 rounded-xl p-1">
                    <table class="w-full text-left">
                        <thead class="border-b border-slate-200">
                            <tr>
                                <th class="py-3 px-3 text-[11px] font-bold text-slate-500 uppercase tracking-wider w-[40%]">Barang (Stok Gudang)</th>
                                <th class="py-3 px-3 text-[11px] font-bold text-slate-500 uppercase tracking-wider w-[15%] text-right">Qty</th>
                                <th class="py-3 px-3 text-[11px] font-bold text-slate-500 uppercase tracking-wider w-[20%] text-right">Harga Jual</th>
                                <th class="py-3 px-3 text-[11px] font-bold text-slate-500 uppercase tracking-wider w-[20%] text-right">Subtotal</th>
                                <th class="py-3 px-3 w-[5%]"></th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 bg-white">
                            <tr v-for="(item, index) in draf.items" :key="index" class="hover:bg-slate-50/50 transition-colors">
                                
                                <!-- Dropdown Desktop -->
                                <td class="py-3 px-3 align-middle">
                                    <Dropdown v-model="item.produk" :options="listProduk" optionLabel="nama" placeholder="Pilih produk..." class="w-full" filter 
                                        :pt="{ root: { class: 'w-full h-[40px] bg-white border border-slate-200 rounded-lg flex items-center hover:border-blue-400' } }">
                                        <template #value="slotProps">
                                            <div v-if="slotProps.value" class="px-2 truncate">
                                                <span class="text-sm text-slate-800 font-semibold">{{ slotProps.value.nama }}</span>
                                            </div>
                                            <span v-else class="text-sm text-slate-400 px-2">{{ slotProps.placeholder }}</span>
                                        </template>
                                        <template #option="slotProps">
                                            <div class="flex flex-col py-0.5">
                                                <span class="text-sm font-bold text-slate-700">{{ slotProps.option.nama }}</span>
                                                <span class="text-[11px] font-semibold mt-0.5" :class="slotProps.option.stok > 0 ? 'text-emerald-600' : 'text-red-500'">
                                                    Stok: {{ slotProps.option.stok }} {{ slotProps.option.satuan_kode }}
                                                </span>
                                            </div>
                                        </template>
                                    </Dropdown>
                                </td>

                                <!-- Qty Desktop -->
                                <td class="py-3 px-3 align-middle relative">
                                    <input v-model.number="item.qty" type="number" min="0.01" step="0.01" required :max="item.produk?.stok" 
                                        :class="['w-full px-3 py-2 bg-white border rounded-lg text-sm font-semibold text-right focus:outline-none focus:ring-2 focus:ring-blue-500/50', 
                                        (item.produk && item.qty > item.produk.stok) ? 'border-red-400 text-red-600 bg-red-50' : 'border-slate-200 text-slate-800']" placeholder="0" />
                                    <!-- Peringatan Stok -->
                                    <span v-if="item.produk && item.qty > item.produk.stok" class="absolute -bottom-1 right-4 text-[10px] font-bold text-red-500 bg-white px-1 leading-none whitespace-nowrap">
                                        Stok tdk cukup!
                                    </span>
                                </td>

                                <!-- Harga Desktop -->
                                <td class="py-3 px-3 align-middle">
                                    <div class="relative w-full">
                                        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 font-bold text-sm">Rp</span>
                                        <input v-model.number="item.harga_jual" type="number" min="0" step="1" 
                                            class="w-full pl-9 pr-3 py-2 bg-white border border-slate-200 rounded-lg text-sm font-semibold text-right focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-slate-800" placeholder="0" />
                                    </div>
                                </td>

                                <!-- Subtotal Desktop -->
                                <td class="py-3 px-3 align-middle text-right">
                                    <span class="text-[15px] font-black text-slate-800">Rp {{ (subtotal(item)).toLocaleString('id-ID') }}</span>
                                </td>

                                <!-- Tombol Hapus Desktop -->
                                <td class="py-3 px-3 align-middle text-center">
                                    <button type="button" @click="hapusItem(index)" :disabled="draf.items.length === 1" 
                                        class="w-8 h-8 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 disabled:opacity-30 flex items-center justify-center mx-auto transition-colors">
                                        <i class="pi pi-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- 2. TAMPILAN MOBILE (- -) -->
                <div class="md:hidden flex flex-col gap-4">
                    <div v-for="(item, index) in draf.items" :key="index" class="p-4 border border-slate-200 rounded-2xl bg-white relative shadow-sm">
                        <!-- Tombol Hapus Pojok -->
                        <button type="button" @click="hapusItem(index)" :disabled="draf.items.length === 1" class="absolute top-3 right-3 w-8 h-8 rounded-lg bg-slate-50 text-slate-400 hover:text-red-500 flex items-center justify-center disabled:opacity-30">
                            <i class="pi pi-trash"></i>
                        </button>
                        
                        <!-- Baris 1: Produk -->
                        <div class="mb-4 pr-10">
                            <label class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1.5 block">Barang (Stok Gudang)</label>
                            <Dropdown v-model="item.produk" :options="listProduk" optionLabel="nama" placeholder="Pilih produk..." class="w-full" filter 
                                :pt="{ root: { class: 'w-full h-[42px] bg-slate-50 border border-slate-200 rounded-xl flex items-center' } }">
                                <template #value="slotProps">
                                    <div v-if="slotProps.value" class="px-2 truncate">
                                        <span class="text-sm text-slate-800 font-semibold">{{ slotProps.value.nama }}</span>
                                    </div>
                                    <span v-else class="text-sm text-slate-400 px-2">{{ slotProps.placeholder }}</span>
                                </template>
                                <template #option="slotProps">
                                    <div class="flex flex-col py-1">
                                        <span class="text-sm font-bold text-slate-700">{{ slotProps.option.nama }}</span>
                                        <span class="text-[11px] font-semibold mt-0.5" :class="slotProps.option.stok > 0 ? 'text-emerald-600' : 'text-red-500'">
                                            Stok: {{ slotProps.option.stok }} {{ slotProps.option.satuan_kode }}
                                        </span>
                                    </div>
                                </template>
                            </Dropdown>
                        </div>

                        <!-- Baris 2: Qty dan Harga Jual (Bersebelahan) -->
                        <div class="grid grid-cols-2 gap-3 mb-4">
                            <div class="relative">
                                <label class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1.5 block">Qty</label>
                                <input v-model.number="item.qty" type="number" min="0.01" step="0.01" required :max="item.produk?.stok" 
                                    :class="['w-full px-3 py-2.5 bg-slate-50 border rounded-xl text-sm font-semibold focus:outline-none focus:ring-2', (item.produk && item.qty > item.produk.stok) ? 'border-red-400 text-red-600' : 'border-slate-200 text-slate-800']" placeholder="0" />
                                <span v-if="item.produk && item.qty > item.produk.stok" class="absolute -bottom-4 left-0 text-[10px] font-bold text-red-500 whitespace-nowrap">Stok tdk cukup!</span>
                            </div>
                            <div>
                                <label class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1.5 block">Harga Jual</label>
                                <div class="relative">
                                    <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 font-bold text-sm">Rp</span>
                                    <input v-model.number="item.harga_jual" type="number" min="0" step="1" 
                                        class="w-full pl-9 pr-3 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm font-semibold text-right focus:outline-none text-slate-800" placeholder="0" />
                                </div>
                            </div>
                        </div>

                        <!-- Baris 3: Subtotal -->
                        <div class="flex justify-between items-center pt-3 border-t border-slate-100">
                            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Subtotal</span>
                            <span class="text-[15px] font-black text-slate-800">Rp {{ (subtotal(item)).toLocaleString('id-ID') }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer / Rekap -->
            <div class="flex flex-col md:flex-row justify-between items-start bg-slate-50 p-5 md:p-6 rounded-[20px] border border-slate-200/60 shadow-inner">
                <div class="flex flex-col gap-2 w-full md:w-auto mb-6 md:mb-0">
                    <label class="flex items-center gap-3 cursor-pointer group">
                        <div class="relative flex items-center">
                            <input type="checkbox" id="pakaiPpn" :true-value="11" :false-value="0" v-model="draf.ppn_persen" 
                                class="peer w-5 h-5 rounded border-slate-300 text-blue-600 focus:ring-blue-500 focus:ring-offset-slate-50 cursor-pointer transition-all">
                        </div>
                        <span class="text-sm font-bold text-slate-700 group-hover:text-blue-700 transition-colors select-none">Kenakan PPN 11% (PPN Keluaran)</span>
                    </label>
                    <div class="text-slate-500 text-[11px] font-medium flex items-center gap-1.5 ml-8">
                        <i class="pi pi-info-circle text-slate-400"></i> Opsional untuk Faktur Pajak.
                    </div>
                </div>

                <div class="flex flex-col w-full md:w-72 gap-2.5 border-t md:border-none border-slate-200/60 pt-5 md:pt-0">
                    <div class="flex justify-between items-center text-sm px-1">
                        <span class="font-bold text-slate-500">Subtotal</span>
                        <span class="font-black text-slate-700">Rp {{ (subtotalSemua).toLocaleString('id-ID') }}</span>
                    </div>
                    <div v-if="draf.ppn_persen > 0" class="flex justify-between items-center text-sm px-1 animate-fade-in">
                        <span class="font-bold text-blue-600">PPN (11%)</span>
                        <span class="font-black text-blue-700">Rp {{ (ppnNominal).toLocaleString('id-ID') }}</span>
                    </div>
                    <div class="flex justify-between items-end mt-2 pb-1 border-b border-slate-200/80 px-1">
                        <span class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-1.5">Total Tagihan</span>
                        <span class="text-2xl font-black text-slate-900 tracking-tight">Rp {{ (grandTotal).toLocaleString('id-ID') }}</span>
                    </div>
                    
                    <button type="submit" :disabled="sedangProses || periodeDitutup || hasErrorStok" 
                        class="mt-4 w-full justify-center px-6 py-3.5 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white font-bold rounded-xl shadow-[0_4px_15px_rgba(37,99,235,0.25)] hover:shadow-[0_6px_20px_rgba(37,99,235,0.4)] transition-all flex items-center gap-2 cursor-pointer disabled:cursor-not-allowed">
                        <i class="pi text-lg" :class="sedangProses ? 'pi-spin pi-spinner' : 'pi-check-circle'"></i>
                        {{ sedangProses ? 'Menyimpan SO...' : 'Simpan & Terbitkan' }}
                    </button>
                </div>
            </div>
        </form>

        <Teleport to="body">
            <CustomerForm v-if="showModalCustomer" @close="showModalCustomer = false" @saved="handleCustomerSaved" />
        </Teleport>
    </div>
</template>

<script setup>
import { reactive, computed, ref, watch, onMounted } from 'vue'
import Dropdown from 'primevue/dropdown'
import CustomerForm from './CustomerForm.vue'
import { useSalesOrder } from '@/features/accounting/composables/useSalesOrder'

const emit = defineEmits(['close', 'saved'])
const {
    listEntitas, listPelanggan, listProduk, sedangProses, pesanError, previewNomor,
    periodeDitutup, muatDataMaster, muatPreviewNomor, simpanSO, muatStokEntitas
} = useSalesOrder()

const showModalCustomer = ref(false)

const hariIni = () => {
    const t = new Date(Date.now() - new Date().getTimezoneOffset() * 60_000)
    return t.toISOString().slice(0, 10)
}

const itemKosong = () => ({ produk: null, qty: null, harga_jual: null })

const draf = reactive({
    entitas_id: '',
    pelanggan_id: '',
    tanggal: hariIni(),
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

watch([() => draf.entitas_id, () => draf.tanggal], async ([entitas, tanggal]) => {
    if (entitas && tanggal) {
        await muatPreviewNomor(entitas, tanggal)
    } else {
        previewNomor.value = 'Pilih entitas & tanggal'
    }
})

watch(() => draf.entitas_id, async (entitasBaru, entitasLama) => {
    if (entitasBaru !== entitasLama) {
        await muatStokEntitas(entitasBaru)
        draf.items = [itemKosong()]
    }
})

const handleCustomerSaved = async () => {
    showModalCustomer.value = false
    await muatDataMaster()
}

const subtotal = (item) => (Number(item.qty) || 0) * (Number(item.harga_jual) || 0)
const subtotalSemua = computed(() => draf.items.reduce((s, i) => s + subtotal(i), 0))
const ppnNominal = computed(() => subtotalSemua.value * (draf.ppn_persen / 100))
const grandTotal = computed(() => subtotalSemua.value + ppnNominal.value)

const hasErrorStok = computed(() => {
    return draf.items.some(i => i.produk && Number(i.qty) > i.produk.stok)
})

const tambahItem = () => draf.items.push(itemKosong())
const hapusItem = (i) => {
    if (draf.items.length > 1) draf.items.splice(i, 1)
}

const kirim = async () => {
    pesanError.value = ''
    const kosong = draf.items.some(i => !i.produk?.id || !(Number(i.qty) > 0))
    if (kosong) {
        pesanError.value = 'Setiap item butuh produk yang valid dan Qty minimal 1.'
        return
    }
    if (hasErrorStok.value) {
        pesanError.value = 'Terdapat item dengan jumlah pesanan melebihi ketersediaan stok.'
        return
    }
    const payload = {
        entitas: draf.entitas_id,
        pelanggan: draf.pelanggan_id,
        tanggal: draf.tanggal,
        catatan: draf.catatan,
        ppn_persen: draf.ppn_persen || 0,
        items: draf.items.map(i => ({
            produk: i.produk.id,
            qty: Number(i.qty) || 0,
            harga_jual: Number(i.harga_jual) || 0,
        })),
    }
    const hasil = await simpanSO(payload)
    if (hasil.success) {
        emit('saved')
    }
}
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>