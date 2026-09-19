import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api/',
    headers: { Accept: 'application/json' },
})

const PUBLIK = [
    'auth/login/', 'auth/register/', 'auth/lupa-password/',
    'retail/login/'
]
const endpointPublik = (url = '') => PUBLIK.some((p) => url.includes(p))

api.interceptors.request.use((cfg) => {
    const isRetail = cfg.url.includes('retail/')
    const token = isRetail
        ? localStorage.getItem('retail_token')
        : localStorage.getItem('token')

    if (token && !endpointPublik(cfg.url)) {
        if (isRetail) {
            cfg.headers.Authorization = `Token ${token}` 
        } else {
            cfg.headers.Authorization = `Token ${token}`
        }
    }
    return cfg
})

api.interceptors.response.use(
    (r) => r,
    async (err) => {
        const { response, config } = err

        if (!response) return Promise.reject(err)

        if (response.status === 401 && !endpointPublik(config?.url)) {
            console.warn("🚨 Token Expired! Auto-logout dipicu untuk:", config.url)
            
            if (config.url.includes('retail/')) {
                localStorage.removeItem('retail_token')
                localStorage.removeItem('retail_user')
            } else {
                localStorage.removeItem('token')
                localStorage.removeItem('profil')
                localStorage.removeItem('modul')
            }

            const { default: router } = await import('@/router')
            const kini = router.currentRoute.value
            if (kini.name !== 'login') {
                router.push({
                    name: 'login', 
                    query: { sesi: 'berakhir', next: kini.fullPath },
                })
            }
        }

        return Promise.reject(err)
    }
)

export default api