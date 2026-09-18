import { ref } from 'vue'
import { apiPembukuan } from '@/services/apiPembukuan' 

export function usePembukuan() {
    const akunList = ref([])
    const jurnalList = ref([])
    const isLoading = ref(false)

    const fetchAkun = async () => {
        try {
            const response = await apiPembukuan.getAkun()
            akunList.value = response.data.results || response.data || []
        } catch (error) {
            console.error("Gagal memuat daftar akun:", error)
        }
    }

    const fetchJurnal = async () => {
        isLoading.value = true
        try {
            const response = await apiPembukuan.getJurnal()
            jurnalList.value = response.data.results || response.data || []
        } catch (error) {
            console.error("Gagal memuat histori jurnal:", error)
        } finally {
            isLoading.value = false
        }
    }

    const simpanJurnal = async (payload) => {
        isLoading.value = true
        try {
            const response = await apiPembukuan.buatJurnal(payload)
            return response.data
        } catch (error) {
            console.error("Gagal menyimpan jurnal:", error)
            return {
                status: 'gagal',
                pesan: error.response?.data?.pesan || error.response?.data?.detail || 'Terjadi kesalahan sistem.'
            }
        } finally {
            isLoading.value = false
        }
    }

    return {
        akunList,
        jurnalList,
        isLoading,
        fetchAkun,
        fetchJurnal,
        simpanJurnal
    }
}