import { ref } from 'vue'
import api from '@/utils/api'
import { CACHE_KEY, denganCache, CacheService } from '@/utils/cacheService' 

export function useMasterCache() {
    const cachedSuppliers = ref([])

    const muatSuppliers = async () => {
        try {
            const data = await denganCache(CACHE_KEY.SUPLIER, async () => {
                const res = await api.get('master/suplier/', { params: { ringkas: 1, aktif: true } })
                return res.data.results || res.data || []
            }, 15) 

            cachedSuppliers.value = data
            return data
        } catch (error) {
            console.error("Gagal memuat suplier:", error)
            return []
        }
    }

    const forceRefreshSuppliers = async () => {
        CacheService.remove(CACHE_KEY.SUPLIER)
        
        return await muatSuppliers()
    }

    return {
        cachedSuppliers,
        muatSuppliers,
        forceRefreshSuppliers
    }
}