const DistributionLayout = () => import('./layout/DistributionLayout.vue')

export default [
    {
        path: '/distribusi',
        component: DistributionLayout,
        meta: { perluLogin: true, modul: 'warehouse_distribusi' },
        children: [
            {
                path: '',
                name: 'delivery-request',
                component: () => import('./views/DeliveryOrderRequest.vue')
            },
            {
                path: 'monitoring',
                name: 'distribusi-monitoring',
                component: () => import('./views/OrderMonitoring.vue')
            },
            {
                path: 'loading',
                name: 'distribusi-loading',
                component: () => import('./views/LoadingValidation.vue')
            },
            {
                path: 'armada',
                name: 'distribusi-armada',
                component: () => import('./views/FleetStatus.vue')
            }
        ]
    }
]