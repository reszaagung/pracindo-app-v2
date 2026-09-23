<template>
    <Dialog
        :visible="true"
        modal
        dismissableMask
        :draggable="false"
        :closable="false"
        :showHeader="false"
        :breakpoints="{ '960px': '92vw', '640px': '96vw' }"
        class="produk-modal"
        @update:visible="emit('close')"
    >
        <div class="produk-shell">
            <div class="produk-header">
                <div class="header-main">
                    <div class="header-icon">
                        <i class="pi pi-box"></i>
                    </div>

                    <div class="header-content">
                        <div class="eyebrow">MASTER DATA</div>
                        <h2>Tambah Produk</h2>
                        <p>
                            Daftarkan produk baru ke master data dan hubungkan
                            supplier yang sesuai.
                        </p>
                    </div>
                </div>

                <button
                    type="button"
                    class="close-button"
                    aria-label="Tutup"
                    @click="emit('close')"
                >
                    <i class="pi pi-times"></i>
                </button>
            </div>

            <div v-if="props.suplierId && suplierTerpilih" class="supplier-context">
                <div class="supplier-context-icon">
                    <i class="pi pi-building"></i>
                </div>

                <div class="supplier-context-content">
                    <span class="context-label">SUPPLIER TRANSAKSI</span>
                    <strong>{{ suplierTerpilih.nama }}</strong>
                    <span v-if="suplierTerpilih.kode" class="context-code">
                        {{ suplierTerpilih.kode }}
                    </span>
                </div>

                <div class="supplier-context-badge">
                    <i class="pi pi-link"></i>
                    Terikat
                </div>
            </div>

            <form class="produk-form" @submit.prevent="simpanProduk">
                <div v-if="errorMsg" class="error-panel">
                    <div class="error-icon">
                        <i class="pi pi-exclamation-triangle"></i>
                    </div>

                    <div class="error-content">
                        <strong>Produk belum dapat disimpan</strong>
                        <span>{{ errorMsg }}</span>
                    </div>

                    <button
                        type="button"
                        class="error-close"
                        @click="errorMsg = ''"
                    >
                        <i class="pi pi-times"></i>
                    </button>
                </div>

                <div class="form-section">
                    <div class="section-heading">
                        <div>
                            <h3>Informasi Produk</h3>
                            <p>Lengkapi identitas utama produk.</p>
                        </div>

                        <span class="required-note">
                            <span>*</span> Wajib diisi
                        </span>
                    </div>

                    <div class="field-grid">
                        <div class="field">
                            <label for="kode_produk">
                                Kode Produk
                                <span>*</span>
                            </label>

                            <div class="input-with-prefix">
                                <span class="input-prefix">SKU</span>

                                <InputText
                                    id="kode_produk"
                                    v-model="form.kode"
                                    class="w-full"
                                    placeholder="Contoh: RM-001"
                                    autocomplete="off"
                                    maxlength="50"
                                    :disabled="isSubmitting"
                                    @input="form.kode = form.kode.toUpperCase()"
                                />
                            </div>

                            <small>
                                Gunakan kode unik agar produk mudah dicari.
                            </small>
                        </div>

                        <div class="field">
                            <label for="nama_produk">
                                Nama Produk
                                <span>*</span>
                            </label>

                            <InputText
                                id="nama_produk"
                                v-model="form.nama"
                                class="w-full"
                                placeholder="Contoh: Tepung Terigu Premium"
                                autocomplete="off"
                                maxlength="150"
                                :disabled="isSubmitting"
                            />

                            <small>
                                Gunakan nama yang konsisten dengan katalog.
                            </small>
                        </div>

                        <div class="field">
                            <label for="jenis_produk">
                                Jenis Produk
                                <span>*</span>
                            </label>

                            <Dropdown
                                id="jenis_produk"
                                v-model="form.jenis"
                                :options="opsiJenis"
                                optionLabel="label"
                                optionValue="value"
                                class="w-full"
                                placeholder="Pilih jenis produk"
                                :disabled="isSubmitting"
                            />

                            <small>
                                Tentukan klasifikasi utama produk.
                            </small>
                        </div>

                        <div class="field">
                            <label for="satuan_produk">
                                Satuan
                                <span>*</span>
                            </label>

                            <Dropdown
                                id="satuan_produk"
                                v-model="form.satuan_id"
                                :options="daftarSatuan"
                                optionLabel="nama"
                                optionValue="id"
                                class="w-full"
                                placeholder="Pilih satuan"
                                filter
                                :loading="loadingMaster"
                                :disabled="isSubmitting || loadingMaster"
                            />

                            <small>
                                Satuan yang digunakan dalam transaksi.
                            </small>
                        </div>
                    </div>
                </div>

                <div class="section-divider">
                    <span></span>
                    <i class="pi pi-link"></i>
                    <span></span>
                </div>

                <div class="form-section">
                    <div class="section-heading">
                        <div>
                            <h3>Katalog Supplier</h3>
                            <p>
                                Hubungkan produk dengan supplier yang dapat
                                memasoknya.
                            </p>
                        </div>

                        <span
                            v-if="props.suplierId"
                            class="supplier-required-badge"
                        >
                            Supplier transaksi wajib
                        </span>
                    </div>

                    <div class="supplier-selection">
                        <div class="supplier-selection-header">
                            <div class="supplier-selection-icon">
                                <i class="pi pi-users"></i>
                            </div>

                            <div>
                                <strong>Supplier terkait produk</strong>
                                <span>
                                    Produk dapat digunakan untuk lebih dari
                                    satu supplier.
                                </span>
                            </div>
                        </div>

                        <MultiSelect
                            v-model="form.suplier_ids"
                            :options="listSuplier"
                            optionLabel="nama"
                            optionValue="id"
                            class="w-full supplier-select"
                            placeholder="Pilih supplier"
                            display="chip"
                            filter
                            :loading="loadingMaster"
                            :disabled="isSubmitting || loadingMaster"
                            :maxSelectedLabels="3"
                        >
                            <template #option="{ option }">
                                <div class="supplier-option">
                                    <div class="supplier-option-icon">
                                        <i class="pi pi-building"></i>
                                    </div>

                                    <div class="supplier-option-content">
                                        <strong>{{ option.nama }}</strong>

                                        <span v-if="option.kode">
                                            {{ option.kode }}
                                        </span>
                                    </div>

                                    <i
                                        v-if="props.suplierId && String(option.id) === String(props.suplierId)"
                                        class="pi pi-link supplier-option-linked"
                                    ></i>
                                </div>
                            </template>

                            <template #chip="{ value }">
                                <div class="supplier-chip">
                                    <i class="pi pi-building"></i>
                                    <span>
                                        {{
                                            listSuplier.find(
                                                supplier =>
                                                    String(supplier.id) === String(value)
                                            )?.nama || value
                                        }}
                                    </span>
                                </div>
                            </template>
                        </MultiSelect>

                        <div class="selection-status">
                            <div class="status-item">
                                <i class="pi pi-check-circle"></i>
                                <span>
                                    {{ form.suplier_ids.length }}
                                    supplier terpilih
                                </span>
                            </div>

                            <div
                                v-if="props.suplierId"
                                class="status-item status-item-primary"
                            >
                                <i class="pi pi-link"></i>
                                <span>Supplier transaksi otomatis terhubung</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="form-section compact-section">
                    <div class="active-card">
                        <div class="active-card-icon">
                            <i class="pi pi-check-circle"></i>
                        </div>

                        <div class="active-card-content">
                            <strong>Status Produk</strong>
                            <span>
                                Produk aktif dan dapat digunakan dalam
                                transaksi.
                            </span>
                        </div>

                        <label class="switch">
                            <input
                                v-model="form.aktif"
                                type="checkbox"
                                :disabled="isSubmitting"
                            />
                            <span class="switch-slider"></span>
                        </label>
                    </div>
                </div>

                <div v-if="loadingMaster" class="loading-panel">
                    <div class="loading-spinner"></div>
                    <span>Menyiapkan master data...</span>
                </div>

                <div class="produk-footer">
                    <div class="footer-info">
                        <i class="pi pi-shield"></i>
                        <span>
                            Data akan tersimpan ke master produk.
                        </span>
                    </div>

                    <div class="footer-actions">
                        <Button
                            type="button"
                            label="Batal"
                            severity="secondary"
                            text
                            :disabled="isSubmitting"
                            @click="emit('close')"
                        />

                        <Button
                            type="submit"
                            :label="isSubmitting ? 'Menyimpan...' : 'Simpan Produk'"
                            icon="pi pi-check"
                            :loading="isSubmitting"
                            :disabled="!formValid || loadingMaster"
                            class="save-button"
                        />
                    </div>
                </div>
            </form>
        </div>
    </Dialog>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Dropdown from 'primevue/dropdown'
