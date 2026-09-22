<template>
    <div
        class="po-page flex flex-col w-full animate-fade-in relative"
    >
        <div
            class="mb-4 md:mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4"
        >
            <div>
                <p
                    class="text-[10px] text-slate-400 mb-1"
                >
                    <router-link
                        to="/accounting"
                        class="hover:text-slate-700 transition-colors"
                    >
                        Portal Akunting
                    </router-link>

                    <span class="mx-1">›</span>

                    <router-link
                        to="/accounting/input/po"
                        class="hover:text-slate-700 transition-colors"
                    >
                        Pembelian
                    </router-link>
                </p>

                <h2
                    class="text-lg md:text-xl font-bold text-slate-800 tracking-tight"
                >
                    Purchase Order
                </h2>
            </div>

            <button
                type="button"
                @click="tampilModalPO = true"
                class="w-full sm:w-auto px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-[10px] font-semibold rounded-xl transition-colors flex items-center justify-center gap-2 shadow-sm transform hover:-translate-y-0.5"
            >
                <i
                    class="pi pi-plus text-[10px]"
                ></i>

                Buat PO Baru
            </button>
        </div>

        <div
            class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6"
        >
            <div
                class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm"
            >
                <p
                    class="text-[9px] font-bold text-slate-400 uppercase tracking-wider mb-1"
                >
                    BELUM DITERIMA PENUH
                </p>

                <h3
                    class="text-xl font-black text-slate-800"
                >
                    {{ belumDiterima.length }}
                </h3>

                <p
                    class="text-[10px] text-slate-500 mt-2"
                >
                    Menunggu barang datang
                </p>
            </div>

            <div
                class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm"
            >
                <p
                    class="text-[9px] font-bold text-slate-400 uppercase tracking-wider mb-1"
                >
                    DRAFT
                </p>

                <h3
                    class="text-xl font-black text-slate-800"
                >
                    {{ draftCount }}
                </h3>

                <p
                    class="text-[10px] text-slate-500 mt-2"
                >
                    Belum diajukan / dikirim
                </p>
            </div>
        </div>

        <div
            class="bg-white border border-slate-200 rounded-[24px] p-4 md:p-6 shadow-sm w-full min-h-[400px]"
        >
            <div
                class="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4 mb-6 pb-4 border-b border-slate-100"
            >
                <div class="hidden xl:block">
                    <h3
                        class="text-xs font-bold text-slate-800"
                    >
                        Daftar PO
                    </h3>

                    <p
                        class="text-[10px] text-slate-500"
                    >
                        Terbaru di atas
                    </p>
                </div>

                <div
                    class="flex flex-col md:flex-row items-center gap-3 w-full xl:w-auto"
                >
                    <div
                        class="relative w-full md:w-64 shrink-0"
                    >
                        <i
                            class="pi pi-search absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-[10px]"
                        ></i>

                        <input
                            type="text"
                            v-model="cari"
                            placeholder="Cari nomor/supplier"
                            class="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-[10px] focus:outline-none focus:ring-2 focus:ring-slate-900 text-slate-700"
                        />
                    </div>

                    <div
                        class="flex bg-slate-50 p-1 rounded-xl w-full overflow-x-auto custom-scrollbar"
                    >
                        <button
                            v-for="tab in [
                                'semua',
                                'DRAFT',
                                'PENDING',
                                'APPROVED',
                                'TERKIRIM',
                                'DISETUJUI',
                                'DITOLAK',
                                'SEBAGIAN',
                                'SELESAI',
                                'BATAL'
                            ]"
                            :key="tab"
                            type="button"
                            @click="
                                saringStatus =
                                    tab.toLowerCase()
                            "
                            :class="
                                saringStatus ===
                                tab.toLowerCase()
                                    ? 'bg-white text-slate-800 shadow-[0_2px_8px_rgba(0,0,0,0.04)] font-bold'
                                    : 'text-slate-500 hover:text-slate-700'
                            "
                            class="px-3 py-1.5 text-[9px] rounded-lg transition-all whitespace-nowrap capitalize shrink-0"
                        >
                            {{ tab.toLowerCase() }}
                        </button>
                    </div>
                </div>
            </div>

            <div
                v-if="isLoadingDaftar"
                class="flex flex-col items-center justify-center py-12 text-center"
            >
                <i
                    class="pi pi-spin pi-spinner text-slate-300 text-xl mb-3"
                ></i>

                <p
                    class="text-[10px] text-slate-500"
                >
                    Memuat data...
                </p>
            </div>

            <div
                v-else-if="tampil.length === 0"
                class="flex flex-col items-center justify-center py-12 text-center"
            >
                <div
                    class="w-12 h-12 bg-slate-50 rounded-full flex items-center justify-center mb-3"
                >
                    <i
                        class="pi pi-inbox text-slate-400 text-lg"
                    ></i>
                </div>

                <h4
                    class="text-xs font-bold text-slate-800 mb-1"
                >
                    Tidak ada PO yang cocok
                </h4>

                <p
                    class="text-[10px] text-slate-500"
                >
                    Ubah kata kunci pencarian atau tab status.
                </p>
            </div>

            <div
                v-else
                class="overflow-x-auto custom-scrollbar pb-2"
            >
                <table
                    class="w-full text-left text-xs min-w-[880px]"
                >
                    <thead
                        class="text-slate-500 bg-slate-50/50"
                    >
                        <tr>
                            <th
                                class="py-3 px-4 font-semibold rounded-tl-xl w-[20%]"
                            >
                                No. PO
                            </th>

                            <th
                                class="py-3 px-4 font-semibold w-[15%]"
                            >
                                Tanggal
                            </th>

                            <th
                                class="py-3 px-4 font-semibold w-[25%]"
                            >
                                Supplier
                            </th>

                            <th
                                class="py-3 px-4 font-semibold w-[25%] text-center"
                            >
                                Aksi
                            </th>

                            <th
                                class="py-3 px-4 font-semibold w-[15%] text-center rounded-tr-xl"
                            >
                                Detail
                            </th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr
                            v-for="po in tampil"
                            :key="po.id"
                            class="border-b border-slate-100 hover:bg-slate-50/50 transition-colors"
                        >
                            <td
                                class="py-3 px-4 font-bold text-slate-800 whitespace-nowrap"
                            >
                                {{
                                    po.no_po ||
                                    po.nomor ||
                                    '-'
                                }}
                            </td>

                            <td
                                class="py-3 px-4 text-slate-600 whitespace-nowrap"
                            >
                                {{ po.tanggal || '-' }}
                            </td>

                            <td
                                class="py-3 px-4 text-slate-700 truncate max-w-[260px]"
                                :title="po.suplier_nama"
                            >
                                {{
                                    po.suplier_nama ||
                                    '-'
                                }}
                            </td>

                            <td
                                class="py-3 px-4 text-center"
                            >
                                <template
                                    v-if="
                                        normalizeStatus(
                                            po.status
                                        ) === 'PENDING'
                                    "
                                >
                                    <button
                                        v-if="
                                            !tampilkanKonfirmasi(
                                                po
                                            )
                                        "
                                        type="button"
                                        @click="
                                            unduhDokumenPO(
                                                po.id,
                                                po.no_po
                                            )
                                        "
                                        title="Cetak Dokumen PO"
                                        class="px-3 py-1.5 bg-white text-slate-700 border border-slate-200 hover:bg-slate-50 hover:border-slate-300 rounded-full text-[10px] font-semibold transition-all flex items-center justify-center mx-auto whitespace-nowrap shadow-sm"
                                    >
                                        <i
                                            class="pi pi-print text-[9px] mr-1.5"
                                        ></i>

                                        Cetak PO
                                    </button>

                                    <div
                                        v-else
                                        class="flex items-center justify-center gap-1.5"
                                    >
                                        <button
                                            type="button"
                                            @click.stop.prevent="
                                                handleApproval(
                                                    po
                                                )
                                            "
                                            :disabled="
                                                approvalLoadingId ===
                                                String(
                                                    po.id
                                                )
                                            "
                                            title="Approval PO"
                                            class="px-2.5 py-1.5 bg-emerald-50 text-emerald-600 hover:bg-emerald-600 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-[9px] font-semibold transition-colors flex items-center shadow-sm"
                                        >
                                            <i
                                                :class="
                                                    approvalLoadingId ===
                                                    String(
                                                        po.id
                                                    )
                                                        ? 'pi pi-spin pi-spinner'
                                                        : 'pi pi-check'
                                                "
                                                class="text-[8px] mr-1"
                                            ></i>

                                            {{
                                                approvalLoadingId ===
                                                String(
                                                    po.id
                                                )
                                                    ? 'Memproses...'
                                                    : 'Approval'
                                            }}
                                        </button>

                                        <button
                                            type="button"
                                            @click="
                                                handleDecline(
                                                    po.id
                                                )
                                            "
                                            :disabled="
                                                sedangProses
                                            "
                                            title="Decline PO"
                                            class="px-2.5 py-1.5 bg-red-50 text-red-600 hover:bg-red-600 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-[9px] font-semibold transition-colors flex items-center shadow-sm"
                                        >
                                            <i
                                                class="pi pi-times text-[8px] mr-1"
                                            ></i>

                                            Decline
                                        </button>
                                    </div>
                                </template>

                                <template
                                    v-else-if="
                                        isApprovedStatus(
                                            po.status
                                        )
                                    "
                                >
                                    <button
                                        type="button"
                                        @click.stop.prevent="
                                            handlePostPO(
                                                po
                                            )
                                        "
                                        :disabled="
                                            postLoadingId ===
                                            String(
                                                po.id
                                            )
                                        "
                                        title="Post PO ke supplier"
                                        class="px-3 py-1.5 bg-blue-50 text-blue-600 hover:bg-blue-600 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-[9px] font-semibold transition-colors flex items-center justify-center mx-auto shadow-sm"
                                    >
                                        <i
                                            :class="
                                                postLoadingId ===
                                                String(
                                                    po.id
                                                )
                                                    ? 'pi pi-spin pi-spinner'
                                                    : 'pi pi-send'
                                            "
                                            class="text-[8px] mr-1.5"
                                        ></i>

                                        {{
                                            postLoadingId ===
                                            String(
                                                po.id
                                            )
                                                ? 'Memproses...'
                                                : 'Post PO'
                                        }}
                                    </button>
                                </template>

                                <template
                                    v-else-if="
                                        normalizeStatus(
                                            po.status
                                        ) === 'TERKIRIM'
                                    "
                                >
                                    <span
                                        class="inline-flex items-center gap-1.5 px-2.5 py-1.5 bg-emerald-50 text-emerald-600 rounded-lg text-[9px] font-semibold"
                                    >
                                        <i
                                            class="pi pi-check-circle text-[9px]"
                                        ></i>

                                        Posted
                                    </span>
                                </template>

                                <template
                                    v-else-if="
                                        normalizeStatus(
                                            po.status
                                        ) === 'DITOLAK'
                                    "
                                >
                                    <span
                                        class="inline-flex items-center gap-1.5 px-2.5 py-1.5 bg-red-50 text-red-600 rounded-lg text-[9px] font-semibold"
                                    >
                                        <i
                                            class="pi pi-times-circle text-[9px]"
                                        ></i>

                                        Declined
                                    </span>
                                </template>

                                <!-- SELESAI -->
                                <template
                                    v-else-if="
                                        normalizeStatus(
                                            po.status
                                        ) === 'SELESAI'
                                    "
                                >
                                    <span
                                        class="inline-flex items-center gap-1.5 px-2.5 py-1.5 bg-slate-100 text-slate-600 rounded-lg text-[9px] font-semibold"
                                    >
                                        <i
                                            class="pi pi-check text-[9px]"
                                        ></i>

                                        Selesai
                                    </span>
                                </template>

                                <!-- STATUS LAIN -->
                                <template v-else>
                                    <button
                                        v-if="
                                            !tampilkanKonfirmasi(
                                                po
                                            )
                                        "
                                        type="button"
                                        @click="
                                            unduhDokumenPO(
                                                po.id,
                                                po.no_po
                                            )
                                        "
                                        title="Cetak Dokumen PO"
                                        class="px-3 py-1.5 bg-white text-slate-700 border border-slate-200 hover:bg-slate-50 hover:border-slate-300 rounded-full text-[10px] font-semibold transition-all flex items-center justify-center mx-auto whitespace-nowrap shadow-sm"
                                    >
                                        <i
                                            class="pi pi-print text-[9px] mr-1.5"
                                        ></i>

                                        Cetak PO
                                    </button>

                                    <span
                                        v-else
                                        class="text-[9px] text-slate-400"
                                    >
                                        Tidak ada aksi
                                    </span>
                                </template>
                            </td>

                            <td
                                class="py-3 px-4 text-center"
                            >
                                <button
                                    type="button"
                                    @click="
                                        bukaDetail(
                                            po.id
                                        )
                                    "
                                    class="px-2.5 py-1.5 bg-slate-100 text-slate-600 hover:bg-slate-800 hover:text-white rounded-lg text-[9px] font-semibold transition-colors flex items-center justify-center mx-auto whitespace-nowrap"
                                >
                                    <i
                                        class="pi pi-eye text-[8px] mr-1"
                                    ></i>

                                    Detail
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- MODAL BUAT PO -->
        <Dialog
            v-model:visible="tampilModalPO"
            modal
            appendTo="body"
            class="po-modal"
            :style="{
                width: '90vw',
                maxWidth: '980px'
            }"
            :breakpoints="{
                '768px': '96vw'
            }"
        >
            <template #header>
                <div>
                    <div
                        class="po-modal-title"
                    >
                        Buat Purchase Order Baru
                    </div>

                    <p
                        class="po-modal-subtitle"
                    >
                        Lengkapi detail pesanan pembelian.
                    </p>
                </div>
            </template>

            <LazyFormPO
                v-if="tampilModalPO"
                @close="
                    tampilModalPO = false
                "
                @saved="
                    poBerhasilDisimpan
                "
            />
        </Dialog>

        <Dialog
            v-model:visible="tampilModalDetail"
            modal
            header="Detail PO"
            :style="{
                width: '85vw',
                maxWidth: '800px'
            }"
            class="p-fluid"
        >
            <LazyDetailPO
                v-if="tampilModalDetail"
                :poId="poIdTerpilih"
            />
        </Dialog>
    </div>
