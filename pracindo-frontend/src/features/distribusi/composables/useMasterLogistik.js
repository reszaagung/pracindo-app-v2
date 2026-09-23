import { ref } from 'vue'
import { apiDistribusi } from '@/features/distribusi/api'
import api from '@/utils/api'

export function useMasterLogistik() {
    const daftarArmada = ref([])
    const daftarKurir = ref([])
    const daftarToko = ref([])
    const sedangMemuatMaster = ref(false)

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

    const muatDataMaster = async () => {
        if (sedangMemuatMaster.value) return

        sedangMemuatMaster.value = true

        try {
            const [
                resArmada,
                resKurir,
                resToko
            ] = await Promise.all([
                apiDistribusi.getArmada(),
                apiDistribusi.getKurir().catch(() => []),
                api.get('retail/cabang/')
            ])

            daftarArmada.value = normalisasiList(resArmada)
            daftarKurir.value = normalisasiList(resKurir)
            daftarToko.value = normalisasiList(resToko)
        } catch (err) {
            console.error(
                'Gagal memuat master data logistik:',
                err
            )
        } finally {
            sedangMemuatMaster.value = false
        }
    }

    return {
        daftarArmada,
        daftarKurir,
        daftarToko,
        sedangMemuatMaster,
        muatDataMaster
    }
}
