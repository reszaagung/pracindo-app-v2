import { ref } from 'vue'
import { retailApi } from '../api'

export function usePenerimaan() {
    const doList = ref([])
    const isLoading = ref(false)

    const fetchDO = async () => {
        isLoading.value = true
        try {
            const data = await retailApi.getPenerimaan()
            doList.value = data.results || data || []
        } catch (error) {
            console.error("Gagal mengambil data DO:", error)
        } finally {
            isLoading.value = false
        }
    }

    const prosesPenerimaan = async (id, items) => {
        isLoading.value = true
        try {
            const data = await retailApi.prosesPenerimaan(id, { items })
            return data
        } catch (error) {
            console.error("Gagal proses DO:", error)
            return { 
                status: 'gagal', 
                pesan: error.response?.data?.pesan || error.response?.data?.message || 'Terjadi kesalahan sistem.' 
            }
        } finally {
            isLoading.value = false
        }
    }

    return {
        doList,
        isLoading,
        fetchDO,
        prosesPenerimaan
    }
}