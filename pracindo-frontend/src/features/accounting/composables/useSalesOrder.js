import { ref, computed } from 'vue'
import { accountingApi } from '@/features/accounting/api'

export function useSalesOrder() {
    const listEntitas = ref([])
    const listPelanggan = ref([])
    const listProduk = ref([])
    const daftarSO = ref([])
    const isLoading = ref(false)
    const sedangProses = ref(false)
    const pesanError = ref('')
    const periodeDitutup = ref(false)
    const previewNomor = ref('Pilih entitas & tanggal')

    const muatDataMaster = async () => {
        try {
            const [rEnt, rPlg] = await Promise.allSettled([
                accountingApi.master.getEntitasCore(),
                accountingApi.master.getPelanggan()
            ])
            const ambil = (r) => (r.status === 'fulfilled' ? (r.value.data.results ?? r.value.data ?? []) : [])
            listEntitas.value = ambil(rEnt)
            listPelanggan.value = ambil(rPlg)
        } catch (error) {
            pesanError.value = "Gagal memuat data master dari server."
        }
    }

const muatStokEntitas = async (entitasId) => {
        if (!entitasId) {
            listProduk.value = []
            return
        }

        try {
            const { data } = await accountingApi.inventory.getStokBarangJadi({ entitas: entitasId })
            
            const rawData = data.rincian || data.results || data || []
            
            const dataSesuaiEntitas = rawData.filter(item => Number(item.entitas_id) === Number(entitasId))
            
            listProduk.value = dataSesuaiEntitas.map(item => {
                const namaBarang = item.item_nama || item.nama || item.label || 'Produk'
                const kemasan = item.kemasan_nama ? ` (${item.kemasan_nama})` : ''
                
                return {
                    id: item.item_id || item.id,
                    kode: item.item_id || item.kode || '-',
                    nama: `${namaBarang}${kemasan}`, 
                    label: `${namaBarang}${kemasan}`,
                    satuan_kode: item.kemasan_nama || 'PCS',
                    stok: Number(item.qty_unit) || Number(item.qty) || 0,
                    harga_jual: Number(item.harga_jual) || 0
                }
            })
        } catch (error) {
            console.error("Gagal memuat stok:", error)
            listProduk.value = []
        }
    }

    const muatPreviewNomor = async (entitasId, tanggal) => {
        if (!entitasId || !tanggal) {
            previewNomor.value = 'Pilih entitas & tanggal'
            return
        }
        try {
            previewNomor.value = 'Memuat nomor...'
            const res = await accountingApi.so.getPreviewNomor({ entitas: entitasId, tanggal })
            previewNomor.value = res.data?.nomor_so || 'Gagal membaca respons'
        } catch (error) {
            console.error(error.response?.data || error.message)
            previewNomor.value = 'Gagal memuat (Cek Console/Server)'
        }
    }

    const fetchSO = async () => {
        isLoading.value = true
        pesanError.value = ''
        try {
            const response = await accountingApi.so.getDaftar()
            let rawData = Array.isArray(response.data) ? response.data : (response.data?.results || response.data?.data || [response.data])
            daftarSO.value = rawData.map(so => ({
                id: so.id,
                nomor_so: so.nomor_so,
                tanggal: so.tanggal,
                entitas: so.entitas_kode ? { kode: so.entitas_kode } : { kode: 'UMUM' },
                pelanggan: { nama: so.pelanggan_nama || '-', kota: '-' },
                grand_total: so.grand_total ?? 0,
                status: so.status
            }))
        } catch (error) {
            pesanError.value = "Gagal memuat daftar Sales Order."
        } finally {
            isLoading.value = false
        }
    }

    const simpanSO = async (payload) => {
        sedangProses.value = true
        pesanError.value = ''
        try {
            const res = await accountingApi.so.simpanBaru(payload)
            await fetchSO()
            return { success: true, data: res.data }
        } catch (error) {
            pesanError.value = error.response?.data?.detail || "Gagal menyimpan Sales Order."
            return { success: false }
        } finally {
            sedangProses.value = false
        }
    }

    return {
        listEntitas, listPelanggan, listProduk, daftarSO,
        isLoading, sedangProses, pesanError, periodeDitutup,
        previewNomor, muatDataMaster, muatPreviewNomor, fetchSO, simpanSO, muatStokEntitas
    }
}