<template>
    <div class="w-full">
        <form
            @submit.prevent="simpanDelivery"
            class="flex flex-col gap-5 sm:gap-6"
            :aria-busy="sedangProses || sedangMemuat"
        >
            <div
                v-if="sedangMemuat"
                class="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm"
            >
                <div
                    class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100"
                    aria-hidden="true"
                >
                    <i class="pi pi-spin pi-spinner text-sm text-slate-500"></i>
                </div>

                <div class="min-w-0">
                    <p class="text-xs font-bold text-slate-700">
                        Memuat data delivery
                    </p>

                    <p class="mt-0.5 text-[11px] font-medium text-slate-400">
                        Menyiapkan Sales Order dan armada...
                    </p>
                </div>
            </div>

            <div
                v-if="errorMessage"
                class="flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-red-700"
                role="alert"
            >
                <div
                    class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-red-100"
                    aria-hidden="true"
                >
                    <i class="pi pi-exclamation-triangle text-sm"></i>
                </div>

                <div class="min-w-0 flex-1">
                    <p class="text-xs font-bold">
                        Gagal memuat data
                    </p>

                    <p class="mt-0.5 text-[11px] font-medium text-red-600">
                        {{ errorMessage }}
                    </p>
                </div>

                <button
                    type="button"
                    class="shrink-0 rounded-lg px-2 py-1 text-[11px] font-bold text-red-700 transition hover:bg-red-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500"
                    @click="muatDataMaster"
                >
                    Coba lagi
                </button>
            </div>

            <div
                v-if="successMessage"
                class="flex items-start gap-3 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-emerald-700 shadow-sm"
                role="status"
                aria-live="polite"
            >
                <div
                    class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-emerald-100"
                    aria-hidden="true"
                >
                    <i class="pi pi-check text-sm text-emerald-600"></i>
                </div>

                <div class="min-w-0">
                    <p class="text-xs font-extrabold">
                        Berhasil
                    </p>

                    <p class="mt-0.5 text-[11px] font-medium text-emerald-600">
                        {{ successMessage }}
                    </p>
                </div>
            </div>

            <div class="grid grid-cols-1 gap-4 lg:grid-cols-2 lg:gap-6">
                <div class="flex flex-col gap-4">
                    <div
                        class="group rounded-2xl border border-slate-200 bg-slate-50 p-4 shadow-sm transition-colors focus-within:border-slate-300 focus-within:bg-white"
                    >
                        <label
                            for="tanggal-pengiriman"
                            class="mb-2 block text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                        >
                            Tanggal Pengiriman
                        </label>

                        <div class="flex items-center gap-3">
                            <div
                                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-slate-500 shadow-sm"
                                aria-hidden="true"
                            >
                                <i class="pi pi-calendar text-sm"></i>
                            </div>

                            <input
                                id="tanggal-pengiriman"
                                v-model="form.tanggal"
                                type="date"
                                required
                                class="min-w-0 flex-1 bg-transparent text-sm font-bold text-slate-800 outline-none"
                            />
                        </div>
                    </div>

                    <div
                        class="rounded-2xl border border-blue-200 bg-gradient-to-br from-blue-50 to-white p-4 shadow-sm transition-colors focus-within:border-blue-300"
                    >
                        <label
                            for="sales-order"
                            class="mb-2 block text-[10px] font-extrabold uppercase tracking-[0.08em] text-blue-600"
                        >
                            Pilih Sales Order
                            <span class="text-blue-400">
                                · Disetujui
                            </span>
                        </label>

                        <div class="flex items-center gap-3">
                            <div
                                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-100 text-blue-600"
                                aria-hidden="true"
                            >
                                <i class="pi pi-file-check text-sm"></i>
                            </div>

                            <select
                                id="sales-order"
                                v-model="form.sales_order_id"
                                required
                                :disabled="sedangMemuat || sedangProses"
                                class="min-w-0 flex-1 cursor-pointer appearance-none bg-transparent text-sm font-bold text-slate-800 outline-none disabled:cursor-not-allowed disabled:opacity-60"
                                @change="pilihSO"
                            >
                                <option value="" disabled>
                                    -- Pilih Dokumen SO --
                                </option>

                                <option
                                    v-for="so in daftarSO"
                                    :key="so.id"
                                    :value="so.id"
                                >
                                    {{ so.nomor_so }} -
                                    {{ so.pelanggan_nama }}
                                </option>
                            </select>

                            <i
                                class="pi pi-chevron-down text-[11px] text-blue-400"
                                aria-hidden="true"
                            ></i>
                        </div>

                        <p
                            v-if="!sedangMemuat && daftarSO.length === 0"
                            class="mt-2 pl-12 text-[11px] font-medium text-slate-400"
                        >
                            Belum ada Sales Order yang disetujui.
                        </p>
                    </div>
                </div>

                <div class="flex flex-col gap-4">
                    <div
                        class="flex min-h-[94px] flex-col justify-center rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"
                        :class="soTerpilih ? '' : 'opacity-80'"
                    >
                        <div class="flex items-center justify-between gap-3">
                            <label
                                class="block text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400"
                            >
                                Informasi Customer
                            </label>

                            <span
                                v-if="soTerpilih"
                                class="rounded-full bg-emerald-50 px-2 py-1 text-[9px] font-extrabold uppercase tracking-wide text-emerald-600"
                            >
                                SO Dipilih
                            </span>
                        </div>

                        <div
                            v-if="soTerpilih"
                            class="mt-2 flex min-w-0 items-center gap-3"
                        >
                            <div
                                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
                                aria-hidden="true"
                            >
                                <i class="pi pi-building text-sm"></i>
                            </div>

                            <div class="min-w-0">
                                <p class="truncate text-sm font-extrabold text-slate-700">
                                    {{ soTerpilih.pelanggan_nama }}
                                </p>

                                <p
                                    v-if="soTerpilih.nomor_so"
                                    class="mt-0.5 truncate text-[10px] font-medium text-slate-400"
                                >
                                    {{ soTerpilih.nomor_so }}
                                </p>
                            </div>
                        </div>

                        <div
                            v-else
                            class="mt-2 flex items-center gap-2 text-xs font-medium italic text-slate-400"
                        >
                            <i
                                class="pi pi-info-circle text-xs"
                                aria-hidden="true"
                            ></i>

                            <span>Pilih SO terlebih dahulu</span>
                        </div>
                    </div>

                    <div
                        class="rounded-2xl border border-slate-200 bg-slate-50 p-4 shadow-sm transition-colors focus-within:border-slate-300 focus-within:bg-white"
                    >
                        <label
                            for="armada"
                            class="mb-2 block text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                        >
                            Armada / Kendaraan
                        </label>

                        <div class="flex items-center gap-3">
                            <div
                                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-slate-500 shadow-sm"
                                aria-hidden="true"
                            >
                                <i class="pi pi-truck text-sm"></i>
                            </div>

                            <select
                                id="armada"
                                v-model="form.kendaraan_id"
                                :disabled="sedangMemuat || sedangProses"
                                class="min-w-0 flex-1 cursor-pointer appearance-none bg-transparent text-sm font-bold text-slate-800 outline-none disabled:cursor-not-allowed disabled:opacity-60"
                            >
                                <option value="">
                                    -- Bebas (Ditentukan Kemudian) --
                                </option>

                                <option
                                    v-for="armada in daftarArmada"
                                    :key="armada.id"
                                    :value="armada.id"
                                >
                                    {{ armada.plat_nomor }} -
                                    {{ armada.nama }}
                                </option>
                            </select>

                            <i
                                class="pi pi-chevron-down text-[11px] text-slate-400"
                                aria-hidden="true"
                            ></i>
                        </div>
                    </div>
                </div>
            </div>

            <section
                v-if="soTerpilih"
                class="mt-1 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
                aria-labelledby="rincian-barang-title"
            >
                <div
                    class="flex flex-col gap-3 border-b border-slate-200 bg-slate-50/80 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-5"
                >
                    <div class="min-w-0">
                        <div class="flex items-center gap-2">
                            <div
                                class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-900 text-white"
                                aria-hidden="true"
                            >
                                <i class="pi pi-box text-xs"></i>
                            </div>

                            <div class="min-w-0">
                                <h3
                                    id="rincian-barang-title"
                                    class="truncate text-sm font-extrabold text-slate-700"
                                >
                                    Rincian Barang
                                </h3>

                                <p class="mt-0.5 text-[10px] font-medium text-slate-400">
                                    Berdasarkan Sales Order terpilih
                                </p>
                            </div>
                        </div>
                    </div>

                    <div
                        class="self-start rounded-full bg-white px-3 py-1.5 text-[10px] font-extrabold text-slate-500 shadow-sm ring-1 ring-slate-200 sm:self-auto"
                    >
                        {{ soTerpilih.items?.length || 0 }} Produk
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full min-w-[620px] border-collapse text-left">
                        <thead>
                            <tr class="border-b border-slate-200 bg-white">
                                <th
                                    class="w-16 px-4 py-3 text-center text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400 sm:px-5"
                                >
                                    No
                                </th>

                                <th
                                    class="px-4 py-3 text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400 sm:px-5"
                                >
                                    Nama Produk
                                </th>

                                <th
                                    class="w-36 px-4 py-3 text-right text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-400 sm:px-5"
                                >
                                    Qty Pesanan
                                </th>
                            </tr>
                        </thead>

                        <tbody class="divide-y divide-slate-100">
                            <tr
                                v-for="(item, index) in soTerpilih.items || []"
                                :key="item.id || `${index}-${item.produk_nama}`"
                                class="transition-colors hover:bg-slate-50/70"
                            >
                                <td
                                    class="px-4 py-4 text-center text-xs font-bold text-slate-400 sm:px-5"
                                >
                                    {{ String(index + 1).padStart(2, '0') }}
                                </td>

                                <td class="px-4 py-4 sm:px-5">
                                    <div class="flex min-w-0 items-center gap-3">
                                        <div
                                            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
                                            aria-hidden="true"
                                        >
                                            <i class="pi pi-box text-xs"></i>
                                        </div>

                                        <div class="min-w-0">
                                            <p class="truncate text-sm font-bold text-slate-800">
                                                {{ item.produk_nama }}
                                            </p>

                                            <p
                                                v-if="item.satuan_kode"
                                                class="mt-0.5 text-[10px] font-medium text-slate-400"
                                            >
                                                Satuan {{ item.satuan_kode }}
                                            </p>
                                        </div>
                                    </div>
                                </td>

                                <td class="px-4 py-4 text-right sm:px-5">
                                    <span class="text-sm font-extrabold text-blue-600">
                                        {{ item.qty }}
                                    </span>

                                    <span class="ml-1 text-xs font-semibold text-slate-400">
                                        {{ item.satuan_kode }}
                                    </span>
                                </td>
                            </tr>

                            <tr v-if="!soTerpilih.items?.length">
                                <td
                                    colspan="3"
                                    class="px-5 py-10 text-center"
                                >
                                    <div class="flex flex-col items-center">
                                        <div
                                            class="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-slate-400"
                                            aria-hidden="true"
                                        >
                                            <i class="pi pi-box text-lg"></i>
                                        </div>

                                        <p class="mt-3 text-xs font-bold text-slate-600">
                                            Tidak ada rincian barang
                                        </p>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <div
                class="flex flex-col-reverse gap-3 pt-1 sm:flex-row sm:items-center sm:justify-end"
            >
                <button
                    type="button"
                    :disabled="sedangProses"
                    class="w-full rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-600 shadow-sm transition-all hover:border-slate-300 hover:bg-slate-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
                    @click="router.push('/distribusi')"
                >
                    Batal
                </button>

                <button
                    type="submit"
                    :disabled="sedangProses || sedangMemuat || !soTerpilih"
                    :aria-busy="sedangProses"
                    class="group flex w-full items-center justify-center gap-2 rounded-xl bg-slate-900 px-6 py-3 text-sm font-extrabold text-white shadow-lg shadow-slate-900/10 transition-all hover:-translate-y-0.5 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:translate-y-0 active:scale-[0.99] disabled:cursor-not-allowed disabled:translate-y-0 disabled:bg-slate-300 disabled:shadow-none sm:w-auto sm:px-8"
                >
                    <i
                        v-if="sedangProses"
                        class="pi pi-spin pi-spinner text-sm"
                        aria-hidden="true"
                    ></i>

                    <i
                        v-else
                        class="pi pi-send text-sm transition-transform duration-200 group-hover:translate-x-0.5"
                        aria-hidden="true"
                    ></i>

                    <span>
                        {{
                            sedangProses
                                ? 'Memproses...'
                                : 'Kirim Request Delivery'
                        }}
                    </span>
                </button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiDistribusi } from '@/features/distribusi/api'
