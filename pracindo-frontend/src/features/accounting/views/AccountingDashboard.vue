<template>
    <div
        class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 p-3 sm:p-4 lg:p-6"
    >
        <div
            class="grid grid-cols-1 xl:grid-cols-[270px_minmax(0,1fr)] gap-4 lg:gap-6 min-h-[calc(100vh-1.5rem)]"
        >
            <aside
                class="rounded-[28px] border border-slate-200/80 bg-white shadow-[0_12px_40px_rgba(15,23,42,0.06)] p-3 h-fit xl:sticky xl:top-6"
            >
                <div
                    class="px-4 pt-4 pb-5 border-b border-slate-100"
                >
                    <div
                        class="flex items-center gap-3"
                    >
                        <div
                            class="w-11 h-11 rounded-2xl bg-slate-950 text-white flex items-center justify-center shadow-lg shadow-slate-900/10"
                        >
                            <i
                                class="pi pi-chart-line text-lg"
                            ></i>
                        </div>

                        <div class="min-w-0">
                            <div
                                class="text-[10px] font-bold tracking-[0.22em] text-slate-400 uppercase"
                            >
                                Accounting
                            </div>

                            <div
                                class="mt-1 text-lg font-black text-slate-900 tracking-tight"
                            >
                                Module
                            </div>
                        </div>
                    </div>

                    <div
                        class="mt-4 rounded-2xl bg-slate-50 border border-slate-100 px-4 py-3"
                    >
                        <div
                            class="text-[10px] font-bold uppercase tracking-wider text-slate-400"
                        >
                            Ruang Kerja
                        </div>

                        <div
                            class="mt-1 text-xs font-semibold text-slate-700"
                        >
                            Kelola transaksi, master, dan monitoring
                        </div>
                    </div>
                </div>

                <nav class="mt-4 space-y-2">
                    <RouterLink
                        v-for="item in modules"
                        :key="item.name"
                        :to="item.to"
                        class="group relative block rounded-2xl border p-4 transition-all duration-200"
                        :class="
                            route.path === item.to ||
                            route.path.startsWith(item.to + '/')
                                ? 'border-slate-900 bg-slate-950 text-white shadow-lg shadow-slate-950/10'
                                : 'border-slate-200 bg-white text-slate-800 hover:border-slate-300 hover:bg-slate-50 hover:-translate-y-[1px]'
                        "
                    >
                        <div class="flex items-start gap-3">
                            <div
                                class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0"
                                :class="
                                    route.path === item.to ||
                                    route.path.startsWith(item.to + '/')
                                        ? 'bg-white/10 text-white'
                                        : 'bg-slate-100 text-slate-500 group-hover:bg-slate-200'
                                "
                            >
                                <i
                                    :class="[
                                        'pi',
                                        item.icon
                                    ]"
                                ></i>
                            </div>

                            <div class="min-w-0 flex-1">
                                <div
                                    class="text-sm font-bold leading-tight"
                                >
                                    {{ item.label }}
                                </div>

                                <div
                                    class="mt-1 text-[11px] leading-relaxed"
                                    :class="
                                        route.path === item.to ||
                                        route.path.startsWith(item.to + '/')
                                            ? 'text-slate-400'
                                            : 'text-slate-500'
                                    "
                                >
                                    {{ item.description }}
                                </div>
                            </div>

                            <i
                                class="pi pi-angle-right text-xs mt-1 transition-transform duration-200"
                                :class="
                                    route.path === item.to ||
                                    route.path.startsWith(item.to + '/')
                                        ? 'text-white'
                                        : 'text-slate-300 group-hover:translate-x-0.5 group-hover:text-slate-500'
                                "
                            ></i>
                        </div>
                    </RouterLink>
                </nav>
            </aside>

            <main class="min-w-0">
                <div
                    class="rounded-[28px] border border-slate-200/80 bg-white/90 shadow-[0_12px_40px_rgba(15,23,42,0.05)] overflow-hidden min-h-full"
                >
                    <div
                        class="px-4 sm:px-6 lg:px-8 pt-5 sm:pt-6 lg:pt-7 pb-4"
                    >
                        <div
                            class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
                        >
                            <div>
                                <div
                                    class="flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-400"
                                >
                                    <span>
                                        Accounting
                                    </span>

                                    <i
                                        class="pi pi-angle-right text-[9px]"
                                    ></i>

                                    <span
                                        class="text-slate-600"
                                    >
                                        Dashboard
                                    </span>
                                </div>

                                <h1
                                    class="mt-2 text-xl sm:text-2xl lg:text-3xl font-black tracking-tight text-slate-900"
                                >
                                    Accounting Dashboard
                                </h1>

                                <p
                                    class="mt-1 text-xs sm:text-sm text-slate-500"
                                >
                                    Akses cepat transaksi dan master data accounting.
                                </p>
                            </div>

                            <div
                                class="inline-flex items-center gap-2 self-start sm:self-auto rounded-full border border-emerald-200 bg-emerald-50 px-3 py-2"
                            >
                                <span
                                    class="w-2 h-2 rounded-full bg-emerald-500"
                                ></span>

                                <span
                                    class="text-[11px] font-bold text-emerald-700"
                                >
                                    Sistem Aktif
                                </span>
                            </div>
                        </div>
                    </div>

                    <div
                        class="px-4 sm:px-6 lg:px-8 pb-6 lg:pb-8"
                    >
                        <div
                            class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4"
                        >
                            <RouterLink
                                v-for="item in quickAccess"
                                :key="item.name"
                                :to="item.to"
                                class="group rounded-2xl border border-slate-200 bg-white p-5 hover:border-slate-300 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-200"
                            >
                                <div
                                    class="flex items-start justify-between gap-4"
                                >
                                    <div
                                        class="w-11 h-11 rounded-2xl flex items-center justify-center"
                                        :class="item.iconBg"
                                    >
                                        <i
                                            :class="[
                                                'pi',
                                                item.icon,
                                                item.iconColor
                                            ]"
                                        ></i>
                                    </div>

                                    <i
                                        class="pi pi-arrow-up-right text-slate-300 group-hover:text-slate-700 transition-colors"
                                    ></i>
                                </div>

                                <div
                                    class="mt-5 text-sm font-black text-slate-900"
                                >
                                    {{ item.label }}
                                </div>

                                <div
                                    class="mt-1 text-xs leading-relaxed text-slate-500"
                                >
                                    {{ item.description }}
                                </div>
                            </RouterLink>
                        </div>

                        <div class="mt-6">
                            <AccountingMonitoringDisplay />
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

