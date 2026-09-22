import { ref } from 'vue'
import { warehouseApi } from '../api'

export function usePacking() {
    const packings = ref([])
    const tangkis = ref([])
    const isLoading = ref(false)
    const error = ref(null)

    const getErrorMessage = (
        err,
        fallback = 'Terjadi kesalahan.'
    ) => {
        const data = err?.response?.data

        if (typeof data === 'string') {
            return data
        }

        if (data?.pesan) {
            return data.pesan
        }

        if (data?.detail) {
            return data.detail
        }

        if (data?.message) {
            return data.message
        }

        if (data && typeof data === 'object') {
            const messages = Object.entries(data)
                .flatMap(([field, value]) => {
                    if (Array.isArray(value)) {
                        return value.map(
                            msg => `${field}: ${msg}`
                        )
                    }

                    if (typeof value === 'string') {
                        return `${field}: ${value}`
                    }

                    return []
                })
                .filter(Boolean)

            if (messages.length) {
                return messages.join('\n')
            }
        }

        return err?.message || fallback
    }

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

    const normalizeSaldo = (response) => {
        const data = response?.data ?? response

        if (!data) {
            return {
                saldo_kg: 0,
                harga_per_kg: 0,
                nilai: 0
            }
        }

        if (Array.isArray(data)) {
            return {
                saldo_kg: data.reduce(
                    (total, item) =>
                        total +
                        Number(
                            item?.saldo_kg ??
                            item?.sisa_qty ??
                            item?.qty_kg ??
                            item?.qty ??
                            0
                        ),
                    0
                ),
                harga_per_kg: 0,
                nilai: data.reduce(
                    (total, item) =>
                        total +
                        Number(
                            item?.nilai ??
                            item?.saldo_nilai ??
                            0
                        ),
                    0
                )
            }
        }

        const nested =
            data?.data &&
            typeof data.data === 'object' &&
            !Array.isArray(data.data)
                ? data.data
                : data

        return {
            saldo_kg: Number(
                nested?.saldo_kg ??
                nested?.sisa_qty ??
                nested?.qty_kg ??
                nested?.qty ??
                0
            ),
            harga_per_kg: Number(
                nested?.harga_per_kg ??
                nested?.harga_rata ??
                nested?.harga ??
                0
            ),
            nilai: Number(
                nested?.nilai ??
                nested?.saldo_nilai ??
                nested?.total_nilai ??
                0
            )
        }
    }

    const normalizeTangki = (item) => ({
        ...item,
        loadingSaldo: Boolean(item?.aktif),
        saldo: {
            saldo_kg: 0,
            harga_per_kg: 0,
            nilai: 0
        },
        saldo_kg: 0,
        harga_per_kg: 0,
        saldo_nilai: 0,
        saldoError: ''
    })

    const fetchPackings = async (
        params = {}
    ) => {
        isLoading.value = true
        error.value = null

        try {
            const response =
                await warehouseApi.getRiwayatPacking(
                    params
                )

            packings.value =
                normalizeList(response)

            return packings.value
        } catch (err) {
            const message =
                getErrorMessage(
                    err,
                    'Gagal memuat riwayat packing.'
                )

            error.value = message

            console.error(
                'Gagal memuat riwayat packing:',
                err
            )

            throw err
        } finally {
            isLoading.value = false
        }
    }

    const fetchTangkisWithSaldo =
        async () => {
            isLoading.value = true
            error.value = null

            try {
                const response =
                    await warehouseApi.getTangkiProduksi()

                const dataTangki =
                    normalizeList(response)

                tangkis.value =
                    dataTangki.map(
                        normalizeTangki
                    )

                const tangkiAktif =
                    tangkis.value.filter(
                        tangki =>
                            tangki?.aktif !== false
                    )

                await Promise.all(
                    tangkiAktif.map(
                        async tangki => {
                            try {
                                const saldoResponse =
                                    await warehouseApi.getSaldoTangki(
                                        tangki.id
                                    )

                                const saldo =
                                    normalizeSaldo(
                                        saldoResponse
                                    )

                                tangki.saldo =
                                    saldo

                                tangki.saldo_kg =
                                    saldo.saldo_kg

                                tangki.harga_per_kg =
                                    saldo.harga_per_kg

                                tangki.saldo_nilai =
                                    saldo.nilai

                                tangki.saldoError =
                                    ''
                            } catch (err) {
                                tangki.saldo = {
                                    saldo_kg: 0,
                                    harga_per_kg: 0,
                                    nilai: 0
                                }

                                tangki.saldo_kg = 0
                                tangki.harga_per_kg = 0
                                tangki.saldo_nilai = 0

                                tangki.saldoError =
                                    getErrorMessage(
                                        err,
                                        'Gagal memuat saldo tangki.'
                                    )

                                console.error(
                                    `Gagal memuat saldo tangki ${tangki.kode || tangki.id}:`,
                                    err
                                )
                            } finally {
                                tangki.loadingSaldo =
                                    false
                            }
                        }
                    )
                )

                return tangkis.value
            } catch (err) {
                const message =
                    getErrorMessage(
                        err,
                        'Gagal memuat data tangki produksi.'
                    )

                error.value = message

                console.error(
                    'Gagal memuat tangki produksi:',
                    err
                )

                throw err
            } finally {
                isLoading.value = false
            }
        }

    const createPacking = async (
        payload
    ) => {
        if (
            !payload ||
            typeof payload !== 'object'
        ) {
            const invalidError =
                new Error(
                    'Payload packing tidak valid.'
                )

            error.value =
                invalidError.message

            throw invalidError
        }

        isLoading.value = true
        error.value = null

        try {
            const response =
                await warehouseApi.simpanPacking(
                    payload
                )

            return (
                response?.data ??
                response
            )
        } catch (err) {
            const message =
                getErrorMessage(
                    err,
                    'Gagal menyimpan eksekusi packing.'
                )

            error.value = message

            console.error(
                'Gagal menyimpan eksekusi packing:',
                err
            )

            throw new Error(
                message,
                {
                    cause: err
                }
            )
        } finally {
            isLoading.value = false
        }
    }

    const clearError = () => {
        error.value = null
    }

    return {
        packings,
        tangkis,
        isLoading,
        error,
        fetchPackings,
        fetchTangkisWithSaldo,
        createPacking,
        clearError
    }
}
