import { ref } from 'vue'
import warehouseApi from '../api'
import { bacaError } from '@/utils/error'

const normalizeList = (data) => {
    if (Array.isArray(data)) {
        return data
    }

    if (Array.isArray(data?.results)) {
        return data.results
    }

    return []
}

const isValidId = (id) => {
    if (id === null || id === undefined || id === '') {
        return false
    }

    const value = String(id).trim()

    return value !== '' && value !== 'undefined' && value !== 'null'
}

export function useDiscrepancy() {
    const daftarSelisih = ref([])
    const isLoading = ref(false)
    const error = ref('')

    let jumlahRequestAktif = 0

    const mulaiRequest = () => {
        jumlahRequestAktif += 1
        isLoading.value = true
    }

    const selesaiRequest = () => {
        jumlahRequestAktif = Math.max(0, jumlahRequestAktif - 1)
        isLoading.value = jumlahRequestAktif > 0
    }

    const bersihkanError = () => {
        error.value = ''
    }

    const setError = (err, fallback) => {
        error.value = bacaError(err, fallback)
    }

    const muatLaporan = async (params = {}) => {
        mulaiRequest()
        bersihkanError()

        try {
            const response = await warehouseApi.getLaporanSelisih(params)

            daftarSelisih.value = normalizeList(response?.data)

            return {
                success: true,
                data: daftarSelisih.value,
            }
        } catch (err) {
            setError(err, 'Gagal memuat laporan selisih.')

            return {
                success: false,
                data: [],
                message: error.value,
            }
        } finally {
            selesaiRequest()
        }
    }

    const muatSelisihTerbuka = async (params = {}) => {
        mulaiRequest()
        bersihkanError()

        try {
            const response = await warehouseApi.getSelisihTerbuka(params)

            daftarSelisih.value = normalizeList(response?.data)

            return {
                success: true,
                data: daftarSelisih.value,
            }
        } catch (err) {
            setError(err, 'Gagal memuat selisih terbuka.')

            return {
                success: false,
                data: [],
                message: error.value,
            }
        } finally {
            selesaiRequest()
        }
    }

    const buatLaporanManual = async (payload) => {
        if (!payload || typeof payload !== 'object') {
            const message = 'Data laporan selisih tidak valid.'
            error.value = message

            return {
                success: false,
                data: null,
                message,
            }
        }

        mulaiRequest()
        bersihkanError()

        try {
            const response = await warehouseApi.buatLaporanManual(payload)

            return {
                success: true,
                data: response?.data ?? null,
            }
        } catch (err) {
            setError(err, 'Gagal membuat laporan selisih.')

            return {
                success: false,
                data: null,
                message: error.value,
            }
        } finally {
            selesaiRequest()
        }
    }

    const ajukan = async (id, catatan = '') => {
        if (!isValidId(id)) {
            const message = 'ID laporan selisih tidak valid.'
            error.value = message

            return {
                success: false,
                data: null,
                message,
            }
        }

        mulaiRequest()
        bersihkanError()

        try {
            const response = await warehouseApi.ajukanKlaim(id, catatan)

            return {
                success: true,
                data: response?.data ?? null,
            }
        } catch (err) {
            setError(err, 'Gagal mengajukan klaim selisih.')

            return {
                success: false,
                data: null,
                message: error.value,
            }
        } finally {
            selesaiRequest()
        }
    }

    const reset = () => {
        daftarSelisih.value = []
        isLoading.value = false
        error.value = ''
        jumlahRequestAktif = 0
    }

    return {
        daftarSelisih,
        isLoading,
        error,
        muatLaporan,
        muatSelisihTerbuka,
        buatLaporanManual,
        ajukan,
        reset,
        bersihkanError,
    }
}