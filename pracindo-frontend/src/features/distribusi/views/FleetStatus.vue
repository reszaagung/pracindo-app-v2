  <template>
    <div class="relative w-full">
        <div
            class="mb-6 flex flex-col gap-4 border-b border-slate-200 pb-5 md:mb-8 md:flex-row md:items-end md:justify-between"
        >
            <div class="min-w-0">
                <div
                    class="mb-2 flex flex-wrap items-center gap-1.5 text-[10px] font-extrabold uppercase tracking-[0.12em] text-slate-400"
                >
                    <span>Distribution</span>

                    <span
                        class="text-slate-300"
                        aria-hidden="true"
                    >
                        /
                    </span>

                    <span class="text-slate-600">
                        Status Armada
                    </span>
                </div>

                <div class="flex items-start gap-3">
                    <div
                        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-slate-900 text-white shadow-md shadow-slate-900/10"
                        aria-hidden="true"
                    >
                        <i class="pi pi-truck text-lg"></i>
                    </div>

                    <div class="min-w-0">
                        <h1
                            class="text-2xl font-extrabold tracking-tight text-slate-800 md:text-3xl"
                        >
                            Pantau Armada
                        </h1>

                        <p class="mt-1 text-xs leading-5 text-slate-500 sm:text-sm">
                            Ketersediaan truk dan kendaraan saat ini.
                        </p>
                    </div>
                </div>
            </div>

            <button
                type="button"
                @click="bukaModal"
                :disabled="sedangMenyimpan"
                class="group flex w-full items-center justify-center gap-2 rounded-xl bg-slate-900 px-5 py-3 text-sm font-extrabold text-white shadow-lg shadow-slate-900/10 transition-all duration-200 hover:-translate-y-0.5 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:translate-y-0 active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
            >
                <span
                    class="flex h-7 w-7 items-center justify-center rounded-lg bg-white/10"
                >
                    <i
                        class="pi pi-plus text-xs transition-transform duration-200 group-hover:rotate-90"
                        aria-hidden="true"
                    ></i>
                </span>

                <span>Registrasi Armada</span>
            </button>
        </div>

        <div
            v-if="memuat"
            class="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3"
            aria-busy="true"
            aria-label="Memuat data armada"
        >
            <div
                v-for="index in 6"
                :key="index"
                class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
            >
                <div class="flex items-start justify-between gap-4">
                    <div class="flex min-w-0 items-center gap-3">
                        <div
                            class="h-11 w-11 shrink-0 animate-pulse rounded-xl bg-slate-200"
                            aria-hidden="true"
                        ></div>

                        <div class="min-w-0 flex-1 space-y-2">
                            <div
                                class="h-4 w-24 animate-pulse rounded bg-slate-200"
                                aria-hidden="true"
                            ></div>

                            <div
                                class="h-3 w-32 animate-pulse rounded bg-slate-100"
                                aria-hidden="true"
                            ></div>
                        </div>
                    </div>

                    <div
                        class="h-6 w-20 animate-pulse rounded-full bg-slate-100"
                        aria-hidden="true"
                    ></div>
                </div>

                <div
                    class="mt-6 h-20 animate-pulse rounded-xl bg-slate-50"
                    aria-hidden="true"
                ></div>

                <div
                    class="mt-5 flex items-end justify-between border-t border-slate-100 pt-4"
                >
                    <div class="space-y-2">
                        <div
                            class="h-2.5 w-24 animate-pulse rounded bg-slate-100"
                            aria-hidden="true"
                        ></div>

                        <div
                            class="h-4 w-16 animate-pulse rounded bg-slate-200"
                            aria-hidden="true"
                        ></div>
                    </div>

                    <div
                        class="h-4 w-14 animate-pulse rounded bg-slate-100"
                        aria-hidden="true"
                    ></div>
                </div>
            </div>
        </div>

        <div
            v-else-if="galat"
            class="rounded-2xl border border-rose-200 bg-rose-50 p-4 shadow-sm"
            role="alert"
        >
            <div class="flex items-start gap-3">
                <div
                    class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-rose-100 text-rose-600"
                    aria-hidden="true"
                >
                    <i class="pi pi-exclamation-triangle text-sm"></i>
                </div>

                <div class="min-w-0 flex-1">
                    <p class="text-xs font-extrabold text-rose-800">
                        Gagal memuat data armada
                    </p>

                    <p class="mt-1 text-xs leading-5 text-rose-600">
                        {{ galat }}
                    </p>

                    <button
                        type="button"
                        @click="muatDataArmada"
                        class="mt-3 rounded-lg bg-white px-3 py-2 text-[11px] font-extrabold text-rose-700 shadow-sm ring-1 ring-rose-200 transition hover:bg-rose-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-500"
                    >
                        Coba Lagi
                    </button>
                </div>
            </div>
        </div>

        <div
            v-else
            class="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3"
        >
            <div
                v-if="armadaList.length === 0"
                class="col-span-full rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-14 text-center shadow-sm"
            >
                <div
                    class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-100 text-slate-400"
                    aria-hidden="true"
                >
                    <i class="pi pi-truck text-2xl"></i>
                </div>

                <h3 class="mt-4 text-sm font-extrabold text-slate-700">
                    Tidak Ada Armada
                </h3>

                <p class="mx-auto mt-1 max-w-md text-xs leading-5 text-slate-500">
                    Belum ada data kendaraan yang terdaftar di sistem.
                </p>

                <button
                    type="button"
                    @click="bukaModal"
                    class="mt-5 inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2.5 text-xs font-extrabold text-white shadow-sm transition-all hover:-translate-y-0.5 hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 active:translate-y-0"
                >
                    <i
                        class="pi pi-plus text-[10px]"
                        aria-hidden="true"
                    ></i>

                    Registrasi Armada Pertama
                </button>
            </div>

            <article
                v-for="truk in armadaList"
                :key="truk.id"
                class="group relative overflow-hidden rounded-2xl border bg-white p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:shadow-slate-900/5"
                :class="
                    truk.aktif !== false
                        ? 'border-slate-200'
                        : 'border-rose-100 bg-rose-50/30'
                "
            >
                <div
                    class="absolute inset-x-0 top-0 h-1"
                    :class="
                        truk.aktif !== false
                            ? 'bg-emerald-500'
                            : 'bg-rose-400'
                    "
                    aria-hidden="true"
                ></div>

                <div class="flex items-start justify-between gap-4">
                    <div class="flex min-w-0 items-center gap-3">
                        <div
                            class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl transition-transform duration-300 group-hover:scale-105"
                            :class="
                                truk.aktif !== false
                                    ? 'bg-slate-100 text-slate-600'
                                    : 'bg-rose-100 text-rose-500'
                            "
                            aria-hidden="true"
                        >
                            <i class="pi pi-truck text-base"></i>
                        </div>

                        <div class="min-w-0">
                            <h3
                                class="truncate text-lg font-extrabold leading-tight text-slate-800"
                            >
                                {{ truk.plat_nomor || truk.kode || '-' }}
                            </h3>

                            <p
                                class="mt-0.5 truncate text-xs font-medium text-slate-500"
                            >
                                {{ truk.nama || 'Nama kendaraan belum diatur' }}
                            </p>
                        </div>
                    </div>

                    <span
                        class="shrink-0 rounded-full px-2.5 py-1 text-[9px] font-extrabold uppercase tracking-[0.08em]"
                        :class="
                            truk.aktif !== false
                                ? 'border border-emerald-200 bg-emerald-50 text-emerald-700'
                                : 'border border-rose-200 bg-rose-50 text-rose-700'
                        "
                    >
                        {{
                            truk.aktif !== false
                                ? 'TERSEDIA'
                                : 'NONAKTIF'
                        }}
                    </span>
                </div>

                <div
                    class="mt-5 rounded-xl border border-slate-100 bg-slate-50 p-4 transition-colors group-hover:bg-slate-50/70"
                >
                    <p
                        class="mb-2 text-[9px] font-extrabold uppercase tracking-[0.1em] text-slate-400"
                    >
                        Informasi Kendaraan
                    </p>

                    <div class="flex items-center gap-2">
                        <div
                            class="flex h-8 w-8 items-center justify-center rounded-lg bg-white text-slate-400 shadow-sm"
                            aria-hidden="true"
                        >
                            <i class="pi pi-id-card text-xs"></i>
                        </div>

                        <div class="min-w-0">
                            <p class="text-[10px] font-semibold text-slate-400">
                                Kode Internal
                            </p>

                            <p class="truncate text-xs font-extrabold text-slate-700">
                                {{ truk.kode || '-' }}
                            </p>
                        </div>
                    </div>
                </div>

                <div
                    class="mt-5 flex items-end justify-between border-t border-slate-100 pt-4"
                >
                    <div>
                        <p
                            class="mb-1 text-[9px] font-extrabold uppercase tracking-[0.1em] text-slate-400"
                        >
                            Kapasitas Maks
                        </p>

                        <p class="text-base font-extrabold text-slate-800">
                            {{ formatKapasitas(truk.kapasitas_kg) }}
                        </p>
                    </div>

                    <button
                        type="button"
                        :aria-label="`Detail ${truk.plat_nomor || truk.kode || 'armada'}`"
                        class="group/detail inline-flex items-center gap-1 rounded-lg px-2 py-1.5 text-xs font-bold text-blue-600 transition hover:bg-blue-50 hover:text-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
                    >
                        Detail

                        <i
                            class="pi pi-arrow-right text-[10px] transition-transform duration-200 group-hover/detail:translate-x-1"
                            aria-hidden="true"
                        ></i>
                    </button>
                </div>
            </article>
        </div>

        <div
            v-if="tampilModal"
            class="fixed inset-0 z-[1000] flex items-end justify-center bg-slate-950/50 p-3 backdrop-blur-sm sm:items-center sm:p-5"
            role="presentation"
            @click.self="tutupModal"
        >
            <div
                class="w-full max-w-lg overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl shadow-slate-950/20 animate-fade-in sm:rounded-3xl"
                role="dialog"
                aria-modal="true"
                aria-labelledby="modal-armada-title"
            >
                <div
                    class="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-5 py-4 sm:px-6"
                >
                    <div class="flex min-w-0 items-center gap-3">
                        <div
                            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-white shadow-sm"
                            aria-hidden="true"
                        >
                            <i class="pi pi-truck text-sm"></i>
                        </div>

                        <div class="min-w-0">
                            <h2
                                id="modal-armada-title"
                                class="truncate text-base font-extrabold text-slate-800"
                            >
                                Registrasi Armada Baru
                            </h2>

                            <p class="mt-0.5 text-[10px] font-medium text-slate-400">
                                Tambahkan kendaraan ke master armada.
                            </p>
                        </div>
                    </div>

                    <button
                        type="button"
                        @click="tutupModal"
                        :disabled="sedangMenyimpan"
                        aria-label="Tutup modal"
                        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl text-slate-400 transition hover:bg-rose-50 hover:text-rose-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-rose-500 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        <i
                            class="pi pi-times text-sm"
                            aria-hidden="true"
                        ></i>
                    </button>
                </div>

                <form
                    @submit.prevent="tanganiSubmit"
                    class="flex flex-col gap-5 p-5 sm:p-6"
                    :aria-busy="sedangMenyimpan"
                >
                    <div
                        v-if="formGalat"
                        class="flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 p-3.5 text-red-700"
                        role="alert"
                    >
                        <div
                            class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-red-100"
                            aria-hidden="true"
                        >
                            <i class="pi pi-exclamation-triangle text-xs"></i>
                        </div>

                        <p class="text-xs font-semibold leading-5">
                            {{ formGalat }}
                        </p>
                    </div>

                    <div class="flex flex-col gap-1.5">
                        <label
                            for="fleet-plat"
                            class="text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                        >
                            Plat Nomor
                            <span class="text-red-500">*</span>
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-car pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                                aria-hidden="true"
                            ></i>

                            <input
                                id="fleet-plat"
                                v-model="form.plat_nomor"
                                type="text"
                                required
                                placeholder="B 1234 CD"
                                autocomplete="off"
                                :disabled="sedangMenyimpan"
                                class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-10 pr-4 text-sm font-bold uppercase text-slate-800 outline-none transition focus:border-blue-400 focus:bg-white focus:ring-2 focus:ring-blue-100 disabled:cursor-not-allowed disabled:opacity-60"
                            />
                        </div>
                    </div>

                    <div class="flex flex-col gap-1.5">
                        <label
                            for="fleet-nama"
                            class="text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                        >
                            Nama Kendaraan
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-truck pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                                aria-hidden="true"
                            ></i>

                            <input
                                id="fleet-nama"
                                v-model="form.nama"
                                type="text"
                                placeholder="Truk Engkel Box"
                                autocomplete="off"
                                :disabled="sedangMenyimpan"
                                class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-10 pr-4 text-sm font-semibold text-slate-800 outline-none transition focus:border-blue-400 focus:bg-white focus:ring-2 focus:ring-blue-100 disabled:cursor-not-allowed disabled:opacity-60"
                            />
                        </div>
                    </div>

                    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <div class="flex flex-col gap-1.5">
                            <label
                                for="fleet-kode"
                                class="text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                            >
                                Kode Internal
                            </label>

                            <div class="relative">
                                <i
                                    class="pi pi-tag pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                                    aria-hidden="true"
                                ></i>

                                <input
                                    id="fleet-kode"
                                    v-model="form.kode"
                                    type="text"
                                    placeholder="T-001"
                                    autocomplete="off"
                                    :disabled="sedangMenyimpan"
                                    class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-10 pr-4 text-sm font-bold uppercase text-slate-800 outline-none transition focus:border-blue-400 focus:bg-white focus:ring-2 focus:ring-blue-100 disabled:cursor-not-allowed disabled:opacity-60"
                                />
                            </div>
                        </div>

                        <div class="flex flex-col gap-1.5">
                            <label
                                for="fleet-kapasitas"
                                class="text-[10px] font-extrabold uppercase tracking-[0.08em] text-slate-500"
                            >
                                Kapasitas (KG)
                                <span class="text-red-500">*</span>
                            </label>

                            <div class="relative">
                                <i
                                    class="pi pi-chart-bar pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                                    aria-hidden="true"
                                ></i>

                                <input
                                    id="fleet-kapasitas"
                                    v-model="form.kapasitas_kg"
                                    type="number"
                                    required
                                    min="1"
                                    placeholder="2000"
                                    :disabled="sedangMenyimpan"
                                    class="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-10 pr-4 text-sm font-bold text-slate-800 outline-none transition focus:border-blue-400 focus:bg-white focus:ring-2 focus:ring-blue-100 disabled:cursor-not-allowed disabled:opacity-60"
                                />
                            </div>
                        </div>
                    </div>

                    <div
                        class="flex flex-col-reverse gap-3 border-t border-slate-100 pt-4 sm:flex-row sm:justify-end"
                    >
                        <button
                            type="button"
                            @click="tutupModal"
                            :disabled="sedangMenyimpan"
                            class="w-full rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-bold text-slate-600 transition-all hover:border-slate-300 hover:bg-slate-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
                        >
                            Batal
                        </button>

                        <button
                            type="submit"
                            :disabled="sedangMenyimpan"
                            :aria-busy="sedangMenyimpan"
                            class="flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-extrabold text-white shadow-lg shadow-blue-600/15 transition-all hover:-translate-y-0.5 hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 active:translate-y-0 disabled:cursor-not-allowed disabled:translate-y-0 disabled:bg-slate-300 disabled:shadow-none sm:w-auto"
                        >
                            <i
                                v-if="sedangMenyimpan"
                                class="pi pi-spin pi-spinner text-sm"
                                aria-hidden="true"
                            ></i>

                            <i
                                v-else
                                class="pi pi-save text-sm"
                                aria-hidden="true"
                            ></i>

                            <span>
                                {{
                                    sedangMenyimpan
                                        ? 'Menyimpan...'
                                        : 'Simpan Armada'
                                }}
                            </span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { apiDistribusi } from '../api.js'

