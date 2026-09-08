import { ref } from 'vue'
import helperApi from '../api'
import { bacaError } from '@/utils/error'

export function useSticker() {
    const sedangProses = ref(false)
    const galat = ref('')
    const hasilCetak = ref(null)

    const buatDanCetakStiker = async (payload) => {
        sedangProses.value = true
        galat.value = ''
        hasilCetak.value = null

        try {
            const { data: generateObj } = await helperApi.buatStiker(payload)
            
            await helperApi.cetakStiker(generateObj.id)
            
            await _pollingStatus(generateObj.id)

        } catch (err) {
            galat.value = bacaError(err, 'Gagal memproses antrean stiker.')
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

            const { data } = await helperApi.cekStatus(id)
            if (data.file_hasil) {
                hasilCetak.value = data
                selesai = true
            }
        }

        if (!selesai) {
            throw new Error("Waktu render terlalu lama. Silakan cek menu riwayat nanti.")
        }
    }

    return {
        sedangProses, galat, hasilCetak, buatDanCetakStiker
    }
}