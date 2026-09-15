import { useRoute } from 'vue-router'

const MENU_HELPER = [
  {
    id: 'helper-stiker',
    label: 'Cetak Stiker',
    ikon: 'pi-print',
    rute: '/helper/stiker',
    activate: true
  },
  {
    id: 'helper-stiker-kecil-12',
    label: 'Cetak Stiker Kecil',
    ikon: 'pi-tags',
    rute: '/helper/stiker-kecil-12',
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