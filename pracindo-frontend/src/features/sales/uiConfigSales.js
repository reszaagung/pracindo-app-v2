// src/features/sales/uiConfigSales.js

// ============================================================
// Konstanta & helper bersama untuk modul Sales
// ============================================================

export function formatRupiah(v) {
  return `Rp ${Number(v || 0).toLocaleString('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`
}

export function formatTanggal(v) {
  if (!v) return '-'
  const d = new Date(v)
  if (isNaN(d)) return v
  return (
    d.toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' })
  )
}

// 1. EXPORT INI DIBUTUHKAN OLEH SalesLayout.vue (UNTUK SIDEBAR)
export const salesMenu = [
    { label: 'CRM & Eksekusi', icon: 'pi pi-users', to: '/sales/crm' },
    { label: 'Sales & Distribusi', icon: 'pi pi-chart-line', to: '/sales/orders' }
]

// 2. EXPORT INI DIBUTUHKAN OLEH DashboardView.vue (UNTUK KOTAK MENU)
export const salesModul = {
    id: 'sales_order',
    nama: 'Sales Order',
    ringkas: 'Manajemen CRM prospek, konversi SO, dan pelacakan target',
    ikon: 'transaksi', 
    rute: '/sales/crm', 
    siap: true,
    catatan: '',
    menu: [
        { label: 'Papan CRM', rute: '/sales/crm' },
        { label: 'Sales Orders', rute: '/sales/orders' }
    ]
}