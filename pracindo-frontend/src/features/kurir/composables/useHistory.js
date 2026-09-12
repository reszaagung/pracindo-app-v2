import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { apiKurir } from '../api'

export function useHistory() {
    const history = ref([])
    const isLoading = ref(false)
    const toast = useToast()

    const loadHistory = async () => {
        isLoading.value = true
        try {
            const data = await apiKurir.getMyDeliveries()
            const list = data.results || data
            
            history.value = list.filter(d => d.status === 'SELESAI')
        } catch (err) {
            toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat riwayat tugas', life: 3000 })
        } finally {
            isLoading.value = false
        }
    }

    return { history, isLoading, loadHistory }
}