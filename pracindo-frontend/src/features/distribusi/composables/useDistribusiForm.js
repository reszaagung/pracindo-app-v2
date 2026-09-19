// src/features/distribusi/composables/useDistribusiForm.js

import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { apiDistribusi } from '@/features/distribusi/api'
import api from '@/utils/api'

// Import fungsi dari Utility yang baru kita buat
import { getGrupUnik, getBarangTersedia as utilBarang, getKemasanTersedia as utilKemasan, getInfoStokBarang as utilInfo } from '@/utils/stockUtils'

export function useDistribusiForm() {
    const router = useRouter()
    const sedangProses = ref(false)
    const sedangMuatStok = ref(false)

    const daftarToko = ref([])
    const daftarArmada = ref([])
    const daftarStokPabrik = ref([])

    const form = reactive({
        tanggal: new Date().toISOString().split('T')[0],
        tujuan_toko_id: '',
        kendaraan_id: '',
        items: [
            { stiker: '', barang_nama: '', stok_terpilih: null, kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 }
        ]
    })

    const previewNomor = computed(() => {
        const date = new Date(form.tanggal || new Date())
        const tahun = date.getFullYear()
        const romawi = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
        const bulan = romawi[date.getMonth()]
        return `DO/MIX/${tahun}/${bulan}/[Otomatis]`
    })

    const tambahItem = () => form.items.push({ stiker: '', barang_nama: '', stok_terpilih: null, kemasan: '', total_unit: 1, total_berat: 0, berat_per_unit: 0 })
    const hapusItem = (index) => form.items.splice(index, 1)

    // LEMPAR KE UTILITY
    const daftarGrupUnik = computed(() => getGrupUnik(daftarStokPabrik.value))
    const getBarangTersedia = (item) => utilBarang(daftarStokPabrik.value, item, form.items)
    const getKemasanTersedia = (item) => utilKemasan(daftarStokPabrik.value, item, form.items)
    const getInfoStokBarang = (item) => utilInfo(daftarStokPabrik.value, item, form.items)

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
        if (!item.stok_terpilih) return
        const batasMaksimal = parseInt(item.stok_terpilih.qty_unit || item.stok_terpilih.qty) || 1
        if (item.total_unit > batasMaksimal) item.total_unit = batasMaksimal
        if (item.total_unit < 0) item.total_unit = 0
        item.total_berat = (item.berat_per_unit > 0 && item.total_unit > 0) ? (item.total_unit * item.berat_per_unit).toFixed(2) : 0
    }

    const muatDataMaster = async () => {
        sedangMuatStok.value = true
        try {
            const [resArmada, resToko, resStok] = await Promise.all([
                apiDistribusi.getArmada(),
                api.get('retail/cabang/'),
                apiDistribusi.getStokPabrik()
            ])
            daftarArmada.value = resArmada.results || resArmada || []
            daftarToko.value = resToko.data?.results || resToko.data || []
            daftarStokPabrik.value = resStok.rincian || resStok.results || resStok || []
        } catch (err) {
            console.error(err)
        } finally {
            sedangMuatStok.value = false
        }
    }

const simpanDistribusi = async () => {
        sedangProses.value = true
        try {
            const tokoTerpilih = daftarToko.value.find(t => t.id === form.tujuan_toko_id)
            const itemsValid = form.items.filter(i => i.stiker && i.barang_nama && i.stok_terpilih && parseInt(i.total_unit) > 0)
            
            if (itemsValid.length === 0) {
                alert('Peringatan: Tidak ada barang valid untuk dikirim.')
                sedangProses.value = false
                return
            }

            const headerEntitasId = itemsValid[0].stok_terpilih.entitas_id;

            const payload = {
                entitas_id: headerEntitasId,
                jenis_tujuan: 'CABANG',
                tujuan_cabang_id: parseInt(form.tujuan_toko_id, 10),
                pelanggan_nama: tokoTerpilih ? tokoTerpilih.nama : 'Cabang Retail',
                alamat: tokoTerpilih?.alamat || '-',
                berat_total_kg: itemsValid.reduce((sum, i) => sum + (parseFloat(i.total_berat) || 0), 0),
                
                baris: itemsValid.map(i => {
                    const rowEntitasId = i.stok_terpilih.entitas_id;
                    const barisData = {
                        produk_id: i.stok_terpilih.item_id || i.stok_terpilih.produk_id || i.stok_terpilih.id,
                        kemasan: i.kemasan,
                        stiker: i.stiker,
                        qty: parseInt(i.total_unit, 10) || 1
                    };

                    if (rowEntitasId !== headerEntitasId) {
                        barisData.entitas_id = rowEntitasId;
                    }

                    return barisData;
                })
            }


            await apiDistribusi.createDistribusi(payload)
            router.push('/distribusi/monitoring')
        } catch (err) {
            console.error(err)
            alert('Gagal menyimpan request distribusi.')
        } finally {
            sedangProses.value = false
        }
    }

    return {
        sedangProses, sedangMuatStok, daftarToko, daftarArmada, daftarStokPabrik,
        form, previewNomor, daftarGrupUnik, 
        getBarangTersedia, 
        tambahItem, hapusItem, getKemasanTersedia, getInfoStokBarang, 
        resetBarang, resetKemasan, hitungOtomatis, kalkulasiBerat, 
        muatDataMaster, simpanDistribusi
    }
}