import { ref } from 'vue'
import { apiDistribusi } from '@/features/distribusi/api' 
import api from '@/utils/api'

export function useMasterLogistik() {
    const daftarArmada = ref([])
    const daftarKurir = ref([])
    const daftarToko = ref([])
    const sedangMemuatMaster = ref(false)

    const muatDataMaster = async () => {
        sedangMemuatMaster.value = true
        try {
            const [resArmada, resKurir, resToko] = await Promise.all([
                apiDistribusi.getArmada(),
                apiDistribusi.getKurir().catch(() => []), 
            
                api.get('core/cabangtoko/')
            ])
            
            daftarArmada.value = resArmada.results || resArmada || []
            daftarKurir.value = resKurir.results || resKurir || []
            daftarToko.value = resToko.data?.results || resToko.data || []
        } catch (err) {
            console.error('Gagal memuat master data logistik:', err)
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