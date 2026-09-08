import api from '@/utils/api'

export default {
    buatStiker(payload) {
        return api.post('fitur/generate-stiker/', payload)
    },
    cetakStiker(id) {
        return api.post(`fitur/generate-stiker/${id}/cetak/`)
    },
    cekStatus(id) {
        return api.get(`fitur/generate-stiker/${id}/`)
    }
}