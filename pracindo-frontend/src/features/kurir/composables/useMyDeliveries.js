import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import { apiKurir } from '../api'

export function useMyDeliveries() {
    const deliveries = ref([])
    const isLoading = ref(false)
    const toast = useToast()

    const loadDeliveries = async () => {
        isLoading.value = true
        try {
            const data = await apiKurir.getMyDeliveries()
            const list = data.results || data
            
            deliveries.value = list.filter(d => d.status !== 'SELESAI' && d.status !== 'BATAL')
        } catch (err) {
            toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat tugas aktif Anda', life: 3000 })
        } finally {
            isLoading.value = false
        }
    }

    const startDelivery = async (id) => {
        try {
            await apiKurir.startDelivery(id)
            toast.add({ severity: 'success', summary: 'Berangkat', detail: 'Hati-hati di jalan!', life: 3000 })
            await loadDeliveries()
        } catch (err) {
            toast.add({ severity: 'error', summary: 'Gagal', detail: err.response?.data?.detail || 'Gagal mulai tugas', life: 3000 })
        }
    }

    const markArrived = async (pengirimanId, stopId) => {
        try {
            await apiKurir.markArrived(pengirimanId, stopId)
            toast.add({ severity: 'success', summary: 'Tiba', detail: 'Lokasi berhasil ditandai', life: 3000 })
            await loadDeliveries()
        } catch (err) {
            toast.add({ severity: 'error', summary: 'Gagal', detail: err.response?.data?.detail || 'Gagal lapor tiba', life: 3000 })
        }
    }

    const uploadProof = async (pengirimanId, stopId, file, jenisDokumen) => {
        try {
            const formData = new FormData()
            formData.append('foto', file)
            formData.append('catatan', `[Upload Otomatis] Jenis Dokumen: ${jenisDokumen}`) 
            const idemKey = `bukti-${stopId}-${Date.now()}`

            await apiKurir.uploadProof(pengirimanId, stopId, formData, idemKey)
            toast.add({ severity: 'success', summary: 'Sukses', detail: 'Dokumen berhasil diunggah', life: 3000 })
            
            await loadDeliveries()
            return true
        } catch (err) {
            toast.add({ severity: 'error', summary: 'Gagal Upload', detail: err.response?.data?.detail || 'Kesalahan saat unggah dokumen', life: 3000 })
            return false
        }
    }

    return { deliveries, isLoading, loadDeliveries, startDelivery, markArrived, uploadProof }
}