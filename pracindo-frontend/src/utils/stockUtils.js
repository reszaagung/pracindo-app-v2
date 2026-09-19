// src/utils/stockUtils.js

export const getNamaAsli = (data) => {
    if (!data) return 'Barang Unknown'
    return data.item_nama || data.produk_nama || data.nama || (data.produk && data.produk.nama) || 'Barang Unknown'
}

export const getNamaGrup = (data) => {
    if (!data) return 'Grup Umum'
    if (data.entitas_kode) {
        if (String(data.entitas_kode).toUpperCase().includes('PCJM')) {
            return 'PT — PT'
        }
        return 'CV — CV'
    }
    return 'Grup Umum'
}

export const getGrupUnik = (daftarStok) => {
    const map = new Map()
    if (daftarStok && daftarStok.length > 0) {
        daftarStok.forEach(stok => {
            const grup = getNamaGrup(stok)
            if (grup) map.set(grup, grup)
        })
    }
    return Array.from(map.values())
}

export const getKemasanTersedia = (daftarStok, barisAktif, semuaBaris, filterNamaBarang = null) => {
    if (!barisAktif || !barisAktif.stiker) return []
    
    const targetBarang = filterNamaBarang || barisAktif.barang_nama;
    if (!targetBarang) return [];

    const kemasanTerpakaiIds = semuaBaris
        .filter(b => 
            b !== barisAktif && 
            b.stiker === barisAktif.stiker && 
            b.barang_nama === targetBarang && 
            b.stok_terpilih
        )
        .map(b => b.stok_terpilih.id || b.stok_terpilih.kemasan_nama || b.stok_terpilih.kemasan || 'CURAH')

    return daftarStok.filter(stok => {
        const matchGrup = getNamaGrup(stok) === barisAktif.stiker
        const matchBarang = getNamaAsli(stok) === targetBarang
        
        const idKemasanStok = stok.id || stok.kemasan_nama || stok.kemasan || 'CURAH'
        
        return matchGrup && matchBarang && !kemasanTerpakaiIds.includes(idKemasanStok)
    })
}

export const getBarangTersedia = (daftarStok, barisAktif, semuaBaris) => {
    if (!barisAktif || !barisAktif.stiker) return []
    const map = new Map()
    
    daftarStok.forEach(stok => {
        if (getNamaGrup(stok) === barisAktif.stiker) {
            const namaBarang = getNamaAsli(stok)
            
            const sisaKemasan = getKemasanTersedia(daftarStok, barisAktif, semuaBaris, namaBarang)
            
            if (sisaKemasan.length > 0 && !map.has(namaBarang)) {
                map.set(namaBarang, namaBarang)
            }
        }
    })
    return Array.from(map.values())
}

export const getInfoStokBarang = (daftarStok, barisAktif, semuaBaris) => {
    if (!barisAktif || !barisAktif.barang_nama || !barisAktif.stiker) return ''
    
    const kemasanList = getKemasanTersedia(daftarStok, barisAktif, semuaBaris)
    
    if (!kemasanList.length) return 'Semua varian kemasan sudah dipilih di baris lain'
    
    const rincian = kemasanList.map(k => {
        const qty = k.qty_unit || k.qty || 0
        const namaKemasan = k.kemasan_nama || k.kemasan || 'Unknown'
        return `${qty} ${namaKemasan}`
    })
    return 'Tersedia: ' + rincian.join(', ')
}