import AccountingMonitoringDisplay from '../components/monitoring/AccountingMonitoringDisplay.vue'

const route = useRoute()

const modules = [
    {
        name: 'po',
        label: 'Purchase Order',
        description: 'Pengadaan & supplier',
        icon: 'pi-file-edit',
        to: '/accounting/input/po'
    },
    {
        name: 'so',
        label: 'Sales Order',
        description: 'Pesanan penjualan',
        icon: 'pi-file-export',
        to: '/accounting/input/so'
    },
    {
        name: 'supplier',
        label: 'Master Supplier',
        description: 'Kelola data supplier',
        icon: 'pi-users',
        to: '/accounting/input/po'
    },
    {
        name: 'product',
        label: 'Master Produk',
        description: 'Kelola produk dan bahan',
        icon: 'pi-box',
        to: '/accounting/input/po'
    },
    {
        name: 'invoice',
        label: 'Invoice',
        description: 'Buku tagihan',
        icon: 'pi-receipt',
        to: '/accounting/invoice/tagihan'
    },
    {
        name: 'expense',
        label: 'Pengeluaran',
        description: 'Input pengeluaran',
        icon: 'pi-wallet',
        to: '/accounting/input/pengeluaran/buat'
    }
]

const quickAccess = [
    {
        name: 'po',
        label: 'Purchase Order',
        description: 'Buat dan kelola pesanan pembelian.',
        icon: 'pi-file-edit',
        iconBg: 'bg-teal-50',
        iconColor: 'text-teal-600',
        to: '/accounting/input/po'
    },
    {
        name: 'so',
        label: 'Sales Order',
        description: 'Kelola transaksi pesanan penjualan.',
        icon: 'pi-file-export',
        iconBg: 'bg-blue-50',
        iconColor: 'text-blue-600',
        to: '/accounting/input/so'
    },
    {
        name: 'supplier',
        label: 'Master Supplier',
        description: 'Kelola data supplier aktif dan informasi supplier.',
        icon: 'pi-users',
        iconBg: 'bg-violet-50',
        iconColor: 'text-violet-600',
        to: '/accounting/input/po'
    },
    {
        name: 'product',
        label: 'Master Produk',
        description: 'Kelola data bahan baku dan produk kemasan.',
        icon: 'pi-box',
        iconBg: 'bg-amber-50',
        iconColor: 'text-amber-600',
        to: '/accounting/input/po'
    },
    {
        name: 'invoice',
        label: 'Manajemen Invoice',
        description: 'Kelola dokumen dan buku tagihan.',
        icon: 'pi-receipt',
        iconBg: 'bg-rose-50',
        iconColor: 'text-rose-600',
        to: '/accounting/invoice/tagihan'
    },
    {
        name: 'expense',
        label: 'Catat Pengeluaran',
        description: 'Input dan kelola transaksi pengeluaran.',
        icon: 'pi-wallet',
        iconBg: 'bg-slate-100',
        iconColor: 'text-slate-700',
        to: '/accounting/input/pengeluaran/buat'
    }
]
</script>