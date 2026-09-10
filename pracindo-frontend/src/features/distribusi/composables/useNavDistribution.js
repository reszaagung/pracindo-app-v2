import { useRoute } from 'vue-router'

export function useNavDistribution() {
    const route = useRoute()

    const menu = [
        { id: 'request', label: 'Request Order', ikon: 'pi-file-edit', rute: '/distribusi', activate: true },
        { id: 'monitoring', label: 'Monitoring Order', ikon: 'pi-desktop', rute: '/distribusi/monitoring', activate: true },
        { id: 'muat', label: 'Validasi Muat (Loading)', ikon: 'pi-check-square', rute: '/distribusi/loading', activate: true },
        { id: 'armada', label: 'Status Armada', ikon: 'pi-truck', rute: '/distribusi/armada', activate: true },
        { id: 'kurir', label: 'Aplikasi Kurir', ikon: 'pi-map', rute: '/kurir', activate: true }
    ]

    const aktif = (ruteTujuan) => {
        if (!route) return false
        if (ruteTujuan === '/distribusi') return route.path === '/distribusi'
        return route.path === ruteTujuan || route.path.startsWith(ruteTujuan + '/')
    }
    
    return { menu, aktif }
}