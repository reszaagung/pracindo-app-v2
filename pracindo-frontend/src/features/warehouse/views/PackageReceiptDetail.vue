<template>
    <CardDetail
        :loading="sedangProses"
        :error="galat"
        :hasData="!!ringkasan"
        :title="ringkasan?.nomor || 'Memuat...'"
        :subtitle="
            ringkasan
                ? `${ringkasan.suplier || '-'} • PO ${ringkasan.po || '-'} • ${ringkasan.tanggal || '-'}`
                : ''
        "
        backRoute="/warehouse/input/receipt?tab=kemasan"
        backLabel="Penerimaan Kemasan"
        :badge="ringkasan?.ada_selisih ? 'Ada Selisih' : 'Sesuai'"
        :badgeClass="
            ringkasan?.ada_selisih
                ? 'bg-rose-50 text-rose-700 border-rose-200'
                : 'bg-emerald-50 text-emerald-700 border-emerald-200'
        "
        :badgeIcon="
            ringkasan?.ada_selisih
                ? 'pi-exclamation-circle'
                : 'pi-check-circle'
        "
    >
        <template v-if="ringkasan">

            <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-5">
                <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
                    <div class="flex items-center justify-between gap-2">
                        <div class="w-9 h-9 rounded-xl bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-500">
                            <i class="pi pi-box text-xs"></i>
                        </div>

                        <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                            Item
                        </span>
                    </div>

                    <p class="text-xl md:text-2xl font-black text-slate-900 mt-3">
                        {{ totalItem }}
                    </p>

                    <p class="text-[10px] text-slate-400 mt-0.5">
                        Kemasan diterima
                    </p>
                </div>

                <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
                    <div class="flex items-center justify-between gap-2">
                        <div class="w-9 h-9 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600">
                            <i class="pi pi-check text-xs"></i>
                        </div>

                        <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                            Diterima
                        </span>
                    </div>

                    <p class="text-xl md:text-2xl font-black text-emerald-700 mt-3">
                        {{ angka(totalDiterima) }}
                    </p>

                    <p class="text-[10px] text-slate-400 mt-0.5">
                        Total qty kemasan
                    </p>
                </div>

                <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
                    <div class="flex items-center justify-between gap-2">
                        <div class="w-9 h-9 rounded-xl bg-rose-50 border border-rose-100 flex items-center justify-center text-rose-600">
                            <i class="pi pi-times text-xs"></i>
                        </div>

                        <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                            Ditolak
                        </span>
                    </div>

                    <p class="text-xl md:text-2xl font-black text-rose-600 mt-3">
                        {{ angka(totalDitolak) }}
                    </p>

                    <p class="text-[10px] text-slate-400 mt-0.5">
                        Total qty ditolak
                    </p>
                </div>

                <div
                    class="border rounded-2xl p-4 shadow-sm"
                    :class="
                        ringkasan.selisih?.length
                            ? 'bg-amber-50 border-amber-200'
                            : 'bg-emerald-50 border-emerald-100'
                    "
                >
                    <div class="flex items-center justify-between gap-2">
                        <div
                            class="w-9 h-9 rounded-xl flex items-center justify-center"
                            :class="
                                ringkasan.selisih?.length
                                    ? 'bg-amber-100 text-amber-600'
                                    : 'bg-emerald-100 text-emerald-600'
                            "
                        >
                            <i
                                class="pi text-xs"
                                :class="
                                    ringkasan.selisih?.length
                                        ? 'pi-exclamation-triangle'
                                        : 'pi-check-circle'
                                "
                            ></i>
                        </div>

                        <span
                            class="text-[10px] font-bold uppercase tracking-wider"
                            :class="
                                ringkasan.selisih?.length
                                    ? 'text-amber-600'
                                    : 'text-emerald-600'
                            "
                        >
                            Selisih
                        </span>
                    </div>

                    <p
                        class="text-xl md:text-2xl font-black mt-3"
                        :class="
                            ringkasan.selisih?.length
                                ? 'text-amber-700'
                                : 'text-emerald-700'
                        "
                    >
                        {{ ringkasan.selisih?.length || 0 }}
                    </p>

                    <p
                        class="text-[10px] mt-0.5"
                        :class="
                            ringkasan.selisih?.length
                                ? 'text-amber-600'
                                : 'text-emerald-600'
                        "
                    >
                        Laporan otomatis
                    </p>
                </div>
            </div>

            <section class="bg-white border border-slate-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden mb-5">
                <div class="px-4 py-4 md:px-6 md:py-5 border-b border-slate-100">
                    <div class="flex items-center gap-3">
                        <div class="w-9 h-9 shrink-0 rounded-xl bg-blue-50 border border-blue-100 text-blue-600 flex items-center justify-center">
                            <i class="pi pi-box text-xs"></i>
                        </div>

                        <div>
                            <h3 class="text-sm md:text-base font-bold text-slate-900">
                                Aset Kemasan Diterima
                            </h3>

                            <p class="text-[11px] md:text-xs text-slate-500 mt-0.5">
                                Detail kuantitas kemasan yang tercatat pada transaksi ini.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="hidden md:block overflow-x-auto custom-scrollbar">
                    <table class="w-full min-w-[720px] text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-100">
                                <th class="px-5 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                    Nama Kemasan
                                </th>

                                <th class="px-4 py-3.5 text-[10px] font-bold text-emerald-600 uppercase tracking-wider text-right">
                                    Qty Diterima
                                </th>

                                <th class="px-4 py-3.5 text-[10px] font-bold text-rose-500 uppercase tracking-wider text-right">
                                    Ditolak
                                </th>

                                <th class="px-5 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right">
                                    Selisih Qty
                                </th>
                            </tr>
                        </thead>

                        <tbody class="divide-y divide-slate-100">
                            <tr
                                v-for="(it, i) in ringkasan.item"
                                :key="it.id ?? i"
                                class="hover:bg-slate-50/60 transition-colors"
                            >
                                <td class="px-5 py-4 align-middle">
                                    <div class="flex items-center gap-3">
                                        <div class="w-9 h-9 shrink-0 rounded-xl bg-slate-100 border border-slate-200 text-slate-500 flex items-center justify-center">
                                            <i class="pi pi-box text-[10px]"></i>
                                        </div>

                                        <div class="min-w-0">
                                            <p class="text-sm font-bold text-slate-800 break-words">
                                                {{ it.nama || '-' }}
                                            </p>
                                        </div>
                                    </div>
                                </td>

                                <td class="px-4 py-4 text-right align-middle">
                                    <span class="inline-flex px-2.5 py-1 rounded-lg bg-emerald-50 border border-emerald-100 text-xs font-bold text-emerald-700">
                                        {{ angka(it.diterima) }}
                                    </span>
                                </td>

                                <td class="px-4 py-4 text-right align-middle">
                                    <span
                                        class="text-xs font-bold"
                                        :class="Number(it.ditolak) > 0 ? 'text-rose-600' : 'text-slate-400'"
                                    >
                                        {{ angka(it.ditolak) }}
                                    </span>
                                </td>

                                <td class="px-5 py-4 text-right align-middle">
                                    <span
                                        v-if="it.selisih != null"
                                        class="inline-flex px-2.5 py-1 rounded-lg border text-xs font-bold"
                                        :class="
                                            Number(it.selisih) !== 0
                                                ? 'bg-rose-50 border-rose-100 text-rose-600'
                                                : 'bg-emerald-50 border-emerald-100 text-emerald-700'
                                        "
                                    >
                                        {{ angka(it.selisih) }}
                                    </span>

                                    <span
                                        v-else
                                        class="text-xs text-slate-400"
                                    >
                                        —
                                    </span>
                                </td>
                            </tr>
                        </tbody>

                        <tfoot
                            v-if="ringkasan.item?.length"
                            class="bg-slate-50/70 border-t border-slate-200"
                        >
                            <tr>
                                <td class="px-5 py-3 text-[10px] font-bold uppercase tracking-wider text-slate-500">
                                    Total
                                </td>

                                <td class="px-4 py-3 text-right text-xs font-black text-emerald-700">
                                    {{ angka(totalDiterima) }}
                                </td>

                                <td class="px-4 py-3 text-right text-xs font-black text-rose-600">
                                    {{ angka(totalDitolak) }}
                                </td>

                                <td class="px-5 py-3 text-right">
                                    —
                                </td>
                            </tr>
                        </tfoot>
                    </table>
                </div>

                <div class="md:hidden p-3 bg-slate-50/40 space-y-3">
                    <article
                        v-for="(it, i) in ringkasan.item"
                        :key="'mobile-' + (it.id ?? i)"
                        class="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden"
                    >
                        <div class="p-4 border-b border-slate-100">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 shrink-0 rounded-xl bg-slate-100 border border-slate-200 text-slate-500 flex items-center justify-center">
                                    <i class="pi pi-box text-xs"></i>
                                </div>

                                <div class="min-w-0">
                                    <p class="text-sm font-bold text-slate-900 break-words">
                                        {{ it.nama || '-' }}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div class="p-4 space-y-3">
                            <div class="grid grid-cols-2 gap-2">
                                <div class="rounded-xl bg-emerald-50 border border-emerald-100 p-3">
                                    <p class="text-[9px] font-bold uppercase tracking-wider text-emerald-600">
                                        Diterima
                                    </p>

                                    <p class="text-sm font-black text-emerald-700 mt-1">
                                        {{ angka(it.diterima) }}
                                    </p>
                                </div>

                                <div class="rounded-xl bg-rose-50 border border-rose-100 p-3">
                                    <p class="text-[9px] font-bold uppercase tracking-wider text-rose-500">
                                        Ditolak
                                    </p>

                                    <p class="text-sm font-black text-rose-600 mt-1">
                                        {{ angka(it.ditolak) }}
                                    </p>
                                </div>
                            </div>

                            <div
                                class="rounded-xl border p-3"
                                :class="
                                    Number(it.selisih) !== 0
                                        ? 'bg-rose-50 border-rose-200'
                                        : 'bg-emerald-50 border-emerald-100'
                                "
                            >
                                <div class="flex items-center justify-between gap-3">
                                    <div>
                                        <p
                                            class="text-[9px] font-bold uppercase tracking-wider"
                                            :class="
                                                Number(it.selisih) !== 0
                                                    ? 'text-rose-500'
                                                    : 'text-emerald-600'
                                            "
                                        >
                                            Selisih Qty
                                        </p>

                                        <p
                                            class="text-[10px] mt-0.5"
                                            :class="
                                                Number(it.selisih) !== 0
                                                    ? 'text-rose-500'
                                                    : 'text-emerald-600'
                                            "
                                        >
                                            {{
                                                Number(it.selisih) !== 0
                                                    ? 'Perlu perhatian'
                                                    : 'Sesuai'
                                            }}
                                        </p>
                                    </div>

                                    <span
                                        class="text-sm font-black"
                                        :class="
                                            Number(it.selisih) !== 0
                                                ? 'text-rose-600'
                                                : 'text-emerald-700'
                                        "
                                    >
                                        {{ it.selisih != null ? angka(it.selisih) : '—' }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </article>

                    <div class="grid grid-cols-2 gap-2 pt-1">
                        <div class="rounded-xl bg-emerald-50 border border-emerald-100 p-3">
                            <p class="text-[9px] font-bold uppercase tracking-wider text-emerald-600">
                                Total Diterima
                            </p>

                            <p class="text-sm font-black text-emerald-700 mt-1">
                                {{ angka(totalDiterima) }}
                            </p>
                        </div>

                        <div class="rounded-xl bg-rose-50 border border-rose-100 p-3">
                            <p class="text-[9px] font-bold uppercase tracking-wider text-rose-500">
                                Total Ditolak
                            </p>

                            <p class="text-sm font-black text-rose-600 mt-1">
                                {{ angka(totalDitolak) }}
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            <section
                v-if="ringkasan.selisih?.length"
                class="bg-white border border-amber-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden"
            >
                <div class="px-4 py-4 md:px-6 md:py-5 bg-amber-50/70 border-b border-amber-100">
                    <div class="flex items-start gap-3">
                        <div class="w-10 h-10 shrink-0 rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center">
                            <i class="pi pi-exclamation-triangle text-sm"></i>
                        </div>

                        <div class="min-w-0">
                            <div class="flex flex-wrap items-center gap-2">
                                <h3 class="text-sm md:text-base font-bold text-amber-950">
                                    Laporan Selisih Kemasan
                                </h3>

                                <span class="inline-flex items-center justify-center min-w-6 h-6 px-1.5 rounded-full bg-amber-200 text-amber-800 text-[10px] font-black">
                                    {{ ringkasan.selisih.length }}
                                </span>
                            </div>

                            <p class="text-[11px] md:text-xs text-amber-700 mt-1 leading-relaxed">
                                Laporan diterbitkan otomatis berdasarkan hasil penerimaan.
                            </p>
                        </div>
                    </div>
                </div>

                <div class="hidden md:block overflow-x-auto custom-scrollbar">
                    <table class="w-full min-w-[720px] text-left">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-100">
                                <th class="px-5 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                    Nomor
                                </th>

                                <th class="px-4 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                    Jenis
                                </th>

                                <th class="px-4 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right">
                                    Qty
                                </th>

                                <th class="px-4 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                    Status
                                </th>

                                <th class="px-5 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                    Resolusi
                                </th>
                            </tr>
                        </thead>

                        <tbody class="divide-y divide-slate-100">
                            <tr
                                v-for="(s, i) in ringkasan.selisih"
                                :key="s.nomor ?? i"
                                class="hover:bg-slate-50/60 transition-colors"
                            >
                                <td class="px-5 py-4 text-xs font-bold text-slate-800">
                                    {{ s.nomor || '-' }}
                                </td>

                                <td class="px-4 py-4 text-xs text-slate-600">
                                    {{ s.jenis || '-' }}
                                </td>

                                <td class="px-4 py-4 text-right">
                                    <span class="text-xs font-black text-rose-600">
                                        {{ angka(s.qty) }}
                                    </span>
                                </td>

                                <td class="px-4 py-4">
                                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-amber-50 border border-amber-200 text-amber-700 text-[9px] font-bold uppercase tracking-wide">
                                        <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                                        {{ s.status || 'Terbuka' }}
                                    </span>
                                </td>

                                <td class="px-5 py-4 text-xs font-medium text-slate-600">
                                    {{ s.resolusi || '-' }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="md:hidden p-3 bg-slate-50/40 space-y-3">
                    <article
                        v-for="(s, i) in ringkasan.selisih"
                        :key="'mobile-selisih-' + (s.nomor ?? i)"
                        class="rounded-2xl bg-white border border-slate-200 shadow-sm p-4"
                    >
                        <div class="flex items-start justify-between gap-3 pb-3 border-b border-slate-100">
                            <div class="min-w-0">
                                <p class="text-xs font-black text-slate-900 break-all">
                                    {{ s.nomor || '-' }}
                                </p>

                                <p class="text-[10px] text-slate-400 mt-1">
                                    {{ s.jenis || '-' }}
                                </p>
                            </div>

                            <span class="shrink-0 inline-flex items-center gap-1.5 px-2 py-1 rounded-lg bg-amber-50 border border-amber-200 text-amber-700 text-[9px] font-bold uppercase">
                                <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                                {{ s.status || 'Terbuka' }}
                            </span>
                        </div>

                        <div class="grid grid-cols-2 gap-2 mt-3">
                            <div class="rounded-xl bg-rose-50 border border-rose-100 p-3">
                                <p class="text-[9px] font-bold uppercase tracking-wider text-rose-500">
                                    Qty Selisih
                                </p>

                                <p class="text-sm font-black text-rose-600 mt-1">
                                    {{ angka(s.qty) }}
                                </p>
                            </div>

                            <div class="rounded-xl bg-slate-50 border border-slate-100 p-3">
                                <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                    Resolusi
                                </p>

                                <p class="text-xs font-bold text-slate-700 mt-1 break-words">
                                    {{ s.resolusi || '-' }}
                                </p>
                            </div>
                        </div>
                    </article>
                </div>
            </section>
        </template>
    </CardDetail>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import CardDetail from '../components/ui/CardDetail.vue'
import { usePackageReceipt } from '../composables/usePackageReceipt'
import { angka } from '@/utils/format'

const props = defineProps({
    id: {
        type: [String, Number],
        required: true,
    },
})

const {
    ringkasan,
    sedangProses,
    galat,
    muatRingkasan,
} = usePackageReceipt()

const totalItem = computed(() => {
    return ringkasan.value?.item?.length || 0
})

const totalDiterima = computed(() => {
    return (ringkasan.value?.item || []).reduce(
        (total, item) => total + (Number(item.diterima) || 0),
        0
    )
})

const totalDitolak = computed(() => {
    return (ringkasan.value?.item || []).reduce(
        (total, item) => total + (Number(item.ditolak) || 0),
        0
    )
})

onMounted(() => {
    muatRingkasan(props.id)
})
</script>

<style scoped>
.custom-scrollbar {
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 transparent;
}

.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 999px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}
</style>