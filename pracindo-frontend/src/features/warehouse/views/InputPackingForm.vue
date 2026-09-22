<template>
    <div class="packing-page">
        <div class="packing-container">
            <div class="page-header">
                <div>
                    <div class="eyebrow">WAREHOUSE • PACKING</div>

                    <h1>Input Packing</h1>

                    <p>
                        Catat proses packing barang jadi dari stok produksi.
                    </p>
                </div>

                <button
                    type="button"
                    class="refresh-btn"
                    :disabled="isLoading"
                    @click="reloadData"
                >
                    <i
                        class="pi pi-refresh"
                        :class="{ 'pi-spin': isLoading }"
                    ></i>
                    Refresh
                </button>
            </div>

            <div
                v-if="error"
                class="alert alert-danger"
            >
                <i class="pi pi-exclamation-circle"></i>
                <div>{{ error }}</div>
            </div>

            <form
                class="form-layout"
                @submit.prevent="submitForm"
            >
                <div class="form-main">
                    <section class="form-card">
                        <div class="section-head">
                            <div class="section-icon">
                                <i class="pi pi-users"></i>
                            </div>

                            <div>
                                <h2>Informasi Packing</h2>

                                <p>
                                    Tentukan entitas dan tangki sumber proses packing.
                                </p>
                            </div>
                        </div>

                        <div class="field-grid">
                            <div class="field">
                                <label for="grup">
                                    Grup / Entitas
                                    <span class="required">*</span>
                                </label>

                                <select
                                    id="grup"
                                    v-model="form.grup"
                                    class="input-control"
                                    :disabled="isLoading"
                                    required
                                >
                                    <option value="">
                                        Pilih grup
                                    </option>

                                    <option
                                        v-for="item in grupOptions"
                                        :key="item.id"
                                        :value="item.id"
                                    >
                                        {{ getEntityLabel(item) }}
                                    </option>
                                </select>
                            </div>

                            <div class="field">
                                <label for="tangki">
                                    Tangki Sumber
                                    <span class="required">*</span>
                                </label>

                                <select
                                    id="tangki"
                                    v-model="form.tangki"
                                    class="input-control"
                                    :disabled="
                                        isLoading ||
                                        !tangkisAktif.length
                                    "
                                    required
                                >
                                    <option value="">
                                        Pilih tangki sumber
                                    </option>

                                    <option
                                        v-for="item in tangkisAktif"
                                        :key="item.id"
                                        :value="item.id"
                                    >
                                        {{ item.kode }}

                                        <template v-if="item.nama">
                                            — {{ item.nama }}
                                        </template>
                                    </option>
                                </select>

                                <div
                                    v-if="selectedTangki"
                                    class="stock-info"
                                    :class="{
                                        danger: stokTidakCukup
                                    }"
                                >
                                    <div class="stock-icon">
                                        <i class="pi pi-box"></i>
                                    </div>

                                    <div class="stock-content">
                                        <span class="stock-label">
                                            Stok tersedia
                                        </span>

                                        <strong>
                                            {{ formatKg(stokTangkiKg) }}
                                            Kg
                                        </strong>
                                    </div>

                                    <i
                                        v-if="
                                            !selectedTangki.loadingSaldo &&
                                            !selectedTangki.saldoError &&
                                            stokTangkiKg > 0 &&
                                            !stokTidakCukup
                                        "
                                        class="pi pi-check-circle stock-check"
                                    ></i>

                                    <i
                                        v-else-if="
                                            selectedTangki.loadingSaldo
                                        "
                                        class="pi pi-spin pi-spinner stock-check stock-loading"
                                    ></i>

                                    <i
                                        v-else
                                        class="pi pi-exclamation-circle stock-check"
                                    ></i>
                                </div>

                                <small
                                    v-if="
                                        selectedTangki?.loadingSaldo
                                    "
                                    class="field-status"
                                >
                                    Memuat saldo tangki...
                                </small>

                                <small
                                    v-else-if="
                                        selectedTangki?.saldoError
                                    "
                                    class="field-error"
                                >
                                    {{ selectedTangki.saldoError }}
                                </small>

                                <small
                                    v-else-if="
                                        selectedTangki &&
                                        stokTangkiKg <= 0
                                    "
                                    class="field-error"
                                >
                                    Tangki tidak memiliki stok produksi.
                                </small>

                                <small
                                    v-else-if="stokTidakCukup"
                                    class="field-error"
                                >
                                    Stok tangki tidak mencukupi kebutuhan packing.
                                </small>
                            </div>
                        </div>

                        <div class="field product-field">
                            <label for="produk">
                                Nama Barang Jadi
                                <span class="required">*</span>
                            </label>

                            <div class="autocomplete-wrap">
                                <input
                                    id="produk"
                                    v-model="produkNama"
                                    type="text"
                                    class="input-control"
                                    :class="{
                                        invalid: produkError
                                    }"
                                    placeholder="Cari nama barang jadi..."
                                    autocomplete="off"
                                    :disabled="isLoading"
                                    @input="handleProdukInput"
                                    @focus="handleProdukFocus"
                                    @blur="handleProdukBlur"
                                    @keydown.down.prevent="
                                        moveProdukSuggestion(1)
                                    "
                                    @keydown.up.prevent="
                                        moveProdukSuggestion(-1)
                                    "
                                    @keydown.enter.prevent="
                                        selectFocusedProduk
                                    "
                                    @keydown.esc="
                                        closeProdukSuggestions
                                    "
                                />

                                <div
                                    v-if="showProdukSuggestions"
                                    class="suggestion-panel"
                                >
                                    <div
                                        v-if="produkLoading"
                                        class="suggestion-state"
                                    >
                                        <i class="pi pi-spin pi-spinner"></i>
                                        Mencari barang...
                                    </div>

                                    <template
                                        v-else-if="
                                            produkOptions.length
                                        "
                                    >
                                        <button
                                            v-for="(
                                                item, index
                                            ) in produkOptions"
                                            :key="item.id"
                                            type="button"
                                            class="suggestion-item"
                                            :class="{
                                                active:
                                                    produkFocusedIndex ===
                                                    index
                                            }"
                                            @mousedown.prevent="
                                                selectProduk(item)
                                            "
                                            @mouseenter="
                                                produkFocusedIndex =
                                                    index
                                            "
                                        >
                                            <div class="suggestion-icon">
                                                <i class="pi pi-box"></i>
                                            </div>

                                            <div class="suggestion-content">
                                                <strong>
                                                    {{
                                                        getProdukName(
                                                            item
                                                        )
                                                    }}
                                                </strong>

                                                <span>
                                                    {{ item.id }}
                                                </span>
                                            </div>

                                            <i
                                                class="pi pi-arrow-up-right suggestion-arrow"
                                            ></i>
                                        </button>
                                    </template>

                                    <div
                                        v-else-if="
                                            produkSearched &&
                                            produkNama.trim()
                                        "
                                        class="suggestion-state empty"
                                    >
                                        <i class="pi pi-search"></i>
                                        Barang tidak ditemukan.
                                    </div>
                                </div>
                            </div>

                            <small
                                v-if="produkResolved"
                                class="field-success"
                            >
                                <i class="pi pi-check-circle"></i>
                                Barang terpilih:
                                {{ produkTerpilihLabel }}
                            </small>

                            <small
                                v-if="produkError"
                                class="field-error"
                            >
                                {{ produkError }}
                            </small>
                        </div>
                    </section>

                    <section class="form-card">
                        <div class="section-head">
                            <div class="section-icon">
                                <i class="pi pi-box"></i>
                            </div>

                            <div>
                                <h2>Jumlah Packing</h2>

                                <p>
                                    Masukkan ukuran netto dan jumlah unit.
                                </p>
                            </div>
                        </div>

                        <div class="field-grid field-grid-3">
                            <div class="field">
                                <label for="netto">
                                    Netto / Unit
                                    <span class="required">*</span>
                                </label>

                                <select
                                    id="netto"
                                    v-model.number="form.netto"
                                    class="input-control"
                                    :disabled="isLoading"
                                    required
                                >
                                    <option :value="null">
                                        Pilih netto
                                    </option>

                                    <option
                                        v-for="value in nettoOptions"
                                        :key="value"
                                        :value="value"
                                    >
                                        {{ value }} Kg
                                    </option>
                                </select>
                            </div>

                            <div class="field">
                                <label for="totalUnit">
                                    Total Unit
                                    <span class="required">*</span>
                                </label>

                                <input
                                    id="totalUnit"
                                    v-model="form.total_unit"
                                    type="number"
                                    min="1"
                                    step="1"
                                    inputmode="numeric"
                                    class="input-control"
                                    placeholder="0"
                                    :disabled="isLoading"
                                    required
                                    @input="normalizeTotalUnit"
                                />
                            </div>

                            <div class="field">
                                <label>
                                    Total Berat
                                </label>

                                <div class="readonly-control">
                                    <span>
                                        {{ formatKg(totalKgPacking) }}
                                    </span>

                                    <span>Kg</span>
                                </div>
                            </div>
                        </div>
                    </section>

                    <section class="form-card">
                        <div class="section-head">
                            <div class="section-icon">
                                <i class="pi pi-shopping-bag"></i>
                            </div>

                            <div>
                                <h2>Kemasan</h2>

                                <p>
                                    Kemasan primer wajib digunakan. Kemasan sekunder bersifat opsional.
                                </p>
                            </div>
                        </div>

                        <div class="field-grid">
                            <div class="field">
                                <div class="label-row">
                                    <label for="kemasanPrimer">
                                        Kemasan Primer
                                        <span class="required">*</span>
                                    </label>

                                    <span class="required-label">
                                        Wajib
                                    </span>
                                </div>

                                <select
                                    id="kemasanPrimer"
                                    v-model="form.kemasan_primer"
                                    class="input-control"
                                    :disabled="
                                        isLoading ||
                                        !kemasanPrimerOptions.length
                                    "
                                    required
                                >
                                    <option value="">
                                        Pilih kemasan primer
                                    </option>

                                    <option
                                        v-for="item in kemasanPrimerOptions"
                                        :key="item.id"
                                        :value="item.id"
                                    >
                                        {{ getKemasanLabel(item) }}
                                        — Stok
                                        {{ formatUnit(item.qty_unit) }}
                                        Unit
                                    </option>
                                </select>

                                <small
                                    v-if="
                                        form.total_unit &&
                                        !kemasanPrimerOptions.length
                                    "
                                    class="field-error"
                                >
                                    Tidak ada stok Kemasan Primer yang mencukupi.
                                </small>
                            </div>

                            <div class="field">
                                <div class="label-row">
                                    <label for="kemasanSekunder">
                                        Kemasan Sekunder
                                        <span class="optional">
                                            Opsional
                                        </span>
                                    </label>

                                    <span class="optional-label">
                                        Opsional
                                    </span>
                                </div>

                                <select
                                    id="kemasanSekunder"
                                    v-model="form.kemasan_sekunder"
                                    class="input-control"
                                    :disabled="
                                        isLoading ||
                                        !kemasanSekunderOptions.length
                                    "
                                >
                                    <option value="">
                                        Tidak menggunakan kemasan sekunder
                                    </option>

                                    <option
                                        v-for="item in kemasanSekunderOptions"
                                        :key="item.id"
                                        :value="item.id"
                                    >
                                        {{ getKemasanLabel(item) }}
                                        — Stok
                                        {{ formatUnit(item.qty_unit) }}
                                        Unit
                                    </option>
                                </select>

                                <small
                                    v-if="
                                        form.kemasan_sekunder &&
                                        !kemasanSekunderTerpilih
                                    "
                                    class="field-error"
                                >
                                    Kemasan sekunder tidak valid.
                                </small>
                            </div>
                        </div>

                        <div
                            v-if="form.kemasan_sekunder"
                            class="field secondary-qty-field"
                        >
                            <label for="qtyKemasanSekunder">
                                Qty Kemasan Sekunder / Unit
                                <span class="required">*</span>
                            </label>

                            <input
                                id="qtyKemasanSekunder"
                                v-model="form.qty_kemasan_sekunder"
                                type="number"
                                min="1"
                                step="1"
                                inputmode="numeric"
                                class="input-control"
                                placeholder="0"
                                :disabled="isLoading"
                                required
                                @input="
                                    normalizeQtyKemasanSekunder
                                "
                            />

                            <small class="field-note">
                                Kebutuhan total:
                                {{
                                    formatUnit(
                                        totalKebutuhanKemasanSekunder
                                    )
                                }}
                                Unit.
                            </small>

                            <small
                                v-if="
                                    stokSekunderTidakCukup
                                "
                                class="field-error"
                            >
                                Stok Kemasan Sekunder tidak mencukupi kebutuhan.
                            </small>
                        </div>
                    </section>

                    <div class="action-row">
                        <button
                            type="button"
                            class="btn btn-secondary"
                            :disabled="isLoading"
                            @click="resetForm"
                        >
                            Reset
                        </button>

                        <button
                            type="submit"
                            class="btn btn-primary"
                            :disabled="submitDisabled"
                        >
                            <i
                                v-if="isLoading"
                                class="pi pi-spin pi-spinner"
                            ></i>

                            <i
                                v-else
                                class="pi pi-check"
                            ></i>

                            {{
                                isLoading
                                    ? 'Menyimpan...'
                                    : 'Simpan Packing'
                            }}
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import {
    computed,
    onBeforeUnmount,
    onMounted,
    reactive,
    ref,
    watch
} from 'vue'

