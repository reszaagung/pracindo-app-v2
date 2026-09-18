<template>
    <div class="max-w-7xl mx-auto pb-10 space-y-6 font-sans">

        <!-- HEADER POS -->
        <header
            class="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-slate-200 pb-4">
            
            <!-- Kiri: Tombol Back & Judul -->
            <div class="flex items-center gap-5">
                <!-- 👇 TOMBOL KEMBALI KE DASHBOARD 👇 -->
                <button @click="router.push('/dashboard')" 
                    class="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-white px-4 py-2.5 rounded-lg text-sm font-semibold transition-colors shadow-sm">
                    <i class="pi pi-arrow-left"></i> Dashboard
                </button>

                <div>
                    <p class="text-sm text-slate-500 mb-1">Retail / Point of Sale</p>
                    <h1 class="text-2xl font-bold text-slate-800">Mesin Kasir Utama</h1>
                </div>
            </div>

            <!-- Kanan: Search Bar Produk -->
            <div class="relative w-full md:w-72">
                <i class="pi pi-search absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400"></i>
                <input v-model="searchQuery" type="text" placeholder="Cari produk atau barcode..."
                    class="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-xl text-sm outline-none focus:border-blue-500 bg-white">
            </div>
        </header>

        <div class="flex flex-col lg:flex-row gap-6">

            <!-- ==========================================
           KIRI: KATALOG PRODUK (60%) 
      =========================================== -->
            <div
                class="w-full lg:w-3/5 bg-white rounded-[20px] shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col h-[calc(100vh-200px)] overflow-hidden">
                <div class="p-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
                    <h2 class="font-bold text-slate-700">Katalog Produk</h2>
                    <span class="text-xs font-semibold bg-blue-100 text-blue-700 px-2.5 py-1 rounded-md">{{
                        filteredProducts.length }} Item</span>
                </div>

                <div
                    class="flex-1 overflow-y-auto p-4 grid grid-cols-2 sm:grid-cols-3 gap-4 custom-scrollbar content-start">

                    <button v-for="item in filteredProducts" :key="item.id" @click="addToCart(item)"
                        :disabled="item.qty <= 0"
                        class="bg-white p-4 rounded-xl shadow-sm border border-slate-200 cursor-pointer hover:border-blue-500 hover:shadow-md transition-all text-left flex flex-col group disabled:opacity-50 disabled:cursor-not-allowed">
                        <div
                            class="h-16 bg-slate-50 rounded-lg mb-3 flex items-center justify-center text-slate-400 text-xs font-mono group-hover:bg-blue-50 transition-colors w-full border border-slate-100">
                            {{ item.kode_produk || 'SKU' }}
                        </div>
                        <p class="font-semibold text-sm text-slate-700 truncate w-full">{{ item.nama_produk || item.nama
                            }}</p>
                        <p class="text-blue-600 font-black mt-1 text-lg">Rp {{ (item.harga_jual || item.harga ||
                            0).toLocaleString('id-ID') }}</p>
                        <div class="mt-auto pt-3 flex justify-between items-center w-full">
                            <span class="text-xs text-slate-400 font-medium">Stok: {{ item.qty || item.stok || 0
                                }}</span>
                            <i class="pi pi-cart-plus text-slate-300 group-hover:text-blue-500"></i>
                        </div>
                    </button>

                </div>
            </div>

            <!-- ==========================================
           KANAN: KERANJANG & PEMBAYARAN (40%)
      =========================================== -->
            <div
                class="w-full lg:w-2/5 bg-white rounded-[20px] shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-slate-100 flex flex-col h-[calc(100vh-200px)] overflow-hidden">

                <!-- Header Keranjang -->
                <div class="p-4 border-b border-slate-100 bg-slate-50/50">
                    <h2 class="font-bold text-slate-700 flex items-center gap-2">
                        <i class="pi pi-shopping-bag text-blue-500"></i> Keranjang
                    </h2>
                </div>

                <!-- Daftar Barang di Keranjang (Scrollable) -->
                <div class="flex-1 overflow-y-auto p-4 custom-scrollbar bg-slate-50/30">
                    <div v-if="cart.length === 0" class="flex h-full flex-col items-center justify-center opacity-60">
                        <i class="pi pi-shopping-cart text-5xl mb-4 text-slate-300"></i>
                        <p class="text-slate-500 text-sm font-medium">Belum ada barang dipilih.</p>
                    </div>

                    <div v-else class="space-y-3">
                        <div v-for="(cartItem, index) in cart" :key="index"
                            class="flex flex-col bg-white border border-slate-200 p-3 rounded-xl shadow-sm">
                            <div class="flex justify-between items-start mb-2">
                                <p class="font-bold text-sm text-slate-800 pr-2">{{ cartItem.nama }}</p>
                                <button @click="hapusItem(index)" class="text-rose-400 hover:text-rose-600"><i
                                        class="pi pi-trash text-sm"></i></button>
                            </div>
                            <div class="flex justify-between items-end">
                                <p class="text-xs text-slate-500 font-medium">Rp {{
                                    cartItem.harga.toLocaleString('id-ID') }}</p>
                                <div
                                    class="flex items-center border border-slate-200 rounded-lg bg-slate-50 overflow-hidden shadow-inner">
                                    <button @click="decreaseQty(index)"
                                        class="text-rose-500 hover:bg-rose-100 px-3 py-1.5 transition-colors"><i
                                            class="pi pi-minus text-xs"></i></button>
                                    <span class="text-sm font-bold w-8 text-center text-slate-700">{{ cartItem.qty
                                        }}</span>
                                    <button @click="increaseQty(index)"
                                        class="text-blue-600 hover:bg-blue-100 px-3 py-1.5 transition-colors"><i
                                            class="pi pi-plus text-xs"></i></button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- AREA FORM: SALES VS END USER & PEMBAYARAN -->
                <div class="p-4 border-t border-slate-200 bg-white space-y-4 shadow-[0_-4px_15px_rgba(0,0,0,0.02)]">

                    <!-- 1. TOGLE TIPE PENJUALAN (End User vs Sales) -->
                    <div class="bg-slate-100 p-1 rounded-xl flex gap-1">
                        <button @click="tipePenjualan = 'END_USER'"
                            :class="tipePenjualan === 'END_USER' ? 'bg-white text-blue-600 shadow-sm font-bold' : 'text-slate-500 hover:text-slate-700 font-medium'"
                            class="flex-1 py-2 rounded-lg text-xs transition-all flex items-center justify-center gap-2">
                            <i class="pi pi-user"></i> End-User (Langsung)
                        </button>
                        <button @click="tipePenjualan = 'SALES'"
                            :class="tipePenjualan === 'SALES' ? 'bg-white text-blue-600 shadow-sm font-bold' : 'text-slate-500 hover:text-slate-700 font-medium'"
                            class="flex-1 py-2 rounded-lg text-xs transition-all flex items-center justify-center gap-2">
                            <i class="pi pi-briefcase"></i> Via Sales
                        </button>
                    </div>

                    <!-- 2. DROPDOWN DINAMIS (Berdasarkan Tipe) -->
                    <div class="space-y-3 p-3 bg-slate-50 border border-slate-100 rounded-xl">
                        <!-- Jika Via Sales, tampilkan pilihan Sales -->
                        <div v-if="tipePenjualan === 'SALES'">
                            <label class="block text-xs font-bold text-slate-600 mb-1">Nama Sales <span
                                    class="text-rose-500">*</span></label>
                            <select v-model="selectedSales"
                                class="w-full text-sm border border-slate-200 rounded-lg px-3 py-2 outline-none focus:border-blue-500 bg-white">
                                <option :value="null" disabled>-- Pilih Sales --</option>
                                <option v-for="s in salesList" :key="s.id" :value="s.id">{{ s.nama }}</option>
                            </select>
                        </div>

                        <!-- Pelanggan (Opsional untuk Tunai, Wajib untuk Tempo) -->
                        <div>
                            <label class="block text-xs font-bold text-slate-600 mb-1">
                                Data Pelanggan <span v-if="metodeBayar === 'TEMPO'" class="text-rose-500">* Wajib untuk
                                    Tempo</span>
                            </label>
                            <select v-model="selectedPelanggan"
                                class="w-full text-sm border border-slate-200 rounded-lg px-3 py-2 outline-none focus:border-blue-500 bg-white">
                                <option :value="null">-- Pelanggan Umum (Tanpa Nama) --</option>
                                <option v-for="p in pelangganList" :key="p.id" :value="p.id">{{ p.nama }}</option>
                            </select>
                        </div>
                    </div>

                    <!-- 3. METODE PEMBAYARAN -->
                    <div>
                        <label class="block text-xs font-bold text-slate-600 mb-2">Metode Bayar</label>
                        <div class="flex gap-2">
                            <button @click="metodeBayar = 'TUNAI'"
                                :class="metodeBayar === 'TUNAI' ? 'bg-emerald-500 text-white shadow-md border-emerald-600' : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'"
                                class="flex-1 py-2 border rounded-lg text-sm font-bold transition-all">TUNAI</button>
                            <button @click="metodeBayar = 'TEMPO'"
                                :class="metodeBayar === 'TEMPO' ? 'bg-orange-500 text-white shadow-md border-orange-600' : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'"
                                class="flex-1 py-2 border rounded-lg text-sm font-bold transition-all">TEMPO
                                (BON)</button>
                        </div>
                    </div>

                    <!-- 4. TOTAL & SUBMIT -->
                    <div class="pt-2">
                        <div class="flex justify-between items-end mb-3">
                            <span class="text-slate-500 font-bold text-sm">TOTAL TAGIHAN</span>
                            <span class="font-black text-slate-900 text-2xl tracking-tight">Rp {{
                                totalHarga.toLocaleString('id-ID') }}</span>
                        </div>

                        <button @click="prosesBayar" :disabled="isButtonDisabled"
                            class="w-full bg-blue-600 text-white font-black py-4 rounded-xl hover:bg-blue-700 active:scale-[0.98] transition-all shadow-lg shadow-blue-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100 flex items-center justify-center gap-2">
                            <i v-if="isLoading" class="pi pi-spin pi-spinner"></i>
                            <i v-else class="pi pi-check-circle"></i>
                            {{ isLoading ? 'MEMPROSES...' : 'BAYAR SEKARANG' }}
                        </button>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useRetail } from '../composables/useRetail'

