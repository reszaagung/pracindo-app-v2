import { computed, ref } from 'vue'
import api from '@/utils/api'
import { bacaError } from '@/utils/error'

export function useProduct() {
    const dataProduk = ref([])
    const isLoading = ref(false)
    const isSaving = ref(false)
    const isDeleting = ref(false)

    const error = ref('')
    const searchQuery = ref('')

    const fetchProduk = async (params = {}) => {
        isLoading.value = true
        error.value = ''

        try {
            const response = await api.get(
                'master/produk/',
                { params }
            )

            const data = response?.data

            dataProduk.value =
                data?.results ||
                data ||
                []
        } catch (err) {
            console.error(
                'Gagal memuat data master produk:',
                err
            )

            dataProduk.value = []

            error.value = bacaError(
                err,
                'Gagal memuat data master produk.'
            )
        } finally {
            isLoading.value = false
        }
    }

    const addProduk = async (payload) => {
        isSaving.value = true
        error.value = ''

        try {
            const response = await api.post(
                'master/produk/',
                payload
            )

            await fetchProduk()

            return {
                success: true,
                data: response?.data || null,
            }
        } catch (err) {
            console.error(
                'Gagal menyimpan produk:',
                err
            )

            console.error(
                'Response Django:',
                err?.response?.data
            )

            const message =
                bacaError(
                    err,
                    'Gagal menyimpan data produk.'
                )

            error.value = message

            return {
                success: false,
                message,
                data:
                    err?.response?.data ||
                    null,
            }
        } finally {
            isSaving.value = false
        }
    }

    const deleteProduk = async (idProduk) => {
        if (!idProduk) {
            const message =
                'ID produk tidak ditemukan.'

            error.value = message

            return {
                success: false,
                message,
            }
        }

        isDeleting.value = true
        error.value = ''

        try {
            await api.delete(
                `master/produk/${idProduk}/`
            )

            await fetchProduk()

            return {
                success: true,
            }
        } catch (err) {
            console.error(
                'Gagal menghapus produk:',
                err
            )

            const message =
                bacaError(
                    err,
                    'Gagal menghapus data produk.'
                )

            error.value = message

            return {
                success: false,
                message,
                data:
                    err?.response?.data ||
                    null,
            }
        } finally {
            isDeleting.value = false
        }
    }

    const filteredProduk = computed(() => {
        const keyword =
            searchQuery.value
                .trim()
                .toLowerCase()

        if (!keyword) {
            return dataProduk.value
        }

        return dataProduk.value.filter(
            (produk) => {
                const nama =
                    String(
                        produk?.nama || ''
                    ).toLowerCase()

                const kode =
                    String(
                        produk?.kode || ''
                    ).toLowerCase()

                const jenis =
                    String(
                        produk?.jenis || ''
                    ).toLowerCase()

                const satuan =
                    String(
                        produk?.satuan_kode || ''
                    ).toLowerCase()

                return (
                    nama.includes(keyword) ||
                    kode.includes(keyword) ||
                    jenis.includes(keyword) ||
                    satuan.includes(keyword)
                )
            }
        )
    })

    return {
        dataProduk,
        filteredProduk,
        searchQuery,

        isLoading,
        isSaving,
        isDeleting,

        error,

        fetchProduk,
        addProduk,
        deleteProduk,
    }
}