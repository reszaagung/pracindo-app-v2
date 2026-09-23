export const menuTransaksi = [
    {
        id: 'po',
        label: 'Purchase Order (PO)',
        rute: '/accounting/input/po',
        ikon: 'pi-file-edit',
        activate: true,
    },

    {
        id: 'so',
        label: 'Sales Order (SO)',
        rute: '/accounting/input/so',
        ikon: 'pi-file-export',
        activate: true,
    },

    {
        id: 'pengeluaran',
        label: 'Catat Pengeluaran',
        rute: '/accounting/input/pengeluaran/buat',
        ikon: 'pi-wallet',
        activate: true,
    },
]

export const menuInvoice = [
    {
        id: 'dokumen',
        label: 'Dokumen & Audit',
        ikon: 'pi-folder-open',
        rute: '/accounting/invoice/dokumen',
        activate: true,
    },

    {
        id: 'tagihan',
        label: 'Manajemen Tagihan',
        ikon: 'pi-receipt',
        rute: '/accounting/invoice/tagihan',
        activate: true,
    },

    {
        id: 'catatan',
        label: 'Catatan Pengeluaran',
        ikon: 'pi-wallet',
        rute: '/accounting/invoice/catatan',
        activate: true,
    },
]

export const menuMonitoring = [
    {
        id: 'monitoring',
        label: 'Monitoring Akunting',
        ikon: 'pi-chart-bar',
        rute: '/accounting/monitoring',
        activate: true,
    },
]

export const akuntingModul = {
    id: 'akunting',
    nama: 'Input Entry',
    ringkas: 'Purchase order, sales order, dan pengeluaran',
    ikon: 'buku',
    rute: '/accounting/input',
    siap: true,
    menu: menuTransaksi,
}

export const bukuTagihanModul = {
    id: 'buku_tagihan',
    nama: 'Buku Tagihan',
    ringkas: 'Manajemen invoice, dokumen, dan catatan pengeluaran',
    ikon: 'transaksi',
    rute: '/accounting/invoice',
    siap: true,
    menu: menuInvoice,
}

export const monitoringAkuntingModul = {
    id: 'monitoring_akunting',
    nama: 'Monitoring',
    ringkas: 'Pantau posisi kas, tagihan, transaksi, dan kondisi akunting',
    ikon: 'chart',
    rute: '/accounting/monitoring',
    siap: true,
    menu: menuMonitoring,
}