const router = useRouter()
const { posProducts, isLoading, pelangganList, salesList, fetchPosProducts, fetchPelanggan, fetchSales, checkoutCart } = useRetail()

const searchQuery = ref('')
const cart = ref([])

const tipePenjualan = ref('END_USER')
const metodeBayar = ref('TUNAI')
const selectedPelanggan = ref(null)
const selectedSales = ref(null)

onMounted(() => {
    fetchPosProducts()
    fetchPelanggan()
    fetchSales()
})

// --- Logic UI ---
const filteredProducts = computed(() => {
    let data = Array.isArray(posProducts.value) ? posProducts.value : (posProducts.value?.results || [])
    if (searchQuery.value) {
        const key = searchQuery.value.toLowerCase()
        return data.filter(p => p.nama_produk?.toLowerCase().includes(key) || p.kode_produk?.toLowerCase().includes(key))
    }
    return data
})

const totalHarga = computed(() => cart.value.reduce((total, item) => total + (item.harga * item.qty), 0))

const isButtonDisabled = computed(() => {
    if (cart.value.length === 0) return true
    if (isLoading.value) return true
    if (metodeBayar.value === 'TEMPO' && !selectedPelanggan.value) return true
    if (tipePenjualan.value === 'SALES' && !selectedSales.value) return true
    return false
})