import { usePacking } from '../composables/usePacking'
import { warehouseApi } from '../api'

const {
    isLoading,
    error,
    tangkis,
    fetchTangkisWithSaldo,
    createPacking,
    clearError
} = usePacking()

const form = reactive({
    grup: '',
    tangki: '',
    produk: null,
    kemasan_primer: '',
    kemasan_sekunder: '',
    qty_kemasan_sekunder: '',
    netto: null,
    total_unit: ''
})

const grupOptions = ref([])
const kemasanOptions = ref([])

const produkNama = ref('')
const produkOptions = ref([])
const produkLoading = ref(false)
const produkError = ref('')
const produkResolved = ref(false)
const showProdukSuggestions = ref(false)
const produkFocusedIndex = ref(-1)
const produkSearched = ref(false)

const nettoOptions = [
    30,
    25,
    20,
    12,
    5,
    1
]

let produkSearchTimer = null
let produkRequestId = 0

const normalizeList = (response) => {
    const data = response?.data ?? response

    if (Array.isArray(data)) {
        return data
    }

    if (Array.isArray(data?.results)) {
        return data.results
    }

    if (Array.isArray(data?.data)) {
        return data.data
    }

    if (Array.isArray(data?.items)) {
        return data.items
    }

    return []
}

const getEntityLabel = (item) => {
    if (!item) {
        return '-'
    }

    const kode = item.kode ?? ''

    const nama =
        item.nama ??
        item.name ??
        item.nama_entitas ??
        ''

    if (kode && nama) {
        return `${kode} — ${nama}`
    }

    return (
        nama ||
        kode ||
        `Entitas #${item.id}`
    )
}

