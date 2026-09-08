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
            }
        ]
    }
]