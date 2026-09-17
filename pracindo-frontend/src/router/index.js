import { createRouter, createWebHistory } from 'vue-router'
import { useGuards } from './guards'
import ruteProduksi from '@/features/produksi/routes.js'
import ruteWarehouse from '@/features/warehouse/routes.js'
import ruteDistribusi from '@/features/distribusi/routes.js'
import ruteAccounting from '@/features/accounting/routes.js' 
import ruteHelper from '@/features/helper/routes.js'
import { kurirRoutes } from '@/features/kurir/routes.js' 
import ruteSales from '@/features/sales/routes.js'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { publik: true }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { publik: true }
  },
  {
    path: '/',
    name: 'dashboard',
    meta: { perluLogin: true, modul: 'dashboard' },
    component: () => import('@/views/DashboardView.vue')
  },
  ...ruteAccounting,
  {
    path: '/master/suplier',
    name: 'master-suplier',
    meta: { perluLogin: true, modul: 'master' },
    component: () => import('@/features/master/views/Supplier.vue')
  },
  {
    path: '/inventory',
    meta: { perluLogin: true, modul: 'inventory' },
    component: () => import('@/features/inventory/layout/MonitoringLayout.vue'),
    children: [
      {
        path: '',
        name: 'inventory-stok-list',
        component: () => import('@/features/inventory/views/StockList.vue')
      },
      {
        path: 'tangki',
        name: 'inventory-tangki',
        component: () => import('@/features/inventory/views/TankMonitor.vue')
      },
      {
        path: 'stok/:id',
        name: 'inventory-stok-detail',
        component: () => import('@/features/inventory/views/StockDetail.vue'),
        props: true
      },
      {
        path: 'klaim/:grup',
        name: 'inventory-klaim',
        component: () => import('@/features/inventory/views/ClaimPosition.vue'),
        props: true
      },
    ]
  },
  ...ruteProduksi,
  ...ruteWarehouse,
  ...ruteDistribusi,
  ...ruteHelper, 
  ...kurirRoutes, 
  ...ruteSales,
  {
    path: '/work-order',
    name: 'work-order',
    meta: { perluLogin: true, modul: 'work_order' },
    component: () => import('@/features/work-order/views/WorkOrderBoard.vue')
  },
  {
    path: '/dokumen',
    name: 'dokumen',
    meta: { perluLogin: true, modul: 'dokumen' },
    component: () => import('@/views/ModulBelumSiap.vue')
  },
  {
    path: '/akses-ditolak',
    name: 'akses-ditolak',
    meta: { perluLogin: true },
    component: () => import('@/views/AksesDitolak.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    meta: { perluLogin: true },
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0, behavior: 'smooth' }
  }
})

useGuards(router)

export default router