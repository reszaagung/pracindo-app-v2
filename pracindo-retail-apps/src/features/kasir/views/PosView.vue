<template>
    <div class="min-h-screen bg-slate-100 text-slate-800 font-sans">
        <div class="w-full max-w-[1700px] mx-auto p-4 lg:p-6">

            <header class="mb-5">
                <div class="bg-white border border-slate-200 shadow-sm">
                    <div
                        class="px-5 py-4 flex flex-col xl:flex-row xl:items-center xl:justify-between gap-4"
                    >
                        <div class="flex items-center gap-4">
                            <button
                                type="button"
                                @click="router.push('/dashboard')"
                                class="h-10 px-4 bg-slate-900 text-white flex items-center gap-2 text-sm font-semibold hover:bg-slate-800 transition"
                            >
                                <i class="pi pi-arrow-left text-xs"></i>
                                Dashboard
                            </button>

                            <div class="hidden sm:block h-8 w-px bg-slate-200"></div>

                            <div>
                                <div class="flex items-center gap-2">
                                    <span class="w-2 h-2 rounded-full bg-blue-600"></span>

                                    <span
                                        class="text-[10px] uppercase tracking-[0.2em] font-black text-slate-400"
                                    >
                                        Retail / Point of Sale
                                    </span>
                                </div>

                                <h1
                                    class="text-xl lg:text-2xl font-black tracking-tight text-slate-900 mt-1"
                                >
                                    Mesin Kasir
                                </h1>
                            </div>
                        </div>

                        <div class="w-full xl:w-[430px]">
                            <div class="relative">
                                <i
                                    class="pi pi-search absolute left-0 top-1/2 -translate-y-1/2 text-slate-400 text-sm"
                                ></i>

                                <input
                                    v-model="searchQuery"
                                    type="text"
                                    placeholder="Cari produk atau barcode..."
                                    class="w-full pl-7 pr-8 py-3 bg-transparent border-0 border-b-2 border-slate-200 focus:border-blue-600 focus:ring-0 outline-none text-sm font-medium placeholder:text-slate-400 transition"
                                />

                                <button
                                    v-if="searchQuery"
                                    type="button"
                                    @click="searchQuery = ''"
                                    class="absolute right-0 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-800 transition"
                                >
                                    <i class="pi pi-times text-xs"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <div
                class="grid grid-cols-1 xl:grid-cols-[minmax(0,1fr)_430px] gap-5 items-start"
            >
                <section
                    class="bg-white border border-slate-200 shadow-sm flex flex-col xl:h-[calc(100vh-155px)]"
                >
                    <div class="px-5 py-4 border-b border-slate-200">
                        <div class="flex items-center justify-between gap-4">
                            <div>
                                <p
                                    class="text-[10px] uppercase tracking-[0.18em] font-black text-slate-400"
                                >
                                    Product Catalog
                                </p>

                                <div class="flex items-center gap-3 mt-1">
                                    <h2 class="text-lg font-black text-slate-900">
                                        Katalog Produk
                                    </h2>

                                    <span
                                        class="min-w-7 h-7 px-2 bg-blue-50 text-blue-700 flex items-center justify-center text-xs font-black"
                                    >
                                        {{ filteredProducts.length }}
                                    </span>
                                </div>
                            </div>

                            <div
                                class="hidden md:flex items-center gap-2 text-[11px] font-medium text-slate-400"
                            >
                                <i class="pi pi-info-circle"></i>
                                Klik produk untuk menambahkan
                            </div>
                        </div>
                    </div>

                    <div class="flex-1 overflow-y-auto p-5 custom-scrollbar">
                        <div
                            v-if="isLoading && filteredProducts.length === 0"
                            class="min-h-[450px] flex items-center justify-center"
                        >
                            <div class="text-center">
                                <i class="pi pi-spin pi-spinner text-2xl text-blue-600"></i>

                                <p class="mt-3 text-sm font-medium text-slate-400">
                                    Memuat produk...
                                </p>
                            </div>
                        </div>

                        <div
                            v-else-if="filteredProducts.length === 0"
                            class="min-h-[450px] flex items-center justify-center"
                        >
                            <div class="text-center">
                                <div
                                    class="w-16 h-16 mx-auto mb-4 border border-dashed border-slate-300 flex items-center justify-center"
                                >
                                    <i class="pi pi-box text-xl text-slate-300"></i>
                                </div>

                                <p class="text-sm font-bold text-slate-600">
                                    Produk tidak ditemukan
                                </p>

                                <p class="text-xs text-slate-400 mt-1">
                                    Coba gunakan kata pencarian lain
                                </p>
                            </div>
                        </div>

                        <div
                            v-else
                            class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 2xl:grid-cols-5 gap-3"
                        >
                            <button
                                v-for="item in filteredProducts"
                                :key="item.id"
                                type="button"
                                @click="addToCart(item)"
                                :disabled="(item.qty || item.stok || 0) <= 0"
                                class="group min-w-0 text-left bg-white border border-slate-200 p-3 hover:border-blue-500 hover:shadow-md transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                            >
                                <div
                                    class="h-20 bg-slate-50 border border-slate-100 flex items-center justify-center group-hover:bg-blue-50 group-hover:border-blue-100 transition"
                                >
                                    <span
                                        class="text-[10px] font-mono font-black tracking-wider text-slate-400 group-hover:text-blue-500"
                                    >
                                        {{ item.kode_produk || 'SKU' }}
                                    </span>
                                </div>

                                <div class="pt-3">
                                    <p class="font-bold text-sm text-slate-800 truncate">
                                        {{ item.nama_produk || item.nama }}
                                    </p>

                                    <p class="text-blue-600 text-base font-black mt-1">
                                        Rp {{
                                            (
                                                item.harga_jual ||
                                                item.harga ||
                                                0
                                            ).toLocaleString('id-ID')
                                        }}
                                    </p>
                                </div>

                                <div
                                    class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between"
                                >
                                    <span
                                        class="text-[10px] font-semibold"
                                        :class="
                                            (item.qty || item.stok || 0) > 0
                                                ? 'text-slate-400'
                                                : 'text-rose-500'
                                        "
                                    >
                                        Stok: {{ item.qty || item.stok || 0 }}
                                    </span>

                                    <span
                                        class="w-7 h-7 border border-slate-200 flex items-center justify-center text-slate-400 group-hover:text-blue-600 group-hover:border-blue-500 transition"
                                    >
                                        <i class="pi pi-plus text-[10px]"></i>
                                    </span>
                                </div>
                            </button>
                        </div>
                    </div>
                </section>

                <aside
                    class="bg-white border border-slate-200 shadow-sm flex flex-col xl:h-[calc(100vh-155px)] xl:sticky xl:top-5"
                >
                    <div class="px-5 py-4 border-b border-slate-200">
                        <div class="flex items-center justify-between">
                            <div>
                                <p
                                    class="text-[10px] uppercase tracking-[0.18em] font-black text-slate-400"
                                >
                                    Current Order
                                </p>

                                <h2 class="text-lg font-black text-slate-900 mt-1">
                                    Keranjang
                                </h2>
                            </div>

                            <div
                                class="min-w-8 h-8 px-2 bg-slate-900 text-white flex items-center justify-center text-xs font-black"
                            >
                                {{ cart.length }}
                            </div>
                        </div>
                    </div>

                    <div class="flex-1 overflow-y-auto custom-scrollbar bg-slate-50/50">
                        <div
                            v-if="cart.length === 0"
                            class="h-full min-h-[260px] flex items-center justify-center px-6"
                        >
                            <div class="text-center">
                                <div
                                    class="w-16 h-16 mx-auto mb-4 border border-dashed border-slate-300 flex items-center justify-center"
                                >
                                    <i class="pi pi-shopping-cart text-xl text-slate-300"></i>
                                </div>

                                <p class="text-sm font-bold text-slate-500">
                                    Keranjang masih kosong
                                </p>

                                <p class="text-xs text-slate-400 mt-1">
                                    Pilih produk dari katalog
                                </p>
                            </div>
                        </div>

                        <div v-else class="divide-y divide-slate-200">
                            <div
                                v-for="(cartItem, index) in cart"
                                :key="index"
                                class="bg-white p-4"
                            >
                                <div class="flex gap-3">
                                    <div
                                        class="w-7 h-7 shrink-0 bg-slate-100 text-slate-500 flex items-center justify-center text-[10px] font-black"
                                    >
                                        {{ String(index + 1).padStart(2, '0') }}
                                    </div>

                                    <div class="flex-1 min-w-0">
                                        <div
                                            class="flex items-start justify-between gap-3"
                                        >
                                            <p
                                                class="font-bold text-sm text-slate-800 leading-snug"
                                            >
                                                {{ cartItem.nama }}
                                            </p>

                                            <button
                                                type="button"
                                                @click="hapusItem(index)"
                                                class="shrink-0 text-slate-300 hover:text-rose-500 transition"
                                            >
                                                <i class="pi pi-trash text-xs"></i>
                                            </button>
                                        </div>

                                        <p class="text-xs text-slate-400 mt-1">
                                            Rp {{
                                                cartItem.harga.toLocaleString('id-ID')
                                            }}
                                            / item
                                        </p>

                                        <div
                                            class="flex items-end justify-between gap-3 mt-3"
                                        >
                                            <div
                                                class="flex items-center border-b-2 border-slate-200"
                                            >
                                                <button
                                                    type="button"
                                                    @click="decreaseQty(index)"
                                                    class="w-7 h-7 text-slate-500 hover:text-rose-500 transition"
                                                >
                                                    <i class="pi pi-minus text-[9px]"></i>
                                                </button>

                                                <span
                                                    class="w-8 text-center text-sm font-black text-slate-800"
                                                >
                                                    {{ cartItem.qty }}
                                                </span>

                                                <button
                                                    type="button"
                                                    @click="increaseQty(index)"
                                                    class="w-7 h-7 text-slate-500 hover:text-blue-600 transition"
                                                >
                                                    <i class="pi pi-plus text-[9px]"></i>
                                                </button>
                                            </div>

                                            <p
                                                class="font-black text-sm text-slate-900"
                                            >
                                                Rp {{
                                                    (
                                                        cartItem.harga *
                                                        cartItem.qty
                                                    ).toLocaleString('id-ID')
                                                }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="border-t border-slate-200 bg-white">
                        <div class="p-5 space-y-5">
                            <div>
                                <p
                                    class="text-[10px] uppercase tracking-[0.18em] font-black text-slate-400 mb-2"
                                >
                                    Tipe Penjualan
                                </p>

                                <div
                                    class="grid grid-cols-2 border-b-2 border-slate-200"
                                >
                                    <button
                                        type="button"
                                        @click="tipePenjualan = 'END_USER'"
                                        :class="
                                            tipePenjualan === 'END_USER'
                                                ? 'text-blue-600 border-b-2 border-blue-600'
                                                : 'text-slate-400'
                                        "
                                        class="py-2.5 -mb-[2px] text-xs font-black flex items-center justify-center gap-2 transition"
                                    >
                                        <i class="pi pi-user text-[10px]"></i>
                                        End User
                                    </button>

                                    <button
                                        type="button"
                                        @click="tipePenjualan = 'SALES'"
                                        :class="
                                            tipePenjualan === 'SALES'
                                                ? 'text-blue-600 border-b-2 border-blue-600'
                                                : 'text-slate-400'
                                        "
                                        class="py-2.5 -mb-[2px] text-xs font-black flex items-center justify-center gap-2 transition"
                                    >
                                        <i
                                            class="pi pi-briefcase text-[10px]"
                                        ></i>
                                        Via Sales
                                    </button>
                                </div>
                            </div>

                            <div v-if="tipePenjualan === 'SALES'">
                                <label
                                    class="block text-[10px] uppercase tracking-[0.14em] font-black text-slate-400 mb-1"
                                >
                                    Sales
                                    <span class="text-rose-500">*</span>
                                </label>

                                <div class="relative">
                                    <select
                                        v-model="selectedSales"
                                        class="w-full appearance-none bg-transparent border-0 border-b-2 border-slate-200 focus:border-blue-600 focus:ring-0 outline-none py-2.5 pr-7 text-sm font-semibold text-slate-700 transition"
                                    >
                                        <option :value="null" disabled>
                                            Pilih Sales
                                        </option>

                                        <option
                                            v-for="s in salesList"
                                            :key="s.id"
                                            :value="s.id"
                                        >
                                            {{ s.nama }}
                                        </option>
                                    </select>

                                    <i
                                        class="pi pi-chevron-down absolute right-0 top-1/2 -translate-y-1/2 text-[9px] text-slate-400 pointer-events-none"
                                    ></i>
                                </div>
                            </div>

                            <div>
                                <label
                                    class="block text-[10px] uppercase tracking-[0.14em] font-black text-slate-400 mb-1"
                                >
                                    Pelanggan

                                    <span
                                        v-if="metodeBayar === 'TEMPO'"
                                        class="text-rose-500"
                                    >
                                        * Wajib Tempo
                                    </span>
                                </label>

                                <div class="relative">
                                    <select
                                        v-model="selectedPelanggan"
                                        class="w-full appearance-none bg-transparent border-0 border-b-2 border-slate-200 focus:border-blue-600 focus:ring-0 outline-none py-2.5 pr-7 text-sm font-semibold text-slate-700 transition"
                                    >
                                        <option :value="null">
                                            Pelanggan Umum
                                        </option>

                                        <option
                                            v-for="p in pelangganList"
                                            :key="p.id"
                                            :value="p.id"
                                        >
                                            {{ p.nama }}
                                        </option>
                                    </select>

                                    <i
                                        class="pi pi-chevron-down absolute right-0 top-1/2 -translate-y-1/2 text-[9px] text-slate-400 pointer-events-none"
                                    ></i>
                                </div>
                            </div>

                            <div>
                                <p
                                    class="text-[10px] uppercase tracking-[0.18em] font-black text-slate-400 mb-2"
                                >
                                    Metode Pembayaran
                                </p>

                                <div class="grid grid-cols-2 gap-3">
                                    <button
                                        type="button"
                                        @click="metodeBayar = 'TUNAI'"
                                        :class="
                                            metodeBayar === 'TUNAI'
                                                ? 'border-blue-600 text-blue-600 bg-blue-50'
                                                : 'border-slate-200 text-slate-500 hover:border-slate-300'
                                        "
                                        class="py-3 border text-xs font-black transition"
                                    >
                                        TUNAI
                                    </button>

                                    <button
                                        type="button"
                                        @click="metodeBayar = 'TEMPO'"
                                        :class="
                                            metodeBayar === 'TEMPO'
                                                ? 'border-orange-500 text-orange-600 bg-orange-50'
                                                : 'border-slate-200 text-slate-500 hover:border-slate-300'
                                        "
                                        class="py-3 border text-xs font-black transition"
                                    >
                                        TEMPO / BON
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div
                            class="px-5 py-4 border-t border-slate-200 bg-slate-50"
                        >
                            <div
                                class="flex items-end justify-between gap-4"
                            >
                                <div>
                                    <p
                                        class="text-[10px] uppercase tracking-[0.18em] font-black text-slate-400"
                                    >
                                        Total Tagihan
                                    </p>

                                    <p class="text-xs text-slate-400 mt-1">
                                        {{ cart.length }} item
                                    </p>
                                </div>

                                <p
                                    class="text-2xl font-black tracking-tight text-slate-900"
                                >
                                    Rp {{ totalHarga.toLocaleString('id-ID') }}
                                </p>
                            </div>
                        </div>

                        <div class="p-5 pt-3">
                            <button
                                type="button"
                                @click="prosesBayar"
                                :disabled="isButtonDisabled"
                                class="w-full h-14 bg-slate-900 text-white font-black text-sm tracking-wide flex items-center justify-center gap-2 hover:bg-blue-600 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
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
                                    isLoading
                                        ? 'MEMPROSES...'
                                        : 'BAYAR SEKARANG'
                                }}
                            </button>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useRetail } from '../composables/useRetail'

