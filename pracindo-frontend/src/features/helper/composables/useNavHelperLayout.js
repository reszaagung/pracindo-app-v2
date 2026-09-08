import { useRoute } from 'vue-router'
import { menuHelper } from '../uiConfigHelper'

export function useNavHelperLayout() {
    const route = useRoute()

    const aktif = (ruteTujuan) => {
        if (!route) return false
        return route.path.startsWith(ruteTujuan)
    }

    return {
        menu: menuHelper,
        aktif
    }
}