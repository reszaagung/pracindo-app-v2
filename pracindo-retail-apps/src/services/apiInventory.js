import api from './api'

export const apiInventory = {
    getStok: () => {
        return api.get('retail/stok/')
    },

    getPenerimaan: () => {
        return api.get('retail/penerimaan/')
    },

    prosesPenerimaan: (id, payload) => {
        return api.post(`retail/penerimaan/${id}/proses/`, payload)
    }
}