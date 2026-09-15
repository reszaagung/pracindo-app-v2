import api from '@/utils/api'

export const retailApi = {
  getKatalog: () => api.get('retail/pos/katalog/').then(r => r.data),
  checkout: (payload) => api.post('retail/pos/checkout/', payload).then(r => r.data),
  getRiwayat: () => api.get('retail/riwayat/').then(r => r.data),
  getSesiAktif: () => api.get('retail/sesi/').then(r => r.data),
  tutupShift: () => api.post('retail/sesi/').then(r => r.data),

  getPelanggan: () => api.get('retail/pelanggan/').then(r => r.data),
  getSales: () => api.get('retail/sales/').then(r => r.data),

  getPenerimaan: () => api.get('retail/penerimaan/').then(r => r.data),
  prosesPenerimaan: (id, payload) => api.post(`retail/penerimaan/${id}/proses/`, payload).then(r => r.data),

  getPiutang: () => api.get('retail/piutang/').then(r => r.data),
  bayarPiutang: (id, payload) => api.post(`retail/piutang/${id}/bayar/`, payload).then(r => r.data),

  getAkunBukuBesar: () => api.get('retail/akuntansi/akun/').then(r => r.data),
  createAkunBukuBesar: (payload) => api.post('retail/akuntansi/akun/', payload).then(r => r.data),
  getMutasiAkun: (id) => api.get(`retail/akuntansi/akun/${id}/mutasi/`).then(r => r.data),
  getJurnalUmum: () => api.get('retail/akuntansi/jurnal/').then(r => r.data),
  createJurnalUmum: (payload) => api.post('retail/akuntansi/jurnal/', payload).then(r => r.data),

  getCabang: () => api.get('retail/cabang/').then(r => r.data),
  createCabang: (payload) => api.post('retail/cabang/', payload).then(r => r.data),
}