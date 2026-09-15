import { ref } from 'vue'
import { retailApi } from '../api'

export function usePiutang() {
  const piutangList = ref([])
  const isLoading = ref(false)

  const fetchPiutang = async () => {
    isLoading.value = true
    try {
      const data = await retailApi.getPiutang()
      piutangList.value = data.results || data
    } catch (error) {
      console.error(error)
      alert('Terjadi kesalahan saat memuat data piutang.')
    } finally {
      isLoading.value = false
    }
  }

  const prosesBayar = async (id, payload) => {
    isLoading.value = true
    try {
      const res = await retailApi.bayarPiutang(id, payload)
      return res
    } catch (error) {
      console.error(error)
      return { 
        status: 'gagal', 
        pesan: error.response?.data?.message || 'Terjadi kesalahan sistem' 
      }
    } finally {
      isLoading.value = false
    }
  }

  return {
    piutangList,
    isLoading,
    fetchPiutang,
    prosesBayar
  }
}