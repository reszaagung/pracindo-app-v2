import { computed, ref } from 'vue'
import api from '@/utils/api'
import { bacaError } from '@/utils/error'

export function useStock() {
    const daftarStok = ref([])
    const stokDetail = ref(null)
    const daftarMutasi = ref([])

    // Loading dipisah agar tidak saling mematikan.
    const loadingStok = ref(false)
    const loadingDetail = ref(false)
    const loadingMutasi = ref(false)

    const galat = ref('')

    const sedangProses = computed(() => {
        return (
            loadingStok.value ||
            loadingDetail.value ||
            loadingMutasi.value
        )
    })

    const muatStok = async (params = {}) => {
        loadingStok.value = true
        galat.value = ''

        try {
            if (params.lapis === 'ENTITAS') {
                const { data } = await api.get(
                    'inventory/mutasi/rekap/',
                    { params }
                )

                daftarStok.value =
                    data?.entitas || []
            } else if (params.lapis === 'POOL') {
                const { data } = await api.get(
                    'inventory/pool/',
                    { params }
                )

                daftarStok.value =
                    data?.rincian || []
            } else if (params.lapis === 'JADI') {
                const { data } = await api.get(
                    'inventory/barang-jadi/',
                    { params }
                )

                daftarStok.value =
                    data?.rincian ||
                    data?.results ||
                    data ||
                    []
            } else {
                daftarStok.value = []
            }
        } catch (err) {
            console.error(
                'Gagal memuat data persediaan:',
                err
            )

            galat.value = bacaError(
                err,
                'Gagal memuat data persediaan stok.'
            )

            daftarStok.value = []
        } finally {
            loadingStok.value = false
        }
    }

    const muatStokDetail = async (
        id,
        params = {}
    ) => {
        if (!id) {
            stokDetail.value = null
            galat.value =
                'ID stok tidak ditemukan.'
            return
        }

        loadingDetail.value = true
        galat.value = ''

        try {
            stokDetail.value = null

            const { data } = await api.get(
                `inventory/stok/${id}/`,
                { params }
            )

            stokDetail.value = data || null
        } catch (err) {
            console.error(
                'Gagal memuat detail stok:',
                err
            )

            stokDetail.value = null

            galat.value = bacaError(
                err,
                'Gagal memuat detail stok.'
            )
        } finally {
            loadingDetail.value = false
        }
    }

    const muatMutasi = async (
        params = {}
    ) => {
        loadingMutasi.value = true
        galat.value = ''

        try {
            daftarMutasi.value = []

            const { data } = await api.get(
                'inventory/mutasi/',
                { params }
            )

            daftarMutasi.value =
                data?.results ||
                data ||
                []
        } catch (err) {
            console.error(
                'Gagal memuat riwayat mutasi:',
                err
            )

            daftarMutasi.value = []

            galat.value = bacaError(
                err,
                'Gagal memuat riwayat mutasi.'
            )
        } finally {
            loadingMutasi.value = false
        }
    }

    return {
        daftarStok,
        stokDetail,
        daftarMutasi,

        sedangProses,
        loadingStok,
        loadingDetail,
        loadingMutasi,

        galat,

        muatStok,
        muatStokDetail,
        muatMutasi,
    }
}