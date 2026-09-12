import api from '@/utils/api'

export const apiKurir = {
    getAvailableTasks: async () => {
        const response = await api.get('logistik/pengiriman/kolam-tugas/')
        return response.data
    },

    getMyDeliveries: async () => {
        const response = await api.get('logistik/pengiriman/tugas-saya/')
        return response.data
    },

    claimTask: async (id) => {
        const response = await api.post(`logistik/pengiriman/${id}/klaim/`)
        return response.data
    },

    startDelivery: async (id) => {
        const response = await api.post(`logistik/pengiriman/${id}/berangkatkan/`)
        return response.data
    },

    markArrived: async (pengirimanId, perhentianId) => {
        const response = await api.post(`logistik/pengiriman/${pengirimanId}/perhentian/${perhentianId}/sampai/`)
        return response.data
    },

    uploadProof: async (pengirimanId, perhentianId, formData, idemKey = '') => {
        // Hanya kirim Idempotency-Key jika ada.
        // Axios otomatis men-set Content-Type multipart/form-data beserta boundary-nya.
        const headers = idemKey ? { 'Idempotency-Key': idemKey } : {}
        const response = await api.post(
            `logistik/pengiriman/${pengirimanId}/perhentian/${perhentianId}/bukti/`, 
            formData, 
            { headers }
        )
        return response.data
    },

    recordReturn: async (pengirimanId, perhentianId, formData, idemKey = '') => {
        const headers = idemKey ? { 'Idempotency-Key': idemKey } : {}
        const response = await api.post(
            `logistik/pengiriman/${pengirimanId}/perhentian/${perhentianId}/retur/`, 
            formData, 
            { headers }
        )
        return response.data
    }
}