const armadaList = ref([])
const memuat = ref(true)
const galat = ref(null)

const tampilModal = ref(false)
const formGalat = ref('')
const sedangMenyimpan = ref(false)

const form = reactive({
    plat_nomor: '',
    nama: '',
    kode: '',
    kapasitas_kg: ''
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

const formatKapasitas = (kg) => {
    if (!kg) return 'Tidak disetel'

    const angka = parseFloat(kg)

    if (Number.isNaN(angka)) {
        return 'Tidak disetel'
    }

    if (angka >= 1000) {
        return `${(angka / 1000).toLocaleString('id-ID')} Ton`
    }

    return `${angka.toLocaleString('id-ID')} Kg`
}

const muatDataArmada = async () => {
    memuat.value = true
    galat.value = null

    try {
        const data = await apiDistribusi.getArmada()

        armadaList.value = normalisasiList(data)
    } catch (error) {
        console.error(error)

        galat.value =
            'Gagal memuat daftar kendaraan dari server.'

        armadaList.value = []
    } finally {
        memuat.value = false
    }
}

const bukaModal = () => {
    form.plat_nomor = ''
    form.nama = ''
    form.kode = ''
    form.kapasitas_kg = ''
    formGalat.value = ''
    tampilModal.value = true
}

const tutupModal = () => {
    if (sedangMenyimpan.value) return

    tampilModal.value = false
}

const tanganiSubmit = () => {
    if (sedangMenyimpan.value) return

    submitArmada()
}

const submitArmada = async () => {
    if (sedangMenyimpan.value) return

    sedangMenyimpan.value = true
    formGalat.value = ''

    try {
        const payload = {
            plat_nomor: form.plat_nomor,
            nama: form.nama,
            kode: form.kode,
            kapasitas_kg: parseFloat(form.kapasitas_kg)
        }

        await apiDistribusi.tambahArmada(payload)

        tutupModal()
        await muatDataArmada()
    } catch (err) {
        console.error(err)

        if (err.response?.data) {
            const data = err.response.data

            if (
                typeof data === 'object' &&
                data !== null
            ) {
                const errorKey = Object.keys(data)[0]

                if (
                    errorKey &&
                    Array.isArray(data[errorKey])
                ) {
                    formGalat.value =
                        `${errorKey}: ${data[errorKey][0]}`
                } else {
                    formGalat.value =
                        data.detail ||
                        'Gagal menyimpan data armada.'
                }
            } else {
                formGalat.value =
                    String(err.response.data)
            }
        } else {
            formGalat.value =
                err.message ||
                'Gagal menyimpan data armada.'
        }
    } finally {
        sedangMenyimpan.value = false
    }
}

onMounted(() => {
    muatDataArmada()
})
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.22s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(8px) scale(0.985);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@media (prefers-reduced-motion: reduce) {
    .animate-fade-in,
    * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