</template>

<script setup>
import {
    onMounted,
    ref,
    defineAsyncComponent
} from 'vue'

import Dialog from 'primevue/dialog'

import {
    usePurchaseOrder
} from '@/features/accounting/composables/usePurchaseOrder'

import api from '@/utils/api'

const KUNCI_SUDAH_DICETAK = 'po_sudah_dicetak'

const muatTandaCetak = () => {
    try {
        const raw =
            localStorage.getItem(
                KUNCI_SUDAH_DICETAK
            )

        const data = raw
            ? JSON.parse(raw)
            : []

        return new Set(
            Array.isArray(data)
                ? data.map((id) => String(id))
                : []
        )
    } catch {
        return new Set()
    }
}

const simpanTandaCetak = (set) => {
    localStorage.setItem(
        KUNCI_SUDAH_DICETAK,
        JSON.stringify([...set])
    )
}

const tampilModalDetail = ref(false)
const poIdTerpilih = ref(null)
const tampilModalPO = ref(false)

const poSudahDiunduh =
    ref(muatTandaCetak())

const approvalLoadingId = ref(null)
const postLoadingId = ref(null)

const LazyFormPO =
    defineAsyncComponent(() =>
        import(
            '@/features/accounting/views/ProcurementCreate.vue'
        )
    )