import api from '@/utils/api'

const router = useRouter()

const sedangProses = ref(false)
const sedangMemuat = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const daftarSO = ref([])
const daftarArmada = ref([])
const soTerpilih = ref(null)

const form = reactive({
    tanggal: new Date().toISOString().split('T')[0],
    sales_order_id: '',
    kendaraan_id: ''
})

const normalisasiList = (data) => {
    if (Array.isArray(data)) {
        return data
    }

    if (Array.isArray(data?.results)) {
        return data.results
    }

    if (Array.isArray(data?.data)) {
        return data.data
    }

    return []
}

const muatDataMaster = async () => {
    if (sedangMemuat.value) return

    sedangMemuat.value = true
    errorMessage.value = ''
    successMessage.value = ''

    try {
        const [resArmada, resSO] = await Promise.all([
            apiDistribusi.getArmada(),
            api.get(
                'sales_order/sales-order/',
                {
                    params: {
                        status: 'DISETUJUI'
                    }
                }
            )
        ])

        daftarArmada.value = normalisasiList(resArmada)
        daftarSO.value = normalisasiList(resSO)

        if (form.sales_order_id) {
            pilihSO()
        }
    } catch (err) {
        console.error(err)

        daftarArmada.value = []
        daftarSO.value = []
        soTerpilih.value = null

        errorMessage.value =
            'Data Sales Order atau armada tidak dapat dimuat saat ini.'
    } finally {
        sedangMemuat.value = false
    }
}

const pilihSO = () => {
    soTerpilih.value =
        daftarSO.value.find(
            (so) =>
                String(so.id) ===
                String(form.sales_order_id)
        ) || null
}

const simpanDelivery = async () => {
    if (
        sedangProses.value ||
        sedangMemuat.value ||
        !soTerpilih.value
    ) {
        return
    }

    sedangProses.value = true
    errorMessage.value = ''
    successMessage.value = ''

    try {
        const payload = {
            jenis_tujuan: 'CUSTOMER',
            sales_order_id: form.sales_order_id,
            tanggal: form.tanggal,
            kendaraan_id: form.kendaraan_id || null
        }

        await api.post(
            'logistik/pengiriman/',
            payload
        )

        successMessage.value =
            'Request delivery berhasil dikirim. Mengalihkan halaman...'

        await new Promise((resolve) => {
            setTimeout(resolve, 1200)
        })

        await router.push('/distribusi')
    } catch (err) {
        console.error(err)

        errorMessage.value =
            'Gagal mengirim request delivery. Silakan coba kembali.'

        successMessage.value = ''
    } finally {
        sedangProses.value = false
    }
}

onMounted(() => {
    muatDataMaster()
})
</script>

<style scoped>
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
