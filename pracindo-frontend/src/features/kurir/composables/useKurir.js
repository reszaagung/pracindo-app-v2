import { ref } from 'vue'
import { apiKurir } from '../api' 

export function useKurir() {
  const availableTasks = ref([])
  const myDeliveries = ref([])
  const historyDeliveries = ref([]) // State baru untuk riwayat
  
  const loading = ref(false)
  const loadingHistory = ref(false) // State loading khusus riwayat
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

  // FUNGSI BARU: Mengambil riwayat pengiriman
  const fetchHistory = async () => {
    loadingHistory.value = true
    error.value = null
    try {
      // Pastikan fungsi getHistoryDeliveries ditambahkan juga di file api.js Anda
      const data = await apiKurir.getHistoryDeliveries()
      historyDeliveries.value = data || []
    } catch (err) {
      error.value = err.message
      console.error('Gagal mengambil riwayat:', err)
    } finally {
      loadingHistory.value = false
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
    historyDeliveries, 
    loading,
    loadingHistory,    
    error,
    fetchAvailableTasks,
    fetchMyDeliveries,
    fetchHistory,      
    claimTask,
    startDelivery,
    markArrived,
    uploadProof,
    recordReturn
  }
}