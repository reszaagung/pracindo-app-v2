<template>
    <CardDetail
        :loading="sedangProses"
        :error="galat"
        :hasData="!!ringkasan"
        :title="ringkasan?.nomor || 'Memuat...'"
        :subtitle="
            ringkasan
                ? `${ringkasan.suplier || '-'} • PO ${ringkasan.po || '-'} • ${tanggal(ringkasan.tanggal)}`
                : ''
        "
        backRoute="/warehouse"
        backLabel="Penerimaan Barang"
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

            <!-- =====================================================
                 SUMMARY
            ====================================================== -->
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-5">

                <!-- Total Item -->
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
                        Produk diterima
                    </p>
                </div>

                <!-- Timbang -->
                <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
                    <div class="flex items-center justify-between gap-2">
                        <div class="w-9 h-9 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600">
                            <i class="pi pi-balance-scale text-xs"></i>
                        </div>

                        <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                            Timbang
                        </span>
                    </div>

                    <p class="text-xl md:text-2xl font-black text-slate-900 mt-3">
                        {{ angka(totalTimbang, 3) }}
                    </p>

                    <p class="text-[10px] text-slate-400 mt-0.5">
                        Total qty diterima
                    </p>
                </div>

                <!-- Ditolak -->
                <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
                    <div class="flex items-center justify-between gap-2">
                        <div class="w-9 h-9 rounded-xl bg-rose-50 border border-rose-100 flex items-center justify-center text-rose-600">
                            <i class="pi pi-times-circle text-xs"></i>
                        </div>

                        <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                            Ditolak
                        </span>
                    </div>

                    <p class="text-xl md:text-2xl font-black text-rose-600 mt-3">
                        {{ angka(totalDitolak, 3) }}
                    </p>

                    <p class="text-[10px] text-slate-400 mt-0.5">
                        Total qty ditolak
                    </p>
                </div>

                <!-- Laporan -->
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
                                        : 'pi-check'
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

            <!-- =====================================================
                 ITEM DITERIMA
            ====================================================== -->
            <section class="bg-white border border-slate-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden mb-5">

                <div class="px-4 py-4 md:px-6 md:py-5 border-b border-slate-100">
                    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                        <div class="flex items-center gap-3">
                            <div class="w-9 h-9 shrink-0 rounded-xl bg-emerald-50 border border-emerald-100 text-emerald-600 flex items-center justify-center">
                                <i class="pi pi-box text-xs"></i>
                            </div>

                            <div>
                                <h3 class="text-sm md:text-base font-bold text-slate-900">
                                    Item Diterima
                                </h3>

                                <p class="text-[11px] md:text-xs text-slate-500 mt-0.5">
                                    Hasil pemeriksaan fisik dan penimbangan barang.
                                </p>
                            </div>
                        </div>

                        <div class="text-[10px] text-slate-400">
                            {{ totalItem }} item
                        </div>
                    </div>
                </div>

                <!-- Desktop -->
                <div class="hidden lg:block overflow-x-auto custom-scrollbar">
                    <table class="w-full min-w-[1050px] text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-100">
                                <th class="px-4 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                    Produk
                                </th>

                                <th class="px-3 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                    Kemasan
                                </th>

                                <th class="px-3 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right">
                                    Koli
                                </th>

                                <th class="px-3 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right">
                                    Isi/Koli
                                </th>

                                <th class="px-3 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right">
                                    Deklarasi
                                </th>

                                <th class="px-3 py-3.5 text-[10px] font-bold text-emerald-600 uppercase tracking-wider text-right">
                                    Timbang
                                </th>

                                <th class="px-3 py-3.5 text-[10px] font-bold text-rose-500 uppercase tracking-wider text-right">
                                    Ditolak
                                </th>

                                <th class="px-4 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right">
                                    Selisih
                                </th>
                            </tr>
                        </thead>

                        <tbody class="divide-y divide-slate-100">
                            <tr
                                v-for="(it, i) in ringkasan.item"
                                :key="it.id ?? i"
                                class="hover:bg-slate-50/70 transition-colors"
                            >
                                <!-- Produk -->
                                <td class="px-4 py-4 align-middle">
                                    <div class="flex items-center gap-3">
                                        <div class="w-9 h-9 shrink-0 rounded-xl bg-slate-100 border border-slate-200 text-slate-500 flex items-center justify-center">
                                            <i class="pi pi-box text-[10px]"></i>
                                        </div>

                                        <div class="min-w-0">
                                            <p class="text-xs md:text-sm font-bold text-slate-800 break-words">
                                                {{ it.nama || '-' }}
                                            </p>

                                            <span
                                                v-if="melebihiToleransi(it.persen)"
                                                class="inline-flex items-center gap-1 mt-1 px-1.5 py-0.5 rounded-md bg-rose-50 border border-rose-100 text-rose-600 text-[9px] font-bold"
                                            >
                                                <i class="pi pi-exclamation-circle text-[8px]"></i>
                                                Selisih
                                            </span>
                                        </div>
                                    </div>
                                </td>

                                <!-- Kemasan -->
                                <td class="px-3 py-4 align-middle">
                                    <span class="inline-flex px-2.5 py-1 rounded-lg bg-slate-50 border border-slate-200 text-[10px] font-bold text-slate-600">
                                        {{ it.kemasan || '-' }}
                                    </span>
                                </td>

                                <!-- Koli -->
                                <td class="px-3 py-4 text-right text-xs font-semibold text-slate-600 align-middle">
                                    {{ it.koli ?? '-' }}
                                </td>

                                <!-- Isi -->
                                <td class="px-3 py-4 text-right text-xs text-slate-600 align-middle">
                                    {{ it.isi_per_koli != null ? angka(it.isi_per_koli, 3) : '-' }}
                                </td>

                                <!-- Deklarasi -->
                                <td class="px-3 py-4 text-right text-xs text-slate-600 align-middle">
                                    {{ it.deklarasi != null ? angka(it.deklarasi, 3) : '-' }}
                                </td>

                                <!-- Timbang -->
                                <td class="px-3 py-4 text-right align-middle">
                                    <span class="text-xs font-bold text-emerald-700">
                                        {{ angka(it.timbang, 3) }}
                                    </span>
                                </td>

                                <!-- Ditolak -->
                                <td class="px-3 py-4 text-right align-middle">
                                    <span
                                        class="text-xs font-bold"
                                        :class="Number(it.ditolak) > 0 ? 'text-rose-600' : 'text-slate-400'"
                                    >
                                        {{ angka(it.ditolak, 3) }}
                                    </span>
                                </td>

                                <!-- Selisih -->
                                <td class="px-4 py-4 text-right align-middle">
                                    <template v-if="it.selisih_berat != null">
                                        <div
                                            class="inline-flex flex-col items-end px-2.5 py-1.5 rounded-lg border"
                                            :class="
                                                melebihiToleransi(it.persen)
                                                    ? 'bg-rose-50 border-rose-100 text-rose-600'
                                                    : 'bg-slate-50 border-slate-100 text-slate-700'
                                            "
                                        >
                                            <span class="text-xs font-bold">
                                                {{ angka(it.selisih_berat, 3) }}
                                            </span>

                                            <span
                                                v-if="it.persen != null"
                                                class="text-[9px] font-semibold mt-0.5 opacity-80"
                                            >
                                                {{ angka(it.persen, 2) }}%
                                            </span>
                                        </div>
                                    </template>

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
                            class="border-t border-slate-200 bg-slate-50/70"
                        >
                            <tr>
                                <td
                                    colspan="5"
                                    class="px-4 py-3 text-[10px] font-bold uppercase tracking-wider text-slate-500"
                                >
                                    Total
                                </td>

                                <td class="px-3 py-3 text-right text-xs font-black text-emerald-700">
                                    {{ angka(totalTimbang, 3) }}
                                </td>

                                <td class="px-3 py-3 text-right text-xs font-black text-rose-600">
                                    {{ angka(totalDitolak, 3) }}
                                </td>

                                <td class="px-4 py-3 text-right">
                                    —
                                </td>
                            </tr>
                        </tfoot>
                    </table>
                </div>

                <!-- Mobile -->
                <div class="lg:hidden p-3 md:p-4 space-y-3 bg-slate-50/40">
                    <article
                        v-for="(it, i) in ringkasan.item"
                        :key="'mobile-' + (it.id ?? i)"
                        class="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden"
                    >
                        <!-- Header -->
                        <div class="p-4 border-b border-slate-100">
                            <div class="flex items-start justify-between gap-3">
                                <div class="flex items-start gap-3 min-w-0">
                                    <div class="w-10 h-10 shrink-0 rounded-xl bg-slate-100 border border-slate-200 text-slate-500 flex items-center justify-center">
                                        <i class="pi pi-box text-xs"></i>
                                    </div>

                                    <div class="min-w-0">
                                        <p class="text-sm font-bold text-slate-900 break-words">
                                            {{ it.nama || '-' }}
                                        </p>

                                        <div class="flex flex-wrap items-center gap-2 mt-1.5">
                                            <span class="text-[10px] font-semibold text-slate-400">
                                                {{ it.kemasan || '-' }}
                                            </span>

                                            <span class="w-1 h-1 rounded-full bg-slate-300"></span>

                                            <span class="text-[10px] font-semibold text-slate-400">
                                                {{ it.koli ?? '-' }} koli
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                <span
                                    v-if="melebihiToleransi(it.persen)"
                                    class="shrink-0 px-2 py-1 rounded-lg bg-rose-50 border border-rose-100 text-rose-600 text-[9px] font-bold"
                                >
                                    Selisih
                                </span>

                                <span
                                    v-else
                                    class="shrink-0 px-2 py-1 rounded-lg bg-emerald-50 border border-emerald-100 text-emerald-600 text-[9px] font-bold"
                                >
                                    Sesuai
                                </span>
                            </div>
                        </div>

                        <div class="p-4 space-y-3">

                            <!-- Packaging -->
                            <div class="grid grid-cols-2 gap-2">
                                <div class="rounded-xl bg-slate-50 border border-slate-100 p-3">
                                    <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                        Isi / Koli
                                    </p>

                                    <p class="text-xs font-bold text-slate-700 mt-1">
                                        {{ it.isi_per_koli != null ? angka(it.isi_per_koli, 3) : '-' }}
                                    </p>
                                </div>

                                <div class="rounded-xl bg-slate-50 border border-slate-100 p-3">
                                    <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                        Deklarasi
                                    </p>

                                    <p class="text-xs font-bold text-slate-700 mt-1">
                                        {{ it.deklarasi != null ? angka(it.deklarasi, 3) : '-' }}
                                    </p>
                                </div>
                            </div>

                            <!-- Quantities -->
                            <div class="grid grid-cols-2 gap-2">
                                <div class="rounded-xl bg-emerald-50 border border-emerald-100 p-3">
                                    <p class="text-[9px] font-bold uppercase tracking-wider text-emerald-600">
                                        Timbang
                                    </p>

                                    <p class="text-sm font-black text-emerald-700 mt-1">
                                        {{ angka(it.timbang, 3) }}
                                    </p>
                                </div>

                                <div class="rounded-xl bg-rose-50 border border-rose-100 p-3">
                                    <p class="text-[9px] font-bold uppercase tracking-wider text-rose-500">
                                        Ditolak
                                    </p>

                                    <p class="text-sm font-black text-rose-600 mt-1">
                                        {{ angka(it.ditolak, 3) }}
                                    </p>
                                </div>
                            </div>

                            <!-- Difference -->
                            <div
                                class="rounded-xl border px-3 py-3"
                                :class="
                                    melebihiToleransi(it.persen)
                                        ? 'bg-rose-50 border-rose-200'
                                        : 'bg-slate-50 border-slate-100'
                                "
                            >
                                <div class="flex items-center justify-between gap-3">
                                    <div>
                                        <p
                                            class="text-[9px] font-bold uppercase tracking-wider"
                                            :class="
                                                melebihiToleransi(it.persen)
                                                    ? 'text-rose-500'
                                                    : 'text-slate-400'
                                            "
                                        >
                                            Selisih
                                        </p>

                                        <p
                                            v-if="it.persen != null"
                                            class="text-[10px] mt-0.5"
                                            :class="
                                                melebihiToleransi(it.persen)
                                                    ? 'text-rose-500'
                                                    : 'text-slate-400'
                                            "
                                        >
                                            Persentase {{ angka(it.persen, 2) }}%
                                        </p>
                                    </div>

                                    <p
                                        class="text-sm font-black"
                                        :class="
                                            melebihiToleransi(it.persen)
                                                ? 'text-rose-600'
                                                : 'text-slate-700'
                                        "
                                    >
                                        {{ it.selisih_berat != null ? angka(it.selisih_berat, 3) : '—' }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </article>

                    <!-- Mobile Total -->
                    <div class="grid grid-cols-2 gap-2 pt-1">
                        <div class="rounded-xl bg-emerald-50 border border-emerald-100 p-3">
                            <p class="text-[9px] font-bold uppercase tracking-wider text-emerald-600">
                                Total Timbang
                            </p>

                            <p class="text-sm font-black text-emerald-700 mt-1">
                                {{ angka(totalTimbang, 3) }}
                            </p>
                        </div>

                        <div class="rounded-xl bg-rose-50 border border-rose-100 p-3">
                            <p class="text-[9px] font-bold uppercase tracking-wider text-rose-500">
                                Total Ditolak
                            </p>

                            <p class="text-sm font-black text-rose-600 mt-1">
                                {{ angka(totalDitolak, 3) }}
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- =====================================================
                 LAPORAN SELISIH
            ====================================================== -->
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
                                    Laporan Selisih Otomatis
                                </h3>

                                <span class="inline-flex items-center justify-center min-w-6 h-6 px-1.5 rounded-full bg-amber-200 text-amber-800 text-[10px] font-black">
                                    {{ ringkasan.selisih.length }}
                                </span>
                            </div>

                            <p class="text-[11px] md:text-xs text-amber-700 mt-1 leading-relaxed">
                                Sistem menerbitkan laporan berdasarkan perbedaan hasil timbang terhadap deklarasi.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Desktop -->
                <div class="hidden md:block overflow-x-auto custom-scrollbar">
                    <table class="w-full min-w-[700px] text-left">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-100">
                                <th class="px-4 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                    Nomor Laporan
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

                                <th class="px-4 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
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
                                <td class="px-4 py-4 text-xs font-bold text-slate-800">
                                    {{ s.nomor || '-' }}
                                </td>

                                <td class="px-4 py-4 text-xs text-slate-600">
                                    {{ s.jenis || '-' }}
                                </td>

                                <td class="px-4 py-4 text-right">
                                    <span class="text-xs font-black text-rose-600">
                                        {{ angka(s.qty, 3) }}
                                    </span>
                                </td>

                                <td class="px-4 py-4">
                                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-amber-50 border border-amber-200 text-amber-700 text-[9px] font-bold uppercase tracking-wide">
                                        <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                                        {{ s.status || 'Terbuka' }}
                                    </span>
                                </td>

                                <td class="px-4 py-4 text-xs font-medium text-slate-600">
                                    {{ s.resolusi || '-' }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Mobile -->
                <div class="md:hidden p-3 bg-slate-50/40 space-y-3">
                    <article
                        v-for="(s, i) in ringkasan.selisih"
                        :key="'mobile-selisih-' + (s.nomor ?? i)"
                        class="rounded-2xl bg-white border border-slate-200 shadow-sm p-4"
                    >
                        <div class="flex items-start justify-between gap-3 pb-3 border-b border-slate-100">
                            <div>
                                <p class="text-xs font-black text-slate-900">
                                    {{ s.nomor || '-' }}
                                </p>

                                <p class="text-[10px] text-slate-400 mt-1">
                                    {{ s.jenis || '-' }}
                                </p>
                            </div>

                            <span class="inline-flex items-center gap-1.5 px-2 py-1 rounded-lg bg-amber-50 border border-amber-200 text-amber-700 text-[9px] font-bold uppercase">
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
                                    {{ angka(s.qty, 3) }}
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
import { useGoodsReceipt } from '../composables/useGoodsReceipt'
import { angka, tanggal } from '@/utils/format'

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
} = useGoodsReceipt()

const totalItem = computed(() => {
    return ringkasan.value?.item?.length || 0
})

const totalTimbang = computed(() => {
    return (ringkasan.value?.item || []).reduce(
        (total, item) => total + (Number(item.timbang) || 0),
        0
    )
})

const totalDitolak = computed(() => {
    return (ringkasan.value?.item || []).reduce(
        (total, item) => total + (Number(item.ditolak) || 0),
        0
    )
})

const melebihiToleransi = (persen) => {
    return persen != null && Math.abs(Number(persen)) > 0.5
}

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