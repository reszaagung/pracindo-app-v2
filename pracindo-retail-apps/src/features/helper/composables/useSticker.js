import { ref } from 'vue'
import { helperApi } from '@/services/helperApi'

export function useSticker() {
    const sedangProses = ref(false)
    const galat = ref('')
    const hasilCetak = ref(null)

    const buatDanCetakStiker = async (payload) => {
        sedangProses.value = true
        galat.value = ''
        hasilCetak.value = null
        try {
            const response = await helperApi.buatStiker(payload)
            const generateObj = response.data

            await helperApi.cetakStiker(generateObj.id)
            await _pollingStatus(generateObj.id)
        } catch (err) {
            galat.value = err.response?.data?.detail || 'Gagal memproses antrean stiker.'
        } finally {
            sedangProses.value = false
        }
    }

    const _pollingStatus = async (id) => {
        let selesai = false
        let percobaan = 0
        const maxPercobaan = 15

        while (!selesai && percobaan < maxPercobaan) {
            await new Promise(resolve => setTimeout(resolve, 1000))
            percobaan++
            const response = await helperApi.cekStatus(id)
            if (response.data.file_hasil) {
                hasilCetak.value = response.data
                selesai = true
            }
        }
        if (!selesai) {
            throw new Error("Waktu render terlalu lama. Silakan cek menu riwayat nanti.")
        }
    }

    return { sedangProses, galat, hasilCetak, buatDanCetakStiker }
}