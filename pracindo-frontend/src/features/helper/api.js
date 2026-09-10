import axios from 'axios'
import { showGlobalLoginModal } from '@/utils/authModalState'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/',
  headers: { Accept: 'application/json' },
})

const PUBLIK = ['auth/login/', 'auth/register/', 'auth/lupa-password/']
const endpointPublik = (url = '') => PUBLIK.some((p) => url.includes(p))

api.interceptors.request.use((cfg) => {
  const token = localStorage.getItem('token')

  if (token && !endpointPublik(cfg.url)) {
    cfg.headers.Authorization = `Token ${token}`
  }
  return cfg
})

api.interceptors.response.use(
  (r) => r,
  async (err) => {
    const { response, config } = err

    if (!response) return Promise.reject(err)

    if (response.status === 401 && !endpointPublik(config?.url)) {
      showGlobalLoginModal.value = true
    }

    return Promise.reject(err)
  }
)

export default api