const LazyDetailPO =
    defineAsyncComponent(() =>
        import(
            '@/features/accounting/views/PurchaseOrderDetail.vue'
        )
    )

const {
    isLoadingDaftar,
    cari,
    saringStatus,
    tampil,
    belumDiterima,
    draftCount,
    muatDaftarPO,
    approvalPO,
    declinePO,
    postPO,
    sedangProses
} = usePurchaseOrder()

onMounted(() => {
    muatDaftarPO()
})

const normalizeStatus = (status) => {
    return String(status || '')
        .trim()
        .toUpperCase()
}

const isApprovedStatus = (status) => {
    const value =
        normalizeStatus(status)

    return (
        value === 'APPROVED' ||
        value === 'DISETUJUI'
    )
}

const tampilkanKonfirmasi = (po) => {
    return poSudahDiunduh.value.has(
        String(po.id)
    )
}

const tandaiSudahDicetak = (id) => {
    poSudahDiunduh.value.add(
        String(id)
    )

    simpanTandaCetak(
        poSudahDiunduh.value
    )
}

const hapusTandaCetak = (id) => {
    poSudahDiunduh.value.delete(
        String(id)
    )

    simpanTandaCetak(
        poSudahDiunduh.value
    )
}

const bukaDetail = (id) => {
    poIdTerpilih.value = id
    tampilModalDetail.value = true
}

