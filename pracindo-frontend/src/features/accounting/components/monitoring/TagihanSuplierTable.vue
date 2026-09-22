<template>
    <section
        class="rounded-3xl border border-slate-800 bg-slate-900 overflow-hidden"
    >
        <div
            class="px-4 sm:px-5 py-4 border-b border-slate-800"
        >
            <h2 class="text-lg sm:text-xl font-black">
                TAGIHAN SUPPLIER
            </h2>

            <p class="text-xs text-slate-500 mt-1">
                Diurutkan berdasarkan urgensi jatuh tempo.
            </p>
        </div>

        <div class="overflow-x-auto">
            <table class="w-full min-w-[720px]">
                <thead class="bg-slate-950/70">
                    <tr>
                        <th class="th">SUPPLIER</th>
                        <th class="th">PO</th>
                        <th class="th">JATUH TEMPO</th>
                        <th class="th text-right">SISA</th>
                        <th class="th text-center">STATUS</th>
                    </tr>
                </thead>

                <tbody>
                    <tr
                        v-for="item in items"
                        :key="item.id"
                        class="border-t border-slate-800/80"
                    >
                        <td class="td font-bold text-slate-200">
                            {{ item.supplier }}
                        </td>

                        <td class="td text-slate-400 font-mono">
                            {{ item.no_po }}
                        </td>

                        <td class="td">
                            <div class="font-bold">
                                {{ formatTanggal(item.tanggal_jatuh_tempo) }}
                            </div>

                            <div
                                class="mt-1 text-[11px] font-black"
                                :class="hariClass(item.status_tempo)"
                            >
                                {{ labelHari(item.hari_tersisa) }}
                            </div>
                        </td>

                        <td
                            class="td text-right font-black tabular-nums whitespace-nowrap"
                        >
                            {{ formatUang(item.sisa_hutang) }}
                        </td>

                        <td class="td text-center">
                            <span
                                class="inline-flex px-2.5 py-1 rounded-full border text-[10px] font-black"
                                :class="statusClass(item.status_tempo)"
                            >
                                {{ labelStatus(item.status_tempo) }}
                            </span>
                        </td>
                    </tr>

                    <tr v-if="!items.length">
                        <td
                            colspan="5"
                            class="px-4 py-14 text-center"
                        >
                            <div class="text-sm font-bold text-slate-400">
                                Tidak ada tagihan terbuka.
                            </div>

                            <div class="mt-1 text-xs text-slate-600">
                                Sistem monitoring dalam kondisi normal.
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
</template>

<script setup>
defineProps({
    items: {
        type: Array,
        default: () => [],
    },
})

function formatUang(nilai) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        maximumFractionDigits: 0,
    }).format(Number(nilai || 0))
}

function formatTanggal(tanggal) {
    if (!tanggal) return '-'

    return new Intl.DateTimeFormat('id-ID', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
    }).format(new Date(tanggal))
}

function labelHari(hari) {
    if (hari === null || hari === undefined) return ''

    const nilai = Number(hari)

    if (nilai < 0) {
        return `${Math.abs(nilai)} HARI TERLAMBAT`
    }

    if (nilai === 0) {
        return 'JATUH TEMPO HARI INI'
    }

    return `H-${nilai}`
}

function labelStatus(status) {
    const map = {
        NORMAL: 'NORMAL',
        PERINGATAN: 'H-7',
        JATUH_TEMPO: 'JATUH TEMPO',
        TERLAMBAT: 'TERLAMBAT',
    }

    return map[status] || status || '-'
}

function statusClass(status) {
    const map = {
        NORMAL:
            'bg-emerald-500/10 text-emerald-300 border-emerald-400/20',
        PERINGATAN:
            'bg-amber-500/10 text-amber-300 border-amber-400/20',
        JATUH_TEMPO:
            'bg-orange-500/10 text-orange-300 border-orange-400/20',
        TERLAMBAT:
            'bg-red-500/10 text-red-300 border-red-400/20',
    }

    return map[status] || 'bg-slate-500/10 text-slate-300'
}

function hariClass(status) {
    const map = {
        NORMAL: 'text-slate-500',
        PERINGATAN: 'text-amber-400',
        JATUH_TEMPO: 'text-orange-400',
        TERLAMBAT: 'text-red-400',
    }

    return map[status] || 'text-slate-500'
}
</script>

<style scoped>
.th {
    padding: 0.75rem 1rem;  
    text-align: left;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: 0.1em;
    color: rgb(100 116 139);
}

.td {
    padding: 1rem;
    font-size: 0.875rem;
}
</style>