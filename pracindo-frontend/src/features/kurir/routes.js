import KurirLayout from './layout/KurirLayout.vue'
import RequestDelivery from './views/RequestDelivery.vue'
import TaskOwn from './views/TaskOwn.vue'
import TaskHistory from './views/TaskHistory.vue'
import ProfilKurir from './views/ProfilKurir.vue'

export const kurirRoutes = [
    {
        path: '/kurir',
        component: KurirLayout,
        meta: { perluLogin: true, modul: 'kurir' },
        children: [
            {
                path: '', 
                redirect: '/kurir/permintaan'
            },
            {
                path: 'permintaan',
                name: 'KurirPermintaan',
                component: RequestDelivery
            },
            {
                path: 'tugas-saya',
                name: 'KurirTugasSaya',
                component: TaskOwn
            },
            {
                path: 'riwayat',
                name: 'KurirRiwayat',
                component: TaskHistory
            },
            {
                path: 'profil',
                name: 'KurirProfil',
                component: ProfilKurir
            }
        ]
    }
]