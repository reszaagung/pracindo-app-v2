import { createRouter, createWebHistory } from 'vue-router'
import LoginRetail from '@/view/public/LoginRetail.vue'
import RegisterCabangForm from '@/view/protect/RegisterCabangForm.vue'
import DashboardRetail from '@/view/protect/DashboardRetail.vue'

import StokView from '@/features/inventory/views/StokView.vue'
import PenerimaanViews from '@/features/inventory/views/PenerimaanViews.vue'

import KasirLayout from '@/layouts/kasir_layout/KasirLayout.vue'
import PosView from '@/features/kasir/views/PosView.vue'
import PembukuanLayout from '@/layouts/pembukuan_layout/PembukuanLayout.vue'
import JurnalUmumView from '@/features/pembukuan/views/JurnalUmumView.vue'
import HelperLayout from '@/layouts/helper_layout/HelperLayout.vue'

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'login',
        component: LoginRetail
    },
    {
        path: '/register',
        name: 'register', 
        component: RegisterCabangForm
    },
    {
        path: '/dashboard',          
        name: 'Dashboard',
        component: DashboardRetail
    },
    {
        path: '/stok',          
        name: 'StokView',
        component: StokView
    },
    {
        path: '/stok/penerimaan',          
        name: 'PenerimaanBarang',
        component: PenerimaanViews
    },
    {
        path: '/kasir',
        component: KasirLayout,
        children: [
            { path: '', name: 'PosView', component: PosView }
        ]
    },
    {
        path: '/pembukuan',
        component: PembukuanLayout,
        children: [
            { path: 'jurnal', name: 'JurnalUmum', component: JurnalUmumView }
        ]
    },
    {
        path: '/helper',
        component: HelperLayout,
        children: [
            {
                path: '',
                name: 'HelperHome',
                component: { template: '<div class="flex items-center justify-center h-full text-slate-400 font-medium">Layar Utama Helper (Kosong)</div>' }
            },
            {
                path: 'stiker',
                name: 'CetakStiker',
                component: { template: '<div class="flex items-center justify-center h-full text-slate-400 font-medium">Komponen Stiker Belum Diimport</div>' }
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('retail_token')
    
    if (to.name !== 'login' && to.name !== 'register' && !token) {
        next({ name: 'login' })
    } else if ((to.name === 'login' || to.name === 'register') && token) {
        next('/dashboard') 
    } else {
        next()
    }
})

export default router