const accountingRoutes = [
    {
        path: '/accounting/input/po',
        name: 'accounting-purchase-order',
        component: () =>
            import(
                './views/PurchaseOrderList.vue'
            ),
        meta: {
            title: 'Purchase Order',
            module: 'accounting',
        },
    },

    {
        path: '/accounting/input/po/create',
        name: 'accounting-purchase-order-create',
        component: () =>
            import(
                './views/ProcurementCreate.vue'
            ),
        meta: {
            title: 'Buat Purchase Order',
            module: 'accounting',
        },
    },

    {
        path: '/accounting/input/po/:id',
        name: 'accounting-purchase-order-detail',
        component: () =>
            import(
                './views/PurchaseOrderDetail.vue'
            ),
        props: true,
        meta: {
            title: 'Detail Purchase Order',
            module: 'accounting',
        },
    },
]

export default accountingRoutes