 import { ref } from 'vue'
import { apiKasir } from '@/services/apiKasir'

export function useRetail() {
    const posProducts = ref([])
    const pelangganList = ref([])
    const salesList = ref([])
    const isLoading = ref(false)

    const fetchPosProducts = async () => {
        isLoading.value = true

        try {
            const response = await apiKasir.getKatalog()

            posProducts.value =
                response?.data?.results ||
                response?.data ||
                []
        } catch (error) {
            console.error('Gagal mengambil katalog produk:', error)
            posProducts.value = []
        } finally {
            isLoading.value = false
        }
    }

    const fetchPelanggan = async () => {
        try {
            const response = await apiKasir.getPelanggan()

            pelangganList.value =
                response?.data?.results ||
                response?.data ||
                []
        } catch (error) {
            console.error('Gagal mengambil pelanggan:', error)
            pelangganList.value = []
        }
    }

    const fetchSales = async () => {
        try {
            const response = await apiKasir.getSales()

            salesList.value =
                response?.data?.results ||
                response?.data ||
                []
        } catch (error) {
            console.error('Gagal mengambil sales:', error)
            salesList.value = []
        }
    }

    const checkoutCart = async (payload) => {
        isLoading.value = true

        try {
            const response = await apiKasir.checkout(payload)

            return response?.data || {
                status: 'gagal',
                pesan: 'Response server tidak valid'
            }
        } catch (error) {
            console.error('Checkout gagal:', error)

            return {
                status: 'gagal',
                pesan:
                    error?.response?.data?.pesan ||
                    error?.response?.data?.detail ||
                    'Terjadi kesalahan saat memproses transaksi'
            }
        } finally {
            isLoading.value = false
        }
    }

    return {
        posProducts,
        pelangganList,
        salesList,
        isLoading,
        fetchPosProducts,
        fetchPelanggan,
        fetchSales,
        checkoutCart
    }
}
