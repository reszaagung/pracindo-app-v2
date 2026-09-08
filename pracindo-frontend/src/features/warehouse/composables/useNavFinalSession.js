import { useRoute } from 'vue-router'

export function useNavDistribution() {
    const route = useRoute()
    const menus = [
        {
            id: 'packaging',
            label: 'Pengemasan',
            ikon: 'pi-box',
            rute: '/warehouse/distribution/packaging',
            activate: true
        },
        {
            id: 'log-packaging',
            label: 'Riwayat Kemas',
            ikon: 'pi-history', 
            rute: '/warehouse/distribution/logs',
            activate: true
        },
        {
            id: 'dispatch',
            label: 'Pengiriman', 
            ikon: 'pi-truck',
            rute: '/warehouse/distribution/dispatch',
            activate: true 
        }
    ]

    const aktif = (path) => {
        return route.path.startsWith(path)
    }

    return {
        menus,
        aktif
    }
}