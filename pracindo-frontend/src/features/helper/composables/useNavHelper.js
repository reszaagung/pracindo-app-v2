import { useRoute } from 'vue-router'

/**
 * Konfigurasi menu sidebar untuk modul Helper.
 * `ikon` memakai nama kelas PrimeIcons lengkap (mis. 'pi-print'),
 * karena di HelperLayout.vue dipakai sebagai :class="['pi', menu.ikon]".
 */
const MENU_HELPER = [
  {
    id: 'helper-stiker',
    label: 'Cetak Stiker',
    ikon: 'pi-print',
    rute: '/helper/stiker',
    activate: true
  }
]

export function useNavHelper() {
  const route = useRoute()

  const aktif = (rute) => {
    if (!rute) return false
    if (route.path === rute) return true

    if (rute === '/helper/stiker') {
      return route.path.startsWith('/helper/stiker/')
    }

    return false
  }

  return {
    menuHelper: MENU_HELPER,
    aktif
  }
}