const getKemasanLabel = (item) => {
    if (!item) {
        return '-'
    }

    return (
        item.produk_nama ??
        item.produk?.nama ??
        item.nama ??
        item.name ??
        item.kode ??
        `Kemasan #${item.id}`
    )
}

const getProdukName = (item) => {
    if (!item) {
        return ''
    }

    return (
        item.nama_item ??
        item.nama ??
        item.nama_produk ??
        item.nama_hasil ??
        item.name ??
        item.deskripsi ??
        item.kode ??
        ''
    )
}

const normalizeText = (value) => {
    return String(value ?? '')
        .trim()
        .toLowerCase()
        .replace(/\s+/g, ' ')
}

const formatKg = (value) => {
    return new Intl.NumberFormat('id-ID', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 3
    }).format(
        Number(value) || 0
    )
}

const formatUnit = (value) => {
    return new Intl.NumberFormat('id-ID', {
        maximumFractionDigits: 0
    }).format(
        Number(value) || 0
    )
}

const totalUnitNumber = computed(() => {
    const value = Number.parseInt(
        form.total_unit,
        10
    )

    return Number.isFinite(value)
        ? value
        : 0
})

const totalKgPacking = computed(() => {
    const netto = Number(form.netto)

    if (
        !Number.isFinite(netto) ||
        netto <= 0
    ) {
        return 0
    }

    return (
        netto *
        totalUnitNumber.value
    )
})

