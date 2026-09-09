export const distribusiModul = {
  id: 'warehouse_distribusi',
  nama: 'Distribusi Pengiriman',
  ringkas: 'Manajemen jadwal pengiriman, perakitan muatan, dan status armada',
  ikon: 'truck',
  rute: '/distribusi',
  siap: true,
  menu: [
    { label: 'Jadwal Pengiriman', rute: '/distribusi' },
    { label: 'Rakit Pengiriman', rute: '/distribusi/buat' },
    { label: 'Loading Muatan', rute: '/distribusi/loading' },
    { label: 'Status Armada', rute: '/distribusi/armada' }
  ]
}