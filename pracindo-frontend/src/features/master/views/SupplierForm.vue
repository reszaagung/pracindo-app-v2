<template>
    <form
        class="flex w-full flex-col"
        @submit.prevent="submitForm"
    >
        <div
            class="border-b border-slate-100 bg-gradient-to-r from-white via-white to-slate-50/70 px-5 py-5 md:px-6"
        >
            <div class="flex items-start gap-3">
                <div
                    class="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-600 ring-1 ring-emerald-100"
                >
                    <i class="pi pi-truck text-lg"></i>
                </div>

                <div>
                    <div
                        class="flex flex-wrap items-center gap-2"
                    >
                        <h2
                            class="text-base font-black text-slate-900 md:text-lg"
                        >
                            {{
                                mode === 'edit'
                                    ? 'Edit Supplier'
                                    : 'Supplier Baru'
                            }}
                        </h2>

                        <span
                            class="rounded-lg border border-emerald-100 bg-emerald-50 px-2 py-1 text-[9px] font-black uppercase tracking-wider text-emerald-700"
                        >
                            Master Data
                        </span>
                    </div>

                    <p
                        class="mt-1 text-xs leading-5 text-slate-500"
                    >
                        {{
                            mode === 'edit'
                                ? 'Perbarui informasi supplier yang terdaftar.'
                                : 'Tambahkan supplier baru ke master data perusahaan.'
                        }}
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
                    <i
                        class="pi pi-exclamation-triangle text-xs"
                    ></i>
                </div>

                <div class="min-w-0">
                    <div
                        class="text-xs font-black text-rose-800"
                    >
                        Data belum dapat disimpan
                    </div>

                    <div
                        class="mt-0.5 text-[11px] leading-5 text-rose-600"
                    >
                        {{ errorMessage }}
                    </div>
                </div>
            </div>
        </Transition>

        <div class="space-y-6 p-5 md:p-6">
            <section>
                <div
                    class="mb-4 flex items-center gap-3"
                >
                    <div
                        class="h-8 w-1 rounded-full bg-emerald-500"
                    ></div>

                    <div>
                        <h3
                            class="text-sm font-black text-slate-800"
                        >
                            Informasi Supplier
                        </h3>

                        <p
                            class="mt-0.5 text-[11px] text-slate-400"
                        >
                            Identitas utama supplier.
                        </p>
                    </div>
                </div>

                <div
                    class="grid grid-cols-1 gap-4 md:grid-cols-2"
                >
                    <div>
                        <label
                            for="supplier-kode"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Kode Supplier
                            <span
                                class="ml-1 text-[10px] font-medium text-slate-400"
                            >
                                Opsional
                            </span>
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-hashtag absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                            ></i>

                            <input
                                id="supplier-kode"
                                v-model="form.kode"
                                type="text"
                                maxlength="30"
                                autocomplete="off"
                                placeholder="Contoh: SUP-001"
                                class="form-input pl-10"
                            />
                        </div>
                    </div>

                    <div>
                        <label
                            for="supplier-nama"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Nama Supplier
                            <span
                                class="ml-1 text-rose-500"
                            >
                                *
                            </span>
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-building absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                            ></i>

                            <input
                                id="supplier-nama"
                                v-model="form.nama"
                                type="text"
                                maxlength="200"
                                autocomplete="organization"
                                placeholder="Masukkan nama supplier"
                                class="form-input pl-10"
                                :class="{
                                    'border-rose-300 focus:border-rose-400 focus:ring-rose-500/10':
                                        touched.nama &&
                                        !form.nama.trim(),
                                }"
                                @blur="
                                    touched.nama = true
                                "
                            />
                        </div>

                        <p
                            v-if="
                                touched.nama &&
                                !form.nama.trim()
                            "
                            class="mt-1.5 text-[10px] font-medium text-rose-500"
                        >
                            Nama supplier wajib
                            diisi.
                        </p>
                    </div>

                    <div>
                        <label
                            for="supplier-termin"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Termin Pembayaran
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-calendar absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                            ></i>

                            <input
                                id="supplier-termin"
                                v-model.number="
                                    form.termin_hari_default
                                "
                                type="number"
                                min="0"
                                max="3650"
                                step="1"
                                inputmode="numeric"
                                placeholder="0"
                                class="form-input pl-10 pr-16"
                            />

                            <span
                                class="pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2 text-[10px] font-bold text-slate-400"
                            >
                                hari
                            </span>
                        </div>

                        <p
                            class="mt-1.5 text-[10px] text-slate-400"
                        >
                            Contoh: 30 untuk
                            pembayaran 30 hari.
                        </p>
                    </div>

                    <div>
                        <label
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Status Supplier
                        </label>

                        <button
                            type="button"
                            :disabled="saving"
                            @click="
                                form.aktif =
                                    !form.aktif
                            "
                            class="flex w-full items-center justify-between rounded-xl border px-3.5 py-3 text-left transition-all disabled:cursor-not-allowed disabled:opacity-60"
                            :class="
                                form.aktif
                                    ? 'border-emerald-200 bg-emerald-50/70'
                                    : 'border-slate-200 bg-slate-50'
                            "
                        >
                            <div
                                class="flex items-center gap-3"
                            >
                                <div
                                    class="flex h-8 w-8 items-center justify-center rounded-lg"
                                    :class="
                                        form.aktif
                                            ? 'bg-emerald-100 text-emerald-600'
                                            : 'bg-slate-200 text-slate-400'
                                    "
                                >
                                    <i
                                        :class="
                                            form.aktif
                                                ? 'pi pi-check-circle'
                                                : 'pi pi-ban'
                                        "
                                        class="text-xs"
                                    ></i>
                                </div>

                                <div>
                                    <div
                                        class="text-xs font-bold"
                                        :class="
                                            form.aktif
                                                ? 'text-emerald-700'
                                                : 'text-slate-600'
                                        "
                                    >
                                        {{
                                            form.aktif
                                                ? 'Supplier Aktif'
                                                : 'Supplier Nonaktif'
                                        }}
                                    </div>

                                    <div
                                        class="mt-0.5 text-[10px] text-slate-400"
                                    >
                                        {{
                                            form.aktif
                                                ? 'Supplier dapat dipilih pada transaksi.'
                                                : 'Supplier tidak ditampilkan pada transaksi aktif.'
                                        }}
                                    </div>
                                </div>
                            </div>

                            <span
                                class="relative h-6 w-11 rounded-full transition-colors"
                                :class="
                                    form.aktif
                                        ? 'bg-emerald-500'
                                        : 'bg-slate-300'
                                "
                            >
                                <span
                                    class="absolute top-1 h-4 w-4 rounded-full bg-white shadow-sm transition-transform"
                                    :class="
                                        form.aktif
                                            ? 'translate-x-6'
                                            : 'translate-x-1'
                                    "
                                ></span>
                            </span>
                        </button>
                    </div>
                </div>
            </section>

            <section>
                <div
                    class="mb-4 flex items-center gap-3"
                >
                    <div
                        class="h-8 w-1 rounded-full bg-blue-500"
                    ></div>

                    <div>
                        <h3
                            class="text-sm font-black text-slate-800"
                        >
                            Informasi Kontak
                        </h3>

                        <p
                            class="mt-0.5 text-[11px] text-slate-400"
                        >
                            Informasi kontak supplier
                            untuk kebutuhan operasional.
                        </p>
                    </div>
                </div>

                <div
                    class="grid grid-cols-1 gap-4 md:grid-cols-2"
                >
                    <div>
                        <label
                            for="supplier-telepon"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Nomor Telepon
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-phone absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                            ></i>

                            <input
                                id="supplier-telepon"
                                v-model="form.telepon"
                                type="tel"
                                maxlength="50"
                                autocomplete="tel"
                                placeholder="08xxxxxxxxxx"
                                class="form-input pl-10"
                            />
                        </div>
                    </div>

                    <div>
                        <label
                            for="supplier-email"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Email
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-envelope absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                            ></i>

                            <input
                                id="supplier-email"
                                v-model="form.email"
                                type="email"
                                maxlength="150"
                                autocomplete="email"
                                placeholder="supplier@email.com"
                                class="form-input pl-10"
                                :class="{
                                    'border-rose-300 focus:border-rose-400 focus:ring-rose-500/10':
                                        touched.email &&
                                        form.email &&
                                        !emailValid,
                                }"
                                @blur="
                                    touched.email = true
                                "
                            />
                        </div>

                        <p
                            v-if="
                                touched.email &&
                                form.email &&
                                !emailValid
                            "
                            class="mt-1.5 text-[10px] font-medium text-rose-500"
                        >
                            Format email belum
                            valid.
                        </p>
                    </div>

                    <div
                        class="md:col-span-2"
                    >
                        <label
                            for="supplier-npwp"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            NPWP
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-id-card absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                            ></i>

                            <input
                                id="supplier-npwp"
                                v-model="form.npwp"
                                type="text"
                                maxlength="32"
                                autocomplete="off"
                                placeholder="Nomor NPWP supplier"
                                class="form-input pl-10"
                            />
                        </div>
                    </div>
                </div>
            </section>

            <section>
                <div
                    class="mb-4 flex items-center gap-3"
                >
                    <div
                        class="h-8 w-1 rounded-full bg-violet-500"
                    ></div>

                    <div>
                        <h3
                            class="text-sm font-black text-slate-800"
                        >
                            Alamat
                        </h3>

                        <p
                            class="mt-0.5 text-[11px] text-slate-400"
                        >
                            Lokasi dan alamat supplier.
                        </p>
                    </div>
                </div>

                <div
                    class="grid grid-cols-1 gap-4 md:grid-cols-3"
                >
                    <div
                        class="md:col-span-2"
                    >
                        <label
                            for="supplier-alamat"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Alamat
                        </label>

                        <textarea
                            id="supplier-alamat"
                            v-model="form.alamat"
                            rows="3"
                            maxlength="500"
                            placeholder="Alamat lengkap supplier..."
                            class="form-input resize-none"
                        ></textarea>
                    </div>

                    <div>
                        <label
                            for="supplier-kota"
                            class="mb-1.5 block text-xs font-bold text-slate-600"
                        >
                            Kota
                        </label>

                        <div class="relative">
                            <i
                                class="pi pi-map-marker absolute left-3.5 top-1/2 -translate-y-1/2 text-xs text-slate-400"
                            ></i>

                            <input
                                id="supplier-kota"
                                v-model="form.kota"
                                type="text"
                                maxlength="100"
                                autocomplete="address-level2"
                                placeholder="Contoh: Jakarta"
                                class="form-input pl-10"
                            />
                        </div>
                    </div>
                </div>
            </section>

            <section>
                <div
                    class="mb-4 flex items-center gap-3"
                >
                    <div
                        class="h-8 w-1 rounded-full bg-amber-500"
                    ></div>

                    <div>
                        <h3
                            class="text-sm font-black text-slate-800"
                        >
                            Catatan
                        </h3>

                        <p
                            class="mt-0.5 text-[11px] text-slate-400"
                        >
                            Informasi tambahan yang relevan.
                        </p>
                    </div>
                </div>

                <textarea
                    v-model="form.catatan"
                    rows="3"
                    maxlength="500"
                    placeholder="Catatan supplier..."
                    class="form-input resize-none"
                ></textarea>
            </section>
        </div>

        <div
            class="flex flex-col-reverse gap-2 border-t border-slate-100 bg-slate-50/70 p-4 sm:flex-row sm:items-center sm:justify-between md:px-6"
        >
            <div
                class="flex items-center gap-2 text-[10px] text-slate-400"
            >
                <i
                    class="pi pi-info-circle"
                ></i>

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
                    :disabled="saving"
                    class="flex-1 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-bold text-slate-600 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50 sm:flex-none"
                >
                    Batal
                </button>

                <button
                    type="submit"
                    :disabled="
                        saving ||
                        !formValid
                    "
                    class="flex flex-1 items-center justify-center gap-2 rounded-xl bg-slate-900 px-5 py-2.5 text-xs font-bold text-white shadow-md transition-all hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50 sm:flex-none"
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
                            : mode === 'edit'
                                ? 'Simpan Perubahan'
                                : 'Simpan Supplier'
                    }}
                </button>
            </div>
        </div>
    </form>
