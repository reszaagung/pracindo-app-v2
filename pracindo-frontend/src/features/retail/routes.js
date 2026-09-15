const RetailLayout = () => import('./layout/RetailLayout.vue')
const AkuntansiLayout = () => import('./layout/AkuntansiLayout.vue')

export const retailRoutes = [
  {
    // RUTE BARU: Halaman Login Retail (Publik / Tanpa Login)
    path: '/retail/login',
    name: 'LoginRetail',
    meta: { perluLogin: false, modul: 'retail' },
    component: () => import('./LoginRetail.vue')
  },
  {
    // Portal Utama (Pilihan Menu)
    path: '/retail',
    name: 'retail-portal',
    meta: { perluLogin: true, modul: 'retail' },
    component: () => import('./views/DashboardView.vue')
  },
  {
    // Akses langsung ke pendaftaran cabang dari pracindo.cloud/regretail
    path: '/regretail',
    name: 'RegistrasiCabang',
    meta: { perluLogin: true, modul: 'retail' },
    component: () => import('./views/RegistrasiCabang.vue')
  },
  {
    path: '/retail',
    component: RetailLayout,
    meta: { perluLogin: true, modul: 'retail' },
    children: [
      {
        path: 'pos',
        name: 'retail-pos',
        component: () => import('./views/PosView.vue')
      },
      {
        path: 'penerimaan',
        name: 'retail-penerimaan',
        component: () => import('./views/PenerimaanBarang.vue')
      },
      {
        path: 'piutang',
        name: 'retail-piutang',
        component: () => import('./views/PiutangView.vue')
      },
      {
        path: 'riwayat',
        name: 'retail-riwayat',
        component: () => import('./views/RiwayatView.vue')
      }
    ]
  },
  {
    path: '/akuntansi', 
    component: AkuntansiLayout,
    meta: { perluLogin: true, modul: 'akuntansi' },
    children: [
      {
        path: '',
        name: 'akuntansi-dashboard',
        component: () => import('./views/KeuanganView.vue')
      },
      {
        path: 'buku-besar',
        name: 'akuntansi-buku-besar',
        component: () => import('./views/BukuBesarView.vue')
      },
      {
        path: 'jurnal',
        name: 'akuntansi-jurnal',
        component: () => import('./views/EntryJurnalView.vue')
      }
    ]
  }
]