import { ref } from 'vue'
import { apiKurir } from '../api'

export function useAvailableTasks() {
    const tasks = ref([])
    const isLoading = ref(false)
    const claimingId = ref(null)

    const loadTasks = async () => {
        isLoading.value = true
        try {
            tasks.value = await apiKurir.getAvailableTasks()
        } catch (error) {
            console.error(error)
        } finally {
            isLoading.value = false
        }
    }

    const claim = async (id) => {
        claimingId.value = id
        try {
            await apiKurir.claimTask(id)
            tasks.value = tasks.value.filter(t => t.id !== id)
            return true
        } catch (error) {
            console.error(error)
            return false
        } finally {
            claimingId.value = null
        }
    }

    return { 
        tasks, 
        isLoading, 
        claimingId, 
        loadTasks, 
        claim 
    }
}