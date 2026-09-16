import { ref } from 'vue'
import { apiInventory } from '@/services/apiInventory'

export function useStok() {
    const stokList = ref([])
    const isLoading = ref(false)

    const fetchStok = async () => {
        isLoading.value = true
        try {
            const response = await apiInventory.getStok()
            stokList.value = response.data.results || response.data || []
        } catch (error) {
        } finally {
            isLoading.value = false
        }
    }

    return { stokList, isLoading, fetchStok }
}