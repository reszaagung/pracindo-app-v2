import { useRoute } from 'vue-router'
// IMPORT menu dari uiConfig agar Anda hanya perlu mengaturnya di satu tempat
import { menuInvoice } from '@/features/accounting/uiConfigAccounting'

export function useNavInvoice() {
    const route = useRoute()

    // Langsung gunakan menu yang sudah di-import
    const menu = menuInvoice

    // Fungsi untuk mengecek apakah tombol menu harus disorot (aktif)
    const aktif = (ruteTujuan) => {
        if (!route) return false

        // Cek pencocokan eksak atau jika sedang berada di sub-rute
        return route.path === ruteTujuan || route.path.startsWith(ruteTujuan + '/')
    }

    return {
        menu,
        aktif
    }
}