import MultiSelect from 'primevue/multiselect'
import api from '@/utils/api'
import { useProduct } from '@/features/master/composables/useProduct'

const props = defineProps({
    suplierId: {
        type: [Number, String],
        default: null
    }
})

const emit = defineEmits(['close', 'saved'])

const { addProduk } = useProduct()

const isSubmitting = ref(false)
const loadingMaster = ref(false)
const errorMsg = ref('')
const daftarSatuan = ref([])
const listSuplier = ref([])

const opsiJenis = [
    { label: 'Bahan Baku', value: 'BAHAN_BAKU' },
    { label: 'Barang Jadi', value: 'BARANG_JADI' },
    { label: 'Kemasan', value: 'KEMASAN' },
    { label: 'Lain-lain', value: 'LAIN' }
]

const form = reactive({
    kode: '',
    nama: '',
    jenis: 'BAHAN_BAKU',
    satuan_id: null,
    suplier_ids: [],
    aktif: true
})

const suplierTerpilih = computed(() => {
    if (!props.suplierId) return null

    return (
        listSuplier.value.find(
            supplier => String(supplier.id) === String(props.suplierId)
        ) || null
    )
})

const supplierWajib = computed(() => Boolean(props.suplierId))

const formValid = computed(() => {
    const informasiValid =
        form.kode.trim().length > 0 &&
        form.nama.trim().length > 0 &&
        Boolean(form.jenis) &&
        Boolean(form.satuan_id)

    if (!informasiValid) {
        return false
    }

    if (supplierWajib.value && form.suplier_ids.length === 0) {
        return false
    }

    return true
})

