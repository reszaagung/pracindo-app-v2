import { ref } from 'vue'
import api from '@/utils/api'

export function useCabangRetail() {
    const daftarToko = ref([])
    const isLoading = ref(false)
    const error = ref(null)

    // 1. Tarik Data (Read)
    const muatDaftarToko = async () => {
        isLoading.value = true
        error.value = null
        try {
            // Sesuaikan endpoint ini jika URL di Django urls.py lu berbeda
            const response = await api.get('core/cabangtoko/') 
            
            // Handle struktur response Django REST Framework (biasanya ada .results kalau pakai pagination)
            daftarToko.value = response.data.results || response.data || []
        } catch (err) {
            console.error(err)
            error.value = 'Gagal memuat data KTP Retail. Cek koneksi atau server.'
        } finally {
            isLoading.value = false
        }
    }

    // 2. Tambah Toko Baru (Create)
    const simpanTokoBaru = async (payload) => {
        isLoading.value = true
        error.value = null
        try {
            const response = await api.post('core/cabangtoko/', payload)
            // Langsung inject data baru ke state lokal biar UI update tanpa refresh
            daftarToko.value.push(response.data)
            return { sukses: true, data: response.data }
        } catch (err) {
            console.error(err)
            return { sukses: false, pesan: err.response?.data?.detail || 'Gagal mendaftarkan toko baru.' }
        } finally {
            isLoading.value = false
        }
    }

    // 3. Update Data Toko (Update)
    const updateToko = async (id, payload) => {
        isLoading.value = true
        try {
            const response = await api.put(`core/cabangtoko/${id}/`, payload)
            // Update item spesifik di array lokal
            const index = daftarToko.value.findIndex(t => t.id === id)
            if (index !== -1) {
                daftarToko.value[index] = response.data
            }
            return { sukses: true }
        } catch (err) {
            console.error(err)
            return { sukses: false, pesan: 'Gagal mengupdate identitas toko.' }
        } finally {
            isLoading.value = false
        }
    }

    // 4. Hapus / Nonaktifkan Toko (Delete)
    const hapusToko = async (id) => {
        isLoading.value = true
        try {
            await api.delete(`core/cabangtoko/${id}/`)
            // Buang data dari array lokal
            daftarToko.value = daftarToko.value.filter(t => t.id !== id)
            return { sukses: true }
        } catch (err) {
            console.error(err)
            return { sukses: false, pesan: 'Gagal menghapus toko.' }
        } finally {
            isLoading.value = false
        }
    }

    return {
        daftarToko,
        isLoading,
        error,
        muatDaftarToko,
        simpanTokoBaru,
        updateToko,
        hapusToko
    }
}