const tangkisAktif = computed(() => {
    return tangkis.value.filter(
        item =>
            item?.aktif !== false
    )
})

const selectedTangki = computed(() => {
    return (
        tangkis.value.find(
            item =>
                String(item.id) ===
                String(form.tangki)
        ) ?? null
    )
})

const stokTangkiKg = computed(() => {
    const tangki =
        selectedTangki.value

    if (!tangki) {
        return 0
    }

    const directSaldo = Number(
        tangki?.saldo_kg ??
        tangki?.saldo?.saldo_kg ??
        tangki?.saldo?.sisa_qty ??
        tangki?.saldo?.qty_kg ??
        0
    )

    if (
        Number.isFinite(directSaldo)
    ) {
        return Math.max(
            directSaldo,
            0
        )
    }

    return 0
})

const stokTidakCukup = computed(() => {
    if (
        !selectedTangki.value ||
        stokTangkiKg.value <= 0
    ) {
        return false
    }

    return (
        totalKgPacking.value > 0 &&
        totalKgPacking.value >
            stokTangkiKg.value
    )
})

const kemasanTersedia = computed(() => {
    return kemasanOptions.value.filter(
        item =>
            Number(item?.qty_unit) > 0
    )
})

const kemasanPrimerOptions = computed(() => {
    return kemasanTersedia.value
        .filter(item =>
            [
                'PRIMER',
                'PRIMER_SEKUNDER'
            ].includes(
                String(
                    item?.kategori ?? ''
                ).toUpperCase()
            )
        )
        .sort(
            (a, b) =>
                Number(b?.qty_unit || 0) -
                Number(a?.qty_unit || 0)
        )
})

const kemasanSekunderOptions = computed(() => {
    const kebutuhan =
        totalKebutuhanKemasanSekunder.value

    return kemasanTersedia.value
        .filter(item =>
            [
                'SEKUNDER',
                'PRIMER_SEKUNDER'
            ].includes(
                String(
                    item?.kategori ?? ''
                ).toUpperCase()
            )
        )
        .filter(item =>
            kebutuhan > 0
                ? Number(
                      item?.qty_unit || 0
                  ) >= kebutuhan
                : true
        )
        .sort(
            (a, b) =>
                Number(b?.qty_unit || 0) -
                Number(a?.qty_unit || 0)
        )
})

const kemasanPrimerTerpilih = computed(() => {
    return (
        kemasanOptions.value.find(
            item =>
                String(item.id) ===
                String(
                    form.kemasan_primer
                )
        ) ?? null
    )
})

const kemasanSekunderTerpilih = computed(() => {
    if (!form.kemasan_sekunder) {
        return null
    }

    return (
        kemasanOptions.value.find(
            item =>
                String(item.id) ===
                String(
                    form.kemasan_sekunder
                )
        ) ?? null
    )
})

const qtyKemasanSekunderNumber =
    computed(() => {
        const value =
            Number.parseInt(
                form.qty_kemasan_sekunder,
                10
            )

        return Number.isFinite(value)
            ? value
            : 0
    })

const totalKebutuhanKemasanSekunder =
    computed(() => {
        if (
            !form.kemasan_sekunder ||
            qtyKemasanSekunderNumber.value <=
                0
        ) {
            return 0
        }

        return (
            totalUnitNumber.value *
            qtyKemasanSekunderNumber.value
        )
    })

const stokSekunderTidakCukup =
    computed(() => {
        const sekunder =
            kemasanSekunderTerpilih.value

        if (!sekunder) {
            return false
        }

        return (
            totalKebutuhanKemasanSekunder.value >
            Number(
                sekunder.qty_unit || 0
            )
        )
    })

const produkTerpilih = computed(() => {
    if (!form.produk) {
        return null
    }

    return (
        produkOptions.value.find(
            item =>
                String(item.id) ===
                String(form.produk)
        ) ?? null
    )
})

const produkTerpilihLabel = computed(() => {
    if (produkTerpilih.value) {
        return getProdukName(
            produkTerpilih.value
        )
    }

    return produkNama.value.trim()
})

const submitDisabled = computed(() => {
    return isLoading.value
})

const normalizeTotalUnit = () => {
    let value =
        String(
            form.total_unit ?? ''
        ).replace(/[^\d]/g, '')

    if (!value) {
        form.total_unit = ''
        return
    }

    value = Number.parseInt(
        value,
        10
    )

    if (
        !Number.isFinite(value) ||
        value < 1
    ) {
        form.total_unit = ''
        return
    }

    form.total_unit = String(value)
}

const normalizeQtyKemasanSekunder = () => {
    let value =
        String(
            form.qty_kemasan_sekunder ??
                ''
        ).replace(/[^\d]/g, '')

    if (!value) {
        form.qty_kemasan_sekunder = ''
        return
    }

    value = Number.parseInt(
        value,
        10
    )

    if (
        !Number.isFinite(value) ||
        value < 1
    ) {
        form.qty_kemasan_sekunder = ''
        return
    }

    form.qty_kemasan_sekunder =
        String(value)
}