const router = useRouter()

const {
    posProducts,
    isLoading,
    pelangganList,
    salesList,
    fetchPosProducts,
    fetchPelanggan,
    fetchSales,
    checkoutCart
} = useRetail()

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

const filteredProducts = computed(() => {
    const data = Array.isArray(posProducts.value)
        ? posProducts.value
        : (posProducts.value?.results || [])

    const key = searchQuery.value.trim().toLowerCase()

    if (!key) {
        return data
    }

    return data.filter(product =>
        product.nama_produk?.toLowerCase().includes(key) ||
        product.nama?.toLowerCase().includes(key) ||
        product.kode_produk?.toLowerCase().includes(key)
    )
})

const totalHarga = computed(() => {
    return cart.value.reduce(
        (total, item) => total + (item.harga * item.qty),
        0
    )
})

const isButtonDisabled = computed(() => {
    if (cart.value.length === 0) {
        return true
    }

    if (isLoading.value) {
        return true
    }

    if (
        metodeBayar.value === 'TEMPO' &&
        !selectedPelanggan.value
    ) {
        return true
    }

    if (
        tipePenjualan.value === 'SALES' &&
        !selectedSales.value
    ) {
        return true
    }

    return false
})

watch(tipePenjualan, (newValue) => {
    if (newValue === 'END_USER') {
        selectedSales.value = null
    }
})

