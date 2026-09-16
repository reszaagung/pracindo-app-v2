// Kita arahkan import ke layout dan view yang ada di dalam folder helper
const HelperWrapper = () => import('./layouts/HelperWrapper.vue')
const GenerateStiker = () => import('./views/GenerateStiker.vue')

export const helperRoutes = {
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
            component: GenerateStiker,
            meta: { perluLogin: true, modulAkses: 'HELPER_VIEW' } // Proteksi rute
        }
    ]
} 