import api from './api' 

export const apiInventory = {
    getStok: () => {
        return api.get('retail/inventory/stok/') 
    },

    getPenerimaan: () => {
        return api.get('retail/inventory/penerimaan/') 
    },

    prosesPenerimaan: (id, payload) => {
        return api.post(`retail/inventory/penerimaan/${id}/proses/`, payload) 
    }
}