import { ref } from 'vue'
import { apiKasir } from '@/services/apiKasir'

export function useKasir() {
    const posProducts = ref([])
    const pelangganList = ref([])
    const salesList = ref([])
    const riwayat = ref([])
    const sesiAktif = ref(null)
    const isLoading = ref(false)

    const fetchPosProducts = async () => {
        isLoading.value = true
        try {
            const response = await apiKasir.getKatalog()
            posProducts.value = response.data.results || response.data || []
        } catch (error) {
            posProducts.value = []
        } finally {
            isLoading.value = false
        }
    }

    const fetchPelanggan = async () => {
        try {
            const response = await apiKasir.getPelanggan()
            pelangganList.value = response.data.results || response.data || []
        } catch (error) { }
    }

    const fetchSales = async () => {
        try {
            const response = await apiKasir.getSales()
            salesList.value = response.data.results || response.data || []
        } catch (error) { }
    }

    const fetchSesi = async () => {
        try {
            const response = await apiKasir.getSesiAktif()
            if (response.data && response.data.status !== 'TIDAK_ADA_SHIFT') {
                sesiAktif.value = response.data
            } else {
                sesiAktif.value = null
            }
        } catch (error) {
            sesiAktif.value = null
        }
    }

    const fetchRiwayat = async () => {
        try {
            const response = await apiKasir.getRiwayat()
            riwayat.value = response.data.results || response.data || []
        } catch (error) { }
    }

    const checkoutCart = async (payload) => {
        isLoading.value = true
        try {
            const response = await apiKasir.checkout(payload)
            return response.data
        } catch (error) {
            return {
                status: 'gagal',
                pesan: error.response?.data?.pesan || error.response?.data?.detail || 'Terjadi kesalahan'
            }
        } finally {
            isLoading.value = false
        }
    }

    const tutupShift = async () => {
        isLoading.value = true
        try {
            const response = await apiKasir.tutupShift()
            sesiAktif.value = null
            return response.data
        } catch (error) {
            throw error
        } finally {
            isLoading.value = false
        }
    }

    return {
        posProducts,
        pelangganList,
        salesList,
        riwayat,
        sesiAktif,
        isLoading,
        fetchPosProducts,
        fetchPelanggan,
        fetchSales,
        fetchSesi,
        fetchRiwayat,
        checkoutCart,
        tutupShift
    }
}