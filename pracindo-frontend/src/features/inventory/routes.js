import MonitoringLayout from './layout/MonitoringLayout.vue'
import StockList from './views/StockList.vue'
import StockDetail from './views/StockDetail.vue'
import TankMonitor from './views/TankMonitor.vue'
import ClaimPosition from './views/ClaimPosition.vue'

export default [
    {
        path: '/inventory',
        meta: {
            perluLogin: true,
            modul: 'inventory',
        },
        component: MonitoringLayout,
        children: [
            {
                path: '',
                name: 'inventory-stok-list',
                component: StockList,
            },
            {
                path: 'tangki',
                name: 'inventory-tangki',
                component: TankMonitor,
            },
            {
                path: 'stok/:id',
                name: 'inventory-stok-detail',
                component: StockDetail,
                props: true,
            },
            {
                path: 'klaim/:grup',
                name: 'inventory-klaim',
                component: ClaimPosition,
                props: true,
            },
        ],
    },
]