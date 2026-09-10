import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { apiDistribusi } from '@/features/distribusi/api'
import api from '@/utils/api'

export function useDistribusiForm() {
    const router = useRouter()
    const sedangProses = ref(false)
    
    const master = reactive({
        entitas: [],
        toko: [],
        armada: [],
        stokPabrik: []
    })

    const form = reactive({
        entitas_id: '',
        tanggal: new Date().toISOString().split('T')[0],
        tujuan_toko_id: '',
        nomor_surat_jalan: 'Otomatis (Saat Disimpan)',
        kendaraan_id: '',
        items: [
            { stok_terpilih: null, barang_nama: '', kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 }
        ]
    })

    const tambahItem = () => {
        form.items.push({ stok_terpilih: null, barang_nama: '', kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 })
    }

    const hapusItem = (index) => {
        form.items.splice(index, 1)
    }

    const getNamaAsli = (data) => {
        if (!data) return 'Barang Unknown'
        return data.item_nama || data.produk_nama || data.nama || (data.produk && data.produk.nama) || 'Barang Unknown'
    }

    const daftarBarangUnik = computed(() => {
        const map = new Map()
        master.stokPabrik.forEach(stok => {
            const nama = getNamaAsli(stok)
            if (nama && !map.has(nama)) map.set(nama, nama)
        })
        return Array.from(map.values())
    })

    const getKemasanTersedia = (namaDipilih) => {
        if (!namaDipilih) return []
        return master.stokPabrik.filter(stok => getNamaAsli(stok) === namaDipilih)
    }

    const resetKemasan = (item) => {
        item.stok_terpilih = null
        item.kemasan = ''
        item.total_unit = 1
        item.total_berat = 0
        item.berat_per_unit = 0
    }

    const kalkulasiBerat = (item) => {
        const batasMaksimal = item.stok_terpilih?.qty_unit || item.stok_terpilih?.qty || 1
        if (item.total_unit > batasMaksimal) item.total_unit = batasMaksimal
        item.total_berat = (item.berat_per_unit > 0 && item.total_unit > 0) ? (item.total_unit * item.berat_per_unit).toFixed(2) : 0
    }

    const hitungOtomatis = (item) => {
        if (!item.stok_terpilih) return
        item.kemasan = item.stok_terpilih.kemasan_nama || item.stok_terpilih.kemasan || 'CURAH'
        const totalKg = parseFloat(item.stok_terpilih.qty_kg || item.stok_terpilih.berat_total_kg) || 0
        const stokTersedia = parseInt(item.stok_terpilih.qty_unit || item.stok_terpilih.qty) || 1
        item.berat_per_unit = totalKg / stokTersedia
        item.total_unit = 1
        kalkulasiBerat(item)
    }

    const muatDataMaster = async () => {
        try {
            const [resArmada, resToko, resStok, resEntitas] = await Promise.all([
                apiDistribusi.getArmada(),
                api.get('core/cabangtoko/'),
                apiDistribusi.getStokPabrik(),
                api.get('core/entitas/').catch(() => ({ data: { results: [] } }))
            ])
            master.armada = resArmada.results || resArmada || []
            master.toko = resToko.data?.results || resToko.data || []
            master.stokPabrik = resStok.rincian || resStok.results || resStok || []
            master.entitas = resEntitas.data?.results || resEntitas.data || []
        } catch (err) {
            console.error(err)
        }
    }

    const simpanDistribusi = async () => {
        sedangProses.value = true
        try {
            const tokoTerpilih = master.toko.find(t => t.id === form.tujuan_toko_id)
            const itemsValid = form.items.filter(i => i.barang_nama && i.stok_terpilih)
            
            const payload = {
                entitas_id: parseInt(form.entitas_id, 10),
                jenis_tujuan: 'CABANG',
                tujuan_cabang_id: parseInt(form.tujuan_toko_id, 10),
                pelanggan_nama: tokoTerpilih ? tokoTerpilih.nama : 'Cabang Retail',
                alamat: tokoTerpilih?.alamat || '-',
                tanggal: form.tanggal,
                berat_total_kg: itemsValid.reduce((sum, item) => sum + (parseFloat(item.total_berat) || 0), 0),
                baris: itemsValid.map(i => ({
                    produk_id: i.stok_terpilih.item_id || i.stok_terpilih.produk_id || i.stok_terpilih.id,
                    kemasan: i.kemasan,
                    qty: parseInt(i.total_unit, 10) || 1
                }))
            }
            await apiDistribusi.createDistribusi(payload)
            router.push('/distribusi')
        } catch (err) {
            console.error(err)
        } finally {
            sedangProses.value = false
        }
    }

    return {
        form,
        master,
        sedangProses,
        daftarBarangUnik,
        tambahItem,
        hapusItem,
        getKemasanTersedia,
        resetKemasan,
        hitungOtomatis,
        kalkulasiBerat,
        muatDataMaster,
        simpanDistribusi
    }
}