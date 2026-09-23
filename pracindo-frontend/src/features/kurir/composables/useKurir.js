import { ref } from 'vue'
import { apiKurir } from '../api'

export function useKurir() {
    const availableTasks = ref([])
    const myDeliveries = ref([])
    const historyDeliveries = ref([])

    const loading = ref(false)
    const loadingHistory = ref(false)
    const error = ref(null)

    let activeRequests = 0
    let historyRequestPromise = null

    const startRequest = () => {
        activeRequests += 1
        loading.value = true
    }

    const finishRequest = () => {
        activeRequests = Math.max(0, activeRequests - 1)
        loading.value = activeRequests > 0
    }

    const getErrorMessage = (err, fallback) => {
        return (
            err?.response?.data?.detail ||
            err?.response?.data?.message ||
            err?.response?.data?.error ||
            err?.message ||
            fallback
        )
    }

    const clearError = () => {
        error.value = null
    }

    const fetchAvailableTasks = async () => {
        startRequest()
        clearError()

        try {
            const data = await apiKurir.getAvailableTasks()

            availableTasks.value = Array.isArray(data) ? data : []

            return {
                success: true,
                data: availableTasks.value,
            }
        } catch (err) {
            error.value = getErrorMessage(
                err,
                'Gagal mengambil tugas tersedia.'
            )

            console.error(
                'Gagal mengambil tugas tersedia:',
                err
            )

            return {
                success: false,
                data: [],
                message: error.value,
            }
        } finally {
            finishRequest()
        }
    }

    const fetchMyDeliveries = async () => {
        startRequest()
        clearError()

        try {
            const data = await apiKurir.getMyDeliveries()

            myDeliveries.value = Array.isArray(data) ? data : []

            return {
                success: true,
                data: myDeliveries.value,
            }
        } catch (err) {
            error.value = getErrorMessage(
                err,
                'Gagal mengambil tugas saya.'
            )

            console.error(
                'Gagal mengambil tugas saya:',
                err
            )

            return {
                success: false,
                data: [],
                message: error.value,
            }
        } finally {
            finishRequest()
        }
    }

    const fetchHistory = async () => {
        if (historyRequestPromise) {
            return historyRequestPromise
        }

        historyRequestPromise = (async () => {
            loadingHistory.value = true
            clearError()

            try {
                const data = await apiKurir.getHistoryDeliveries()

                historyDeliveries.value = Array.isArray(data)
                    ? data
                    : []

                return {
                    success: true,
                    data: historyDeliveries.value,
                }
            } catch (err) {
                error.value = getErrorMessage(
                    err,
                    'Gagal mengambil riwayat pengiriman.'
                )

                console.error(
                    'Gagal mengambil riwayat:',
                    err
                )

                return {
                    success: false,
                    data: [],
                    message: error.value,
                }
            } finally {
                loadingHistory.value = false
            }
        })()

        try {
            return await historyRequestPromise
        } finally {
            historyRequestPromise = null
        }
    }

    const claimTask = async (taskId) => {
        clearError()

        try {
            const response = await apiKurir.claimTask(taskId)

            await fetchAvailableTasks()

            return {
                success: true,
                data: response?.data ?? response ?? null,
            }
        } catch (err) {
            error.value = getErrorMessage(
                err,
                'Gagal mengambil tugas.'
            )

            console.error(
                'Gagal klaim tugas:',
                err
            )

            return {
                success: false,
                data: null,
                message: error.value,
            }
        }
    }

    const startDelivery = async (taskId) => {
        clearError()

        try {
            const response = await apiKurir.startDelivery(taskId)

            await fetchMyDeliveries()

            return {
                success: true,
                data: response?.data ?? response ?? null,
            }
        } catch (err) {
            error.value = getErrorMessage(
                err,
                'Gagal memulai perjalanan.'
            )

            console.error(
                'Gagal memulai perjalanan:',
                err
            )

            return {
                success: false,
                data: null,
                message: error.value,
            }
        }
    }

    const markArrived = async (
        pengirimanId,
        perhentianId
    ) => {
        clearError()

        try {
            const response = await apiKurir.markArrived(
                pengirimanId,
                perhentianId
            )

            await fetchMyDeliveries()

            return {
                success: true,
                data: response?.data ?? response ?? null,
            }
        } catch (err) {
            error.value = getErrorMessage(
                err,
                'Gagal menandai pengiriman sampai.'
            )

            console.error(
                'Gagal menandai sampai:',
                err
            )

            return {
                success: false,
                data: null,
                message: error.value,
            }
        }
    }

    const uploadProof = async (
        pengirimanId,
        perhentianId,
        formData,
        idemKey = ''
    ) => {
        clearError()

        try {
            const response = await apiKurir.uploadProof(
                pengirimanId,
                perhentianId,
                formData,
                idemKey
            )

            await fetchMyDeliveries()

            return {
                success: true,
                data: response?.data ?? response ?? null,
            }
        } catch (err) {
            error.value = getErrorMessage(
                err,
                'Gagal mengunggah bukti pengiriman.'
            )

            console.error(
                'Gagal upload bukti:',
                err
            )

            return {
                success: false,
                data: null,
                message: error.value,
            }
        }
    }

    const recordReturn = async (
        pengirimanId,
        perhentianId,
        formData,
        idemKey = ''
    ) => {
        clearError()

        try {
            const response = await apiKurir.recordReturn(
                pengirimanId,
                perhentianId,
                formData,
                idemKey
            )

            await fetchMyDeliveries()

            return {
                success: true,
                data: response?.data ?? response ?? null,
            }
        } catch (err) {
            error.value = getErrorMessage(
                err,
                'Gagal mencatat retur pengiriman.'
            )

            console.error(
                'Gagal mencatat retur:',
                err
            )

            return {
                success: false,
                data: null,
                message: error.value,
            }
        }
    }

    const refreshAll = async () => {
        clearError()

        await Promise.all([
            fetchAvailableTasks(),
            fetchMyDeliveries(),
            fetchHistory(),
        ])

        return {
            availableTasks: availableTasks.value,
            myDeliveries: myDeliveries.value,
            historyDeliveries: historyDeliveries.value,
        }
    }

    const reset = () => {
        availableTasks.value = []
        myDeliveries.value = []
        historyDeliveries.value = []
        loading.value = false
        loadingHistory.value = false
        error.value = null
        activeRequests = 0
        historyRequestPromise = null
    }

    return {
        availableTasks,
        myDeliveries,
        historyDeliveries,
        loading,
        loadingHistory,
        error,
        fetchAvailableTasks,
        fetchMyDeliveries,
        fetchHistory,
        claimTask,
        startDelivery,
        markArrived,
        uploadProof,
        recordReturn,
        refreshAll,
        clearError,
        reset,
    }
}