watch(tipePenjualan, (newVal) => {
    if (newVal === 'END_USER') {
        selectedSales.value = null
    }
})

// --- Logic Keranjang ---
const addToCart = (product) => {
    const pId = product.produk_id || product.id
    const pStok = product.qty || product.stok || 0
    const existing = cart.value.find(item => item.id === pId)

    if (existing) {
        if (existing.qty < pStok) existing.qty++
    } else {
        if (pStok > 0) {
            cart.value.push({
                id: pId,
                kemasan: product.kemasan_id || product.kemasan || null,
                nama: product.nama_produk || product.nama,
                harga: product.harga_jual || product.harga,
                stok: pStok,
                qty: 1
            })
        }
    }
}

const increaseQty = (index) => {
    const item = cart.value[index]
    if (item.qty < item.stok) item.qty++
}

const decreaseQty = (index) => {
    if (cart.value[index].qty > 1) {
        cart.value[index].qty--
    }
}

const hapusItem = (index) => {
    cart.value.splice(index, 1)
}

const prosesBayar = async () => {
    const payload = {
        subtotal: totalHarga.value,
        metode_bayar: metodeBayar.value,
        pelanggan_id: selectedPelanggan.value,
        sales_id: tipePenjualan.value === 'SALES' ? selectedSales.value : null,
        keranjang: cart.value.map(item => ({
            produk_id: item.id,
            kemasan_id: item.kemasan,
            qty_unit: item.qty,
            harga: item.harga
        }))
    }

    const result = await checkoutCart(payload)

    if (result.status === 'sukses') {
        alert(`Transaksi Berhasil!\nNomor Struk: ${result.nomor_struk}`)
        cart.value = []
        metodeBayar.value = 'TUNAI'
        tipePenjualan.value = 'END_USER'
        selectedPelanggan.value = null
        selectedSales.value = null
        fetchPosProducts()
    } else {
        alert(`Transaksi Gagal: ${result.pesan}`)
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