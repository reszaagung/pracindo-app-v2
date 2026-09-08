export const gudangModul = {
  id: 'gudang',
  nama: 'Penerimaan & Packing',
  ringkas: 'Penerimaan barang, pengemasan (packing), laporan selisih, dan QC',
  ikon: 'box',
  rute: '/warehouse/input/receipt',
  siap: true,
  menu: [
    { label: 'Penerimaan', rute: '/warehouse/input/receipt' },
    { label: 'Packing Barang', rute: '/warehouse/input/packing' },
    { label: 'Selisih / Retur', rute: '/warehouse/input/discrepancy' },
    { label: 'Inspeksi QC', rute: '/warehouse/input/qc' },
  ]
}