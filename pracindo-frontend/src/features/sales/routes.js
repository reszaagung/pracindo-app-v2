// src/features/sales/routes.js

export default [
  {
    path: '/sales',
    component: () => import('./layout/SalesLayout.vue'),
    meta: { perluLogin: true, modul: 'sales' },
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