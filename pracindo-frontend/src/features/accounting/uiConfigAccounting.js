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

export const akuntingModul = {
    id: 'akunting',
    nama: 'Input Entry',
    ringkas: 'Purchase order, faktur, dan pembayaran',
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

/*
|--------------------------------------------------------------------------
| MONITORING AKUNTING
|--------------------------------------------------------------------------
| Modul ini menjadi entry point layar IDS.
| /accounting = dashboard utama
| /accounting/monitoring = IDS fullscreen
*/
export const monitoringAkuntingModul = {
    id: 'monitoring_akunting',
    nama: 'Monitoring Akunting',
    ringkas: 'Informasi saldo kas, tagihan, dan kondisi jatuh tempo',
    ikon: 'pi-chart-bar',
    rute: '/accounting',
    siap: true,
    menu: [
        {
            id: 'monitoring',
            label: 'Information Display',
            ikon: 'pi-desktop',
            rute: '/accounting',
            activate: true,
        },

        {
            id: 'monitoring-fullscreen',
            label: 'IDS Fullscreen',
            ikon: 'pi-window-maximize',
            rute: '/accounting/monitoring',
            activate: true,
        },
    ],
}