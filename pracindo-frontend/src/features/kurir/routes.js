import KurirLayout from './layout/KurirLayout.vue'
import KurirDashboard from './views/KurirDashboard.vue'
import OrderPool from './views/OrderPool.vue'
import OnGoDelivery from './views/OnGoDelivery.vue'
import History from './views/History.vue'
// import WorkOrder from '@/features/work-order/views/WorkOrderBoard.vue' // Sesuaikan jika ada

export const kurirRoutes = [
    {
        path: '/kurir',
        component: KurirLayout,
        meta: { perluLogin: true, modul: 'kurir' },
        children: [
            {
                path: '', 
                name: 'KurirDashboard',
                component: KurirDashboard
            },
            {
                path: 'order-pool',
                name: 'KurirOrderPool',
                component: OrderPool
            },
            {
                path: 'on-go-delivery',
                name: 'KurirOnGoDelivery',
                component: OnGoDelivery
            },
            {
                path: 'history',
                name: 'KurirHistory',
                component: History
            },
            {
                path: 'work-order',
                name: 'KurirWorkOrder',
                component: () => import('@/features/work-order/views/WorkOrderBoard.vue') 
            }
        ]
    }
]