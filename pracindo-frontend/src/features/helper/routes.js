import HelperWrapper from './layout/HelperWrapper.vue'

export default [
    {
        path: '/helper',
        component: HelperWrapper,
        children: [
            {
                path: '',
                redirect: '/helper/stiker'
            },
            {
                path: 'stiker',
                name: 'HelperGenerateStiker',
                component: () => import('./views/GenerateStiker.vue')
            },
            {
                path: 'stiker-kecil-12',
                name: 'HelperGenerateStikerKecil12',
                component: () => import('./views/GenerateStikerKecil12.vue')
            }
        ]
    }
]