const sinkronkanSuplierDefault = () => {
    if (!props.suplierId) {
        return
    }

    const sudahTerpilih = form.suplier_ids.some(
        id => String(id) === String(props.suplierId)
    )

    if (!sudahTerpilih) {
        form.suplier_ids.unshift(props.suplierId)
    }
}

const loadDataMaster = async () => {
    loadingMaster.value = true
    errorMsg.value = ''

    try {
        const [satuanResponse, supplierResponse] = await Promise.all([
            api.get('master/satuan/', {
                params: {
                    aktif: true
                }
            }),
            api.get('master/suplier/', {
                params: {
                    ringkas: 1,
                    aktif: true
                }
            })
        ])

        daftarSatuan.value =
            satuanResponse.data?.results ||
            satuanResponse.data ||
            []

        listSuplier.value =
            supplierResponse.data?.results ||
            supplierResponse.data ||
            []

        const satuanKg = daftarSatuan.value.find(
            satuan =>
                String(satuan.kode || '').toLowerCase() === 'kg' ||
                String(satuan.nama || '').toLowerCase() === 'kilogram'
        )

        if (!form.satuan_id && satuanKg) {
            form.satuan_id = satuanKg.id
        }

        sinkronkanSuplierDefault()
    } catch (err) {
        console.error('Gagal memuat master data produk:', err)

        errorMsg.value =
            err.response?.data?.detail ||
            err.response?.data?.message ||
            'Master data produk gagal dimuat. Silakan coba kembali.'
    } finally {
        loadingMaster.value = false
    }
}

