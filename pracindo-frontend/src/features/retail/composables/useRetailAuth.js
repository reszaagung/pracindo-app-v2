import { useAuth } from '@/composables/useAuth'

const KODE_MODUL_RETAIL = 'retail'

export function useRetailAuth() {
    const auth = useAuth()
    const { login: loginDasar, bisaAkses } = auth

    const login = async (username, password) => {
        const hasil = await loginDasar(username, password)

        if (!hasil.success) {
            return hasil
        }

        if (!bisaAkses(KODE_MODUL_RETAIL)) {
            return {
                success: false,
                message: 'Akun ini tidak memiliki akses ke modul Retail.'
            }
        }

        return hasil
    }

    return {
        ...auth,
        login
    }
}