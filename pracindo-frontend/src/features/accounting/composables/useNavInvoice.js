import { useRoute } from 'vue-router'
import { menuInvoice } from '@/features/accounting/uiConfigAccounting'

export function useNavInvoice() {
    const route = useRoute()

    const menu = menuInvoice

    const aktif = (ruteTujuan) => {
        if (!route) return false

        return route.path === ruteTujuan || route.path.startsWith(ruteTujuan + '/')
    }

    return {
        menu,
        aktif
    }
}