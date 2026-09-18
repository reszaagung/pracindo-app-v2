import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { apiDistribusi } from '@/features/distribusi/api'
import api from '@/utils/api'

export function useDistribusiForm() {
    const router = useRouter()
    const sedangProses = ref(false)
    const sedangMuatStok = ref(false)

    const daftarEntitas = ref([])
    const daftarToko = ref([])
    const daftarArmada = ref([])
    const daftarStokPabrik = ref([])

    const form = reactive({
        entitas_id: '',
        tanggal: new Date().toISOString().split('T')[0],
        tujuan_toko_id: '',
        nomor_surat_jalan: 'Otomatis (Saat Disimpan)',
        kendaraan_id: '',
        items: [
            { stiker: '', barang_nama: '', stok_terpilih: null, kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 }
        ]
    })

    const previewNomor = computed(() => {
        if (!form.entitas_id) return 'Otomatis (Pilih Perusahaan)'
        const entitas = daftarEntitas.value.find(e => e.id === form.entitas_id)
        if (!entitas) return 'Otomatis (Setelah Disimpan)'
        
        const date = new Date()
        const tahun = date.getFullYear()
        const romawi = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
        const bulan = romawi[date.getMonth()]
        
        return `DO/${entitas.kode}/${tahun}/${bulan}/[Otomatis]`
    })

    const tambahItem = () => form.items.push({ stiker: '', barang_nama: '', stok_terpilih: null, kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 })
    const hapusItem = (index) => form.items.splice(index, 1)

    // Helper Penamaan
    const getNamaAsli = (data) => {
        if (!data) return 'Barang Unknown'
        return data.item_nama || data.produk_nama || data.nama || (data.produk && data.produk.nama) || 'Barang Unknown'
    }

    const getNamaGrup = (data) => {
        if (!data) return ''
        let grup = data.grup_bahan_nama || data.grup_bahan || data.entitas_nama || ''
        if (typeof grup === 'object') return grup.nama || grup.kode || 'Grup Terdeteksi'
        return String(grup)
    }

    // Ekstrak Daftar Grup Unik
    const daftarGrupUnik = computed(() => {
        const map = new Map()
        daftarStokPabrik.value.forEach(stok => {
            const grup = getNamaGrup(stok)
            if (grup && !map.has(grup)) map.set(grup, grup)
        })
        return Array.from(map.values())
    })

    // Ekstrak Barang Berdasarkan Grup
    const getBarangTersedia = (grupDipilih) => {
        if (!grupDipilih) return []
        const map = new Map()
        daftarStokPabrik.value.forEach(stok => {
            if (getNamaGrup(stok) === grupDipilih) {
                const namaBarang = getNamaAsli(stok)
                if (namaBarang && !map.has(namaBarang)) map.set(namaBarang, namaBarang)
            }
        })
        return Array.from(map.values())
    }

    // Ekstrak Kemasan Berdasarkan Barang DAN Grup
    const getKemasanTersedia = (namaBarang, grupDipilih) => {
        if (!namaBarang || !grupDipilih) return []
        return daftarStokPabrik.value.filter(stok => 
            getNamaAsli(stok) === namaBarang && getNamaGrup(stok) === grupDipilih
        )
    }

    const getInfoStokBarang = (item) => {
        if (!item.barang_nama || !item.stiker) return ''
        const kemasanList = getKemasanTersedia(item.barang_nama, item.stiker)
        if (!kemasanList.length) return 'Stok kosong'
        
        const rincian = kemasanList.map(k => {
            const qty = k.qty_unit || k.qty || 0
            const namaKemasan = k.kemasan_nama || k.kemasan || 'Unknown'
            return `${qty} ${namaKemasan}`
        })
        return 'Stok: ' + rincian.join(', ')
    }

    // Reset Bertingkat
    const resetBarang = (item) => {
        item.barang_nama = ''
        resetKemasan(item)
    }

    const resetKemasan = (item) => {
        item.stok_terpilih = null
        item.kemasan = ''
        item.total_unit = 1
        item.total_berat = 0
        item.berat_per_unit = 0
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

    const kalkulasiBerat = (item) => {
        const batasMaksimal = item.stok_terpilih?.qty_unit || item.stok_terpilih?.qty || 1
        if (item.total_unit > batasMaksimal) item.total_unit = batasMaksimal
        item.total_berat = (item.berat_per_unit > 0 && item.total_unit > 0) ? (item.total_unit * item.berat_per_unit).toFixed(2) : 0
    }

    const pilihEntitas = async () => {
        form.items = [{ stiker: '', barang_nama: '', stok_terpilih: null, kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 }]
        daftarStokPabrik.value = []
        if (!form.entitas_id) return
        
        sedangMuatStok.value = true
        try {
            const resStok = await apiDistribusi.getStokPabrik({ entitas: form.entitas_id })
            daftarStokPabrik.value = resStok.rincian || resStok.results || resStok || []
        } catch (err) {
            console.error(err)
        } finally {
            sedangMuatStok.value = false
        }
    }

    const muatDataMaster = async () => {
        try {
            const [resArmada, resToko, resEntitas] = await Promise.all([
                apiDistribusi.getArmada(),
                api.get('retail/cabang/'),
                api.get('core/entitas/').catch(() => ({ data: { results: [] } }))
            ])
            daftarArmada.value = resArmada.results || resArmada || []
            daftarToko.value = resToko.data?.results || resToko.data || []
            
            let entitasData = resEntitas.data?.results || resEntitas.data || []
            if (Array.isArray(entitasData)) {
                daftarEntitas.value = entitasData.filter(e => e.aktif !== false)
            }
        } catch (err) {
            console.error(err)
        }
    }

    const simpanDistribusi = async () => {
        sedangProses.value = true
        try {
            const tokoTerpilih = daftarToko.value.find(t => t.id === form.tujuan_toko_id)
            const itemsValid = form.items.filter(i => i.stiker && i.barang_nama && i.stok_terpilih)
            
            const payload = {
                entitas_id: parseInt(form.entitas_id, 10),
                jenis_tujuan: 'CABANG',
                tujuan_cabang_id: parseInt(form.tujuan_toko_id, 10),
                pelanggan_nama: tokoTerpilih ? tokoTerpilih.nama : 'Cabang Retail',
                alamat: tokoTerpilih?.alamat || '-',
                tanggal: form.tanggal,
                berat_total_kg: itemsValid.reduce((sum, i) => sum + (parseFloat(i.total_berat) || 0), 0),
                baris: itemsValid.map(i => ({
                    produk_id: i.stok_terpilih.item_id || i.stok_terpilih.produk_id || i.stok_terpilih.id,
                    kemasan: i.kemasan,
                    stiker: i.stiker,
                    qty: parseInt(i.total_unit, 10) || 1
                }))
            }
            await apiDistribusi.createDistribusi(payload)
            router.push('/distribusi/monitoring')
        } catch (err) {
            console.error(err)
            alert('Gagal menyimpan.')
        } finally {
            sedangProses.value = false
        }
    }

    return {
        sedangProses, sedangMuatStok, daftarEntitas, daftarToko, daftarArmada, daftarStokPabrik,
        form, previewNomor, daftarGrupUnik, // 👈 Diexport
        getBarangTersedia, // 👈 Diexport
        tambahItem, hapusItem, getKemasanTersedia, getInfoStokBarang, 
        resetBarang, resetKemasan, hitungOtomatis, kalkulasiBerat, pilihEntitas, 
        muatDataMaster, simpanDistribusi
    }
}