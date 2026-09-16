import api from '@/services/api'

export const apiKasir = {
    getKatalog: () => api.get('retail/pos/katalog/'),
    getPelanggan: () => api.get('retail/pelanggan/'),
    getSales: () => api.get('retail/sales/'),
    getSesiAktif: () => api.get('retail/sesi/'),
    getRiwayat: () => api.get('retail/riwayat/'),
    checkout: (payload) => api.post('retail/pos/checkout/', payload),
    tutupShift: () => api.post('retail/sesi/')
}