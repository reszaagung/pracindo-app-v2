import { ref } from 'vue'
import { apiDistribusi } from '../api'

export function useArmada() {
    const daftarArmada = ref([])
    const sedangMemuat = ref(false)

    const normalisasiList = (data) => {
        if (Array.isArray(data)) {
            return data
        }

        if (Array.isArray(data?.results)) {
            return data.results
        }

        if (Array.isArray(data?.data)) {
            return data.data
        }

        return []
    }

    const muatArmada = async () => {
        if (sedangMemuat.value) return

        sedangMemuat.value = true

        try {
            const data = await apiDistribusi.getArmada()
            daftarArmada.value = normalisasiList(data)
        } catch (err) {
            console.error('Gagal memuat data armada:', err)
        } finally {
            sedangMemuat.value = false
        }
    }

    return {
        daftarArmada,
        sedangMemuat,
        muatArmada
    }
}