const poBerhasilDisimpan = async () => {
    tampilModalPO.value = false

    await muatDaftarPO()

    alert(
        'Purchase Order berhasil disimpan.'
    )
}

const unduhDokumenPO = async (
    id,
    no_po
) => {
    try {
        const fallbackName =
            no_po
                ? no_po.replace(
                    /\//g,
                    '_'
                )
                : id

        const response =
            await api.get(
                `akunting/purchase-order/${id}/cetak/`,
                {
                    responseType:
                        'blob'
                }
            )

        const url =
            window.URL.createObjectURL(
                new Blob([
                    response.data
                ])
            )

        const link =
            document.createElement(
                'a'
            )

        link.href = url

        link.setAttribute(
            'download',
            `PO_${fallbackName}.docx`
        )

        document.body.appendChild(
            link
        )

        link.click()

        document.body.removeChild(
            link
        )

        window.URL.revokeObjectURL(
            url
        )

        tandaiSudahDicetak(id)
    } catch (error) {
        console.error(
            'Gagal mengunduh dokumen:',
            error
        )

        alert(
            'Gagal mencetak dokumen. Pastikan backend sudah merender template Word-nya.'
        )
    }
}

/* =========================
   APPROVAL
========================= */

const handleApproval = async (po) => {
    const id = po?.id

    if (!id) {
        console.error(
            'ID Purchase Order tidak ditemukan.'
        )

        alert(
            'ID Purchase Order tidak ditemukan.'
        )

        return
    }

    if (
        approvalLoadingId.value !== null
    ) {
        return
    }

    approvalLoadingId.value =
        String(id)

    try {
        const res =
            await approvalPO(id)

        if (!res?.success) {
            console.error(
                'Approval gagal:',
                res?.message
            )

            alert(
                res?.message ||
                    'Gagal melakukan Approval PO.'
            )

            return
        }

        alert(
            res?.message ||
                'Purchase Order berhasil di-Approval.'
        )
    } catch (error) {
        console.error(
            'ERROR HANDLE APPROVAL:',
            error
        )

        const message =
            error?.response?.data?.detail ||
            error?.response?.data?.message ||
            error?.response?.data?.error ||
            error?.message ||
            'Terjadi kesalahan saat melakukan Approval PO.'

        alert(message)
    } finally {
        approvalLoadingId.value =
            null
    }
}

