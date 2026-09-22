import api from '@/utils/api'

export const accountingApi = {
    master: {
        getPortalEntitas: () => api.get('auth/portal/'),
        getEntitasCore: () => api.get('core/entitas/'),
        getSupplier: (params) => api.get('master/suplier/', { params }),
        getPelanggan: () => api.get('master/pelanggan/'),
        getProduk: () => api.get('master/produk/'),
        getSatuan: (params) => api.get('master/satuan/', { params }),
        buatProduk: (payload) => api.post('master/produk/', payload),
        cekPeriode: (params) => api.get('core/periode/status/', { params }),
    },

    inventory: {
        getStokBarangJadi: (params) =>
            api.get('inventory/barang-jadi/', { params }),
    },

    po: {
        getDaftar: () => api.get('akunting/purchase-order/'),
        getPreviewNomor: (params) =>
            api.get('akunting/purchase-order/preview-nomor/', { params }),
        simpanBaru: (payload) =>
            api.post('akunting/purchase-order/', payload),
        ajukan: (id) =>
            api.post(`akunting/purchase-order/${id}/ajukan/`),
        setujui: (id) =>
            api.post(`akunting/purchase-order/${id}/setujui/`),
        tolak: (id, payload) =>
            api.post(`akunting/purchase-order/${id}/tolak/`, payload),
        kirim: (id) =>
            api.post(`akunting/purchase-order/${id}/kirim/`),
        batalkan: (id, payload) =>
            api.post(`akunting/purchase-order/${id}/batalkan/`, payload),
    },

    so: {
        getDaftar: () => api.get('sales-order/'),
        getPreviewNomor: (params) =>
            api.get('sales-order/preview-nomor/', { params }),
        simpanBaru: (payload) =>
            api.post('sales-order/', payload),
    },

    expense: {
        getAkun: () => api.get('akunting/akun/'),
        getDaftar: (params) =>
            api.get('akunting/pengeluaran-kas/', { params }),
        simpanBaru: (payload, config) =>
            api.post('akunting/pengeluaran-kas/', payload, config),
        posting: (id) =>
            api.post(`akunting/pengeluaran-kas/${id}/posting/`),
    },

    invoice: {
        getFakturJual: () =>
            api.get('akunting/faktur-jual/'),
        terbitkanDariDO: (deliveryOrderId, payload) =>
            api.post(
                `akunting/faktur-jual/dari-do/${deliveryOrderId}/`,
                payload,
            ),
    },

    dokumen: {
        upload: (payload) =>
            api.post('dokumen-audit/', payload),
        hapus: (po_id, config) =>
            api.delete(`dokumen-audit/${po_id}/`, config),
    },

    monitoring: {
        getSummary: (params) =>
            api.get('keuangan/monitoring/', { params }),

        getTagihan: (params) =>
            api.get('keuangan/monitoring/tagihan/', { params }),

        getKas: (params) =>
            api.get('keuangan/monitoring/kas/', { params }),

        simpanPengeluaran: (payload, config) =>
            api.post(
                'keuangan/pengeluaran/',
                payload,
                config,
            ),
    },
}