const addToCart = (product) => {
    const productId = product.produk_id || product.id
    const stock = product.qty || product.stok || 0

    const existing = cart.value.find(
        item => item.id === productId
    )

    if (existing) {
        if (existing.qty < stock) {
            existing.qty++
        }

        return
    }

    if (stock <= 0) {
        return
    }

    cart.value.push({
        id: productId,
        kemasan: product.kemasan_id || product.kemasan || null,
        nama: product.nama_produk || product.nama,
        harga: product.harga_jual || product.harga || 0,
        stok: stock,
        qty: 1
    })
}

const increaseQty = (index) => {
    const item = cart.value[index]

    if (!item) {
        return
    }

    if (item.qty < item.stok) {
        item.qty++
    }
}

const decreaseQty = (index) => {
    const item = cart.value[index]

    if (!item) {
        return
    }

    if (item.qty > 1) {
        item.qty--
    }
}

const hapusItem = (index) => {
    cart.value.splice(index, 1)
}

const prosesBayar = async () => {
    if (isButtonDisabled.value) {
        return
    }

    const payload = {
        subtotal: totalHarga.value,
        metode_bayar: metodeBayar.value,
        pelanggan_id: selectedPelanggan.value,
        sales_id:
            tipePenjualan.value === 'SALES'
                ? selectedSales.value
                : null,
        keranjang: cart.value.map(item => ({
            produk_id: item.id,
            kemasan_id: item.kemasan,
            qty_unit: item.qty,
            harga: item.harga
        }))
    }

    const result = await checkoutCart(payload)

    if (result?.status === 'sukses') {
        alert(
            `Transaksi Berhasil!\nNomor Struk: ${result.nomor_struk}`
        )

        cart.value = []
        metodeBayar.value = 'TUNAI'
        tipePenjualan.value = 'END_USER'
        selectedPelanggan.value = null
        selectedSales.value = null

        await fetchPosProducts()

        return
    }

    alert(
        `Transaksi Gagal: ${
            result?.pesan || 'Terjadi kesalahan'
        }`
    )
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
