import { ref } from 'vue'
import { apiKurir } from '../api'

export function useMyDeliveries() {
    const deliveries = ref([])
    const isLoading = ref(false)

    const loadDeliveries = async () => {
        isLoading.value = true
        try {
            deliveries.value = await apiKurir.getMyDeliveries()
        } catch (error) {
            console.error(error)
        } finally {
            isLoading.value = false
        }
    }

    const startDelivery = async (deliveryId) => {
        try {
            await apiKurir.startDelivery(deliveryId)
            await loadDeliveries()
        } catch (error) {
            console.error(error)
        }
    }

    const markArrived = async (deliveryId, stopId) => {
        try {
            await apiKurir.markArrived(deliveryId, stopId)
            await loadDeliveries()
        } catch (error) {
            console.error(error)
        }
    }

    const uploadProof = async (deliveryId, stopId, file, jenisDokumen) => {
        try {
            const formData = new FormData()
            formData.append('file', file)
            formData.append('jenis_dokumen', jenisDokumen)

            await apiKurir.uploadProof(deliveryId, stopId, formData)
            await loadDeliveries()
            return true
        } catch (error) {
            console.error(error)
            return false
        }
    }

    return { 
        deliveries, 
        isLoading, 
        loadDeliveries, 
        startDelivery, 
        markArrived, 
        uploadProof 
    }
}