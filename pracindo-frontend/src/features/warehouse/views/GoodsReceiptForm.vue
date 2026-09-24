<!-- features/warehouse/views/GoodsReceiptForm.vue -->
<template>
    <div class="w-full min-w-0 animate-fade-in relative">

        <!-- =========================================================
             STATE: BERHASIL DISIMPAN
        ========================================================== -->
        <template v-if="hasil">
            <section class="w-full bg-white border border-emerald-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden">

                <!-- Success Header -->
                <div class="p-5 md:p-7 bg-gradient-to-br from-emerald-50 to-white border-b border-emerald-100">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 shrink-0 rounded-2xl bg-emerald-100 text-emerald-600 flex items-center justify-center border border-emerald-200 shadow-sm">
                            <i class="pi pi-check text-xl"></i>
                        </div>

                        <div class="min-w-0">
                            <div class="flex flex-wrap items-center gap-2 mb-1">
                                <span class="inline-flex items-center gap-1.5 px-2 py-1 rounded-md bg-emerald-100 text-emerald-700 border border-emerald-200 text-[10px] font-bold uppercase tracking-wider">
                                    <i class="pi pi-check-circle text-[9px]"></i>
                                    Berhasil
                                </span>
                            </div>

                            <h1 class="text-xl md:text-2xl font-bold text-slate-900 tracking-tight">
                                Penerimaan Tersimpan
                            </h1>

                            <p class="text-xs md:text-sm text-slate-600 mt-1 leading-relaxed">
                                {{ hasil.pesan || 'Transaksi penerimaan barang berhasil dicatat ke dalam sistem.' }}
                            </p>
                        </div>
                    </div>
                </div>

                <div class="p-5 md:p-7 space-y-6">

                    <!-- Nomor Dokumen -->
                    <div class="rounded-2xl border border-slate-200 bg-slate-50/80 p-4 md:p-5">
                        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                            <div>
                                <p class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                                    Nomor Dokumen Penerimaan
                                </p>

                                <p class="text-lg md:text-xl font-black text-slate-900 mt-1 break-all">
                                    {{ hasil.penerimaan?.nomor || '-' }}
                                </p>
                            </div>

                            <div class="w-10 h-10 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-slate-500 shrink-0">
                                <i class="pi pi-file-check"></i>
                            </div>
                        </div>
                    </div>

                    <!-- Selisih -->
                    <div v-if="hasil.laporan_selisih?.length">
                        <div class="flex items-start gap-3 mb-3">
                            <div class="w-8 h-8 shrink-0 rounded-lg bg-amber-100 text-amber-600 flex items-center justify-center">
                                <i class="pi pi-exclamation-triangle text-sm"></i>
                            </div>

                            <div>
                                <h3 class="text-sm font-bold text-slate-900">
                                    Laporan Selisih Terbit
                                </h3>

                                <p class="text-xs text-slate-500 mt-0.5">
                                    Sistem membuat laporan selisih berdasarkan hasil pengecekan penerimaan.
                                </p>
                            </div>
                        </div>

                        <div class="overflow-x-auto custom-scrollbar rounded-2xl border border-slate-200">
                            <table class="w-full min-w-[520px] text-left">
                                <thead>
                                    <tr class="bg-slate-50 border-b border-slate-100">
                                        <th class="px-4 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                            Nomor Laporan
                                        </th>

                                        <th class="px-4 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                            Jenis
                                        </th>

                                        <th class="px-4 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right">
                                            Qty Selisih
                                        </th>
                                    </tr>
                                </thead>

                                <tbody class="divide-y divide-slate-100">
                                    <tr
                                        v-for="s in hasil.laporan_selisih"
                                        :key="s.nomor"
                                        class="hover:bg-slate-50/70 transition-colors"
                                    >
                                        <td class="px-4 py-3.5 text-sm font-bold text-slate-800">
                                            {{ s.nomor || '-' }}
                                        </td>

                                        <td class="px-4 py-3.5 text-sm text-slate-600">
                                            {{ s.jenis || '-' }}
                                        </td>

                                        <td class="px-4 py-3.5 text-sm text-right font-bold text-rose-600">
                                            {{ angka(s.qty_selisih, 3) }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Actions -->
                    <div class="pt-5 border-t border-slate-100 flex flex-col sm:flex-row gap-3">
                        <router-link
                            v-if="hasil.penerimaan?.id"
                            :to="`/warehouse/input/receipt/${hasil.penerimaan.id}`"
                            class="h-11 px-5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-sm font-bold transition-all shadow-sm inline-flex items-center justify-center gap-2"
                        >
                            <i class="pi pi-eye text-xs"></i>
                            Lihat Detail
                        </router-link>

                        <button
                            type="button"
                            @click="$emit('tutup')"
                            class="h-11 px-5 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-sm font-bold transition-all inline-flex items-center justify-center gap-2"
                        >
                            <i class="pi pi-arrow-left text-xs"></i>
                            Kembali ke Daftar
                        </button>
                    </div>
                </div>
            </section>
        </template>

        <!-- =========================================================
             STATE: FORM
        ========================================================== -->
        <form
            v-else
            @submit.prevent="kirim"
            class="space-y-5 md:space-y-6 pb-24 lg:pb-2"
            novalidate
        >

            <!-- =====================================================
                 STEP 1 - REFERENSI
            ====================================================== -->
            <section class="bg-white border border-slate-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden">

                <div class="px-4 py-4 md:px-6 md:py-5 border-b border-slate-100 flex items-center gap-3">
                    <div class="w-9 h-9 shrink-0 rounded-xl bg-blue-50 text-blue-600 border border-blue-100 flex items-center justify-center">
                        <span class="text-xs font-black">01</span>
                    </div>

                    <div>
                        <h2 class="text-sm md:text-base font-bold text-slate-900">
                            Referensi Dokumen
                        </h2>

                        <p class="text-[11px] md:text-xs text-slate-500 mt-0.5">
                            Tentukan PO dan informasi utama penerimaan.
                        </p>
                    </div>
                </div>

                <div class="p-4 md:p-6 space-y-5">

                    <!-- PO -->
                    <div class="space-y-2">
                        <label
                            for="po-penerimaan"
                            class="block text-[11px] font-bold text-slate-600 uppercase tracking-wider"
                        >
                            Purchase Order
                            <span class="text-rose-500">*</span>
                        </label>

                        <div class="relative">
                            <i class="pi pi-file-edit absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-sm pointer-events-none"></i>

                            <select
                                id="po-penerimaan"
                                v-model="poIdTerpilih"
                                :disabled="sedangProses"
                                required
                                class="w-full h-12 pl-11 pr-11 rounded-xl bg-slate-50 border border-slate-200 text-sm font-semibold text-slate-800 focus:outline-none focus:bg-white focus:border-slate-400 focus:ring-4 focus:ring-slate-100 appearance-none cursor-pointer transition-all disabled:opacity-60 disabled:cursor-not-allowed"
                            >
                                <option value="" disabled>
                                    Pilih PO supplier
                                </option>

                                <option
                                    v-for="po in daftarPOSiapTerima"
                                    :key="po.id"
                                    :value="po.id"
                                >
                                    {{ po.no_po }} • {{ po.suplier_nama }}
                                </option>
                            </select>

                            <i class="pi pi-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 text-xs pointer-events-none"></i>
                        </div>

                        <p
                            v-if="!daftarPOSiapTerima.length && !sedangProses"
                            class="text-xs text-amber-600 flex items-center gap-1.5"
                        >
                            <i class="pi pi-info-circle"></i>
                            Tidak ada PO yang tersedia untuk diterima.
                        </p>
                    </div>

                    <!-- Selected PO Summary -->
                    <transition name="slide-fade">
                        <div
                            v-if="poTerpilih"
                            class="rounded-2xl border border-blue-100 bg-blue-50/60 overflow-hidden"
                        >
                            <div class="p-4 md:p-5">
                                <div class="flex items-start justify-between gap-4 mb-4">
                                    <div class="min-w-0">
                                        <p class="text-[10px] font-bold uppercase tracking-wider text-blue-500">
                                            PO Terpilih
                                        </p>

                                        <p class="text-sm md:text-base font-black text-blue-950 mt-1 break-all">
                                            {{ poTerpilih.no_po || '-' }}
                                        </p>

                                        <p class="text-xs text-blue-700 mt-1 break-words">
                                            {{ poTerpilih.suplier_nama || '-' }}
                                        </p>
                                    </div>

                                    <div class="w-10 h-10 shrink-0 rounded-xl bg-white border border-blue-100 text-blue-600 flex items-center justify-center">
                                        <i class="pi pi-check-circle"></i>
                                    </div>
                                </div>

                                <div class="grid grid-cols-2 md:grid-cols-3 gap-2">
                                    <div class="rounded-xl bg-white/80 border border-blue-100 p-3">
                                        <p class="text-[9px] uppercase tracking-wider font-bold text-slate-400">
                                            Item
                                        </p>
                                        <p class="text-sm font-black text-slate-800 mt-1">
                                            {{ baris.length }}
                                        </p>
                                    </div>

                                    <div class="rounded-xl bg-white/80 border border-blue-100 p-3">
                                        <p class="text-[9px] uppercase tracking-wider font-bold text-slate-400">
                                            Sisa Qty
                                        </p>
                                        <p class="text-sm font-black text-slate-800 mt-1">
                                            {{ angka(totalSisa, 3) }}
                                        </p>
                                    </div>

                                    <div class="rounded-xl bg-white/80 border border-blue-100 p-3 col-span-2 md:col-span-1">
                                        <p class="text-[9px] uppercase tracking-wider font-bold text-slate-400">
                                            Status
                                        </p>

                                        <p class="text-xs font-bold text-blue-700 mt-1 inline-flex items-center gap-1.5">
                                            <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
                                            Siap Diproses
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </transition>

                    <!-- Document Inputs -->
                    <transition name="slide-fade">
                        <div
                            v-if="poTerpilih"
                            class="grid grid-cols-1 md:grid-cols-2 gap-4"
                        >
                            <div class="space-y-2">
                                <label
                                    for="surat-jalan"
                                    class="block text-[11px] font-bold text-slate-600 uppercase tracking-wider"
                                >
                                    No. Surat Jalan
                                    <span class="text-rose-500">*</span>
                                </label>

                                <div class="relative">
                                    <i class="pi pi-truck absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs pointer-events-none"></i>

                                    <input
                                        id="surat-jalan"
                                        v-model="form.no_surat_jalan"
                                        type="text"
                                        autocomplete="off"
                                        maxlength="100"
                                        required
                                        placeholder="Nomor surat jalan supplier"
                                        class="w-full h-11 pl-10 pr-3 rounded-xl bg-slate-50 border border-slate-200 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:bg-white focus:border-slate-400 focus:ring-4 focus:ring-slate-100 transition-all"
                                    />
                                </div>
                            </div>

                            <div class="space-y-2">
                                <label
                                    for="tanggal-terima"
                                    class="block text-[11px] font-bold text-slate-600 uppercase tracking-wider"
                                >
                                    Tanggal Terima
                                    <span class="text-rose-500">*</span>
                                </label>

                                <div class="relative">
                                    <i class="pi pi-calendar absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs pointer-events-none"></i>

                                    <input
                                        id="tanggal-terima"
                                        v-model="form.tanggal"
                                        type="date"
                                        required
                                        class="w-full h-11 pl-10 pr-3 rounded-xl bg-slate-50 border border-slate-200 text-sm text-slate-800 focus:outline-none focus:bg-white focus:border-slate-400 focus:ring-4 focus:ring-slate-100 transition-all"
                                    />
                                </div>
                            </div>

                            <div class="space-y-2 md:col-span-2">
                                <label
                                    for="catatan"
                                    class="block text-[11px] font-bold text-slate-600 uppercase tracking-wider"
                                >
                                    Catatan
                                    <span class="font-normal normal-case text-slate-400">
                                        (Opsional)
                                    </span>
                                </label>

                                <textarea
                                    id="catatan"
                                    v-model="form.catatan"
                                    rows="3"
                                    maxlength="500"
                                    placeholder="Catatan tambahan untuk transaksi penerimaan..."
                                    class="w-full px-3.5 py-3 rounded-xl bg-slate-50 border border-slate-200 text-sm text-slate-800 placeholder:text-slate-400 resize-none focus:outline-none focus:bg-white focus:border-slate-400 focus:ring-4 focus:ring-slate-100 transition-all"
                                ></textarea>

                                <div class="flex justify-end">
                                    <span class="text-[10px] text-slate-400">
                                        {{ form.catatan.length }}/500
                                    </span>
                                </div>
                            </div>
                        </div>
                    </transition>
                </div>
            </section>

            <!-- =====================================================
                 STEP 2 - FISIK
            ====================================================== -->
            <section
                v-if="poTerpilih"
                class="bg-white border border-slate-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden animate-fade-in"
            >
                <div class="px-4 py-4 md:px-6 md:py-5 border-b border-slate-100">
                    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                        <div class="flex items-center gap-3">
                            <div class="w-9 h-9 shrink-0 rounded-xl bg-slate-100 text-slate-700 border border-slate-200 flex items-center justify-center">
                                <span class="text-xs font-black">02</span>
                            </div>

                            <div>
                                <h2 class="text-sm md:text-base font-bold text-slate-900">
                                    Pengecekan Fisik
                                </h2>

                                <p class="text-[11px] md:text-xs text-slate-500 mt-0.5">
                                    Masukkan hasil timbang dan informasi kemasan setiap item.
                                </p>
                            </div>
                        </div>

                        <!-- Mini summary -->
                        <div class="grid grid-cols-3 gap-2 md:min-w-[340px]">
                            <div class="rounded-xl bg-slate-50 border border-slate-100 px-3 py-2.5">
                                <p class="text-[9px] uppercase font-bold tracking-wider text-slate-400">
                                    Diterima
                                </p>
                                <p class="text-xs md:text-sm font-black text-emerald-600 mt-0.5">
                                    {{ angka(totalDiterima, 3) }}
                                </p>
                            </div>

                            <div class="rounded-xl bg-slate-50 border border-slate-100 px-3 py-2.5">
                                <p class="text-[9px] uppercase font-bold tracking-wider text-slate-400">
                                    Ditolak
                                </p>
                                <p class="text-xs md:text-sm font-black text-rose-600 mt-0.5">
                                    {{ angka(totalDitolak, 3) }}
                                </p>
                            </div>

                            <div class="rounded-xl bg-slate-50 border border-slate-100 px-3 py-2.5">
                                <p class="text-[9px] uppercase font-bold tracking-wider text-slate-400">
                                    Item Diisi
                                </p>
                                <p class="text-xs md:text-sm font-black text-slate-800 mt-0.5">
                                    {{ jumlahItemDiisi }}/{{ baris.length }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="p-3 md:p-5">

                    <!-- =================================================
                         DESKTOP
                    ================================================== -->
                    <div class="hidden lg:block overflow-x-auto custom-scrollbar">
                        <table class="w-full min-w-[1100px] text-left border-collapse">
                            <thead>
                                <tr class="bg-slate-50 border border-slate-100">
                                    <th class="px-3 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider w-[18%]">
                                        Produk
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right w-[9%]">
                                        Sisa PO
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider w-[12%]">
                                        Kemasan
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right w-[8%]">
                                        Koli
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right w-[9%]">
                                        Isi/Koli
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right w-[10%]">
                                        Deklarasi
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-emerald-600 uppercase tracking-wider text-right w-[11%]">
                                        Qty Diterima
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-rose-500 uppercase tracking-wider text-right w-[10%]">
                                        Qty Ditolak
                                    </th>

                                    <th class="px-3 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right w-[13%]">
                                        Selisih
                                    </th>
                                </tr>
                            </thead>

                            <tbody class="divide-y divide-slate-100">
                                <tr
                                    v-for="r in baris"
                                    :key="r.po_item_id"
                                    class="group hover:bg-slate-50/60 transition-colors"
                                >
                                    <!-- Produk -->
                                    <td class="px-3 py-4 align-top">
                                        <div class="flex items-start gap-2.5">
                                            <div class="w-8 h-8 shrink-0 rounded-lg bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-500">
                                                <i class="pi pi-box text-[10px]"></i>
                                            </div>

                                            <div class="min-w-0">
                                                <p class="text-xs font-bold text-slate-800 break-words">
                                                    {{ r.nama_item || '-' }}
                                                </p>

                                                <span
                                                    v-if="statusBaris(r) === 'warning'"
                                                    class="inline-flex items-center gap-1 mt-1 px-1.5 py-0.5 rounded-md bg-amber-50 text-amber-700 border border-amber-100 text-[9px] font-bold"
                                                >
                                                    <i class="pi pi-exclamation-triangle text-[8px]"></i>
                                                    Perlu perhatian
                                                </span>

                                                <span
                                                    v-else-if="statusBaris(r) === 'complete'"
                                                    class="inline-flex items-center gap-1 mt-1 px-1.5 py-0.5 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-100 text-[9px] font-bold"
                                                >
                                                    <i class="pi pi-check text-[8px]"></i>
                                                    Terisi
                                                </span>
                                            </div>
                                        </div>
                                    </td>

                                    <!-- Sisa -->
                                    <td class="px-2 py-4 align-top text-right">
                                        <span class="text-xs font-bold text-slate-600">
                                            {{ angka(r.sisa_qty, 3) }}
                                        </span>
                                    </td>

                                    <!-- Kemasan -->
                                    <td class="px-2 py-4 align-top">
                                        <select
                                            v-model="r.jenis_kemasan"
                                            class="w-full h-9 px-2.5 rounded-lg bg-white border border-slate-200 text-[11px] font-semibold text-slate-700 focus:outline-none focus:border-slate-400 focus:ring-2 focus:ring-slate-100 transition-all"
                                        >
                                            <option
                                                v-for="k in JENIS_KEMASAN"
                                                :key="k"
                                                :value="k"
                                            >
                                                {{ k }}
                                            </option>
                                        </select>
                                    </td>

                                    <!-- Koli -->
                                    <td class="px-2 py-4 align-top">
                                        <input
                                            v-if="r.jenis_kemasan !== 'CURAH'"
                                            v-model.number="r.jumlah_koli"
                                            type="number"
                                            min="0"
                                            step="1"
                                            required
                                            inputmode="numeric"
                                            class="w-full h-9 px-2 rounded-lg bg-white border border-slate-200 text-xs text-right font-semibold text-slate-700 focus:outline-none focus:border-slate-400 focus:ring-2 focus:ring-slate-100 transition-all"
                                        />

                                        <span
                                            v-else
                                            class="block text-center text-[10px] font-semibold text-slate-400 py-2"
                                        >
                                            —
                                        </span>
                                    </td>

                                    <!-- Isi/Koli -->
                                    <td class="px-2 py-4 align-top">
                                        <input
                                            v-if="r.jenis_kemasan !== 'CURAH'"
                                            v-model.number="r.isi_per_koli"
                                            type="number"
                                            min="0"
                                            step="0.001"
                                            required
                                            inputmode="decimal"
                                            class="w-full h-9 px-2 rounded-lg bg-white border border-slate-200 text-xs text-right font-semibold text-slate-700 focus:outline-none focus:border-slate-400 focus:ring-2 focus:ring-slate-100 transition-all"
                                        />

                                        <span
                                            v-else
                                            class="block text-center text-[10px] font-semibold text-slate-400 py-2"
                                        >
                                            —
                                        </span>
                                    </td>

                                    <!-- Deklarasi -->
                                    <td class="px-2 py-4 align-top text-right">
                                        <span
                                            v-if="deklarasi(r) != null"
                                            class="inline-flex px-2 py-1 rounded-md bg-slate-50 border border-slate-100 text-xs font-bold text-slate-600"
                                        >
                                            {{ angka(deklarasi(r), 3) }}
                                        </span>

                                        <span
                                            v-else
                                            class="text-xs text-slate-400"
                                        >
                                            —
                                        </span>
                                    </td>

                                    <!-- Diterima -->
                                    <td class="px-2 py-4 align-top">
                                        <input
                                            v-model.number="r.qty_diterima"
                                            type="number"
                                            min="0"
                                            step="0.001"
                                            :max="r.sisa_qty"
                                            inputmode="decimal"
                                            class="w-full h-9 px-2 rounded-lg bg-emerald-50/50 border border-emerald-200 text-xs text-right font-bold text-emerald-700 focus:outline-none focus:bg-white focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 transition-all"
                                        />
                                    </td>

                                    <!-- Ditolak -->
                                    <td class="px-2 py-4 align-top">
                                        <input
                                            v-model.number="r.qty_ditolak"
                                            type="number"
                                            min="0"
                                            step="0.001"
                                            inputmode="decimal"
                                            class="w-full h-9 px-2 rounded-lg bg-rose-50/50 border border-rose-200 text-xs text-right font-bold text-rose-600 focus:outline-none focus:bg-white focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition-all"
                                        />
                                    </td>

                                    <!-- Selisih -->
                                    <td class="px-3 py-4 align-top text-right">
                                        <template v-if="selisih(r) != null">
                                            <span
                                                class="inline-flex flex-col items-end px-2.5 py-1.5 rounded-lg border"
                                                :class="melebihiToleransi(r)
                                                    ? 'bg-rose-50 border-rose-100 text-rose-600'
                                                    : 'bg-slate-50 border-slate-100 text-slate-700'"
                                            >
                                                <span class="text-xs font-bold">
                                                    {{ angka(selisih(r), 3) }}
                                                </span>

                                                <span class="text-[9px] font-semibold opacity-80 mt-0.5">
                                                    {{ angka(persenSelisih(r), 2) }}%
                                                </span>
                                            </span>
                                        </template>

                                        <span v-else class="text-xs text-slate-400">
                                            —
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- =================================================
                         MOBILE / TABLET
                    ================================================== -->
                    <div class="lg:hidden space-y-4">
                        <article
                            v-for="r in baris"
                            :key="'mobile-' + r.po_item_id"
                            class="rounded-2xl border border-slate-200 bg-slate-50/50 overflow-hidden"
                        >
                            <!-- Item Header -->
                            <div class="p-4 bg-white border-b border-slate-100">
                                <div class="flex items-start justify-between gap-3">
                                    <div class="flex items-start gap-3 min-w-0">
                                        <div class="w-10 h-10 shrink-0 rounded-xl bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-500">
                                            <i class="pi pi-box text-sm"></i>
                                        </div>

                                        <div class="min-w-0">
                                            <p class="text-sm font-bold text-slate-900 break-words">
                                                {{ r.nama_item || '-' }}
                                            </p>

                                            <p class="text-[10px] text-slate-400 mt-1">
                                                Sisa PO:
                                                <span class="font-bold text-slate-600">
                                                    {{ angka(r.sisa_qty, 3) }}
                                                </span>
                                            </p>
                                        </div>
                                    </div>

                                    <span
                                        v-if="statusBaris(r) === 'complete'"
                                        class="shrink-0 inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-100 text-[9px] font-bold"
                                    >
                                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                                        Terisi
                                    </span>

                                    <span
                                        v-else-if="statusBaris(r) === 'warning'"
                                        class="shrink-0 inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-amber-50 text-amber-700 border border-amber-100 text-[9px] font-bold"
                                    >
                                        <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                                        Perhatian
                                    </span>
                                </div>
                            </div>

                            <div class="p-4 space-y-4">

                                <!-- Kemasan -->
                                <div class="space-y-1.5">
                                    <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                        Jenis Kemasan
                                    </label>

                                    <select
                                        v-model="r.jenis_kemasan"
                                        class="w-full h-11 px-3 rounded-xl bg-white border border-slate-200 text-sm font-semibold text-slate-700 focus:outline-none focus:border-slate-400 focus:ring-4 focus:ring-slate-100 transition-all"
                                    >
                                        <option
                                            v-for="k in JENIS_KEMASAN"
                                            :key="k"
                                            :value="k"
                                        >
                                            {{ k }}
                                        </option>
                                    </select>
                                </div>

                                <!-- Koli / Isi -->
                                <div
                                    v-if="r.jenis_kemasan !== 'CURAH'"
                                    class="grid grid-cols-2 gap-3"
                                >
                                    <div class="space-y-1.5">
                                        <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                            Jumlah Koli
                                        </label>

                                        <input
                                            v-model.number="r.jumlah_koli"
                                            type="number"
                                            min="0"
                                            step="1"
                                            required
                                            inputmode="numeric"
                                            class="w-full h-11 px-3 rounded-xl bg-white border border-slate-200 text-sm text-right font-bold text-slate-700 focus:outline-none focus:border-slate-400 focus:ring-4 focus:ring-slate-100 transition-all"
                                        />
                                    </div>

                                    <div class="space-y-1.5">
                                        <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                            Isi / Koli
                                        </label>

                                        <input
                                            v-model.number="r.isi_per_koli"
                                            type="number"
                                            min="0"
                                            step="0.001"
                                            required
                                            inputmode="decimal"
                                            class="w-full h-11 px-3 rounded-xl bg-white border border-slate-200 text-sm text-right font-bold text-slate-700 focus:outline-none focus:border-slate-400 focus:ring-4 focus:ring-slate-100 transition-all"
                                        />
                                    </div>
                                </div>

                                <!-- Deklarasi -->
                                <div class="flex items-center justify-between gap-4 px-3 py-3 rounded-xl bg-white border border-slate-200">
                                    <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                                        Deklarasi
                                    </span>

                                    <span class="text-sm font-black text-slate-700">
                                        {{ deklarasi(r) != null ? angka(deklarasi(r), 3) : 'Tidak tersedia' }}
                                    </span>
                                </div>

                                <!-- Qty -->
                                <div class="grid grid-cols-2 gap-3">
                                    <div class="space-y-1.5">
                                        <label class="block text-[10px] font-bold text-emerald-600 uppercase tracking-wider">
                                            Qty Diterima
                                        </label>

                                        <input
                                            v-model.number="r.qty_diterima"
                                            type="number"
                                            min="0"
                                            step="0.001"
                                            :max="r.sisa_qty"
                                            inputmode="decimal"
                                            class="w-full h-12 px-3 rounded-xl bg-emerald-50/40 border border-emerald-200 text-sm text-right font-black text-emerald-700 focus:outline-none focus:bg-white focus:border-emerald-400 focus:ring-4 focus:ring-emerald-50 transition-all"
                                        />
                                    </div>

                                    <div class="space-y-1.5">
                                        <label class="block text-[10px] font-bold text-rose-500 uppercase tracking-wider">
                                            Qty Ditolak
                                        </label>

                                        <input
                                            v-model.number="r.qty_ditolak"
                                            type="number"
                                            min="0"
                                            step="0.001"
                                            inputmode="decimal"
                                            class="w-full h-12 px-3 rounded-xl bg-rose-50/40 border border-rose-200 text-sm text-right font-black text-rose-600 focus:outline-none focus:bg-white focus:border-rose-400 focus:ring-4 focus:ring-rose-50 transition-all"
                                        />
                                    </div>
                                </div>

                                <!-- Selisih -->
                                <div
                                    v-if="selisih(r) != null"
                                    class="rounded-xl border px-3 py-3"
                                    :class="melebihiToleransi(r)
                                        ? 'bg-rose-50 border-rose-200'
                                        : 'bg-white border-slate-200'"
                                >
                                    <div class="flex items-center justify-between gap-3">
                                        <div>
                                            <p
                                                class="text-[10px] font-bold uppercase tracking-wider"
                                                :class="melebihiToleransi(r)
                                                    ? 'text-rose-500'
                                                    : 'text-slate-400'"
                                            >
                                                Selisih
                                            </p>

                                            <p
                                                class="text-xs font-medium mt-0.5"
                                                :class="melebihiToleransi(r)
                                                    ? 'text-rose-600'
                                                    : 'text-slate-500'"
                                            >
                                                Batas toleransi ±0,5%
                                            </p>
                                        </div>

                                        <div class="text-right">
                                            <p
                                                class="text-sm font-black"
                                                :class="melebihiToleransi(r)
                                                    ? 'text-rose-600'
                                                    : 'text-slate-700'"
                                            >
                                                {{ angka(selisih(r), 3) }}
                                            </p>

                                            <p
                                                class="text-[10px] font-bold"
                                                :class="melebihiToleransi(r)
                                                    ? 'text-rose-500'
                                                    : 'text-slate-400'"
                                            >
                                                {{ angka(persenSelisih(r), 2) }}%
                                            </p>
                                        </div>
                                    </div>
                                </div>

                                <!-- Alasan Tolak -->
                                <transition name="slide-fade">
                                    <div
                                        v-if="Number(r.qty_ditolak) > 0"
                                        class="space-y-1.5"
                                    >
                                        <label class="block text-[10px] font-bold text-rose-600 uppercase tracking-wider">
                                            Alasan Penolakan
                                            <span class="text-rose-500">*</span>
                                        </label>

                                        <textarea
                                            v-model="r.alasan_tolak"
                                            rows="2"
                                            maxlength="300"
                                            required
                                            placeholder="Jelaskan alasan barang ditolak..."
                                            class="w-full px-3 py-2.5 rounded-xl bg-white border border-rose-200 text-sm text-slate-700 placeholder:text-slate-400 resize-none focus:outline-none focus:border-rose-400 focus:ring-4 focus:ring-rose-50 transition-all"
                                        ></textarea>
                                    </div>
                                </transition>
                            </div>
                        </article>
                    </div>

                    <!-- =================================================
                         VALIDATION / WARNING
                    ================================================== -->
                    <div class="mt-5 space-y-3">

                        <!-- Tolerance -->
                        <div
                            v-for="r in barisMelebihiToleransi"
                            :key="'tol-' + r.po_item_id"
                            class="rounded-xl border border-amber-200 bg-amber-50 px-3.5 py-3 flex items-start gap-3"
                        >
                            <div class="w-8 h-8 shrink-0 rounded-lg bg-amber-100 text-amber-600 flex items-center justify-center">
                                <i class="pi pi-exclamation-triangle text-xs"></i>
                            </div>

                            <div class="text-xs text-amber-800 leading-relaxed">
                                <strong>{{ r.nama_item }}:</strong>
                                selisih melebihi toleransi ±0,5%.
                                Laporan selisih akan dibuat otomatis setelah transaksi berhasil disimpan.
                            </div>
                        </div>

                        <!-- Over PO -->
                        <div
                            v-for="r in barisLewatSisa"
                            :key="'lewat-' + r.po_item_id"
                            class="rounded-xl border border-red-200 bg-red-50 px-3.5 py-3 flex items-start gap-3"
                        >
                            <div class="w-8 h-8 shrink-0 rounded-lg bg-red-100 text-red-600 flex items-center justify-center">
                                <i class="pi pi-times-circle text-xs"></i>
                            </div>

                            <div class="text-xs text-red-800 leading-relaxed">
                                <strong>{{ r.nama_item }}:</strong>
                                Qty diterima melebihi sisa PO.
                                Maksimal:
                                <strong>{{ angka(r.sisa_qty, 3) }}</strong>.
                            </div>
                        </div>

                        <!-- Missing reasons -->
                        <div
                            v-for="r in barisTanpaAlasan"
                            :key="'alasan-' + r.po_item_id"
                            class="rounded-xl border border-rose-200 bg-rose-50 px-3.5 py-3 flex items-start gap-3"
                        >
                            <div class="w-8 h-8 shrink-0 rounded-lg bg-rose-100 text-rose-600 flex items-center justify-center">
                                <i class="pi pi-comment text-xs"></i>
                            </div>

                            <div class="text-xs text-rose-800 leading-relaxed">
                                <strong>{{ r.nama_item }}:</strong>
                                alasan penolakan wajib diisi karena terdapat Qty Ditolak.
                            </div>
                        </div>
                    </div>

                    <!-- =================================================
                         GLOBAL ERROR
                    ================================================== -->
                    <transition name="slide-fade">
                        <div
                            v-if="pesanError"
                            class="mt-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 flex items-start gap-3"
                        >
                            <div class="w-8 h-8 shrink-0 rounded-lg bg-red-100 text-red-600 flex items-center justify-center">
                                <i class="pi pi-exclamation-circle text-xs"></i>
                            </div>

                            <div>
                                <p class="text-xs font-bold text-red-800">
                                    Data belum dapat disimpan
                                </p>

                                <p class="text-xs text-red-700 mt-0.5 leading-relaxed">
                                    {{ pesanError }}
                                </p>
                            </div>
                        </div>
                    </transition>
                </div>
            </section>

            <!-- =====================================================
                 STEP 3 - RINGKASAN
            ====================================================== -->
            <section
                v-if="poTerpilih"
                class="bg-white border border-slate-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden"
            >
                <div class="px-4 py-4 md:px-6 md:py-5 border-b border-slate-100 flex items-center gap-3">
                    <div class="w-9 h-9 shrink-0 rounded-xl bg-emerald-50 text-emerald-600 border border-emerald-100 flex items-center justify-center">
                        <span class="text-xs font-black">03</span>
                    </div>

                    <div>
                        <h2 class="text-sm md:text-base font-bold text-slate-900">
                            Ringkasan Penerimaan
                        </h2>

                        <p class="text-[11px] md:text-xs text-slate-500 mt-0.5">
                            Periksa kembali data sebelum transaksi dikirim.
                        </p>
                    </div>
                </div>

                <div class="p-4 md:p-6">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">

                        <div class="rounded-2xl bg-slate-50 border border-slate-100 p-4">
                            <div class="flex items-center justify-between gap-2">
                                <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                                    Item
                                </span>
                                <i class="pi pi-box text-slate-300 text-xs"></i>
                            </div>

                            <p class="text-xl font-black text-slate-900 mt-2">
                                {{ jumlahItemDiisi }}
                            </p>

                            <p class="text-[10px] text-slate-400 mt-0.5">
                                dari {{ baris.length }} item
                            </p>
                        </div>

                        <div class="rounded-2xl bg-emerald-50 border border-emerald-100 p-4">
                            <div class="flex items-center justify-between gap-2">
                                <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-600">
                                    Diterima
                                </span>
                                <i class="pi pi-check text-emerald-300 text-xs"></i>
                            </div>

                            <p class="text-xl font-black text-emerald-700 mt-2">
                                {{ angka(totalDiterima, 3) }}
                            </p>

                            <p class="text-[10px] text-emerald-500 mt-0.5">
                                Qty diterima
                            </p>
                        </div>

                        <div class="rounded-2xl bg-rose-50 border border-rose-100 p-4">
                            <div class="flex items-center justify-between gap-2">
                                <span class="text-[10px] font-bold uppercase tracking-wider text-rose-500">
                                    Ditolak
                                </span>
                                <i class="pi pi-times text-rose-300 text-xs"></i>
                            </div>

                            <p class="text-xl font-black text-rose-600 mt-2">
                                {{ angka(totalDitolak, 3) }}
                            </p>

                            <p class="text-[10px] text-rose-500 mt-0.5">
                                Qty ditolak
                            </p>
                        </div>

                        <div class="rounded-2xl bg-blue-50 border border-blue-100 p-4">
                            <div class="flex items-center justify-between gap-2">
                                <span class="text-[10px] font-bold uppercase tracking-wider text-blue-500">
                                    Selisih
                                </span>
                                <i class="pi pi-chart-line text-blue-300 text-xs"></i>
                            </div>

                            <p class="text-xl font-black text-blue-700 mt-2">
                                {{ barisMelebihiToleransi.length }}
                            </p>

                            <p class="text-[10px] text-blue-500 mt-0.5">
                                Perlu laporan
                            </p>
                        </div>
                    </div>

                    <div
                        v-if="!jumlahItemDiisi"
                        class="mt-4 rounded-xl bg-slate-50 border border-slate-100 px-4 py-3 flex items-start gap-3"
                    >
                        <i class="pi pi-info-circle text-slate-400 mt-0.5 text-xs"></i>

                        <p class="text-xs text-slate-500 leading-relaxed">
                            Isi minimal satu item pada kolom <strong>Qty Diterima</strong> sebelum menyimpan transaksi.
                        </p>
                    </div>
                </div>
            </section>

            <!-- =====================================================
                 ACTION BAR DESKTOP
            ====================================================== -->
            <div
                v-if="poTerpilih"
                class="hidden lg:flex sticky bottom-4 z-20 items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-white/95 backdrop-blur-md p-3.5 shadow-xl shadow-slate-900/10"
            >
                <div class="min-w-0">
                    <p class="text-xs font-bold text-slate-800">
                        {{ poTerpilih.no_po }}
                    </p>

                    <p class="text-[10px] text-slate-400 mt-0.5">
                        Pastikan hasil timbang dan data dokumen sudah sesuai.
                    </p>
                </div>

                <div class="flex items-center gap-2 shrink-0">
                    <button
                        type="button"
                        @click="$emit('tutup')"
                        :disabled="sedangProses"
                        class="h-10 px-4 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center gap-2"
                    >
                        Batal
                    </button>

                    <button
                        type="submit"
                        :disabled="sedangProses || barisLewatSisa.length > 0"
                        class="h-10 px-5 rounded-xl bg-slate-900 hover:bg-slate-800 active:bg-slate-950 disabled:bg-slate-300 text-white text-xs font-bold transition-all shadow-sm disabled:cursor-not-allowed inline-flex items-center gap-2"
                    >
                        <i
                            v-if="sedangProses"
                            class="pi pi-spin pi-spinner text-[10px]"
                        ></i>

                        <i
                            v-else
                            class="pi pi-save text-[10px]"
                        ></i>

                        {{ sedangProses ? 'Menyimpan...' : 'Simpan Penerimaan' }}
                    </button>
                </div>
            </div>

            <!-- =====================================================
                 ACTION BAR MOBILE
            ====================================================== -->
            <div
                v-if="poTerpilih"
                class="lg:hidden fixed bottom-0 left-0 right-0 z-40 px-3 py-3 bg-white/95 backdrop-blur-md border-t border-slate-200 shadow-[0_-8px_24px_rgba(15,23,42,0.08)]"
            >
                <div class="flex items-center gap-2 max-w-screen-xl mx-auto">
                    <button
                        type="button"
                        @click="$emit('tutup')"
                        :disabled="sedangProses"
                        class="h-11 flex-1 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Batal
                    </button>

                    <button
                        type="submit"
                        :disabled="sedangProses || barisLewatSisa.length > 0"
                        class="h-11 flex-[1.5] rounded-xl bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 text-white text-xs font-bold transition-all shadow-sm disabled:cursor-not-allowed inline-flex items-center justify-center gap-2"
                    >
                        <i
                            v-if="sedangProses"
                            class="pi pi-spin pi-spinner text-[10px]"
                        ></i>

                        <i
                            v-else
                            class="pi pi-save text-[10px]"
                        ></i>

                        {{ sedangProses ? 'Menyimpan...' : 'Simpan Penerimaan' }}
                    </button>
                </div>
            </div>
        </form>
    </div>
</template>

<script setup>
import {
    ref,
    reactive,
    computed,
    onMounted,
    onUnmounted,
    watch,
} from 'vue'

import {
    useGoodsReceipt,
} from '../composables/useGoodsReceipt'

import {
    useNavInputEntry,
} from '../composables/useNavInputEntry'

import {
    angka,
    hariIni,
} from '@/utils/format'

const emit = defineEmits(['tutup'])

const JENIS_KEMASAN = [
    'KARUNG',
    'DRUM',
    'JERIGEN',
    'DUS',
    'SAK',
    'CURAH',
]

const {
    daftarPOSiapTerima,
    sedangProses,
    muatPOSiapTerima,
    simpanPenerimaan,
} = useGoodsReceipt()

const { setNavInfo, resetNav } = useNavInputEntry()

const poIdTerpilih = ref('')

const form = reactive({
    no_surat_jalan: '',
    tanggal: hariIni(),
    catatan: '',
})

const baris = ref([])
const pesanError = ref('')
const hasil = ref(null)

const poTerpilih = computed(() => {
    return daftarPOSiapTerima.value.find(
        (po) => String(po.id) === String(poIdTerpilih.value)
    ) ?? null
})

/* =========================================================
   SUMMARY
========================================================= */

const totalSisa = computed(() => {
    return baris.value.reduce(
        (total, r) => total + Math.max(Number(r.sisa_qty) || 0, 0),
        0
    )
})

const totalDiterima = computed(() => {
    return baris.value.reduce(
        (total, r) => total + Math.max(Number(r.qty_diterima) || 0, 0),
        0
    )
})

const totalDitolak = computed(() => {
    return baris.value.reduce(
        (total, r) => total + Math.max(Number(r.qty_ditolak) || 0, 0),
        0
    )
})

const jumlahItemDiisi = computed(() => {
    return baris.value.filter(
        (r) => Number(r.qty_diterima) > 0
    ).length
})

/* =========================================================
   WATCH PO
========================================================= */

watch(poTerpilih, (po) => {
    pesanError.value = ''

    baris.value = (po?.item ?? []).map((it) => ({
        po_item_id: it.id,
        nama_item: it.nama_item,
        sisa_qty: Number(it.sisa_qty) || 0,

        jenis_kemasan: 'CURAH',
        jumlah_koli: null,
        isi_per_koli: null,

        qty_diterima: null,
        qty_ditolak: 0,
        alasan_tolak: '',
    }))
})

/* =========================================================
   DECLARATION
========================================================= */

const deklarasi = (r) => {
    if (
        r.jenis_kemasan === 'CURAH' ||
        !r.jumlah_koli ||
        !r.isi_per_koli
    ) {
        return null
    }

    const koli = Number(r.jumlah_koli)
    const isi = Number(r.isi_per_koli)

    if (!Number.isFinite(koli) || !Number.isFinite(isi)) {
        return null
    }

    return koli * isi
}

/* =========================================================
   SELISIH
========================================================= */

const selisih = (r) => {
    const d = deklarasi(r)

    if (
        d == null ||
        r.qty_diterima == null ||
        r.qty_diterima === ''
    ) {
        return null
    }

    return Number(r.qty_diterima) - d
}

const persenSelisih = (r) => {
    const d = deklarasi(r)
    const s = selisih(r)

    if (
        d == null ||
        !d ||
        s == null
    ) {
        return null
    }

    return (s / d) * 100
}

const melebihiToleransi = (r) => {
    const p = persenSelisih(r)

    return (
        p != null &&
        Math.abs(p) > 0.5
    )
}

/* =========================================================
   VALIDATION
========================================================= */

const barisMelebihiToleransi = computed(() => {
    return baris.value.filter(melebihiToleransi)
})

const barisLewatSisa = computed(() => {
    return baris.value.filter((r) => {
        const qty = Number(r.qty_diterima)

        return (
            Number.isFinite(qty) &&
            qty > Number(r.sisa_qty)
        )
    })
})

const barisTanpaAlasan = computed(() => {
    return baris.value.filter((r) => {
        const qtyTolak = Number(r.qty_ditolak)

        return (
            qtyTolak > 0 &&
            !String(r.alasan_tolak || '').trim()
        )
    })
})

const statusBaris = (r) => {
    const diterima = Number(r.qty_diterima) || 0
    const ditolak = Number(r.qty_ditolak) || 0

    if (melebihiToleransi(r)) {
        return 'warning'
    }

    if (diterima > 0) {
        return 'complete'
    }

    if (ditolak > 0) {
        return 'warning'
    }

    return 'empty'
}

/* =========================================================
   VALIDATION FORM
========================================================= */

const validasiForm = () => {
    if (!poTerpilih.value) {
        return 'Silakan pilih Purchase Order terlebih dahulu.'
    }

    if (!String(form.no_surat_jalan || '').trim()) {
        return 'Nomor surat jalan wajib diisi.'
    }

    if (!form.tanggal) {
        return 'Tanggal penerimaan wajib diisi.'
    }

    if (!baris.value.length) {
        return 'PO terpilih tidak memiliki item yang dapat diterima.'
    }

    if (barisLewatSisa.value.length > 0) {
        return 'Terdapat Qty Diterima yang melebihi sisa PO.'
    }

    if (barisTanpaAlasan.value.length > 0) {
        return 'Alasan penolakan wajib diisi untuk item yang memiliki Qty Ditolak.'
    }

    const barisKirim = baris.value.filter(
        (r) => Number(r.qty_diterima) > 0
    )

    if (!barisKirim.length) {
        return 'Minimal satu item harus memiliki Qty Diterima lebih dari 0.'
    }

    return ''
}

/* =========================================================
   SUBMIT
========================================================= */

const kirim = async () => {
    if (sedangProses.value) {
        return
    }

    pesanError.value = ''

    const errorValidasi = validasiForm()

    if (errorValidasi) {
        pesanError.value = errorValidasi
        return
    }

    const barisKirim = baris.value
        .filter((r) => Number(r.qty_diterima) > 0)
        .map((r) => ({
            po_item_id: r.po_item_id,
            jenis_kemasan: r.jenis_kemasan,

            jumlah_koli:
                r.jenis_kemasan === 'CURAH'
                    ? null
                    : r.jumlah_koli,

            isi_per_koli:
                r.jenis_kemasan === 'CURAH'
                    ? null
                    : r.isi_per_koli,

            qty_diterima: String(
                Number(r.qty_diterima) || 0
            ),

            qty_ditolak: String(
                Number(r.qty_ditolak) || 0
            ),

            alasan_tolak:
                String(r.alasan_tolak || '').trim(),
        }))

    const res = await simpanPenerimaan({
        po_id: poTerpilih.value.id,

        no_surat_jalan:
            String(form.no_surat_jalan || '').trim(),

        tanggal: form.tanggal,

        dokumen_id: null,

        catatan:
            String(form.catatan || '').trim(),

        baris: barisKirim,
    })

    if (res?.success) {
        hasil.value = res.data
        return
    }

    pesanError.value =
        res?.message ||
        'Penerimaan gagal disimpan. Silakan periksa kembali data Anda.'
}

/* =========================================================
   LIFECYCLE
========================================================= */

onMounted(() => {
    setNavInfo(
        'Penerimaan Barang Baru',
        'Warehouse > Penerimaan > Entry'
    )

    muatPOSiapTerima()
})

onUnmounted(() => {
    resetNav()
})
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.25s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(6px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.slide-fade-enter-active,
.slide-fade-leave-active {
    transition:
        opacity 0.2s ease,
        transform 0.2s ease;
}

.slide-fade-enter-from {
    opacity: 0;
    transform: translateY(-6px);
}

.slide-fade-leave-to {
    opacity: 0;
    transform: translateY(6px);
}

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

input:focus,
select:focus,
textarea:focus,
button:focus {
    outline: none;
}

input::placeholder,
textarea::placeholder {
    color: #94a3b8;
}
</style>