const searchProduk = async () => {
    const query =
        produkNama.value.trim()

    if (!query) {
        produkOptions.value = []
        produkSearched.value = false
        produkFocusedIndex.value = -1
        showProdukSuggestions.value =
            false

        return
    }

    const requestId =
        ++produkRequestId

    produkLoading.value = true
    produkError.value = ''
    produkSearched.value = false
    showProdukSuggestions.value = true

    try {
        const response =
            await warehouseApi.getMasterProduk({
                search: query
            })

        if (
            requestId !==
            produkRequestId
        ) {
            return
        }

        produkOptions.value =
            normalizeList(response)

        produkFocusedIndex.value = -1
        produkSearched.value = true
    } catch (err) {
        if (
            requestId !==
            produkRequestId
        ) {
            return
        }

        produkOptions.value = []
        produkSearched.value = true

        produkError.value =
            err?.response?.data
                ?.detail ??
            err?.response?.data
                ?.message ??
            'Gagal mengambil Master Items.'
    } finally {
        if (
            requestId ===
            produkRequestId
        ) {
            produkLoading.value =
                false
        }
    }
}

const handleProdukInput = () => {
    form.produk = null
    produkResolved.value = false
    produkError.value = ''
    produkSearched.value = false
    produkFocusedIndex.value = -1

    clearTimeout(
        produkSearchTimer
    )

    const query =
        produkNama.value.trim()

    if (!query) {
        produkOptions.value = []
        showProdukSuggestions.value =
            false

        return
    }

    showProdukSuggestions.value = true

    produkSearchTimer = setTimeout(
        () => {
            searchProduk()
        },
        250
    )
}

const handleProdukFocus = () => {
    if (!produkNama.value.trim()) {
        return
    }

    showProdukSuggestions.value =
        true

    if (
        !produkOptions.value.length &&
        !produkLoading.value
    ) {
        searchProduk()
    }
}

const handleProdukBlur = () => {
    setTimeout(() => {
        showProdukSuggestions.value =
            false

        produkFocusedIndex.value =
            -1
    }, 180)
}

const selectProduk = (item) => {
    if (!item?.id) {
        return
    }

    form.produk = item.id
    produkNama.value =
        getProdukName(item)
    produkResolved.value = true
    produkError.value = ''
    showProdukSuggestions.value =
        false
    produkFocusedIndex.value = -1

    produkOptions.value = [
        item,
        ...produkOptions.value.filter(
            option =>
                String(
                    option.id
                ) !== String(item.id)
        )
    ]
}

const moveProdukSuggestion = (
    direction
) => {
    if (
        !showProdukSuggestions.value ||
        !produkOptions.value.length
    ) {
        return
    }

    const total =
        produkOptions.value.length

    let nextIndex =
        produkFocusedIndex.value +
        direction

    if (nextIndex < 0) {
        nextIndex =
            total - 1
    }

    if (nextIndex >= total) {
        nextIndex = 0
    }

    produkFocusedIndex.value =
        nextIndex
}

const selectFocusedProduk = () => {
    if (!produkOptions.value.length) {
        return
    }

    if (
        produkFocusedIndex.value >= 0 &&
        produkFocusedIndex.value <
            produkOptions.value.length
    ) {
        selectProduk(
            produkOptions.value[
                produkFocusedIndex.value
            ]
        )

        return
    }

    const normalizedInput =
        normalizeText(
            produkNama.value
        )

    const exactMatch =
        produkOptions.value.find(
            item =>
                normalizeText(
                    item?.nama_item
                ) === normalizedInput ||
                normalizeText(
                    item?.nama
                ) === normalizedInput ||
                normalizeText(
                    getProdukName(item)
                ) === normalizedInput ||
                normalizeText(
                    item?.id
                ) === normalizedInput
        )

    if (exactMatch) {
        selectProduk(exactMatch)
    }
}

const closeProdukSuggestions = () => {
    showProdukSuggestions.value =
        false

    produkFocusedIndex.value =
        -1
}

const loadMasterData = async () => {
    clearError()

    try {
        const [
            grupResponse,
            kemasanResponse
        ] = await Promise.all([
            warehouseApi.getGrupAktif(),
            warehouseApi.getKemasanAktif()
        ])

        grupOptions.value =
            normalizeList(grupResponse)

        kemasanOptions.value =
            normalizeList(
                kemasanResponse
            )

        await fetchTangkisWithSaldo()
    } catch (err) {
        console.error(
            'Gagal memuat data packing:',
            err
        )
    }
}

