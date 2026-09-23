import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api/',
    headers: {
        Accept: 'application/json',
    },
})

const PUBLIK = [
    'auth/login/',
    'auth/register/',
    'auth/lupa-password/',
]

const endpointPublik = (url = '') =>
    PUBLIK.some((p) => url.includes(p))

api.interceptors.request.use(
    (cfg) => {
        const token = localStorage.getItem('token')

        if (token && !endpointPublik(cfg.url)) {
            cfg.headers.Authorization = `Token ${token}`
        }

        return cfg
    },
    (error) => Promise.reject(error)
)

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const { response, config } = error

        if (!response) {
            return Promise.reject(error)
        }

        if (
            response.status === 401 &&
            !endpointPublik(config?.url)
        ) {
            localStorage.removeItem('token')
            localStorage.removeItem('profil')
            localStorage.removeItem('modul')

            const pathname = window.location.pathname
            const search = window.location.search
            const hash = window.location.hash
            const next = `${pathname}${search}${hash}`

            if (pathname !== '/login') {
                window.location.replace(
                    `/login?sesi=berakhir&next=${encodeURIComponent(next)}`
                )
            }
        }

        return Promise.reject(error)
    }
)

export default api