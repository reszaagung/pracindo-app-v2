import { ref } from 'vue'
import api from '@/utils/api'
import { bacaError } from '@/utils/error'

export function useClaim() {
    const posisiKlaim = ref([])
    const saldoEntitas = ref([])
    const mutasiKlaim = ref([])
    const isiPool = ref(null)

    const sedangProses = ref(false)
    const galat = ref('')

    let jumlahRequestAktif = 0
    let timerRealtime = null
    let realtimeBerjalan = false
    let grupAktif = null

    const mulaiRequest = () => {
        jumlahRequestAktif += 1
        sedangProses.value = true
    }

    const selesaiRequest = () => {
        jumlahRequestAktif = Math.max(0, jumlahRequestAktif - 1)
        sedangProses.value = jumlahRequestAktif > 0
    }

    const muatPosisiKlaim = async (grup) => {
        grupAktif = grup
        mulaiRequest()

        try {
            const { data } = await api.get('inventory/posisi-klaim/', {
                params: { grup },
            })

            posisiKlaim.value = Array.isArray(data)
                ? data
                : Array.isArray(data?.results)
                    ? data.results
                    : []
        } catch (err) {
            galat.value = bacaError(
                err,
                'Gagal memuat posisi klaim.'
            )
        } finally {
            selesaiRequest()
        }
    }

    const muatSaldoEntitas = async () => {
        mulaiRequest()

        try {
            const { data } = await api.get('inventory/saldo-entitas/')

            saldoEntitas.value = Array.isArray(data)
                ? data
                : Array.isArray(data?.results)
                    ? data.results
                    : []
        } catch (err) {
            galat.value = bacaError(
                err,
                'Gagal memuat saldo entitas.'
            )
        } finally {
            selesaiRequest()
        }
    }

    const muatMutasiKlaim = async (grup) => {
        mulaiRequest()

        try {
            const { data } = await api.get('inventory/mutasi/', {
                params: {
                    grup,
                    limit: 200,
                },
            })

            mutasiKlaim.value = Array.isArray(data)
                ? data
                : Array.isArray(data?.results)
                    ? data.results
                    : []
        } catch (err) {
            galat.value = bacaError(
                err,
                'Gagal memuat mutasi klaim.'
            )
        } finally {
            selesaiRequest()
        }
    }

    const muatIsiPool = async (grup) => {
        mulaiRequest()

        try {
            const { data } = await api.get('inventory/pool/', {
                params: { grup },
            })

            isiPool.value = data
        } catch (err) {
            galat.value = bacaError(
                err,
                'Gagal memuat isi pool.'
            )
        } finally {
            selesaiRequest()
        }
    }

    const muatSemua = async (grup) => {
        grupAktif = grup
        galat.value = ''

        await Promise.all([
            muatPosisiKlaim(grup),
            muatSaldoEntitas(),
            muatMutasiKlaim(grup),
            muatIsiPool(grup),
        ])
    }

    const refreshRealtime = async () => {
        if (!grupAktif || sedangProses.value) {
            return
        }

        await Promise.all([
            muatPosisiKlaim(grupAktif),
            muatSaldoEntitas(),
            muatMutasiKlaim(grupAktif),
            muatIsiPool(grupAktif),
        ])
    }

    const jadwalkanRealtime = async (grup, interval) => {
        if (!realtimeBerjalan) {
            return
        }

        if (grup !== grupAktif) {
            return
        }

        await refreshRealtime()

        if (!realtimeBerjalan) {
            return
        }

        timerRealtime = window.setTimeout(() => {
            jadwalkanRealtime(grup, interval)
        }, interval)
    }

    const mulaiRealtime = (grup, interval = 5000) => {
        hentikanRealtime()

        grupAktif = grup
        realtimeBerjalan = true

        jadwalkanRealtime(grup, interval)
    }

    const hentikanRealtime = () => {
        realtimeBerjalan = false

        if (timerRealtime !== null) {
            window.clearTimeout(timerRealtime)
            timerRealtime = null
        }
    }

    const kirimAksi = async (url, payload) => {
        mulaiRequest()
        galat.value = ''

        try {
            const { data } = await api.post(url, payload)

            if (grupAktif) {
                await Promise.all([
                    muatPosisiKlaim(grupAktif),
                    muatSaldoEntitas(),
                    muatMutasiKlaim(grupAktif),
                    muatIsiPool(grupAktif),
                ])
            }

            return {
                success: true,
                data,
            }
        } catch (err) {
            galat.value = bacaError(
                err,
                'Gagal menyimpan.'
            )

            return {
                success: false,
                message: galat.value,
            }
        } finally {
            selesaiRequest()
        }
    }

    const setorKePool = (payload) =>
        kirimAksi('inventory/setor-ke-pool/', payload)

    const klaimHasil = (payload) =>
        kirimAksi('inventory/klaim-hasil/', payload)

    const opname = (payload) =>
        kirimAksi('inventory/pemeriksaan/', payload)

    const reset = () => {
        hentikanRealtime()

        posisiKlaim.value = []
        saldoEntitas.value = []
        mutasiKlaim.value = []
        isiPool.value = null
        sedangProses.value = false
        galat.value = ''

        jumlahRequestAktif = 0
        grupAktif = null
    }

    return {
        posisiKlaim,
        saldoEntitas,
        mutasiKlaim,
        isiPool,
        sedangProses,
        galat,
        muatPosisiKlaim,
        muatSaldoEntitas,
        muatMutasiKlaim,
        muatIsiPool,
        muatSemua,
        refreshRealtime,
        mulaiRealtime,
        hentikanRealtime,
        setorKePool,
        klaimHasil,
        opname,
        reset,
    }
}