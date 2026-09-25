import { useRoute } from 'vue-router'

export function useNavMonitorLayout() {
    const route = useRoute()

    const menu = [
        {
            id: 'stok',
            label: 'Posisi Stok Gudang',
            ikon: 'pi-box',
            rute: '/inventory',
            activate: true,
        },
        {
            id: 'tangki',
            label: 'Monitor Tangki',
            ikon: 'pi-database',
            rute: '/inventory/tangki',
            activate: true,
        },
        {
            id: 'klaim-distribusi',
            label: 'Transaksi & Klaim Pool',
            ikon: 'pi-truck',
            rute: '/inventory/klaim',
            activate: true,
        },
    ]

    const aktif = (ruteTujuan) => {
        if (!ruteTujuan) {
            return false
        }

        if (ruteTujuan === '/inventory') {
            return (
                route.path === '/inventory' ||
                route.path.startsWith('/inventory/stok/')
            )
        }

        return (
            route.path === ruteTujuan ||
            route.path.startsWith(`${ruteTujuan}/`)
        )
    }

    return {
        menu,
        aktif,
    }
}

