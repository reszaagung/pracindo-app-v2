import { ref } from 'vue'
import warehouseApi from '../api'
import { bacaError } from '@/utils/error'

const isValidId = (id) => {
    if (id === null || id === undefined || id === '') {
        return false
    }

    const value = String(id).trim()

    return value !== '' && value !== 'undefined' && value !== 'null'
}

const normalizeList = (data) => {
    if (Array.isArray(data)) {
        return data
    }

    if (Array.isArray(data?.results)) {
        return data.results
    }

    return []
}

export function usePackageReceipt() {
    const daftarPOKemasan = ref([])
    const daftarPenerimaan = ref([])
    const ringkasan = ref(null)
    const sedangProses = ref(false)
    const galat = ref('')

    let jumlahRequestAktif = 0

    const mulaiRequest = () => {
        jumlahRequestAktif += 1
        sedangProses.value = true
    }

    const selesaiRequest = () => {
        jumlahRequestAktif = Math.max(0, jumlahRequestAktif - 1)
        sedangProses.value = jumlahRequestAktif > 0
    }

    const bersihkanError = () => {
        galat.value = ''
    }

    const setError = (err, fallback) => {
        galat.value = bacaError(err, fallback)
    }

    const muatPOKemasan = async (params = {}) => {
        mulaiRequest()

        try {
            const response = await warehouseApi.getPOSiapTerima({
                ...params,
                kategori: 'kemasan',
            })

            daftarPOKemasan.value = normalizeList(response?.data)
        } catch (err) {
            setError(
                err,
                'Gagal memuat PO kemasan siap terima.'
            )
        } finally {
            selesaiRequest()
        }
    }

    const muatPenerimaan = async (params = {}) => {
        mulaiRequest()

        try {
            const response = await warehouseApi.getPenerimaan({
                ...params,
                kategori: 'kemasan',
            })

            daftarPenerimaan.value = normalizeList(response?.data)
        } catch (err) {
            setError(
                err,
                'Gagal memuat daftar penerimaan kemasan.'
            )
        } finally {
            selesaiRequest()
        }
    }

    const muatRingkasan = async (id) => {
        if (!isValidId(id)) {
            console.warn(
                '[usePackageReceipt] muatRingkasan dibatalkan: ID tidak valid.',
                id
            )

            ringkasan.value = null

            return {
                success: false,
                message: 'ID penerimaan tidak valid.',
            }
        }

        mulaiRequest()
        bersihkanError()

        try {
            const response =
                await warehouseApi.getRingkasanPenerimaan(id)

            ringkasan.value = response?.data ?? null

            return {
                success: true,
                data: ringkasan.value,
            }
        } catch (err) {
            setError(
                err,
                'Gagal memuat detail ringkasan kemasan.'
            )

            return {
                success: false,
                data: null,
                message: galat.value,
            }
        } finally {
            selesaiRequest()
        }
    }

    const simpanPenerimaan = async (payload) => {
        mulaiRequest()
        bersihkanError()

        try {
            const response =
                await warehouseApi.simpanPenerimaan({
                    ...payload,
                    kategori: 'kemasan',
                })

            return {
                success: true,
                data: response?.data ?? null,
            }
        } catch (err) {
            setError(
                err,
                'Gagal menyimpan penerimaan kemasan.'
            )

            return {
                success: false,
                data: null,
                message: galat.value,
            }
        } finally {
            selesaiRequest()
        }
    }

    const muatSemua = async (params = {}) => {
        bersihkanError()

        await Promise.all([
            muatPOKemasan(params),
            muatPenerimaan(params),
        ])
    }

    const reset = () => {
        daftarPOKemasan.value = []
        daftarPenerimaan.value = []
        ringkasan.value = null
        galat.value = ''
        jumlahRequestAktif = 0
        sedangProses.value = false
    }

    return {
        daftarPOKemasan,
        daftarPenerimaan,
        ringkasan,
        sedangProses,
        galat,
        muatPOKemasan,
        muatPenerimaan,
        muatRingkasan,
        simpanPenerimaan,
        muatSemua,
        reset,
        bersihkanError,
    }
}