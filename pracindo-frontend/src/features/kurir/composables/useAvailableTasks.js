import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { apiKurir } from '../api' 

export function useAvailableTasks() {
    const tasks = ref([])
    const isLoading = ref(false)
    const claimingId = ref(null)
    const toast = useToast()

    const loadTasks = async () => {
        isLoading.value = true
        try {
            const data = await apiKurir.getAvailableTasks()
            tasks.value = data.results || data
        } catch (err) {
            toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat kolam tugas', life: 3000 })
        } finally {
            isLoading.value = false
        }
    }

    const claim = async (id) => {
        claimingId.value = id
        try {
            await apiKurir.claimTask(id)
            toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Tugas berhasil diklaim!', life: 3000 })
            await loadTasks()
            return true
        } catch (err) {
            const errorMsg = err.response?.data?.detail || 'Terjadi kesalahan saat klaim'
            toast.add({ severity: 'error', summary: 'Gagal Klaim', detail: errorMsg, life: 3000 })
            return false
        } finally {
            claimingId.value = null
        }
    }

    return { tasks, isLoading, claimingId, loadTasks, claim }
}