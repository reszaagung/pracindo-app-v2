import { ref } from 'vue'
import { warehouseApi } from '../api' 

export function usePacking() {
  const packings = ref([])
  const tangkis = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const fetchPackings = async (params = {}) => {
    isLoading.value = true
    error.value = null
    try {
      const { data } = await warehouseApi.getRiwayatPacking(params)
      packings.value = data.results || data
    } catch (err) {
      error.value = err.response?.data?.pesan || err.message
    } finally {
      isLoading.value = false
    }
  }

  const fetchTangkisWithSaldo = async () => {
    isLoading.value = true
    error.value = null
    try {
      const res = await warehouseApi.getTangkiProduksi()
      const dataTangki = Array.isArray(res) ? res : (res?.data?.results || res?.results || res?.data || [])

      tangkis.value = dataTangki.map(t => ({
        ...t,
        loadingSaldo: true,
        saldo: []
      }))

      await Promise.all(
        tangkis.value.map(async (t) => {
          try {
            if (t.aktif) {
              const saldoRes = await warehouseApi.getSaldoTangki(t.id)
              t.saldo = saldoRes?.results ?? saldoRes?.data ?? saldoRes ?? []
            }
          } catch (e) {
            console.error(`Gagal memuat saldo tangki ${t.kode}`, e)
          } finally {
            t.loadingSaldo = false
          }
        })
      )
    } catch (err) {
      error.value = err.response?.data?.pesan || err.message
    } finally {
      isLoading.value = false
    }
  }

  const createPacking = async (payload) => {
    isLoading.value = true
    error.value = null
    try {
      const { data } = await warehouseApi.simpanPacking(payload)
      return data
    } catch (err) {
      error.value = err.response?.data?.pesan || err.response?.data?.detail || err.message
      throw error.value
    } finally {
      isLoading.value = false
    }
  }

  return {
    packings,
    tangkis,
    isLoading,
    error,
    fetchPackings,
    fetchTangkisWithSaldo,
    createPacking
  }
}