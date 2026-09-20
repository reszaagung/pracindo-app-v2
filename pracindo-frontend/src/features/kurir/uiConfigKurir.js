export const STATUS_WARNA = {
    'MENUNGGU': 'bg-slate-100 text-slate-600 border-slate-200',
    'DISIAPKAN': 'bg-orange-100 text-orange-700 border-orange-200',
    'BERANGKAT': 'bg-blue-100 text-blue-700 border-blue-200',
    'SAMPAI': 'bg-purple-100 text-purple-700 border-purple-200',
    'DITERIMA': 'bg-emerald-100 text-emerald-700 border-emerald-200',
    'SELESAI': 'bg-emerald-100 text-emerald-700 border-emerald-200',
    'RETUR': 'bg-rose-100 text-rose-700 border-rose-200',
    'DIRETUR': 'bg-rose-100 text-rose-700 border-rose-200',
}

export const STATUS_LABEL = {
    'MENUNGGU': 'Menunggu Kurir',
    'DISIAPKAN': 'Sedang Disiapkan',
    'BERANGKAT': 'Dalam Perjalanan',
    'SAMPAI': 'Tiba di Tujuan',
    'DITERIMA': 'Bukti Diterima',
    'SELESAI': 'Terkirim Selesai',
    'RETUR': 'Retur Dicatat',
    'DIRETUR': 'Barang Diretur',
}

export const BOTTOM_NAV_MENU = [
    { 
        name: 'Permintaan', 
        path: '/kurir/permintaan', 
        iconPath: 'M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4',
        hasBadge: true 
    },
    { 
        name: 'Tugas Saya',
        path: '/kurir/tugas-saya',
        iconPath: 'M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0' 
    },
    { 
        name: 'Riwayat', 
        path: '/kurir/riwayat', // PERBAIKAN: Disesuaikan dengan router (bukan history)
        iconPath: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' 
    },
    {   
        name: 'Profil',
        path: '/kurir/profil',
        routeName: 'KurirProfil',
        iconPath: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z'
    }
]

export const JENIS_UPLOAD = {
    SURAT_JALAN: { 
        id: 'surat_jalan', 
        label: 'Surat Jalan', 
        ikon: '📸', 
        accept: 'image/*' 
    },
    STRUK_BON: { 
        id: 'struk_bon', 
        label: 'Struk / Bon', 
        ikon: '📄', 
        accept: 'image/*,application/pdf' 
    }
}