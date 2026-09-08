import api from '@/utils/api'

export const warehouseApi = {
  getPOSiapTerima: (params) => api.get('warehouse/po-siap-terima/', { params }),
  getPenerimaan: (params) => api.get('warehouse/penerimaan/', { params }),
  getRingkasanPenerimaan: (id) => api.get(`warehouse/penerimaan/${id}/ringkasan/`),
  simpanPenerimaan: (payload) => api.post('warehouse/penerimaan/', payload),

  getGrupAktif: () => api.get('inventory/entitas/', { params: { aktif: true } }), 
  getKemasanAktif: () => api.get('inventory/pool/kemasan/'), 
  getBarangJadi: () => api.get('inventory/barang-jadi/', { params: { lapis: 'JADI' } }),

  getTangkiProduksi: () => api.get('produksi/tangki/'), 
  getSaldoTangki: (id) => api.get(`produksi/tangki/${id}/saldo/`), 
  
  getRiwayatPacking: (params) => api.get('inventory/packing/', { params }),
  simpanPacking: (payload) => api.post('inventory/packing/', payload),

  getLaporanSelisih: (params) => api.get('warehouse/laporan-selisih/', { params }),
  getSelisihTerbuka: (params) => api.get('warehouse/laporan-selisih/terbuka/', { params }),
  buatLaporanManual: (payload) => api.post('warehouse/laporan-selisih/', payload),
  ajukanKlaim: (id, catatan) => api.post(`warehouse/laporan-selisih/${id}/ajukan/`, { catatan }),

  getMasterProduk: (params) => api.get('master/master-produk/', { params }),
  getDetailMasterProduk: (id) => api.get(`master/master-produk/${id}/`),
  buatMasterProduk: (payload) => api.post('master/master-produk/', payload),
  updateMasterProduk: (id, payload) => api.put(`master/master-produk/${id}/`, payload),
  patchMasterProduk: (id, payload) => api.patch(`master/master-produk/${id}/`, payload),


  getDistribusi: (params) => api.get('warehouse/distribusi/', { params }),
  getDetailDistribusi: (id) => api.get(`warehouse/distribusi/${id}/`),
  buatDistribusi: (payload) => api.post('warehouse/distribusi/', payload),
  hapusDistribusi: (id) => api.delete(`warehouse/distribusi/${id}/`),
  
  sahkanDistribusi: (id) => api.post(`warehouse/distribusi/${id}/sahkan/`),
}

export default warehouseApi