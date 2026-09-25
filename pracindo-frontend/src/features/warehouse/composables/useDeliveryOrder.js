import { ref } from 'vue'
import api from '@/utils/api'

export function useDeliveryOrder() {
    const isLoading = ref(false)
    const errorMsg = ref('')
    const daftarLog = ref([])

    const muatData = async (params = {}) => {
        isLoading.value = true
        errorMsg.value = ''
        try {
            const response = await api.get('warehouse/delivery-order/', { params })
            daftarLog.value = response.data?.results || response.data || []
        } catch (error) {
            console.error('Gagal memuat log DO:', error)
            errorMsg.value = 'Gagal memuat data Surat Jalan.'
            daftarLog.value = []
        } finally {
            isLoading.value = false
        }
    }

    return {
        isLoading,
        errorMsg,
        daftarLog,
        muatData
    }
}