const simpanProduk = async () => {
    if (!formValid.value || isSubmitting.value) {
        return
    }

    isSubmitting.value = true
    errorMsg.value = ''

    try {
        const payload = {
            kode: form.kode.trim().toUpperCase(),
            nama: form.nama.trim(),
            jenis: form.jenis,
            satuan: form.satuan_id,
            suplier: form.suplier_ids,
            aktif: form.aktif
        }

        const result = await addProduk(payload)

        if (result.success) {
            emit('saved', result.data)
            return
        }

        errorMsg.value =
            result.message ||
            'Gagal menyimpan produk. Silakan periksa kembali data yang diisi.'
    } catch (err) {
        console.error('Gagal menyimpan produk:', err)

        errorMsg.value =
            err.response?.data?.detail ||
            err.response?.data?.message ||
            'Terjadi kesalahan saat menyimpan produk.'
    } finally {
        isSubmitting.value = false
    }
}

watch(
    () => props.suplierId,
    () => {
        sinkronkanSuplierDefault()
    }
)

onMounted(() => {
    loadDataMaster()
})
</script>

<style scoped>

.produk-shell {
    width: 100%;
    overflow: hidden;
    border-radius: 20px;
    background: #ffffff;
}

.produk-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
    padding: 26px 28px 24px;
    background:
        radial-gradient(circle at top right, rgba(59, 130, 246, 0.12), transparent 38%),
        linear-gradient(135deg, #f8fbff 0%, #ffffff 65%);
    border-bottom: 1px solid #e9eef5;
}

.header-main {
    display: flex;
    align-items: flex-start;
    gap: 16px;
}

.header-icon {
    width: 48px;
    height: 48px;
    flex: 0 0 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    color: #ffffff;
    font-size: 1.15rem;
    box-shadow: 0 10px 24px rgba(37, 99, 235, 0.22);
}

.header-content .eyebrow {
    margin-bottom: 5px;
    color: #64748b;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.14em;
}

.header-content h2 {
    margin: 0;
    color: #0f172a;
    font-size: 1.45rem;
    font-weight: 800;
    line-height: 1.2;
}

.header-content p {
    max-width: 620px;
    margin: 6px 0 0;
    color: #64748b;
    font-size: 0.86rem;
    line-height: 1.55;
}

.close-button {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 36px;
    border: 0;
    border-radius: 10px;
    background: #f1f5f9;
    color: #64748b;
    cursor: pointer;
    transition: 0.2s ease;
}

.close-button:hover {
    background: #e2e8f0;
    color: #0f172a;
    transform: rotate(4deg);
}

.supplier-context {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 20px 28px 0;
    padding: 14px 16px;
    border: 1px solid #bfdbfe;
    border-radius: 14px;
    background: linear-gradient(135deg, #eff6ff, #f8fbff);
}

.supplier-context-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 40px;
    border-radius: 11px;
    background: #dbeafe;
    color: #2563eb;
}

.supplier-context-content {
    min-width: 0;
    display: flex;
    flex-direction: column;
}

.context-label {
    margin-bottom: 2px;
    color: #64748b;
    font-size: 0.64rem;
    font-weight: 800;
    letter-spacing: 0.09em;
}

.supplier-context-content strong {
    overflow: hidden;
    color: #0f172a;
    font-size: 0.92rem;
    font-weight: 700;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.context-code {
    color: #64748b;
    font-size: 0.74rem;
    margin-top: 1px;
}

.supplier-context-badge {
    margin-left: auto;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 10px;
    flex: 0 0 auto;
    border: 1px solid #bfdbfe;
    border-radius: 999px;
    background: #ffffff;
    color: #2563eb;
    font-size: 0.72rem;
    font-weight: 700;
}

.produk-form {
    padding: 26px 28px 28px;
}

.error-panel {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 24px;
    padding: 13px 14px;
    border: 1px solid #fecaca;
    border-radius: 13px;
    background: #fff7f7;
    color: #991b1b;
}

.error-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 32px;
    border-radius: 9px;
    background: #fee2e2;
}

