import api from '@/services/api'

export const apiPembukuan = {
    getAkun: () => api.get('retail/akuntansi/akun/'),
    getJurnal: () => api.get('retail/akuntansi/jurnal/'),
    buatJurnal: (payload) => api.post('retail/akuntansi/jurnal/', payload),
    getMutasiAkun: (id) => api.get(`retail/akuntansi/akun/${id}/mutasi/`)
}