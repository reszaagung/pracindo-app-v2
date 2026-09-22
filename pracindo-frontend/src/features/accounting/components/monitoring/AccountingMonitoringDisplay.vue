<template>
    <section
        class="h-full min-h-[500px] rounded-[28px]
               border border-slate-200
               bg-slate-950 text-white
               overflow-hidden shadow-xl"
    >
        <!-- HEADER -->
        <div
            class="flex items-center justify-between
                   px-5 py-4
                   border-b border-slate-800"
        >
            <div>
                <div
                    class="text-[10px] font-black
                           tracking-[0.25em]
                           text-slate-500"
                >
                    ACCOUNTING
                </div>

                <h2
                    class="text-xl sm:text-2xl
                           font-black tracking-tight"
                >
                    INFORMATION DISPLAY
                </h2>
            </div>

            <div class="text-right">
                <div
                    class="text-xl sm:text-2xl
                           font-black tabular-nums"
                >
                    {{ waktuDisplay }}
                </div>

                <div
                    class="text-[10px]
                           text-slate-500"
                >
                    UPDATE {{ updateDisplay }}
                </div>
            </div>
        </div>

        <!-- STATUS -->
        <div
            class="px-5 pt-5"
        >
            <div
                class="rounded-2xl border px-4 py-4"
                :class="statusPanelClass"
            >
                <div
                    class="text-[10px]
                           tracking-[0.2em]
                           font-black"
                    :class="statusTextClass"
                >
                    STATUS OPERASIONAL
                </div>

                <div
                    class="mt-1 text-xl
                           font-black"
                >
                    {{ statusIDS.label }}
                </div>
            </div>
        </div>

        <!-- KPI -->
        <div
            class="grid grid-cols-2
                   xl:grid-cols-4
                   gap-3 p-5"
        >
            <div
                class="rounded-2xl
                       border border-slate-800
                       bg-slate-900 p-4"
            >
                <div
                    class="text-[10px]
                           font-black text-slate-500"
                >
                    SALDO KAS
                </div>

                <div
                    class="mt-2 text-lg
                           sm:text-2xl
                           font-black truncate"
                >
                    {{ formatUang(saldoKas) }}
                </div>
            </div>

            <div
                class="rounded-2xl
                       border border-slate-800
                       bg-slate-900 p-4"
            >
                <div
                    class="text-[10px]
                           font-black text-slate-500"
                >
                    TAGIHAN
                </div>

                <div
                    class="mt-2 text-lg
                           sm:text-2xl
                           font-black"
                >
                    {{ jumlahTagihan }}
                </div>

                <div
                    class="text-[10px]
                           text-slate-500"
                >
                    {{ formatUang(totalTagihan) }}
                </div>
            </div>

            <div
                class="rounded-2xl
                       border border-amber-500/20
                       bg-amber-950/20 p-4"
            >
                <div
                    class="text-[10px]
                           font-black text-amber-500"
                >
                    PERINGATAN
                </div>

                <div
                    class="mt-2 text-lg
                           sm:text-2xl
                           font-black text-amber-300"
                >
                    {{ jumlahPeringatan }}
                </div>
            </div>

            <div
                class="rounded-2xl
                       border border-red-500/20
                       bg-red-950/20 p-4"
            >
                <div
                    class="text-[10px]
                           font-black text-red-500"
                >
                    TERLAMBAT
                </div>

                <div
                    class="mt-2 text-lg
                           sm:text-2xl
                           font-black text-red-300"
                >
                    {{ jumlahTerlambat }}
                </div>
            </div>
        </div>

        <!-- CONTENT -->
        <div
            class="grid grid-cols-1
                   xl:grid-cols-[1.7fr_1fr]
                   gap-4 px-5 pb-5"
        >
            <!-- TAGIHAN -->
            <div
                class="rounded-2xl
                       border border-slate-800
                       bg-slate-900
                       overflow-hidden"
            >
                <div
                    class="px-4 py-3
                           border-b border-slate-800"
                >
                    <div
                        class="text-sm
                               font-black"
                    >
                        TAGIHAN SUPPLIER
                    </div>

                    <div
                        class="text-[10px]
                               text-slate-500"
                    >
                        Prioritas jatuh tempo
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table
                        class="w-full
                               min-w-[600px]"
                    >
                        <thead
                            class="bg-slate-950"
                        >
                            <tr>
                                <th class="th">
                                    SUPPLIER
                                </th>

                                <th class="th">
                                    PO
                                </th>

                                <th class="th">
                                    TEMPO
                                </th>

                                <th class="th text-right">
                                    SISA
                                </th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr
                                v-for="item in tagihan.slice(0, 8)"
                                :key="item.id"
                                class="border-t
                                       border-slate-800"
                            >
                                <td class="td font-bold">
                                    {{ item.supplier }}
                                </td>

                                <td
                                    class="td text-slate-400
                                           font-mono"
                                >
                                    {{ item.no_po }}
                                </td>

                                <td class="td">
                                    {{ labelHari(item.hari_tersisa) }}
                                </td>

                                <td
                                    class="td text-right
                                           font-black"
                                >
                                    {{ formatUang(item.sisa_hutang) }}
                                </td>
                            </tr>

                            <tr
                                v-if="!tagihan.length"
                            >
                                <td
                                    colspan="4"
                                    class="px-4 py-10
                                           text-center
                                           text-slate-600"
                                >
                                    Tidak ada tagihan terbuka.
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- KAS -->
            <div
                class="rounded-2xl
                       border border-slate-800
                       bg-slate-900"
            >
                <div
                    class="px-4 py-3
                           border-b border-slate-800"
                >
                    <div
                        class="text-sm
                               font-black"
                    >
                        POSISI KAS
                    </div>
                </div>

                <div class="p-4 space-y-3">
                    <div
                        v-for="item in rekening"
                        :key="item.id"
                        class="rounded-xl
                               bg-slate-950
                               border border-slate-800
                               p-4"
                    >
                        <div
                            class="flex
                                   justify-between
                                   gap-3"
                        >
                            <div>
                                <div
                                    class="font-bold
                                           text-slate-200"
                                >
                                    {{
                                        item.nama ||
                                        item.nama_bank ||
                                        'Kas'
                                    }}
                                </div>

                                <div
                                    class="text-[10px]
                                           text-slate-600"
                                >
                                    {{ item.jenis || 'KAS_KECIL' }}
                                </div>
                            </div>

                            <div
                                class="font-black
                                       text-right"
                            >
                                {{ formatUang(item.saldo) }}
                            </div>
                        </div>
                    </div>

                    <div
                        v-if="!rekening.length"
                        class="py-8
                               text-center
                               text-slate-600"
                    >
                        Belum ada rekening.
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import {
    computed,
} from 'vue'

