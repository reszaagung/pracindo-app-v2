// src/features/sales/routes.js

export default [
  {
    path: '/sales',
    component: () => import('./layout/SalesLayout.vue'),
    // PERBAIKAN: Ubah menjadi 'sales_order' agar dikenali oleh useGuards dan backend
    meta: { perluLogin: true, modul: 'sales_order' },
    children: [
      {
        path: '',
        redirect: '/sales/crm'
      },
      {
        path: 'crm',
        name: 'sales-crm-board',
        component: () => import('./views/SalesCrmBoard.vue')
      },
      {
        path: 'orders',
        name: 'sales-order-board',
        component: () => import('./views/SalesOrderboard.vue')
      }
    ]
  }
]