import { computed, ref } from 'vue'
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

    const muatDaftarPO = async () => {
        isLoadingDaftar.value = true

        try {
            const { data } = await api.get(
                'akunting/purchase-order/'
            )

            daftarPO.value =
                data?.results ||
                data ||
                []
        } catch (err) {
            console.error(
                'Gagal memuat daftar PO:',
                err
            )

            daftarPO.value = []
        } finally {
            isLoadingDaftar.value = false
        }
    }

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
                    String(
                        po?.status || ''
                    ).toLowerCase() ===
                    statusFilter
                )
            })
            .filter((po) => {
                if (!q) {
                    return true
                }

                const nomor =
                    String(
                        po?.no_po ||
                        po?.nomor ||
                        ''
                    ).toLowerCase()

                const supplier =
                    String(
                        po?.suplier_nama ||
                        ''
                    ).toLowerCase()

                return (
                    nomor.includes(q) ||
                    supplier.includes(q)
                )
            })
            .sort((a, b) =>
                String(
                    b?.tanggal || ''
                ).localeCompare(
                    String(
                        a?.tanggal || ''
                    )
                )
            )
    })

    const belumDiterima = computed(() =>
        daftarPO.value.filter((po) =>
            [
                'TERKIRIM',
                'DISETUJUI',
                'SEBAGIAN'
            ].includes(po?.status)
        )
    )

    const draftCount = computed(() =>
        daftarPO.value.filter(
            (po) =>
                po?.status === 'DRAFT'
        ).length
    )

    const totalBulanIni = computed(() => {
        const kini = new Date()

        return daftarPO.value
            .filter((po) => {
                const tanggal =
                    po?.tanggal

                if (!tanggal) {
                    return false
                }

                const d =
                    new Date(tanggal)

                if (
                    Number.isNaN(
                        d.getTime()
                    )
                ) {
                    return false
                }

                return (
                    d.getMonth() ===
                        kini.getMonth() &&
                    d.getFullYear() ===
                        kini.getFullYear()
                )
            })
            .reduce(
                (total, po) =>
                    total +
                    Number(
                        po?.total_nilai ?? 0
                    ),
                0
            )
    })

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

            const portal =
                resPortal?.data

            listEntitas.value =
                portal?.entitas ||
                portal?.data?.entitas ||
                portal?.results ||
                portal?.data ||
                (
                    Array.isArray(
                        portal
                    )
                        ? portal
                        : []
                )

            const supplier =
                resSupplier?.data

            listSupplier.value =
                supplier?.results ||
                (
                    Array.isArray(
                        supplier
                    )
                        ? supplier
                        : []
                )
        } catch (err) {
            console.error(
                'Gagal memuat master:',
                err
            )

            listEntitas.value = []
            listSupplier.value = []

            pesanError.value =
                bacaError(
                    err,
                    'Gagal memuat data master (Entitas/Suplier).'
                )
        } finally {
            sedangProses.value = false
        }
    }

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
                data?.nomor ||
                'TIDAK TERSEDIA'
        } catch (err) {
            console.error(
                'Gagal memuat preview nomor PO:',
                err
            )

            previewNomor.value =
                'GAGAL MEMUAT NOMOR'
        }
    }

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
                !data?.terbuka

            if (
                periodeDitutup.value
            ) {
                pesanError.value =
                    data?.pesan ||
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

    const buatProdukBaru = async (
        nama,
        jenis = 'BAHAN_BAKU'
    ) => {
        const namaProduk =
            String(nama || '').trim()

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
                data?.results ||
                data ||
                []
        }

        let satuanDefault = null

        if (
            jenis === 'KEMASAN'
        ) {
            satuanDefault =
                listSatuan.value.find(
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
                ) ||
                listSatuan.value[0]
        } else {
            satuanDefault =
                listSatuan.value.find(
                    (satuan) =>
                        String(
                            satuan?.kode ||
                            ''
                        ).toLowerCase() ===
                        'kg'
                ) ||
                listSatuan.value[0]
        }

        if (
            !satuanDefault?.id
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
            generateKode(prefix)

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
                id: data?.id,
                kode: data?.kode,
                nama: data?.nama,
                satuan_kode:
                    data?.satuan_kode,
                jenis: data?.jenis
            }
        } catch (err) {
            throw new Error(
                bacaError(
                    err,
                    'Gagal membuat produk baru.'
                ),
                {
                    cause: err
                }
            )
        }
    }

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
                (
                    Array.isArray(
                        form?.items
                    )
                        ? form.items
                        : []
                )
                    .filter(
                        (item) =>
                            item?.produk_id &&
                            parseFloat(
                                item?.qty_pesan
                            ) > 0
                    )
                    .map((item) => ({
                        produk_id:
                            item.produk_id,
                        qty_pesan:
                            String(
                                item.qty_pesan
                            ),
                        harga_per_kg:
                            String(
                                item?.harga_per_kg ??
                                item?.harga_per_unit ??
                                0
                            ),
                        satuan:
                            item?.satuan ||
                            (
                                form?.kategori_po ===
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
                    form?.entitas_id,

                suplier_id:
                    form?.suplier_id,

                tanggal:
                    form?.tanggal,

                tanggal_kirim_diminta:
                    form?.tanggal_kirim_diminta ||
                    null,

                catatan:
                    form?.catatan,

                pakai_ppn:
                    form?.pakai_ppn,

                ppn_persen:
                    form?.ppn_persen ||
                    11.00,

                kategori_po:
                    form?.kategori_po ||
                    'BAHAN_BAKU',

                items:
                    payloadItems
            }

            const response =
                await api.post(
                    'akunting/purchase-order/',
                    payload
                )

            const idPO =
                response?.data?.id

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
                data:
                    response?.data ||
                    null
            }
        } catch (err) {
            console.error(
                'Gagal menyimpan PO:',
                err
            )

            pesanError.value =
                bacaError(
                    err,
                    'Gagal menyimpan PO.'
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
        }
    }

    const ajukanPO = async (
        po_id
    ) => {
        if (
            po_id === null ||
            po_id === undefined ||
            po_id === ''
        ) {
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
            const response =
                await api.post(
                    `akunting/purchase-order/${po_id}/ajukan/`
                )

            await muatDaftarPO()

            return {
                success: true,
                message:
                    response?.data?.message ||
                    'Purchase Order berhasil diajukan.',
                data:
                    response?.data ||
                    null
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
        }
    }

    const approvalPO = async (
        po_id
    ) => {
        if (
            po_id === null ||
            po_id === undefined ||
            po_id === ''
        ) {
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
            const response =
                await api.post(
                    `akunting/purchase-order/${po_id}/setujui/`
                )

            const data =
                response?.data

            if (
                data?.success === false
            ) {
                const message =
                    data?.message ||
                    data?.detail ||
                    'Approval Purchase Order gagal.'

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
                    'Purchase Order berhasil di-Approval.',
                data:
                    data || null
            }
        } catch (err) {
            console.error(
                'Gagal melakukan Approval PO:',
                err
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
        }
    }

    const declinePO = async (
        po_id,
        alasan
    ) => {
        if (
            po_id === null ||
            po_id === undefined ||
            po_id === ''
        ) {
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
            const response =
                await api.post(
                    `akunting/purchase-order/${po_id}/tolak/`,
                    {
                        alasan
                    }
                )

            await muatDaftarPO()

            return {
                success: true,
                message:
                    response?.data?.message ||
                    response?.data?.detail ||
                    'Purchase Order berhasil di-Decline.',
                data:
                    response?.data ||
                    null
            }
        } catch (err) {
            console.error(
                'Gagal melakukan Decline PO:',
                err
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
        }
    }

    const postPO = async (
        po_id
    ) => {
        if (
            po_id === null ||
            po_id === undefined ||
            po_id === ''
        ) {
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
                data:
                    data || null
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
        if (
            po_id === null ||
            po_id === undefined ||
            po_id === ''
        ) {
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
            const response =
                await api.post(
                    `akunting/purchase-order/${po_id}/batalkan/`,
                    {
                        alasan
                    }
                )

            await muatDaftarPO()

            return {
                success: true,
                message:
                    response?.data?.message ||
                    response?.data?.detail ||
                    'Purchase Order berhasil dibatalkan.',
                data:
                    response?.data ||
                    null
            }
        } catch (err) {
            console.error(
                'Gagal membatalkan PO:',
                err
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