export default [
  {
    path: '/accounting/input',
    meta: { perluLogin: true, modul: 'akunting' },
    component: () => import('@/features/accounting/layout/TransactionEntryLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/accounting/input/po'
      },
      {
        path: 'po',
        name: 'transaksi-po-list',
        component: () => import('./views/PurchaseOrderList.vue')
      },
      {
        path: 'po/buat',
        name: 'transaksi-po-buat',
        component: () => import('./views/ProcurementCreate.vue')
      },
      {
        path: 'so',
        name: 'transaksi-so-list',
        component: () => import('./views/SalesOrderList.vue')
      },
      {
        path: 'so/buat',
        name: 'transaksi-so-buat',
        component: () => import('./views/SalesOrderCreate.vue')
      },
      {
        path: 'pengeluaran/buat',
        name: 'transaksi-pengeluaran',
        component: () => import('./views/Expense.vue') 
      },
    ]
  },

  {
    path: '/accounting/invoice',
    meta: { perluLogin: true, modul: 'buku_tagihan' }, 
    component: () => import('@/features/accounting/layout/InvoiceLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/accounting/invoice/dokumen'
      },
      {
        path: 'dokumen',
        name: 'accounting-invoice-dokumen',
        component: () => import('./views/DocumentAuditView.vue')
      },
      {
        path: 'tagihan',
        name: 'accounting-invoice-tagihan',
        component: () => import('./views/InvoiceList.vue')
      },
      {
        path: 'tagihan/create',
        name: 'accounting-invoice-buat',
        component: () => import('./views/InvoiceCreate.vue')
      },
      {
        path: 'catatan',
        name: 'accounting-invoice-catatan',
        // Menggunakan Expense.vue juga sesuai gambar
        component: () => import('./views/Expense.vue')
      }
    ]
  }
]