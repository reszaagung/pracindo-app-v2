export const RETAIL_MODUL = [
  {
    id: 'pos',
    nama: 'Mesin Kasir (POS)',
    ringkas: 'Antarmuka Point of Sale untuk transaksi pelanggan.',
    ikon: 'transaksi',
    rute: '/kasir',
    siap: true,
  },
  {
    id: 'riwayat',
    nama: 'Riwayat Transaksi',
    ringkas: 'Cek struk, retur barang, dan pembatalan transaksi.',
    ikon: 'buku',
    rute: '/kasir/riwayat',
    siap: true,
  },
  {
    id: 'pembukuan',
    nama: 'Pembukuan Cabang',
    ringkas: 'Input jurnal, kas kecil, dan mutasi pengeluaran toko.',
    ikon: 'buku',
    rute: '/pembukuan/jurnal',
    siap: true,
  },
  {
    id: 'stok',
    nama: 'Stok & Opname',
    ringkas: 'Modul untuk cek stok warna dan opname harian cabang.',
    ikon: 'gudang',
    rute: '/stok', 
    siap: true,     
  },
]

export const IKON = {
  transaksi: '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/>',
  buku: '<path d="M5 3h14v18H5zM9 8h6M9 12h6M9 16h3"/>',
  gudang: '<path d="M3 9l9-5 9 5v11H3z"/><path d="M8 20v-7h8v7"/>',
  kirim: '<path d="M2 7h11v9H2zM13 10h4l3 3v3h-7z"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
  master: '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.7 3.1 3 7 3s7-1.3 7-3V6"/>',
  panah: '<path d="M5 12h14M12 5l7 7-7 7"/>',
}