</template>

<script setup>
import {
    computed,
    reactive,
    ref,
    watch
} from 'vue'

import { useSupplier } from '@/features/master/composables/useSupplier'

const props = defineProps({
    modelValue: {
        type: Object,
        default: null
    },

    mode: {
        type: String,
        default: 'create'
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
    simpanSuplier,
    sedangSimpan
} = useSupplier()

const defaultForm = () => ({
    id: null,
    kode: '',
    nama: '',
    termin_hari_default: 0,
    aktif: true,
    telepon: '',
    email: '',
    npwp: '',
    alamat: '',
    kota: '',
    catatan: ''
})

const form = reactive(
    defaultForm()
)

const touched = reactive({
    nama: false,
    email: false
})

const errorMessage =
    ref('')

const saving = computed(
    () =>
        Boolean(
            props.loading ||
                sedangSimpan.value
        )
)

const applyModel = (
    value
) => {
    Object.assign(
        form,
        defaultForm(),
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
        touched.email = false
    },
    {
        deep: true
    }
)

const emailValid =
    computed(() => {
        if (!form.email) {
            return true
        }

        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
            form.email.trim()
        )
    })

const formValid =
    computed(() => {
        return (
            form.nama.trim()
                .length > 0 &&
            emailValid.value &&
            Number(
                form.termin_hari_default
            ) >= 0
        )
    })

const buatPayload = () => {
    const payload = {
        kode: form.kode.trim(),
        nama: form.nama.trim(),
        termin_hari_default:
            Number(
                form.termin_hari_default ||
                    0
            ),
        aktif: Boolean(
            form.aktif
        ),
        telepon:
            form.telepon.trim(),
        email:
            form.email.trim(),
        npwp:
            form.npwp.trim(),
        alamat:
            form.alamat.trim(),
        kota:
            form.kota.trim(),
        catatan:
            form.catatan.trim()
    }

    return payload
}

const submitForm = async () => {
    touched.nama = true
    touched.email = true
    errorMessage.value = ''

    if (
        !form.nama.trim()
    ) {
        errorMessage.value =
            'Nama supplier wajib diisi.'
        return
    }

    if (
        !emailValid.value
    ) {
        errorMessage.value =
            'Format email supplier belum valid.'
        return
    }

    if (
        Number(
            form.termin_hari_default
        ) < 0
    ) {
        errorMessage.value =
            'Termin pembayaran tidak boleh negatif.'
        return
    }

    if (saving.value) {
        return
    }

    const payload =
        buatPayload()

    const id =
        props.mode ===
            'edit' &&
        form.id
            ? form.id
            : null

    const hasil =
        await simpanSuplier(
            payload,
            id
        )

    if (
        !hasil?.success
    ) {
        const fieldErrors =
            hasil?.errorField ||
            {}

        const firstFieldError =
            Object.values(
                fieldErrors
            )
                .flat()
                .find(
                    (value) =>
                        value
                )

        errorMessage.value =
            firstFieldError ||
            hasil?.message ||
            'Gagal menyimpan supplier.'

        return
    }

    const data =
        hasil?.data ||
        {
            ...form,
            ...payload,
            id:
                id ||
                null
        }

    emit(
        'update:modelValue',
        data
    )

    emit(
        'save',
        data
    )

    emit(
        'saved',
        data
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
    border-color: #10b981;
    box-shadow:
        0 0 0 4px
        rgb(16 185 129 / 0.08);
}

textarea.form-input {
    line-height: 1.6;
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
textarea:focus-visible {
    outline: 2px solid #10b981;
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