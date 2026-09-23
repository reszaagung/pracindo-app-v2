// src/features/inventory/api.js
import api from '@/utils/api'

export const inventoryApi = {
    getEntitas: (params = {}) =>
        api.get('inventory/entitas/', { params }),

    getProduk: (params = {}) =>
        api.get('inventory/produk/', { params }),

    getStok: (params = {}) =>
        api.get('inventory/stok/', { params }),

    getPool: (params = {}) =>
        api.get('inventory/pool/', { params }),

    getPoolKemasan: (params = {}) =>
        api.get('inventory/pool/kemasan/', { params }),

    getPoolKartuStok: (produkId, params = {}) =>
        api.get(`inventory/pool/${produkId}/kartu/`, { params }),

    getMutasi: (params = {}) =>
        api.get('inventory/mutasi/', { params }),

    getMutasiRekap: (params = {}) =>
        api.get('inventory/mutasi/rekap/', { params }),

    getPosisiKlaim: (params = {}) =>
        api.get('inventory/posisi-klaim/', { params }),

    getSaldoEntitas: (params = {}) =>
        api.get('inventory/saldo-entitas/', { params }),

    getPemeriksaan: (params = {}) =>
        api.get('inventory/pemeriksaan/', { params }),

    getBarangJadi: (params = {}) =>
        api.get('inventory/barang-jadi/', { params }),

    getKemasan: (params = {}) =>
        api.get('inventory/kemasan/', { params }),

    getPembelian: (params = {}) =>
        api.get('inventory/pembelian/', { params }),

    getPacking: (params = {}) =>
        api.get('inventory/packing/', { params }),

    setorKePool: (payload) =>
        api.post('inventory/setor-ke-pool/', payload),

    klaimHasil: (payload) =>
        api.post('inventory/klaim-hasil/', payload),

    opname: (payload) =>
        api.post('inventory/pemeriksaan/', payload),
}

export default inventoryApi