const validateForm = async () => {
    clearError()
    produkError.value = ''

    if (!form.grup) {
        throw new Error(
            'Grup / Entitas wajib dipilih.'
        )
    }

    if (!form.tangki) {
        throw new Error(
            'Tangki sumber wajib dipilih.'
        )
    }

    if (
        selectedTangki.value?.loadingSaldo
    ) {
        throw new Error(
            'Saldo tangki masih dimuat. Tunggu sampai saldo tersedia.'
        )
    }

    if (
        selectedTangki.value?.saldoError
    ) {
        throw new Error(
            selectedTangki.value.saldoError
        )
    }

    if (!produkNama.value.trim()) {
        throw new Error(
            'Nama barang jadi wajib diisi.'
        )
    }

    if (!form.produk) {
        showProdukSuggestions.value =
            true

        throw new Error(
            'Pilih nama barang jadi dari Master Items.'
        )
    }

    if (!form.netto) {
        throw new Error(
            'Netto per unit wajib dipilih.'
        )
    }

    if (
        totalUnitNumber.value <= 0
    ) {
        throw new Error(
            'Total unit harus lebih dari 0.'
        )
    }

    if (stokTangkiKg.value <= 0) {
        throw new Error(
            `Tangki ${
                selectedTangki.value?.kode ??
                ''
            } tidak memiliki stok.`
        )
    }

    if (
        totalKgPacking.value >
        stokTangkiKg.value
    ) {
        throw new Error(
            `Stok tidak cukup. Tersedia ${formatKg(
                stokTangkiKg.value
            )} Kg, sedangkan packing membutuhkan ${formatKg(
                totalKgPacking.value
            )} Kg.`
        )
    }

    if (!form.kemasan_primer) {
        throw new Error(
            'Kemasan Primer wajib dipilih.'
        )
    }

    if (
        !kemasanPrimerTerpilih.value
    ) {
        throw new Error(
            'Kemasan Primer yang dipilih tidak ditemukan.'
        )
    }

    if (
        Number(
            kemasanPrimerTerpilih.value
                .qty_unit || 0
        ) <
        totalUnitNumber.value
    ) {
        throw new Error(
            `Stok ${
                getKemasanLabel(
                    kemasanPrimerTerpilih.value
                )
            } tidak mencukupi kebutuhan ${formatUnit(
                totalUnitNumber.value
            )} Unit.`
        )
    }

    if (form.kemasan_sekunder) {
        if (
            qtyKemasanSekunderNumber.value <=
            0
        ) {
            throw new Error(
                'Qty Kemasan Sekunder harus lebih dari 0.'
            )
        }

        if (
            !kemasanSekunderTerpilih.value
        ) {
            throw new Error(
                'Kemasan Sekunder yang dipilih tidak ditemukan.'
            )
        }

        if (
            stokSekunderTidakCukup.value
        ) {
            throw new Error(
                `Stok ${
                    getKemasanLabel(
                        kemasanSekunderTerpilih.value
                    )
                } tidak mencukupi kebutuhan ${formatUnit(
                    totalKebutuhanKemasanSekunder.value
                )} Unit.`
            )
        }
    }

    if (
        totalKgPacking.value <= 0
    ) {
        throw new Error(
            'Total berat packing harus lebih dari 0 Kg.'
        )
    }
}


const submitForm = async () => {
    try {
        await validateForm()

        const payload = {
    qty_kg: totalKgPacking.value,
    total_unit: totalUnitNumber.value,
    entitas: form.grup,
    tangki: form.tangki,
    produk: form.produk,
    kemasan_primer: form.kemasan_primer,
    kemasan_sekunder: form.kemasan_sekunder || null,
    qty_kemasan_sekunder: form.kemasan_sekunder
        ? qtyKemasanSekunderNumber.value
        : 0
}

        await createPacking(
            payload
        )

        resetForm()

        await fetchTangkisWithSaldo()
    } catch (err) {
        console.error(
            'Submit packing gagal:',
            err
        )

        const message =
            err?.response?.data
                ?.detail ??
            err?.response?.data
                ?.message ??
            err?.response?.data
                ?.pesan ??
            err?.message ??
            'Gagal menyimpan packing.'

        error.value = message
    }
}

const resetForm = () => {
    clearTimeout(
        produkSearchTimer
    )

    produkRequestId++

    form.grup = ''
    form.tangki = ''
    form.produk = null
    form.kemasan_primer = ''
    form.kemasan_sekunder = ''
    form.qty_kemasan_sekunder = ''
    form.netto = null
    form.total_unit = ''

    produkNama.value = ''
    produkOptions.value = []
    produkLoading.value = false
    produkError.value = ''
    produkResolved.value = false
    produkSearched.value = false
    showProdukSuggestions.value =
        false
    produkFocusedIndex.value = -1

    clearError()
}

const reloadData = async () => {
    await loadMasterData()
}

watch(
    () => [
        form.netto,
        form.total_unit
    ],
    () => {
        const primer =
            kemasanPrimerTerpilih.value

        if (
            primer &&
            Number(
                primer.qty_unit || 0
            ) <
                totalUnitNumber.value
        ) {
            form.kemasan_primer = ''
        }

        const sekunder =
            kemasanSekunderTerpilih.value

        if (
            sekunder &&
            totalKebutuhanKemasanSekunder.value >
                Number(
                    sekunder.qty_unit || 0
                )
        ) {
            form.kemasan_sekunder = ''
            form.qty_kemasan_sekunder =
                ''
        }
    }
)

watch(
    () => form.kemasan_sekunder,
    (value) => {
        if (!value) {
            form.qty_kemasan_sekunder =
                ''
        }
    }
)

onMounted(loadMasterData)

