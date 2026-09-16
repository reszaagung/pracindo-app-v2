import { ref } from 'vue'
import { apiInventory } from '@/services/apiInventory'

export function usePenerimaan() {
    const doList = ref([])
    const isLoading = ref(false)

    const fetchDO = async () => {
        isLoading.value = true
        try {
            const response = await apiInventory.getPenerimaan()
            doList.value = response.data.results || response.data || []
        } catch (error) {
        } finally {
            isLoading.value = false
        }
    }

    const prosesPenerimaan = async (id, items) => {
        isLoading.value = true
        try {
            const response = await apiInventory.prosesPenerimaan(id, { items })
            return response.data
        } catch (error) {
            return {
                status: 'gagal',
                pesan: error.response?.data?.pesan || 'Terjadi kesalahan sistem.'
            }
        } finally {
            isLoading.value = false
        }
    }

    return { doList, isLoading, fetchDO, prosesPenerimaan }
}