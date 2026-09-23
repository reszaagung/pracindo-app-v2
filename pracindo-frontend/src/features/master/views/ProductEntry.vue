<template>
    <form
        class="flex w-full flex-col"
        @submit.prevent="simpan"
    >
        <div
            class="border-b border-slate-100 bg-gradient-to-r from-white via-white to-slate-50/70 px-5 py-5 md:px-6"
        >
            <div class="flex items-start gap-3">
                <div
                    class="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-blue-50 text-blue-600 ring-1 ring-blue-100"
                >
                    <i class="pi pi-box text-lg"></i>
                </div>

                <div>
                    <div class="flex flex-wrap items-center gap-2">
                        <h2 class="text-base font-black text-slate-900 md:text-lg">
                            Produk Baru
                        </h2>

                        <span
                            class="rounded-lg border border-blue-100 bg-blue-50 px-2 py-1 text-[9px] font-black uppercase tracking-wider text-blue-700"
                        >
                            Master Produk
                        </span>
                    </div>

                    <p class="mt-1 text-xs leading-5 text-slate-500">
                        Tambahkan produk baru beserta jenis dan satuan dasarnya.
                    </p>
                </div>
            </div>
        </div>

        <Transition name="slide">
            <div
                v-if="errorMessage"
                class="mx-5 mt-5 flex items-start gap-3 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 md:mx-6"
            >
                <div
                    class="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-white text-rose-500 shadow-sm"
                >
                    <i class="pi pi-exclamation-triangle text-xs"></i>
                </div>

                <div class="min-w-0">
                    <div class="text-xs font-black text-rose-800">
                        Produk belum dapat disimpan
                    </div>

                    <div class="mt-0.5 text-[11px] leading-5 text-rose-600">
                        {{ errorMessage }}
                    </div>
                </div>
            </div>
        </Transition>

        <div class="space-y-6 p-5 md:p-6">
            <section>
                <div class="mb-4 flex items-center gap-3">
                    <div class="h-8 w-1 rounded-full bg-blue-500"></div>

                    <div>
                        <h3 class="text-sm font-black text-slate-800">
                            Informasi Produk
                        </h3>

                        <p class="mt-0.5 text-[11px] text-slate-400">
                            Identitas utama produk yang akan digunakan di transaksi.
                        </p>
                    </div>
                </div>

                <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
                    <div class="md:col-span-2">
                        <label
                            for="produk-nama"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Nama Produk
                            <span class="ml-1 text-rose-500">*</span>
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-box absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                            ></i>

                            <input
                                id="produk-nama"
                                v-model="form.nama"
                                type="text"
                                maxlength="200"
                                autocomplete="off"
                                placeholder="Contoh: Resin A, PAIL 20KG, Bahan Baku X"
                                class="form-input pl-10"
                                :class="{
                                    'border-rose-300 focus:border-rose-400 focus:ring-rose-500/10':
                                        touched.nama && !form.nama.trim(),
                                }"
                                @blur="touched.nama = true"
                            />
                        </div>

                        <p
                            v-if="touched.nama && !form.nama.trim()"
                            class="mt-1.5 text-[10px] font-medium text-rose-500"
                        >
                            Nama produk wajib diisi.
                        </p>
                    </div>

                    <div>
                        <label
                            for="produk-kode"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Kode Produk
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-hashtag absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                            ></i>

                            <input
                                id="produk-kode"
                                v-model="form.kode"
                                type="text"
                                maxlength="50"
                                autocomplete="off"
                                placeholder="Otomatis bila dikosongkan"
                                class="form-input pl-10 pr-20"
                            />

                            <span
                                class="pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 text-[10px] font-bold text-slate-400"
                            >
                                Optional
                            </span>
                        </div>

                        <p class="mt-1.5 text-[10px] text-slate-400">
                            Kode dibuat otomatis berdasarkan jenis produk jika dikosongkan.
                        </p>
                    </div>

                    <div>
                        <label
                            for="produk-jenis"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Jenis Produk
                            <span class="ml-1 text-rose-500">*</span>
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-tag absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                            ></i>

                            <select
                                id="produk-jenis"
                                v-model="form.jenis"
                                :disabled="saving"
                                class="form-input cursor-pointer appearance-none pl-10 pr-10 disabled:cursor-not-allowed disabled:bg-slate-50"
                            >
                                <option value="BAHAN_BAKU">
                                    Bahan Baku
                                </option>

                                <option value="KEMASAN">
                                    Kemasan
                                </option>
                            </select>

                            <i
                                class="pi pi-chevron-down pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 text-[10px] text-slate-400"
                            ></i>
                        </div>
                    </div>

                    <div>
                        <label
                            for="produk-satuan"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Satuan Dasar
                            <span class="ml-1 text-rose-500">*</span>
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-sliders-h absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                            ></i>

                            <select
                                id="produk-satuan"
                                v-model="form.satuan"
                                :disabled="saving || loadingSatuan"
                                class="form-input cursor-pointer appearance-none pl-10 pr-10 disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-400"
                            >
                                <option
                                    :value="null"
                                    disabled
                                >
                                    {{
                                        loadingSatuan
                                            ? 'Memuat satuan...'
                                            : 'Pilih satuan'
                                    }}
                                </option>

                                <option
                                    v-for="satuan in listSatuan"
                                    :key="satuan.id"
                                    :value="satuan.id"
                                >
                                    {{ satuan.nama || satuan.kode }}
                                    <template
                                        v-if="
                                            satuan.nama &&
                                            satuan.kode
                                        "
                                    >
                                        ({{ satuan.kode }})
                                    </template>
                                </option>
                            </select>

                            <i
                                class="pi pi-chevron-down pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 text-[10px] text-slate-400"
                            ></i>
                        </div>

                        <p
                            v-if="form.jenis === 'KEMASAN'"
                            class="mt-1.5 text-[10px] text-slate-400"
                        >
                            Kemasan umumnya menggunakan PCS, UNIT, atau PACK.
                        </p>

                        <p
                            v-else
                            class="mt-1.5 text-[10px] text-slate-400"
                        >
                            Bahan baku umumnya menggunakan KG.
                        </p>
                    </div>

                    <div>
                        <label class="mb-1.5 block text-xs font-bold text-slate-600">
                            Preview Produk
                        </label>

                        <div
                            class="flex min-h-[46px] items-center justify-between rounded-xl border border-slate-200 bg-slate-50 px-3.5"
                        >
                            <div class="flex min-w-0 items-center gap-3">
                                <div
                                    class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg"
                                    :class="
                                        form.jenis === 'KEMASAN'
                                            ? 'bg-amber-50 text-amber-600'
                                            : 'bg-blue-50 text-blue-600'
                                    "
                                >
                                    <i
                                        :class="
                                            form.jenis === 'KEMASAN'
                                                ? 'pi pi-inbox'
                                                : 'pi pi-box'
                                        "
                                        class="text-xs"
                                    ></i>
                                </div>

                                <div class="min-w-0">
                                    <div
                                        class="truncate text-xs font-bold text-slate-700"
                                    >
                                        {{
                                            form.nama.trim() ||
                                            'Nama produk'
                                        }}
                                    </div>

                                    <div
                                        class="mt-0.5 text-[10px] text-slate-400"
                                    >
                                        {{
                                            selectedSatuanLabel ||
                                            'Satuan belum dipilih'
                                        }}
                                    </div>
                                </div>
                            </div>

                            <span
                                class="shrink-0 rounded-lg px-2 py-1 text-[9px] font-black uppercase tracking-wide"
                                :class="
                                    form.jenis === 'KEMASAN'
                                        ? 'bg-amber-50 text-amber-700'
                                        : 'bg-blue-50 text-blue-700'
                                "
                            >
                                {{ form.jenis.replace('_', ' ') }}
                            </span>
                        </div>
                    </div>
                </div>
            </section>
        </div>

        <div
            class="flex flex-col-reverse gap-2 border-t border-slate-100 bg-slate-50/70 p-4 sm:flex-row sm:items-center sm:justify-between md:px-6"
        >
            <div
                class="flex items-center gap-2 text-[10px] text-slate-400"
            >
                <i class="pi pi-info-circle"></i>

                <span>
                    Field bertanda
                    <strong class="text-rose-500">*</strong>
                    wajib diisi.
                </span>
            </div>

            <div
                class="flex w-full items-center gap-2 sm:w-auto"
            >
                <button
                    type="button"
                    @click="$emit('close')"
                    :disabled="saving || loadingSatuan"
                    class="flex-1 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50 sm:flex-none"
                >
                    Batal
                </button>

                <button
                    type="submit"
                    :disabled="
                        saving ||
                        loadingSatuan ||
                        !formValid
                    "
                    class="flex flex-1 items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-2.5 text-xs font-bold text-white shadow-md transition-all hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50 sm:flex-none"
                >
                    <i
                        :class="
                            saving
                                ? 'pi pi-spin pi-spinner'
                                : 'pi pi-check'
                        "
                    ></i>

                    {{
                        saving
                            ? 'Menyimpan...'
                            : 'Simpan Produk'
                    }}
                </button>
            </div>
        </div>
    </form>
