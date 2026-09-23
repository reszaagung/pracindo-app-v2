// src/features/inventory/uiConfigInventory.js
export const inventoryModul = {
    id: 'inventory',
    nama: 'Inventory',
    ringkas: 'Stok tiga lapis dan posisi klaim',
    ikon: 'gudang',
    rute: '/inventory',
    siap: true,
    sembunyiDiDashboardUntuk: ['AKUNTING'],
    menu: [
        {
            label: 'Stok',
            rute: '/inventory/stock',
        },
        {
            label: 'Monitoring Tangki',
            rute: '/inventory/tank-monitor',
        },
        {
            label: 'Posisi Klaim',
            rute: '/inventory/claim-position',
        },
    ],
}