onBeforeUnmount(() => {
    clearTimeout(
        produkSearchTimer
    )

    produkRequestId++
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

.packing-page {
    min-height: 100%;
    padding: 28px;
    background:
        radial-gradient(
            circle at top left,
            rgba(37, 99, 235, 0.055),
            transparent 34%
        ),
        #f7f9fc;
    color: #172033;
    font-family:
        'Plus Jakarta Sans',
        Inter,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        'Segoe UI',
        sans-serif;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}

.packing-container {
    width: min(1180px, 100%);
    margin: 0 auto;
}

.page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 24px;
}

.eyebrow {
    margin-bottom: 7px;
    color: #64748b;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
}

.page-header h1 {
    margin: 0;
    color: #111827;
    font-size: 28px;
    line-height: 1.2;
    font-weight: 800;
    letter-spacing: -0.035em;
}

.page-header p {
    margin: 7px 0 0;
    color: #64748b;
    font-size: 12px;
    line-height: 1.5;
    font-weight: 500;
}

.refresh-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-height: 40px;
    padding: 0 14px;
    border: 1px solid #dce3eb;
    border-radius: 10px;
    background: #ffffff;
    color: #334155;
    font-family: inherit;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    transition:
        background 0.18s ease,
        border-color 0.18s ease,
        box-shadow 0.18s ease,
        transform 0.18s ease;
}

.refresh-btn:hover:not(:disabled) {
    border-color: #c7d0dc;
    background: #f8fafc;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
}

.refresh-btn:active:not(:disabled) {
    transform: translateY(1px);
}

.refresh-btn:disabled {
    opacity: 0.55;
    cursor: not-allowed;
}

.alert {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 18px;
    padding: 13px 15px;
    border-radius: 11px;
    font-size: 11px;
    line-height: 1.5;
    font-weight: 600;
}

.alert-danger {
    border: 1px solid #fecaca;
    background: #fef2f2;
    color: #b91c1c;
}

.form-layout {
    width: 100%;
}

.form-main {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.form-card {
    position: relative;
    padding: 22px;
    border: 1px solid #e4e9f0;
    border-radius: 17px;
    background: rgba(255, 255, 255, 0.98);
    box-shadow:
        0 4px 16px rgba(15, 23, 42, 0.035),
        0 1px 2px rgba(15, 23, 42, 0.02);
}

.section-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}

.section-icon {
    display: grid;
    place-items: center;
    width: 38px;
    height: 38px;
    flex: 0 0 38px;
    border-radius: 10px;
    background: #eef4ff;
    color: #2563eb;
    font-size: 14px;
}

.section-head h2 {
    margin: 0;
    color: #172033;
    font-size: 14px;
    line-height: 1.35;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.section-head p {
    margin: 4px 0 0;
    color: #7b8798;
    font-size: 10px;
    line-height: 1.5;
    font-weight: 500;
}

.field-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
}

.field-grid-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
}

.field {
    min-width: 0;
}

.product-field {
    position: relative;
    margin-top: 16px;
}

.secondary-qty-field {
    max-width: 50%;
    margin-top: 16px;
}

.field label {
    display: block;
    margin-bottom: 8px;
    color: #334155;
    font-size: 11px;
    line-height: 1.4;
    font-weight: 700;
}

.label-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.required {
    color: #dc2626;
}

.optional {
    display: inline-flex;
    align-items: center;
    padding: 3px 7px;
    border-radius: 999px;
    background: #f1f5f9;
    color: #64748b;
    font-size: 8px;
    line-height: 1;
    font-weight: 800;
    letter-spacing: 0.02em;
}

.required-label {
    display: inline-flex;
    align-items: center;
    padding: 3px 7px;
    border-radius: 999px;
    background: #eff6ff;
    color: #2563eb;
    font-size: 8px;
    line-height: 1;
    font-weight: 800;
    letter-spacing: 0.02em;
}

.optional-label {
    display: inline-flex;
    align-items: center;
    padding: 3px 7px;
    border-radius: 999px;
    background: #f1f5f9;
    color: #64748b;
    font-size: 8px;
    line-height: 1;
    font-weight: 800;
    letter-spacing: 0.02em;
}

.input-control,
.readonly-control {
    width: 100%;
    min-height: 44px;
    box-sizing: border-box;
    padding: 0 13px;
    border: 1px solid #d9e0e8;
    border-radius: 10px;
    background: #ffffff;
    color: #172033;
    font-family: inherit;
    font-size: 11px;
    font-weight: 600;
    outline: none;
    transition:
        border-color 0.18s ease,
        box-shadow 0.18s ease,
        background 0.18s ease;
}

.input-control::placeholder {
    color: #a1a9b6;
    font-weight: 500;
}

.input-control:hover:not(:disabled),
.readonly-control:hover {
    border-color: #c5ced9;
}

.input-control:focus {
    border-color: #7aa7ff;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08);
}

.input-control:disabled {
    background: #f8fafc;
    color: #94a3b8;
    cursor: not-allowed;
}

.input-control.invalid {
    border-color: #ef4444;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.06);
}

.readonly-control {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #f8fafc;
    color: #334155;
}

.readonly-control span:last-child {
    color: #94a3b8;
    font-weight: 700;
}

.stock-info {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 9px;
    padding: 9px 11px;
    border: 1px solid #dbe7f5;
    border-radius: 10px;
    background: #f7faff;
}

.stock-info.danger {
    border-color: #fecaca;
    background: #fff7f7;
}

.stock-icon {
    display: grid;
    place-items: center;
    width: 30px;
    height: 30px;
    flex: 0 0 30px;
    border-radius: 8px;
    background: #eaf2ff;
    color: #2563eb;
    font-size: 10px;
}

