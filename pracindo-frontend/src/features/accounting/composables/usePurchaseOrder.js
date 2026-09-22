import { ref, computed } from 'vue'
import api from '@/utils/api'
import { bacaError } from '@/utils/error'
import { generateKode } from '@/utils/generate_id'

export function usePurchaseOrder() {
    const daftarPO = ref([])
    const isLoadingDaftar = ref(false)
    const cari = ref('')
    const saringStatus = ref('semua')

    const listEntitas = ref([])
    const listSupplier = ref([])
    const listSatuan = ref([])

    const sedangProses = ref(false)
    const pesanError = ref('')
    const previewNomor = ref('')

    const periodeDitutup = ref(false)

    // ==========================================
    // LOAD DAFTAR PO
    // ==========================================

    const muatDaftarPO = async () => {
        isLoadingDaftar.value = true

        try {
            const { data } = await api.get(
                'akunting/purchase-order/'
            )

            daftarPO.value =
                data.results ||
                data ||
                []
        } catch (err) {
            console.error(
                'Gagal memuat daftar PO:',
                err
            )
        } finally {
            isLoadingDaftar.value = false
        }
    }

    // ==========================================
    // FILTER / SEARCH
    // ==========================================

    const tampil = computed(() => {
        const q = cari.value
            .trim()
            .toLowerCase()

        return daftarPO.value
            .filter((po) => {
                const statusFilter =
                    saringStatus.value

                if (
                    statusFilter === 'semua'
                ) {
                    return true
                }

                return (
                    (po.status || '')
                        .toLowerCase() ===
                    statusFilter
                )
            })
            .filter(
                (po) =>
                    !q ||
                    (
                        po.no_po ||
                        po.nomor ||
                        ''
                    )
                        .toLowerCase()
                        .includes(q) ||
                    (
                        po.suplier_nama ||
                        ''
                    )
                        .toLowerCase()
                        .includes(q)
            )
            .sort((a, b) => {
                return (
                    b.tanggal || ''
                ).localeCompare(
                    a.tanggal || ''
                )
            })
    })

    // ==========================================
    // SUMMARY
    // ==========================================

    const belumDiterima = computed(() =>
        daftarPO.value.filter((po) =>
            [
                'TERKIRIM',
                'DISETUJUI',
                'SEBAGIAN'
            ].includes(po.status)
        )
    )

    const draftCount = computed(() =>
        daftarPO.value.filter(
            (po) =>
                po.status === 'DRAFT'
        ).length
    )

    const totalBulanIni = computed(() => {
        const kini = new Date()

        return daftarPO.value
            .filter((po) => {
                const d = new Date(
                    po.tanggal
                )

                return (
                    d.getMonth() ===
                        kini.getMonth() &&
                    d.getFullYear() ===
                        kini.getFullYear()
                )
            })
            .reduce(
                (s, po) =>
                    s +
                    Number(
                        po.total_nilai ?? 0
                    ),
                0
            )
    })

    // ==========================================
    // MASTER DATA
    // ==========================================

    const muatDataMaster = async () => {
        sedangProses.value = true
        pesanError.value = ''

        try {
            const [
                resPortal,
                resSupplier
            ] = await Promise.all([
                api.get(
                    'auth/portal/'
                ),
                api.get(
                    'master/suplier/',
                    {
                        params: {
                            ringkas: 1,
                            aktif: true
                        }
                    }
                )
            ])

            const pd =
                resPortal.data

            listEntitas.value =
                pd?.entitas ||
                pd?.data?.entitas ||
                pd?.results ||
                pd?.data ||
                (Array.isArray(pd)
                    ? pd
                    : [])

            listSupplier.value =
                resSupplier.data?.results ||
                resSupplier.data ||
                []
        } catch (err) {
            console.error(
                'Gagal memuat master:',
                err
            )

            pesanError.value =
                bacaError(
                    err,
                    'Gagal memuat data master (Entitas/Suplier).'
                )
        } finally {
            sedangProses.value = false
        }
    }

    // ==========================================
    // PREVIEW NOMOR
    // ==========================================

    const muatPreviewNomor = async (
        entitasId,
        tanggal,
        jenis = 'BAHAN_BAKU'
    ) => {
        if (
            !entitasId ||
            !tanggal
        ) {
            previewNomor.value =
                'Pilih entitas & tanggal'

            return
        }

        try {
            const { data } =
                await api.get(
                    'akunting/purchase-order/preview-nomor/',
                    {
                        params: {
                            entitas:
                                entitasId,
                            tanggal,
                            jenis
                        }
                    }
                )

            previewNomor.value =
                data.nomor ||
                'TIDAK TERSEDIA'
        } catch {
            previewNomor.value =
                'GAGAL MEMUAT NOMOR'
        }
    }

    // ==========================================
    // CEK PERIODE
    // ==========================================

    const cekStatusPeriode = async (
        entitasId,
        tanggal
    ) => {
        if (
            !entitasId ||
            !tanggal
        ) {
            periodeDitutup.value =
                false

            return
        }

        try {
            const { data } =
                await api.get(
                    'core/periode/status/',
                    {
                        params: {
                            entitas:
                                entitasId,
                            tanggal
                        }
                    }
                )

            periodeDitutup.value =
                !data.terbuka

            if (
                periodeDitutup.value
            ) {
                pesanError.value =
                    data.pesan ||
                    'Periode akuntansi untuk entitas & tanggal ini sudah ditutup.'
            }
        } catch (err) {
            console.error(
                'Gagal mengecek status periode:',
                err
            )

            periodeDitutup.value =
                false
        }
    }

    // ==========================================
    // BUAT PRODUK BARU
    // ==========================================

    const buatProdukBaru = async (
        nama,
        jenis = 'BAHAN_BAKU'
    ) => {
        const namaProduk =
            nama.trim()

        if (!namaProduk) {
            throw new Error(
                'Nama produk wajib diisi.'
            )
        }

        if (
            !listSatuan.value.length
        ) {
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
                data.results ||
                data ||
                []
        }

        let satuanDefault = null

        if (
            jenis === 'KEMASAN'
        ) {
            satuanDefault =
                listSatuan.value.find(
                    (s) =>
                        [
                            'pcs',
                            'unit',
                            'pack'
                        ].includes(
                            s.kode?.toLowerCase()
                        )
                ) ||
                listSatuan.value[0]
        } else {
            satuanDefault =
                listSatuan.value.find(
                    (s) =>
                        s.kode?.toLowerCase() ===
                        'kg'
                ) ||
                listSatuan.value[0]
        }

        if (
            !satuanDefault
        ) {
            throw new Error(
                'Belum ada data satuan pada master.'
            )
        }

        const prefix =
            jenis === 'KEMASAN'
                ? 'PK'
                : 'RM'

        const kode =
            generateKode(
                prefix
            )

        try {
            const { data } =
                await api.post(
                    'master/produk/',
                    {
                        kode,
                        nama: namaProduk,
                        jenis,
                        satuan:
                            satuanDefault.id
                    }
                )

            return {
                id: data.id,
                kode: data.kode,
                nama: data.nama,
                satuan_kode:
                    data.satuan_kode,
                jenis: data.jenis
            }
        } catch (err) {
            throw new Error(
                bacaError(
                    err,
                    'Gagal membuat produk baru.'
                ),
                { cause: err }
            )
        }
    }

    // ==========================================
    // SIMPAN PO
    // ==========================================

    const simpanPO = async (
        form,
        isKirim = false
    ) => {
        if (periodeDitutup.value) {
            pesanError.value =
                'Tidak dapat menyimpan PO karena periode telah ditutup.'

            return {
                success: false,
                message:
                    pesanError.value
            }
        }

        sedangProses.value = true
        pesanError.value = ''

        try {
            const payloadItems =
                form.items
                    .filter(
                        (i) =>
                            i.produk_id &&
                            parseFloat(
                                i.qty_pesan
                            ) > 0
                    )
                    .map((i) => ({
                        produk_id:
                            i.produk_id,

                        qty_pesan:
                            String(
                                i.qty_pesan
                            ),

                        harga_per_kg:
                            String(
                                i.harga_per_kg ??
                                i.harga_per_unit ??
                                0
                            ),

                        satuan:
                            i.satuan ||
                            (
                                form.kategori_po ===
                                'KEMASAN'
                                    ? 'pcs'
                                    : 'kg'
                            )
                    }))

            if (
                !payloadItems.length
            ) {
                pesanError.value =
                    'Minimal harus ada 1 item dengan produk dan Qty lebih dari 0.'

                return {
                    success: false,
                    message:
                        pesanError.value
                }
            }

            const payload = {
                entitas_id:
                    form.entitas_id,

                suplier_id:
                    form.suplier_id,

                tanggal:
                    form.tanggal,

                tanggal_kirim_diminta:
                    form.tanggal_kirim_diminta ||
                    null,

                catatan:
                    form.catatan,

                pakai_ppn:
                    form.pakai_ppn,

                ppn_persen:
                    form.ppn_persen ||
                    11.00,

                kategori_po:
                    form.kategori_po ||
                    'BAHAN_BAKU',

                items:
                    payloadItems
            }

            const res =
                await api.post(
                    'akunting/purchase-order/',
                    payload
                )

            const idPO =
                res.data.id

            if (
                isKirim &&
                idPO
            ) {
                await api.post(
                    `akunting/purchase-order/${idPO}/ajukan/`
                )
            }

            await muatDaftarPO()

            return {
                success: true,
                data: res.data
            }
        } catch (err) {
            pesanError.value =
                bacaError(
                    err,
                    'Gagal menyimpan PO.'
                )

            return {
                success: false,
                message:
                    pesanError.value
            }
        } finally {
            sedangProses.value = false
        }
    }

    // ==========================================
    // AJUKAN PO
    // ==========================================

    const ajukanPO = async (
        po_id
    ) => {
        console.group(
            '📤 AJUKAN PO'
        )

        console.log(
            'PO ID:',
            po_id
        )

        sedangProses.value = true
        pesanError.value = ''

        try {
            const response =
                await api.post(
                    `akunting/purchase-order/${po_id}/ajukan/`
                )

            console.log(
                'Response ajukan:',
                response
            )

            await muatDaftarPO()

            return {
                success: true,
                message:
                    response?.data?.message ||
                    'Purchase Order berhasil diajukan.',
                data:
                    response?.data
            }
        } catch (err) {
            console.error(
                'Gagal mengajukan PO:',
                err
            )

            pesanError.value =
                bacaError(
                    err,
                    'Gagal mengajukan PO.'
                )

            return {
                success: false,
                message:
                    pesanError.value,
                data:
                    err?.response?.data ||
                    null
            }
        } finally {
            sedangProses.value = false

            console.groupEnd()
        }
    }

    // ==========================================
    // APPROVAL
    // ==========================================

    const approvalPO = async (
        po_id
    ) => {
        console.group(
            '🚀 COMPOSABLE approvalPO'
        )

        console.log(
            '1. approvalPO dipanggil'
        )

        console.log(
            '2. po_id:',
            po_id
        )

        const endpoint =
            `akunting/purchase-order/${po_id}/setujui/`

        console.log(
            '3. endpoint:',
            endpoint
        )

        // Validasi ID
        if (
            po_id === null ||
            po_id === undefined ||
            po_id === ''
        ) {
            console.error(
                '❌ po_id kosong'
            )

            console.groupEnd()

            return {
                success: false,
                message:
                    'ID Purchase Order tidak ditemukan.',
                data: null
            }
        }

        sedangProses.value = true
        pesanError.value = ''

        try {
            console.log(
                '4. Mengirim POST approval...'
            )

            const response =
                await api.post(
                    endpoint
                )

            console.log(
                '5. Response API:',
                response
            )

            console.log(
                '6. Response data:',
                response?.data
            )

            const data =
                response?.data

            /*
             * Backend mungkin mengembalikan:
             *
             * {
             *   success: true,
             *   message: "..."
             * }
             *
             * atau hanya object PO.
             *
             * Yang penting:
             * HTTP request sukses = approval berhasil,
             * kecuali backend secara eksplisit
             * mengembalikan success: false.
             */

            if (
                data?.success === false
            ) {
                const message =
                    data?.message ||
                    data?.detail ||
                    'Approval Purchase Order gagal.'

                console.error(
                    '❌ Backend mengembalikan success=false:',
                    message
                )

                pesanError.value =
                    message

                return {
                    success: false,
                    message,
                    data
                }
            }

            console.log(
                '7. POST approval berhasil'
            )

            /*
             * Reload daftar PO setelah
             * approval berhasil.
             */
            console.log(
                '8. Memuat ulang daftar PO...'
            )

            await muatDaftarPO()

            console.log(
                '9. Daftar PO berhasil dimuat ulang'
            )

            const message =
                data?.message ||
                data?.detail ||
                'Purchase Order berhasil di-Approval.'

            console.log(
                '✅ Approval sukses:',
                message
            )

            return {
                success: true,
                message,
                data
            }
        } catch (err) {
            console.error(
                '🔥 ERROR approvalPO:',
                err
            )

            console.error(
                '🔥 status:',
                err?.response?.status
            )

            console.error(
                '🔥 response.data:',
                err?.response?.data
            )

            console.error(
                '🔥 error.message:',
                err?.message
            )

            const message =
                err?.response?.data?.detail ||
                err?.response?.data?.message ||
                err?.response?.data?.error ||
                bacaError(
                    err,
                    'Gagal melakukan Approval PO.'
                )

            pesanError.value =
                message

            return {
                success: false,
                message,
                data:
                    err?.response?.data ||
                    null,
                error: err
            }
        } finally {
            sedangProses.value = false

            console.log(
                '10. approvalPO selesai'
            )

            console.log(
                'sedangProses:',
                sedangProses.value
            )

            console.groupEnd()
        }
    }

    // ==========================================
    // DECLINE
    // ==========================================

    const declinePO = async (
        po_id,
        alasan
    ) => {
        console.group(
            '🔴 DECLINE PO'
        )

        console.log(
            'PO ID:',
            po_id
        )

        console.log(
            'Alasan:',
            alasan
        )

        sedangProses.value = true
        pesanError.value = ''

        try {
            const response =
                await api.post(
                    `akunting/purchase-order/${po_id}/tolak/`,
                    {
                        alasan
                    }
                )

            console.log(
                'Response decline:',
                response
            )

            await muatDaftarPO()

            return {
                success: true,
                message:
                    response?.data?.message ||
                    response?.data?.detail ||
                    'Purchase Order berhasil di-Decline.',
                data:
                    response?.data
            }
        } catch (err) {
            console.error(
                'Gagal melakukan Decline PO:',
                err
            )

            console.error(
                'Response error:',
                err?.response?.data
            )

            pesanError.value =
                bacaError(
                    err,
                    'Gagal melakukan Decline PO.'
                )

            return {
                success: false,
                message:
                    pesanError.value,
                data:
                    err?.response?.data ||
                    null
            }
        } finally {
            sedangProses.value = false

            console.groupEnd()
        }
    }

    const postPO = async (po_id) => {
        sedangProses.value = true
        pesanError.value = ''

        if (
            po_id === null ||
            po_id === undefined ||
            po_id === ''
        ) {
            sedangProses.value = false

            return {
                success: false,
                message:
                    'ID Purchase Order tidak ditemukan.',
                data: null
            }
        }

        try {
            const response =
                await api.post(
                    `akunting/purchase-order/${po_id}/kirim/`
                )

            const data =
                response?.data

            if (
                data?.success === false
            ) {
                const message =
                    data?.message ||
                    data?.detail ||
                    'Gagal melakukan Post Purchase Order.'

                pesanError.value =
                    message

                return {
                    success: false,
                    message,
                    data
                }
            }

            await muatDaftarPO()

            return {
                success: true,
                message:
                    data?.message ||
                    data?.detail ||
                    'Purchase Order berhasil di-Post ke supplier.',
                data
            }
        } catch (err) {
            console.error(
                'Gagal melakukan Post PO:',
                err
            )

            const message =
                err?.response?.data?.detail ||
                err?.response?.data?.message ||
                err?.response?.data?.error ||
                bacaError(
                    err,
                    'Gagal melakukan Post PO ke Suplier.'
                )

            pesanError.value =
                message

            return {
                success: false,
                message,
                data:
                    err?.response?.data ||
                    null
            }
        } finally {
            sedangProses.value = false
        }
    }

    const batalkanPO = async (
        po_id,
        alasan
    ) => {
        console.group(
            '⚫ BATALKAN PO'
        )

        console.log(
            'PO ID:',
            po_id
        )

        console.log(
            'Alasan:',
            alasan
        )

        sedangProses.value = true
        pesanError.value = ''

        try {
            const response =
                await api.post(
                    `akunting/purchase-order/${po_id}/batalkan/`,
                    {
                        alasan
                    }
                )

            console.log(
                'Response batalkan:',
                response
            )

            await muatDaftarPO()

            return {
                success: true,
                message:
                    response?.data?.message ||
                    response?.data?.detail ||
                    'Purchase Order berhasil dibatalkan.',
                data:
                    response?.data
            }
        } catch (err) {
            console.error(
                'Gagal membatalkan PO:',
                err
            )

            console.error(
                'Response error:',
                err?.response?.data
            )

            pesanError.value =
                bacaError(
                    err,
                    'Gagal membatalkan PO.'
                )

            return {
                success: false,
                message:
                    pesanError.value,
                data:
                    err?.response?.data ||
                    null
            }
        } finally {
            sedangProses.value = false

            console.groupEnd()
        }
    }

    return {
        daftarPO,
        isLoadingDaftar,
        cari,
        saringStatus,
        tampil,
        belumDiterima,
        draftCount,
        totalBulanIni,
        muatDaftarPO,

        listEntitas,
        listSupplier,
        sedangProses,

        pesanError,
        previewNomor,
        muatDataMaster,
        muatPreviewNomor,

        buatProdukBaru,
        simpanPO,

        periodeDitutup,
        cekStatusPeriode,

        ajukanPO,

        approvalPO,
        declinePO,
        postPO,

        setujuiPO: approvalPO,
        tolakPO: declinePO,
        kirimPO: postPO,

        batalkanPO
    }
}