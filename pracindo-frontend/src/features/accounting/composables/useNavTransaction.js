import { useRoute } from 'vue-router'
// Mengambil variabel menuTransaksi dari uiConfig
import { menuTransaksi } from '@/features/accounting/uiConfigAccounting'

export function useNavTransaksi() {
    const route = useRoute()
    
    // Langsung gunakan menu dari uiConfig
    const transaksi = menuTransaksi

    const aktif = (ruteTujuan) => {
        if (!route) return false
        return route.path === ruteTujuan || route.path.startsWith(ruteTujuan + '/')
    }

    return {
        transaksi,
        aktif
    }
}