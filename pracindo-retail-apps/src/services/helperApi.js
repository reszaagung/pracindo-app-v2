import api from '@/services/api' // Panggil API utama aplikasi lu

export const helperApi = {
    // Sesuaikan endpoint ini dengan backend Django lu
    buatStiker: (payload) => api.post('fitur/generate-stiker/', payload),
    cetakStiker: (id) => api.post(`fitur/generate-stiker/${id}/cetak/`),
    cekStatus: (id) => api.get(`fitur/generate-stiker/${id}/status/`)
}