.error-content {
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.error-content strong {
    font-size: 0.8rem;
}

.error-content span {
    color: #b91c1c;
    font-size: 0.78rem;
    line-height: 1.5;
}

.error-close {
    margin-left: auto;
    border: 0;
    background: transparent;
    color: #991b1b;
    cursor: pointer;
    padding: 2px;
}

.form-section {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.compact-section {
    margin-top: 18px;
}

.section-heading {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
}

.section-heading h3 {
    margin: 0;
    color: #0f172a;
    font-size: 0.98rem;
    font-weight: 800;
}

.section-heading p {
    margin: 4px 0 0;
    color: #64748b;
    font-size: 0.79rem;
    line-height: 1.5;
}

.required-note {
    color: #94a3b8;
    font-size: 0.72rem;
    white-space: nowrap;
}

.required-note span {
    color: #ef4444;
}

.supplier-required-badge {
    padding: 5px 9px;
    border: 1px solid #bfdbfe;
    border-radius: 999px;
    background: #eff6ff;
    color: #2563eb;
    font-size: 0.68rem;
    font-weight: 700;
    white-space: nowrap;
}

.field-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
}

.field {
    display: flex;
    min-width: 0;
    flex-direction: column;
    gap: 7px;
}

.field label {
    color: #334155;
    font-size: 0.79rem;
    font-weight: 700;
}

.field label span {
    color: #ef4444;
}

.field small {
    color: #94a3b8;
    font-size: 0.7rem;
    line-height: 1.4;
}

.input-with-prefix {
    display: flex;
    align-items: stretch;
}

.input-prefix {
    display: flex;
    align-items: center;
    padding: 0 11px;
    border: 1px solid #dbe3ed;
    border-right: 0;
    border-radius: 9px 0 0 9px;
    background: #f8fafc;
    color: #64748b;
    font-size: 0.69rem;
    font-weight: 800;
    letter-spacing: 0.04em;
}

.input-with-prefix :deep(.p-inputtext) {
    border-radius: 0 9px 9px 0;
}

.field :deep(.p-inputtext),
.field :deep(.p-dropdown),
.field :deep(.p-multiselect) {
    min-height: 42px;
    border-radius: 9px;
    border-color: #dbe3ed;
    box-shadow: none;
}

.field :deep(.p-inputtext:enabled:focus),
.field :deep(.p-dropdown:not(.p-disabled).p-focus),
.field :deep(.p-multiselect:not(.p-disabled).p-focus) {
    border-color: #60a5fa;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.section-divider {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 25px 0;
    color: #cbd5e1;
}

.section-divider span {
    height: 1px;
    flex: 1;
    background: #e2e8f0;
}

.section-divider i {
    font-size: 0.72rem;
    color: #94a3b8;
}

.supplier-selection {
    padding: 16px;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    background: #fbfdff;
}

.supplier-selection-header {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 13px;
}

.supplier-selection-icon {
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 34px;
    border-radius: 9px;
    background: #eef2ff;
    color: #4f46e5;
}

.supplier-selection-header strong {
    display: block;
    color: #1e293b;
    font-size: 0.8rem;
    font-weight: 750;
}

.supplier-selection-header span {
    display: block;
    margin-top: 2px;
    color: #94a3b8;
    font-size: 0.7rem;
}

.supplier-select :deep(.p-multiselect-label) {
    padding-top: 7px;
    padding-bottom: 7px;
}

.supplier-select :deep(.p-multiselect-token) {
    border-radius: 7px;
    background: #eff6ff;
    color: #1d4ed8;
}

.supplier-option {
    display: flex;
    align-items: center;
    width: 100%;
    gap: 10px;
    padding: 2px 0;
}

.supplier-option-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 32px;
    border-radius: 8px;
    background: #f1f5f9;
    color: #64748b;
}

.supplier-option-content {
    min-width: 0;
    display: flex;
    flex-direction: column;
}

