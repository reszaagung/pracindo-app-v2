<template>
    <div class="flex flex-col w-full animate-fade-in relative pb-8">
        <div class="mb-6">
            <p class="text-xs text-slate-400 mb-1">
                <router-link
                    to="/inventory"
                    class="hover:text-slate-700 transition-colors"
                >
                    Stok
                </router-link>
                <span class="mx-1">/</span>
                <span class="text-slate-600 font-semibold">
                    Posisi Klaim
                </span>
            </p>

            <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
                <div>
                    <h1 class="text-xl md:text-2xl font-bold text-slate-800 tracking-tight">
                        Posisi Klaim — Grup {{ grup }}
                    </h1>

                    <p class="text-xs md:text-sm text-slate-500 mt-1">
                        Monitoring posisi klaim, saldo entitas, dan mutasi secara realtime.
                    </p>
                </div>

                <div
                    class="inline-flex items-center gap-2 px-3 py-2 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-bold"
                >
                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    REALTIME
                </div>
            </div>
        </div>

        <div
            v-if="galat"
            class="mb-5 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600 font-medium flex items-start gap-3"
        >
            <i class="pi pi-exclamation-triangle mt-0.5"></i>
            <span>{{ galat }}</span>
        </div>

        <div
            v-if="tidakSeimbang"
            class="mb-5 p-4 bg-amber-50 border border-amber-200 rounded-xl text-sm text-amber-700 font-medium flex items-start gap-3"
        >
            <i class="pi pi-shield mt-0.5 text-amber-500"></i>
            <div>
                <strong>Peringatan Sistem:</strong>
                Total posisi bersih
                {{ angka(totalBersih, 2) }}
                berbeda dengan nilai pool
                {{ angka(totalNilaiPool, 2) }}.
            </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
            <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                        Entitas
                    </span>
                    <div class="w-9 h-9 rounded-xl bg-slate-100 flex items-center justify-center">
                        <i class="pi pi-users text-slate-600"></i>
                    </div>
                </div>
                <div class="text-2xl font-black text-slate-800">
                    {{ posisiKlaim.length }}
                </div>
            </div>

            <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                        Mutasi
                    </span>
                    <div class="w-9 h-9 rounded-xl bg-blue-50 flex items-center justify-center">
                        <i class="pi pi-history text-blue-600"></i>
                    </div>
                </div>
                <div class="text-2xl font-black text-slate-800">
                    {{ mutasiKlaim.length }}
                </div>
            </div>

            <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                        Nilai Pool
                    </span>
                    <div class="w-9 h-9 rounded-xl bg-violet-50 flex items-center justify-center">
                        <i class="pi pi-database text-violet-600"></i>
                    </div>
                </div>
                <div class="text-xl font-black text-slate-800">
                    {{ angka(totalNilaiPool, 2) }}
                </div>
            </div>

            <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                        Posisi Bersih
                    </span>
                    <div class="w-9 h-9 rounded-xl bg-emerald-50 flex items-center justify-center">
                        <i class="pi pi-chart-line text-emerald-600"></i>
                    </div>
                </div>
                <div
                    class="text-xl font-black"
                    :class="totalBersih < 0 ? 'text-rose-600' : 'text-slate-800'"
                >
                    {{ angka(totalBersih, 2) }}
                </div>
            </div>
        </div>

        <section class="bg-white border border-slate-200 rounded-[24px] shadow-sm mb-6 overflow-hidden">
            <div class="px-5 md:px-6 py-4 border-b border-slate-100">
                <div class="flex items-center justify-between gap-4">
                    <div>
                        <h2 class="text-sm font-bold text-slate-800">
                            Sisa Realtime Entitas
                        </h2>
                        <p class="text-xs text-slate-400 mt-1">
                            Saldo klaim global masing-masing entitas.
                        </p>
                    </div>

                    <div class="w-9 h-9 rounded-xl bg-emerald-50 flex items-center justify-center">
                        <i class="pi pi-sync text-emerald-500"></i>
                    </div>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-sm min-w-[900px]">
                    <thead class="bg-slate-50 text-slate-500">
                        <tr>
                            <th class="text-left px-5 py-3 font-semibold">Entitas</th>
                            <th class="text-right px-5 py-3 font-semibold">Total Setor</th>
                            <th class="text-right px-5 py-3 font-semibold">Total Tarik</th>
                            <th class="text-right px-5 py-3 font-semibold">Total Rugi</th>
                            <th class="text-right px-5 py-3 font-semibold">Saldo</th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-slate-100">
                        <tr
                            v-for="s in saldoEntitas"
                            :key="s.entitas_id"
                            class="hover:bg-slate-50 transition-colors"
                        >
                            <td class="px-5 py-4 font-bold text-slate-800">
                                {{ s.entitas }}
                            </td>

                            <td class="px-5 py-4 text-right text-emerald-600 font-semibold">
                                {{ angka(s.total_setor, 2) }}
                            </td>

                            <td class="px-5 py-4 text-right text-amber-600 font-semibold">
                                {{ angka(s.total_tarik, 2) }}
                            </td>

                            <td class="px-5 py-4 text-right text-rose-500 font-semibold">
                                {{ angka(s.total_rugi, 2) }}
                            </td>

                            <td
                                class="px-5 py-4 text-right font-black"
                                :class="
                                    Number(s.saldo || 0) < 0
                                        ? 'text-rose-600'
                                        : 'text-slate-800'
                                "
                            >
                                {{ angka(s.saldo, 2) }}
                            </td>
                        </tr>
                    </tbody>

                    <tbody v-if="!sedangProses && saldoEntitas.length === 0">
                        <tr>
                            <td
                                colspan="5"
                                class="py-12 text-center text-slate-400"
                            >
                                Belum ada saldo entitas.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <section class="bg-white border border-slate-200 rounded-[24px] shadow-sm mb-6 overflow-hidden">
            <div class="px-5 md:px-6 py-4 border-b border-slate-100">
                <h2 class="text-sm font-bold text-slate-800">
                    Posisi Klaim Grup {{ grup }}
                </h2>
                <p class="text-xs text-slate-400 mt-1">
                    Posisi klaim khusus grup bahan yang sedang dipantau.
                </p>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-sm min-w-[950px]">
                    <thead class="bg-slate-50 text-slate-500">
                        <tr>
                            <th class="text-left px-5 py-3 font-semibold">Entitas</th>
                            <th class="text-right px-5 py-3 font-semibold">Setor</th>
                            <th class="text-right px-5 py-3 font-semibold">Ambil</th>
                            <th class="text-right px-5 py-3 font-semibold">Bersih</th>
                            <th class="text-right px-5 py-3 font-semibold">Qty Bersih KG</th>
                            <th class="text-center px-5 py-3 font-semibold">Posisi</th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-slate-100">
                        <tr
                            v-for="p in posisiKlaim"
                            :key="p.entitas"
                            class="hover:bg-slate-50 transition-colors"
                        >
                            <td class="px-5 py-4 font-bold text-slate-800">
                                {{ p.entitas }}
                            </td>

                            <td class="px-5 py-4 text-right text-emerald-600 font-semibold">
                                {{ angka(p.setor, 2) }}
                            </td>

                            <td class="px-5 py-4 text-right text-amber-600 font-semibold">
                                {{ angka(p.ambil, 2) }}
                            </td>

                            <td
                                class="px-5 py-4 text-right font-black"
                                :class="
                                    Number(p.bersih || 0) < 0
                                        ? 'text-rose-600'
                                        : 'text-slate-800'
                                "
                            >
                                {{ angka(p.bersih, 2) }}
                            </td>

                            <td class="px-5 py-4 text-right font-semibold text-slate-700">
                                {{ angka(p.qty_bersih, 3) }}
                            </td>

                            <td class="px-5 py-4 text-center">
                                <span
                                    class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase border"
                                    :class="
                                        p.berhutang
                                            ? 'bg-rose-50 text-rose-600 border-rose-200'
                                            : 'bg-emerald-50 text-emerald-600 border-emerald-200'
                                    "
                                >
                                    <i
                                        class="pi"
                                        :class="
                                            p.berhutang
                                                ? 'pi-arrow-down-right'
                                                : 'pi-arrow-up-right'
                                        "
                                    ></i>
                                    {{ p.berhutang ? 'Berhutang' : 'Berpiutang' }}
                                </span>
                            </td>
                        </tr>
                    </tbody>

                    <tbody v-if="!sedangProses && posisiKlaim.length === 0">
                        <tr>
                            <td
                                colspan="6"
                                class="py-12 text-center text-slate-400"
                            >
                                Belum ada posisi klaim di grup ini.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <section class="bg-white border border-slate-200 rounded-[24px] shadow-sm overflow-hidden">
            <div class="px-5 md:px-6 py-4 border-b border-slate-100">
                <div class="flex items-center justify-between gap-4">
                    <div>
                        <h2 class="text-sm font-bold text-slate-800">
                            Mutasi Klaim
                        </h2>
                        <p class="text-xs text-slate-400 mt-1">
                            Mutasi terbaru dari ledger klaim grup {{ grup }}.
                        </p>
                    </div>

                    <div class="px-3 py-1.5 rounded-lg bg-slate-100 text-slate-500 text-[10px] font-bold">
                        {{ mutasiKlaim.length }} DATA
                    </div>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-sm min-w-[1200px]">
                    <thead class="bg-slate-50 text-slate-500">
                        <tr>
                            <th class="text-left px-5 py-3 font-semibold">Waktu</th>
                            <th class="text-left px-5 py-3 font-semibold">Entitas</th>
                            <th class="text-left px-5 py-3 font-semibold">Grup</th>
                            <th class="text-left px-5 py-3 font-semibold">Tipe</th>
                            <th class="text-right px-5 py-3 font-semibold">Qty KG</th>
                            <th class="text-right px-5 py-3 font-semibold">Nilai</th>
                            <th class="text-left px-5 py-3 font-semibold">Referensi</th>
                            <th class="text-left px-5 py-3 font-semibold">Keterangan</th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-slate-100">
                        <tr
                            v-for="m in mutasiKlaim"
                            :key="m.id"
                            class="hover:bg-slate-50 transition-colors"
                        >
                            <td class="px-5 py-4 whitespace-nowrap text-slate-500">
                                {{ tanggal(m.waktu) }}
                            </td>

                            <td class="px-5 py-4 font-bold text-slate-800">
                                {{ m.entitas_kode }}
                            </td>

                            <td class="px-5 py-4 font-semibold text-slate-600">
                                {{ m.grup_kode || m.grup_bahan }}
                            </td>

                            <td class="px-5 py-4">
                                <span
                                    class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase border"
                                    :class="
                                        m.arah === 1
                                            ? 'bg-emerald-50 text-emerald-600 border-emerald-200'
                                            : 'bg-amber-50 text-amber-600 border-amber-200'
                                    "
                                >
                                    <i
                                        class="pi"
                                        :class="
                                            m.arah === 1
                                                ? 'pi-arrow-down-left'
                                                : 'pi-arrow-up-right'
                                        "
                                    ></i>
                                    {{ m.tipe }}
                                </span>
                            </td>

                            <td class="px-5 py-4 text-right font-semibold text-slate-700">
                                {{ angka(m.qty_kg, 3) }}
                            </td>

                            <td
                                class="px-5 py-4 text-right font-bold"
                                :class="
                                    m.arah === 1
                                        ? 'text-emerald-600'
                                        : 'text-amber-600'
                                "
                            >
                                {{ m.arah === -1 ? '-' : '+' }}{{ angka(m.nilai, 2) }}
                            </td>

                            <td class="px-5 py-4 text-slate-600">
                                <span class="font-semibold">{{ m.ref_type }}</span>
                                <span class="text-slate-400 ml-1">#{{ m.ref_id }}</span>
                            </td>

                            <td class="px-5 py-4 text-slate-500">
                                {{ m.keterangan || '-' }}
                            </td>
                        </tr>
                    </tbody>

                    <tbody v-if="!sedangProses && mutasiKlaim.length === 0">
                        <tr>
                            <td
                                colspan="8"
                                class="py-12 text-center text-slate-400"
                            >
                                Belum ada mutasi klaim.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>
    </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { useClaim } from '../composables/useClaim'
import { angka, tanggal } from '@/utils/format'

const props = defineProps({
    grup: {
        type: [String, Number],
        required: true,
    },
})

const {
    posisiKlaim,
    saldoEntitas,
    mutasiKlaim,
    isiPool,
    sedangProses,
    galat,
    muatSemua,
    mulaiRealtime,
    hentikanRealtime,
} = useClaim()

const totalBersih = computed(() =>
    posisiKlaim.value.reduce(
        (sum, item) => sum + Number(item.bersih || 0),
        0
    )
)

const totalNilaiPool = computed(() =>
    Number(isiPool.value?.total_nilai || 0)
)

const tidakSeimbang = computed(() =>
    posisiKlaim.value.length > 0 &&
    Math.abs(totalBersih.value - totalNilaiPool.value) > 0.01
)

onMounted(async () => {
    await muatSemua(props.grup)
    mulaiRealtime(props.grup, 5000)
})

onUnmounted(() => {
    hentikanRealtime()
})
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>