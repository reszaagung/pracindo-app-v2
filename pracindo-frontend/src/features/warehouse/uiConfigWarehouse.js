// src/features/warehouse/uiConfigWarehouse.js

export const gudangModul = {
  id: 'warehouse',
  nama: 'Gudang',
  ringkas: 'Penerimaan barang, pengemasan (packing), laporan selisih, dan QC',
  ikon: 'gudang',
  rute: '/warehouse/input/receipt',
  siap: true,
  menu: [
    { label: 'Penerimaan', rute: '/warehouse/input/receipt' },
    { label: 'Packing Barang', rute: '/warehouse/input/packing' },
    { label: 'Selisih / Retur', rute: '/warehouse/input/discrepancy' },
    { label: 'Inspeksi QC', rute: '/warehouse/input/qc' },
  ]
}

export const distribusiModul = {
  id: 'warehouse_distribusi',
  nama: 'Distribusi & Kemasan',
  ringkas: 'Manajemen jadwal pengiriman, armada, dan loading',
  ikon: 'kirim',
  rute: '/distribusi',
  siap: true,
  menu: [
    { label: 'Input Packing', rute: '/distribusi/packing' },
    { label: 'Riwayat Packing', rute: '/distribusi/packing/log' },
    { label: 'Jadwal Pengiriman', rute: '/distribusi' },
    { label: 'Rakit Pengiriman', rute: '/distribusi/buat' },
    { label: 'Loading Muatan', rute: '/distribusi/loading' },
    { label: 'Status Armada', rute: '/distribusi/armada' },
  ]
}