.supplier-option-content strong {
    overflow: hidden;
    color: #334155;
    font-size: 0.78rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.supplier-option-content span {
    color: #94a3b8;
    font-size: 0.66rem;
}

.supplier-option-linked {
    margin-left: auto;
    color: #2563eb;
    font-size: 0.78rem;
}

.supplier-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.supplier-chip i {
    font-size: 0.68rem;
}

.selection-status {
    display: flex;
    flex-wrap: wrap;
    gap: 10px 16px;
    margin-top: 11px;
}

.status-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #64748b;
    font-size: 0.68rem;
}

.status-item i {
    color: #10b981;
    font-size: 0.72rem;
}

.status-item-primary {
    color: #2563eb;
}

.status-item-primary i {
    color: #2563eb;
}

.active-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 15px;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    background: #f8fafc;
}

.active-card-icon {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 36px;
    border-radius: 10px;
    background: #dcfce7;
    color: #16a34a;
}

.active-card-content {
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.active-card-content strong {
    color: #334155;
    font-size: 0.8rem;
}

.active-card-content span {
    color: #94a3b8;
    font-size: 0.69rem;
}

.switch {
    position: relative;
    width: 46px;
    height: 26px;
    margin-left: auto;
    flex: 0 0 46px;
    cursor: pointer;
}

.switch input {
    position: absolute;
    opacity: 0;
    pointer-events: none;
}

.switch-slider {
    position: absolute;
    inset: 0;
    border-radius: 999px;
    background: #cbd5e1;
    transition: 0.2s ease;
}

.switch-slider::before {
    content: "";
    position: absolute;
    width: 20px;
    height: 20px;
    top: 3px;
    left: 3px;
    border-radius: 50%;
    background: #ffffff;
    box-shadow: 0 2px 5px rgba(15, 23, 42, 0.18);
    transition: 0.2s ease;
}

.switch input:checked + .switch-slider {
    background: #10b981;
}

.switch input:checked + .switch-slider::before {
    transform: translateX(20px);
}

.loading-panel {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    margin-top: 18px;
    padding: 11px;
    border-radius: 10px;
    background: #f8fafc;
    color: #64748b;
    font-size: 0.72rem;
}

.loading-spinner {
    width: 15px;
    height: 15px;
    border: 2px solid #dbeafe;
    border-top-color: #2563eb;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

.produk-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    margin-top: 26px;
    padding-top: 20px;
    border-top: 1px solid #e2e8f0;
}

.footer-info {
    display: flex;
    align-items: center;
    gap: 7px;
    color: #94a3b8;
    font-size: 0.7rem;
}

.footer-info i {
    color: #64748b;
}

.footer-actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

.save-button {
    min-width: 155px;
}

:deep(.produk-modal.p-dialog) {
    overflow: hidden;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    box-shadow:
        0 24px 64px rgba(15, 23, 42, 0.14),
        0 8px 24px rgba(15, 23, 42, 0.07);
}

:deep(.produk-modal .p-dialog-content) {
    padding: 0;
    border-radius: 20px;
}

:deep(.p-button) {
    border-radius: 9px;
}

:deep(.p-button.p-button-text.p-button-secondary) {
    color: #64748b;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

@media (max-width: 700px) {
    .produk-header {
        padding: 21px 18px 19px;
    }

    .produk-form {
        padding: 20px 18px 20px;
    }

    .supplier-context {
        margin: 16px 18px 0;
    }

    .field-grid {
        grid-template-columns: 1fr;
    }

    .section-heading {
        flex-direction: column;
        gap: 7px;
    }

    .supplier-context-badge {
        display: none;
    }

    .produk-footer {
        align-items: stretch;
        flex-direction: column;
    }

    .footer-actions {
        justify-content: flex-end;
    }
}

@media (max-width: 480px) {
    .header-content h2 {
        font-size: 1.2rem;
    }

    .header-content p {
        font-size: 0.78rem;
    }

    .header-icon {
        width: 42px;
        height: 42px;
        flex-basis: 42px;
    }

    .supplier-context {
        align-items: flex-start;
    }

    .footer-actions {
        width: 100%;
    }

    .footer-actions :deep(.p-button) {
        flex: 1;
    }
}

</style>