</template>

<script setup>
import {
    computed,
    onMounted,
    reactive,
    ref,
    watch
} from 'vue'

import api from '@/utils/api'
import { bacaError } from '@/utils/error'
import { useProduct } from '@/features/master/composables/useProduct'
import { generateKode } from '@/utils/generate_id'

const props = defineProps({
    modelValue: {
        type: Object,
        default: null
    },

    loading: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits([
    'update:modelValue',
    'save',
    'saved',
    'close'
])

const {
    addProduk,
    isSaving
} = useProduct()

const form = reactive({
    id: null,
    kode: '',
    nama: '',
    jenis: 'BAHAN_BAKU',
    satuan: null
})

const listSatuan = ref([])
const loadingSatuan = ref(false)
const errorMessage = ref('')

const touched = reactive({
    nama: false,
    satuan: false
})

const saving = computed(
    () =>
        Boolean(
            props.loading ||
                isSaving.value
        )
)

const applyModel = (
    value
) => {
    Object.assign(
        form,
        {
            id: null,
            kode: '',
            nama: '',
            jenis: 'BAHAN_BAKU',
            satuan: null
        },
        value || {}
    )
}

applyModel(
    props.modelValue
)

watch(
    () => props.modelValue,
    (value) => {
        applyModel(value)
        errorMessage.value = ''
        touched.nama = false
        touched.satuan = false
    },
    {
        deep: true
    }
)

const loadSatuan = async () => {
    loadingSatuan.value = true
    errorMessage.value = ''

    try {
        const { data } =
            await api.get(
                'master/satuan/',
                {
                    params: {
                        aktif: true
                    }
                }
            )

        listSatuan.value =
            data?.results ||
            data ||
            []

        if (
            !form.satuan &&
            listSatuan.value.length
        ) {
            const preferred =
                form.jenis ===
                'KEMASAN'
                    ? listSatuan.value.find(
                          (satuan) =>
                              [
                                  'pcs',
                                  'unit',
                                  'pack'
                              ].includes(
                                  String(
                                      satuan?.kode ||
                                          ''
                                  ).toLowerCase()
                              )
                      )
                    : listSatuan.value.find(
                          (satuan) =>
                              String(
                                  satuan?.kode ||
                                      ''
                              ).toLowerCase() ===
                              'kg'
                      )

            form.satuan =
                preferred?.id ||
                listSatuan.value[0]
                    ?.id ||
                null
        }
    } catch (err) {
        errorMessage.value =
            bacaError(
                err,
                'Gagal memuat data satuan.'
            )
    } finally {
        loadingSatuan.value = false
    }
}

onMounted(() => {
    loadSatuan()
})

const selectedSatuan =
    computed(() =>
        listSatuan.value.find(
            (satuan) =>
                String(
                    satuan.id
                ) ===
                String(
                    form.satuan
                )
        )
    )

const selectedSatuanLabel =
    computed(() => {
        if (
            !selectedSatuan.value
        ) {
            return ''
        }

        if (
            selectedSatuan.value.nama &&
            selectedSatuan.value.kode
        ) {
            return `${selectedSatuan.value.nama} (${selectedSatuan.value.kode})`
        }

        return (
            selectedSatuan.value.nama ||
            selectedSatuan.value.kode ||
            ''
        )
    })

const formValid =
    computed(() => {
        return (
            form.nama.trim()
                .length > 0 &&
            !!form.jenis &&
            !!form.satuan
        )
    })

const normalisasiKode = (
    jenis
) =>
    jenis === 'KEMASAN'
        ? generateKode('PK')
        : generateKode('RM')

const simpan = async () => {
    touched.nama = true
    touched.satuan = true
    errorMessage.value = ''

    if (
        !form.nama.trim()
    ) {
        errorMessage.value =
            'Nama produk wajib diisi.'
        return
    }

    if (!form.jenis) {
        errorMessage.value =
            'Jenis produk wajib dipilih.'
        return
    }

    if (!form.satuan) {
        errorMessage.value =
            'Satuan dasar wajib dipilih.'
        return
    }

    if (saving.value) {
        return
    }

    const payload = {
        kode:
            form.kode.trim() ||
            normalisasiKode(
                form.jenis
            ),
        nama:
            form.nama.trim(),
        jenis:
            form.jenis,
        satuan:
            form.satuan
    }

    const hasil =
        await addProduk(
            payload
        )

    if (
        !hasil?.success
    ) {
        errorMessage.value =
            hasil?.message ||
            'Gagal menyimpan produk.'

        return
    }

    const produkBaru =
        hasil?.data || null

    emit(
        'update:modelValue',
        produkBaru
    )

    emit(
        'save',
        produkBaru
    )

    emit(
        'saved',
        produkBaru
    )
}
</script>

<style scoped>
.form-input {
    width: 100%;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    background: #ffffff;
    padding: 0.7rem 0.875rem;
    font-size: 0.75rem;
    font-weight: 500;
    color: #334155;
    outline: none;
    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease,
        background-color 0.2s ease;
}

.form-input::placeholder {
    color: #94a3b8;
}

.form-input:hover {
    border-color: #cbd5e1;
}

.form-input:focus {
    border-color: #3b82f6;
    box-shadow:
        0 0 0 4px
        rgb(59 130 246 / 0.08);
}

.form-input:disabled {
    background: #f8fafc;
}

.slide-enter-active,
.slide-leave-active {
    transition:
        opacity 0.2s ease,
        transform 0.2s ease;
}

.slide-enter-from,
.slide-leave-to {
    opacity: 0;
    transform: translateY(-5px);
}

button:focus-visible,
input:focus-visible,
select:focus-visible {
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
}

@media (
    prefers-reduced-motion: reduce
) {
    *,
    *::before,
    *::after {
        transition: none !important;
        animation: none !important;
    }
}
</style>