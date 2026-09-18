import api from '@/utils/api' 

export const apiDistribusi = {
    getArmada: async () => {
        const response = await api.get('logistik/kendaraan/') 
        return response.data
    },
    // 👇 FUNGSI INI YANG BIKIN BISA NYIMPAN ARMADA BARU 👇
    tambahArmada: async (payload) => {
        const response = await api.post('logistik/kendaraan/', payload)
        return response.data
    },

    getKurir: async () => {
        try {
            const response = await api.get('logistik/kurir/') 
            return response.data
        } catch (error) {
            return []
        }
    },
    getDistribusiTersedia: async (entitasId = '') => {
        const response = await api.get('logistik/distribusi-tersedia/', { 
            params: { entitas: entitasId } 
        })
        return response.data
    },
    getSemuaPengiriman: async (params = {}) => {
        const response = await api.get('logistik/pengiriman/', { params })
        return response.data
    },

    rakitPengiriman: async (payload) => {
        const response = await api.post('logistik/pengiriman/', payload)
        return response.data
    },

    createDistribusi: async (payload) => {
        const response = await api.post('warehouse/distribusi/', payload)
        return response.data
    },

    getStokPabrik: async (params = {}) => {
        try {
            const response = await api.get('inventory/barang-jadi/', { params })
            return response.data
        } catch (error) {
            return { rincian: [], results: [] }
        }
    },
    getKolamTugas: async () => {
        const response = await api.get('logistik/pengiriman/kolam-tugas/')
        return response.data
    },
    klaimTugas: async (pengirimanId) => {
        const response = await api.post(`logistik/pengiriman/${pengirimanId}/klaim/`)
        return response.data
    }
}