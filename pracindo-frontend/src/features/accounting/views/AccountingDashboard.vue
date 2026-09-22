<template>
    <div
        class="min-h-screen bg-slate-100 p-3 sm:p-4 lg:p-5"
    >
        <div
            class="grid grid-cols-1 xl:grid-cols-[240px_minmax(0,1fr)] gap-4 h-full"
        >
            <!-- MODULE -->
            <aside
                class="rounded-3xl border border-slate-200 bg-white p-3 shadow-sm"
            >
                <div
                    class="px-3 py-3 border-b border-slate-100 mb-3"
                >
                    <div
                        class="text-[10px] font-black tracking-[0.25em] text-slate-400"
                    >
                        ACCOUNTING
                    </div>

                    <div
                        class="mt-1 text-lg font-black text-slate-900"
                    >
                        Module
                    </div>
                </div>

                <nav class="space-y-2">
                    <RouterLink
                        v-for="item in modules"
                        :key="item.name"
                        :to="item.to"
                        class="block rounded-2xl border p-4 transition"
                        :class="
                            route.path.startsWith(item.to)
                                ? 'border-slate-900 bg-slate-950 text-white'
                                : 'border-slate-200 bg-slate-50 text-slate-800 hover:bg-slate-100'
                        "
                    >
                        <div
                            class="text-sm font-black"
                        >
                            {{ item.label }}
                        </div>

                        <div
                            class="mt-1 text-[11px]"
                            :class="
                                route.path.startsWith(item.to)
                                    ? 'text-slate-400'
                                    : 'text-slate-500'
                            "
                        >
                            {{ item.description }}
                        </div>
                    </RouterLink>
                </nav>
            </aside>

            <!-- IDS -->
            <main class="min-w-0">
                <AccountingMonitoringDisplay />
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
        to: '/accounting/input/po',
    },
    {
        name: 'so',
        label: 'Sales Order',
        description: 'Pesanan penjualan',
        to: '/accounting/input/so',
    },
    {
        name: 'invoice',
        label: 'Invoice',
        description: 'Buku tagihan',
        to: '/accounting/invoice/tagihan',
    },
    {
        name: 'expense',
        label: 'Pengeluaran',
        description: 'Input pengeluaran',
        to: '/accounting/input/pengeluaran/buat',
    },
]
</script>