.stock-content {
    min-width: 0;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.stock-label {
    color: #7b8798;
    font-size: 8px;
    line-height: 1.2;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stock-content strong {
    color: #172033;
    font-size: 12px;
    line-height: 1.3;
    font-weight: 800;
}

.stock-info.danger .stock-icon {
    background: #fee2e2;
    color: #dc2626;
}

.stock-info.danger .stock-content strong {
    color: #b91c1c;
}

.stock-check {
    color: #16a34a;
    font-size: 13px;
}

.stock-loading {
    color: #2563eb;
}

.stock-info.danger .stock-check {
    color: #dc2626;
}

.autocomplete-wrap {
    position: relative;
    width: 100%;
}

.suggestion-panel {
    position: absolute;
    z-index: 100;
    top: calc(100% + 6px);
    right: 0;
    left: 0;
    max-height: 280px;
    overflow-y: auto;
    border: 1px solid #dce3eb;
    border-radius: 12px;
    background: #ffffff;
    box-shadow:
        0 18px 38px rgba(15, 23, 42, 0.11),
        0 4px 10px rgba(15, 23, 42, 0.04);
    scrollbar-width: thin;
}

.suggestion-panel::-webkit-scrollbar {
    width: 5px;
}

.suggestion-panel::-webkit-scrollbar-thumb {
    border-radius: 99px;
    background: #cbd5e1;
}

.suggestion-item {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border: 0;
    border-bottom: 1px solid #edf1f5;
    background: #ffffff;
    text-align: left;
    font-family: inherit;
    cursor: pointer;
    transition: background 0.15s ease;
}

.suggestion-item:last-child {
    border-bottom: 0;
}

.suggestion-item:hover,
.suggestion-item.active {
    background: #f6f8fb;
}

.suggestion-item:active {
    background: #eef3f9;
}

.suggestion-icon {
    display: grid;
    place-items: center;
    width: 32px;
    height: 32px;
    flex: 0 0 32px;
    border-radius: 9px;
    background: #eef4ff;
    color: #2563eb;
    font-size: 11px;
}

.suggestion-content {
    min-width: 0;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.suggestion-content strong {
    overflow: hidden;
    color: #172033;
    font-size: 10px;
    line-height: 1.4;
    font-weight: 800;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.suggestion-content span {
    overflow: hidden;
    color: #94a3b8;
    font-size: 8px;
    line-height: 1.4;
    font-weight: 600;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.suggestion-arrow {
    flex: 0 0 auto;
    color: #a6afbd;
    font-size: 9px;
    transition:
        color 0.15s ease,
        transform 0.15s ease;
}

.suggestion-item:hover .suggestion-arrow,
.suggestion-item.active .suggestion-arrow {
    color: #2563eb;
    transform: translate(1px, -1px);
}

.suggestion-state {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-height: 52px;
    padding: 12px;
    color: #64748b;
    font-size: 10px;
    font-weight: 600;
}

.suggestion-state.empty {
    color: #94a3b8;
}

.field-note,
.field-status,
.field-success,
.field-error {
    display: block;
    margin-top: 7px;
    font-size: 9px;
    line-height: 1.45;
    font-weight: 500;
}

.field-note {
    color: #8a95a5;
}

.field-status {
    color: #64748b;
}

.field-success {
    color: #15803d;
    font-weight: 700;
}

.field-error {
    color: #dc2626;
    font-weight: 600;
}

.action-row {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
    padding-top: 2px;
}

.btn {
    min-height: 44px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 0 18px;
    border: 1px solid transparent;
    border-radius: 10px;
    font-family: inherit;
    font-size: 10px;
    font-weight: 800;
    cursor: pointer;
    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        background 0.18s ease,
        border-color 0.18s ease;
}

.btn:hover:not(:disabled) {
    transform: translateY(-1px);
}

.btn:active:not(:disabled) {
    transform: translateY(0);
}

.btn:disabled {
    opacity: 0.55;
    cursor: not-allowed;
}

.btn-secondary {
    border-color: #dce2ea;
    background: #ffffff;
    color: #475569;
}

.btn-secondary:hover:not(:disabled) {
    background: #f8fafc;
    border-color: #cbd5e1;
}

.btn-primary {
    border-color: #2563eb;
    background: #2563eb;
    color: #ffffff;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.17);
}

.btn-primary:hover:not(:disabled) {
    border-color: #1d4ed8;
    background: #1d4ed8;
    box-shadow: 0 10px 22px rgba(37, 99, 235, 0.21);
}

input[type='number']::-webkit-inner-spin-button,
input[type='number']::-webkit-outer-spin-button {
    margin: 0;
    -webkit-appearance: none;
}

input[type='number'] {
    -moz-appearance: textfield;
}

@media (max-width: 900px) {
    .field-grid,
    .field-grid-3 {
        grid-template-columns: 1fr;
    }

    .secondary-qty-field {
        max-width: none;
    }
}

@media (max-width: 640px) {
    .packing-page {
        padding: 16px;
    }

    .page-header {
        flex-direction: column;
        gap: 14px;
    }

    .page-header h1 {
        font-size: 24px;
    }

    .refresh-btn {
        width: 100%;
    }

    .form-card {
        padding: 17px;
        border-radius: 14px;
    }

    .section-head {
        margin-bottom: 17px;
    }

    .action-row {
        flex-direction: column-reverse;
    }

    .btn {
        width: 100%;
    }

    .suggestion-panel {
        max-height: 240px;
    }
}
</style>

