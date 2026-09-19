import { ref } from 'vue'
import { apiKurir } from '../api' 

export function useKurir() {
  const availableTasks = ref([])
  const myDeliveries = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchAvailableTasks = async () => {
    loading.value = true
    error.value = null
    try {
      const data = await apiKurir.getAvailableTasks()
      availableTasks.value = data || []
    } catch (err) {
      error.value = err.message
      console.error('Gagal mengambil tugas tersedia:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchMyDeliveries = async () => {
    loading.value = true
    error.value = null
    try {
      const data = await apiKurir.getMyDeliveries()
      myDeliveries.value = data || []
    } catch (err) {
      error.value = err.message
      console.error('Gagal mengambil tugas saya:', err)
    } finally {
      loading.value = false
    }
  }

  const claimTask = async (taskId) => {
    try {
      await apiKurir.claimTask(taskId)
      await fetchAvailableTasks() 
    } catch (err) {
      console.error('Gagal klaim tugas:', err)
      throw err
    }
  }

  const startDelivery = async (taskId) => {
    try {
      await apiKurir.startDelivery(taskId)
      await fetchMyDeliveries() 
    } catch (err) {
      console.error('Gagal memulai perjalanan:', err)
      throw err
    }
  }

  const markArrived = async (pengirimanId, perhentianId) => {
    try {
      await apiKurir.markArrived(pengirimanId, perhentianId)
      // PERBAIKAN: Tambahkan feedback UI
      alert('Tugas berhasil ditandai sampai! Memperbarui data...') 
      await fetchMyDeliveries()
    } catch (err) {
      alert('Gagal menandai sampai: ' + err.message)
      console.error('Gagal menandai sampai:', err)
      throw err
    }
  }

  const uploadProof = async (pengirimanId, perhentianId, formData, idemKey = '') => {
    try {
      await apiKurir.uploadProof(pengirimanId, perhentianId, formData, idemKey)
      await fetchMyDeliveries()
    } catch (err) {
      console.error('Gagal upload bukti:', err)
      throw err
    }
  }

  const recordReturn = async (pengirimanId, perhentianId, formData, idemKey = '') => {
    try {
      await apiKurir.recordReturn(pengirimanId, perhentianId, formData, idemKey)
      await fetchMyDeliveries()
    } catch (err) {
      console.error('Gagal mencatat retur:', err)
      throw err
    }
  }

  return {
    availableTasks,
    myDeliveries,
    loading,
    error,
    fetchAvailableTasks,
    fetchMyDeliveries,
    claimTask,
    startDelivery,
    markArrived,
    uploadProof,
    recordReturn
  }
}