import {
    useMonitoringAkunting,
} from '../../composables/useMonitoringAkunting'

const {
    memuat,
    tagihan,
    rekening,

    saldoKas,
    jumlahTagihan,
    totalTagihan,
    jumlahPeringatan,
    jumlahTerlambat,

    statusIDS,

    waktuDisplay,
    updateDisplay,

    formatUang,
    labelHari,
} = useMonitoringAkunting()

const statusPanelClass = computed(() => {
    switch (statusIDS.value.key) {
        case 'KRITIS':
            return 'border-red-500/30 bg-red-950/30'

        case 'JATUH_TEMPO':
            return 'border-orange-500/30 bg-orange-950/20'

        case 'PERINGATAN':
            return 'border-amber-500/30 bg-amber-950/20'

        default:
            return 'border-emerald-500/20 bg-emerald-950/10'
    }
})

const statusTextClass = computed(() => {
    switch (statusIDS.value.key) {
        case 'KRITIS':
            return 'text-red-400'

        case 'JATUH_TEMPO':
            return 'text-orange-400'

        case 'PERINGATAN':
            return 'text-amber-400'

        default:
            return 'text-emerald-400'
    }
})
</script>

<style scoped>
.th {
    padding: 0.75rem 1rem;
    text-align: left;
    font-size: 9px;
    font-weight: 900;
    letter-spacing: 0.1em;
    color: rgb(71 85 105);
}

.td {
    padding: 0.75rem 1rem;
    font-size: 0.75rem;
}
</style>