/* =========================
   POST PO
========================= */

const handlePostPO = async (po) => {
    const id = po?.id

    if (!id) {
        console.error(
            'ID Purchase Order tidak ditemukan.'
        )

        alert(
            'ID Purchase Order tidak ditemukan.'
        )

        return
    }

    if (
        postLoadingId.value !== null
    ) {
        return
    }

    postLoadingId.value =
        String(id)

    try {
        const res =
            await postPO(id)

        if (!res?.success) {
            console.error(
                'Post PO gagal:',
                res?.message
            )

            alert(
                res?.message ||
                    'Gagal melakukan Post PO ke supplier.'
            )

            return
        }

        alert(
            res?.message ||
                'Purchase Order berhasil di-Post ke supplier.'
        )
    } catch (error) {
        console.error(
            'ERROR HANDLE POST PO:',
            error
        )

        const message =
            error?.response?.data?.detail ||
            error?.response?.data?.message ||
            error?.response?.data?.error ||
            error?.message ||
            'Terjadi kesalahan saat melakukan Post PO.'

        alert(message)
    } finally {
        postLoadingId.value = null
    }
}

/* =========================
   DECLINE
========================= */

const handleDecline = async (
    id
) => {
    if (!id) {
        alert(
            'ID Purchase Order tidak ditemukan.'
        )

        return
    }

    const alasan = prompt(
        'Masukkan alasan Decline PO ini:'
    )

    if (alasan === null) {
        return
    }

    if (
        alasan.trim().length < 3
    ) {
        alert(
            'Alasan Decline harus diisi dengan jelas.'
        )

        return
    }

    try {
        const res =
            await declinePO(
                id,
                alasan.trim()
            )

        if (res?.success) {
            hapusTandaCetak(id)

            await muatDaftarPO()

            alert(
                'Purchase Order berhasil di-Decline.'
            )
        } else {
            alert(
                res?.message ||
                    'Gagal melakukan Decline PO.'
            )
        }
    } catch (error) {
        console.error(
            'ERROR DECLINE PO:',
            error
        )

        const message =
            error?.response?.data?.detail ||
            error?.response?.data?.message ||
            error?.response?.data?.error ||
            error?.message ||
            'Terjadi kesalahan saat melakukan Decline PO.'

        alert(message)
    }
}
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.custom-scrollbar::-webkit-scrollbar {
    height: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 4px;
}

.po-page {
    font-family:
        "Inter",
        "Segoe UI",
        -apple-system,
        BlinkMacSystemFont,
        sans-serif;
}
</style>

<style>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap");

.po-modal.p-dialog {
    border-radius: 16px;
    overflow: hidden;
    max-height: calc(100dvh - 48px);
    font-family:
        "Inter",
        "Segoe UI",
        -apple-system,
        BlinkMacSystemFont,
        sans-serif;
}

.po-modal .p-dialog-header {
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid #f1f5f9;
}

.po-modal-title {
    font-weight: 700;
    font-size: 0.95rem;
    color: #0f172a;
}

.po-modal-subtitle {
    margin: 0.2rem 0 0;
    font-size: 0.68rem;
    font-weight: 400;
    color: #64748b;
}

.po-modal .p-dialog-content {
    padding: 1.5rem;
    overflow-y: auto;
}
</style>

