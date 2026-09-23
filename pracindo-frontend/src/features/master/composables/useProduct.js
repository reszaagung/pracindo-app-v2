import { ref, computed } from 'vue'
import api from '@/utils/api'

export function useProduct() {
    const dataProduk = ref([])
    const isLoading = ref(false)
    const error = ref(null)
    const searchQuery = ref('')

    const fetchProduk = async (params = {}) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await api.get('master/produk/', { params })
            dataProduk.value = response.data?.results || response.data || []

            return {
                success: true,
                data: dataProduk.value
            }
        } catch (err) {
            console.error('Gagal memuat data master produk:', err)

            const responseData = err.response?.data

            error.value =
                responseData?.detail ||
                responseData?.message ||
                'Gagal memuat data dari database.'

            return {
                success: false,
                message: error.value
            }
        } finally {
            isLoading.value = false
        }
    }

    const addProduk = async (payload) => {
        isLoading.value = true
        error.value = null

        try {
            const response = await api.post('master/produk/', payload)

            await fetchProduk()

            return {
                success: true,
                data: response.data
            }
        } catch (err) {
            console.error('Detail Penolakan Django:', err.response?.data)

            const responseData = err.response?.data
            let errorMessage = 'Gagal menyimpan data ke server.'

            if (responseData) {
                if (
                    typeof responseData === 'object' &&
                    !responseData.detail &&
                    !responseData.message
                ) {
                    const messages = []

                    Object.entries(responseData).forEach(([key, value]) => {
                        const text = Array.isArray(value)
                            ? value.join(', ')
                            : String(value)

                        messages.push(`${key.toUpperCase()}: ${text}`)
                    })

                    if (messages.length) {
                        errorMessage = messages.join(' | ')
                    }
                } else {
                    errorMessage =
                        responseData.detail ||
                        responseData.message ||
                        errorMessage
                }
            }

            error.value = errorMessage

            return {
                success: false,
                message: errorMessage,
                data: responseData
            }
        } finally {
            isLoading.value = false
        }
    }

    const deleteProduk = async (id_produk) => {
        isLoading.value = true
        error.value = null

        try {
            await api.delete(`master/produk/${id_produk}/`)
            await fetchProduk()

            return {
                success: true
            }
        } catch (err) {
            console.error('Gagal menghapus produk:', err)

            const responseData = err.response?.data
            const errorMessage =
                responseData?.detail ||
                responseData?.message ||
                'Gagal menghapus data dari server.'

            error.value = errorMessage

            return {
                success: false,
                message: errorMessage
            }
        } finally {
            isLoading.value = false
        }
    }

    const filteredProduk = computed(() => {
        const query = searchQuery.value.trim().toLowerCase()

        if (!query) {
            return dataProduk.value
        }

        return dataProduk.value.filter((prod) => {
            const nama = String(prod?.nama || '').toLowerCase()
            const kode = String(prod?.kode || '').toLowerCase()

            return (
                nama.includes(query) ||
                kode.includes(query)
            )
        })
    })

    return {
        dataProduk,
        filteredProduk,
        searchQuery,
        isLoading,
        error,
        fetchProduk,
        addProduk,
        deleteProduk
    }
}
