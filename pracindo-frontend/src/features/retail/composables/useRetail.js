import { ref } from 'vue'
import { retailApi }  from '../api'

export function useRetail() {
  const posProducts = ref([])
  const pelangganList = ref([])
  const salesList = ref([])
  const riwayat = ref([])
  const isLoading = ref(false)

  const fetchPosProducts = async () => {
    isLoading.value = true
    try {
      const data = await retailApi.getKatalog()
      posProducts.value = data
    } catch (error) {
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  const fetchPelanggan = async () => {
    try {
      const data = await retailApi.getPelanggan()
      pelangganList.value = data.results || data
    } catch (error) {
      console.error(error)
    }
  }

  const fetchSales = async () => {
    try {
      const data = await retailApi.getSales()
      salesList.value = data.results || data
    } catch (error) {
      console.error(error)
    }
  }

  const checkoutCart = async (payload) => {
    isLoading.value = true
    try {
      const res = await retailApi.checkout(payload)
      return res
    } catch (error) {
      return { 
        status: 'gagal', 
        pesan: error.response?.data?.message || 'Terjadi kesalahan server' 
      }
    } finally {
      isLoading.value = false
    }
  }

  const fetchRiwayat = async () => {
    try {
      const data = await retailApi.getRiwayat()
      riwayat.value = data.results || data
    } catch (error) {
      console.error(error)
    }
  }

  return {
    posProducts,
    pelangganList,
    salesList,
    riwayat,
    isLoading,
    fetchPosProducts,
    fetchPelanggan,
    fetchSales,
    checkoutCart,
    fetchRiwayat
  }
}