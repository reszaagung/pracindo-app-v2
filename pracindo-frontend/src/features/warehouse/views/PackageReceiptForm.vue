<template>
    <div class="w-full min-w-0 animate-fade-in relative">
        <template v-if="hasil">
            <section class="bg-white border border-emerald-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden">
                <div class="p-5 md:p-7 bg-gradient-to-br from-emerald-50 to-white border-b border-emerald-100">
                    <div class="flex items-start gap-4">
                        <div class="w-12 h-12 shrink-0 rounded-2xl bg-emerald-100 text-emerald-600 border border-emerald-200 flex items-center justify-center">
                            <i class="pi pi-check text-xl"></i>
                        </div>

                        <div class="min-w-0">
                            <span class="inline-flex items-center gap-1.5 px-2 py-1 rounded-md bg-emerald-100 text-emerald-700 border border-emerald-200 text-[10px] font-bold uppercase tracking-wider">
                                <i class="pi pi-check-circle text-[9px]"></i>
                                Berhasil
                            </span>

                            <h1 class="text-xl md:text-2xl font-bold text-slate-900 tracking-tight mt-2">
                                Penerimaan Kemasan Tersimpan
                            </h1>

                            <p class="text-xs md:text-sm text-slate-600 mt-1 leading-relaxed">
                                {{ hasil.pesan || 'Data penerimaan kemasan berhasil disimpan ke sistem.' }}
                            </p>
                        </div>
                    </div>
                </div>

                <div class="p-5 md:p-7 space-y-6">
                    <div class="rounded-2xl bg-slate-50 border border-slate-200 p-4 md:p-5">
                        <div class="flex items-center justify-between gap-4">
                            <div class="min-w-0">
                                <p class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                                    Nomor Dokumen
                                </p>

                                <p class="text-lg md:text-xl font-black text-slate-900 mt-1 break-all">
                                    {{ hasil.penerimaan?.nomor || '-' }}
                                </p>
                            </div>

                            <div class="w-10 h-10 shrink-0 rounded-xl bg-white border border-slate-200 text-slate-500 flex items-center justify-center">
                                <i class="pi pi-file-check"></i>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div class="rounded-2xl bg-emerald-50 border border-emerald-100 p-4">
                            <div class="flex items-center gap-2">
                                <div class="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-600 flex items-center justify-center">
                                    <i class="pi pi-check text-xs"></i>
                                </div>

                                <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-600">
                                    Status
                                </span>
                            </div>

                            <p class="text-sm font-black text-emerald-700 mt-2">
                                Berhasil Disimpan
                            </p>
                        </div>

                        <div class="rounded-2xl bg-blue-50 border border-blue-100 p-4">
                            <div class="flex items-center gap-2">
                                <div class="w-8 h-8 rounded-lg bg-blue-100 text-blue-600 flex items-center justify-center">
                                    <i class="pi pi-file text-xs"></i>
                                </div>

                                <span class="text-[10px] font-bold uppercase tracking-wider text-blue-600">
                                    Dokumen
                                </span>
                            </div>

                            <p class="text-sm font-black text-blue-700 mt-2 break-all">
                                {{ hasil.penerimaan?.nomor || '-' }}
                            </p>
                        </div>
                    </div>

                    <div
                        v-if="hasil.penerimaan?.id"
                        class="rounded-2xl border border-blue-100 bg-blue-50/60 p-4"
                    >
                        <div class="flex items-start gap-3">
                            <div class="w-9 h-9 shrink-0 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center">
                                <i class="pi pi-info-circle text-sm"></i>
                            </div>

                            <div>
                                <p class="text-xs font-bold text-blue-900">
                                    Penerimaan siap diperiksa
                                </p>

                                <p class="text-[11px] text-blue-700 mt-1 leading-relaxed">
                                    Gunakan halaman detail untuk memeriksa transaksi penerimaan dan hasil pencatatannya.
                                </p>
                            </div>
                        </div>
                    </div>

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
                            @click="resetForm"
                            class="h-11 px-5 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-sm font-bold transition-all inline-flex items-center justify-center gap-2"
                        >
                            <i class="pi pi-plus text-xs"></i>
                            Input Penerimaan Lain
                        </button>

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

        <form
            v-else
            @submit.prevent="kirim"
            class="space-y-5 md:space-y-6 pb-24 lg:pb-2"
            novalidate
        >
            <div class="flex items-start gap-3">
                <button
                    type="button"
                    @click="$emit('tutup')"
                    aria-label="Kembali ke daftar penerimaan"
                    class="group w-10 h-10 shrink-0 rounded-xl border border-slate-200 bg-white flex items-center justify-center text-slate-500 hover:text-slate-900 hover:bg-slate-50 hover:border-slate-300 shadow-sm transition-all"
                >
                    <i class="pi pi-arrow-left text-sm group-hover:-translate-x-0.5 transition-transform"></i>
                </button>

                <div class="min-w-0">
                    <div class="flex items-center gap-2 mb-1">
                        <span class="inline-flex items-center gap-1.5 px-2 py-1 rounded-md bg-violet-50 border border-violet-100 text-violet-600 text-[10px] font-bold uppercase tracking-wider">
                            <i class="pi pi-shopping-bag text-[9px]"></i>
                            Kemasan
                        </span>
                    </div>

                    <h1 class="text-xl md:text-2xl font-bold text-slate-900 tracking-tight">
                        Terima Kemasan Baru
                    </h1>

                    <p class="text-xs md:text-sm text-slate-500 mt-1 leading-relaxed">
                        Pilih PO kemasan, masukkan jumlah fisik, lalu periksa kembali hasil penerimaan sebelum disimpan.
                    </p>
                </div>
            </div>

            <section class="bg-white border border-slate-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden">
                <div class="px-4 py-4 md:px-6 md:py-5 border-b border-slate-100 flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-blue-50 border border-blue-100 text-blue-600 flex items-center justify-center shrink-0">
                        <span class="text-xs font-black">01</span>
                    </div>

                    <div>
                        <h2 class="text-sm md:text-base font-bold text-slate-900">
                            Referensi Dokumen
                        </h2>

                        <p class="text-[11px] md:text-xs text-slate-500 mt-0.5">
                            Tentukan PO dan informasi dokumen penerimaan.
                        </p>
                    </div>
                </div>

                <div class="p-4 md:p-6 space-y-5">
                    <div class="space-y-2">
                        <label
                            for="po-kemasan"
                            class="block text-[11px] font-bold text-slate-600 uppercase tracking-wider"
                        >
                            Purchase Order Kemasan
                            <span class="text-rose-500">*</span>
                        </label>

                        <div class="relative">
                            <i class="pi pi-file-edit absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-sm pointer-events-none"></i>

                            <select
                                id="po-kemasan"
                                v-model="poIdTerpilih"
                                :disabled="sedangProses || !daftarPOKemasan.length"
                                required
                                class="w-full h-12 pl-11 pr-11 rounded-xl bg-slate-50 border border-slate-200 text-sm font-semibold text-slate-800 focus:outline-none focus:bg-white focus:border-slate-400 focus:ring-4 focus:ring-slate-100 appearance-none transition-all disabled:opacity-60 disabled:cursor-not-allowed"
                            >
                                <option value="" disabled>
                                    Pilih PO supplier
                                </option>

                                <option
                                    v-for="po in daftarPOKemasan"
                                    :key="po.id"
                                    :value="po.id"
                                >
                                    {{ po.no_po }} • {{ po.suplier_nama }}
                                </option>
                            </select>

                            <i class="pi pi-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 text-xs pointer-events-none"></i>
                        </div>

                        <p
                            v-if="!daftarPOKemasan.length && !sedangProses"
                            class="text-xs text-amber-600 flex items-center gap-1.5"
                        >
                            <i class="pi pi-info-circle"></i>
                            Tidak ada PO kemasan yang siap diterima.
                        </p>
                    </div>

                    <transition name="slide-fade">
                        <div
                            v-if="poTerpilih"
                            class="rounded-2xl border border-violet-100 bg-violet-50/60 overflow-hidden"
                        >
                            <div class="p-4 md:p-5">
                                <div class="flex items-start justify-between gap-4">
                                    <div class="min-w-0">
                                        <p class="text-[10px] font-bold uppercase tracking-wider text-violet-500">
                                            PO Terpilih
                                        </p>

                                        <p class="text-sm md:text-base font-black text-violet-950 mt-1 break-all">
                                            {{ poTerpilih.no_po || '-' }}
                                        </p>

                                        <p class="text-xs text-violet-700 mt-1 break-words">
                                            {{ poTerpilih.suplier_nama || '-' }}
                                        </p>
                                    </div>

                                    <div class="w-10 h-10 shrink-0 rounded-xl bg-white border border-violet-100 text-violet-600 flex items-center justify-center">
                                        <i class="pi pi-check-circle"></i>
                                    </div>
                                </div>

                                <div class="grid grid-cols-2 md:grid-cols-3 gap-2 mt-4">
                                    <div class="rounded-xl bg-white/80 border border-violet-100 p-3">
                                        <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                            Item
                                        </p>

                                        <p class="text-sm font-black text-slate-800 mt-1">
                                            {{ baris.length }}
                                        </p>
                                    </div>

                                    <div class="rounded-xl bg-white/80 border border-violet-100 p-3">
                                        <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                            Sisa PO
                                        </p>

                                        <p class="text-sm font-black text-slate-800 mt-1">
                                            {{ formatAngka(totalSisa) }}
                                        </p>
                                    </div>

                                    <div class="rounded-xl bg-white/80 border border-violet-100 p-3 col-span-2 md:col-span-1">
                                        <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                            Status
                                        </p>

                                        <p class="text-[11px] font-bold text-violet-700 mt-1 inline-flex items-center gap-1.5">
                                            <span class="w-1.5 h-1.5 rounded-full bg-violet-500"></span>
                                            Siap Diproses
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </transition>

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
                                    <i class="pi pi-truck absolute left-0 top-1/2 -translate-y-1/2 text-slate-400 text-xs pointer-events-none"></i>

                                    <input
                                        id="surat-jalan"
                                        v-model="form.no_surat_jalan"
                                        type="text"
                                        maxlength="100"
                                        autocomplete="off"
                                        required
                                        placeholder="Nomor surat jalan supplier"
                                        class="input-underline pl-6"
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
                                    <i class="pi pi-calendar absolute left-0 top-1/2 -translate-y-1/2 text-slate-400 text-xs pointer-events-none"></i>

                                    <input
                                        id="tanggal-terima"
                                        v-model="form.tanggal"
                                        type="date"
                                        required
                                        class="input-underline pl-6"
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
                                    maxlength="500"
                                    rows="3"
                                    placeholder="Catatan tambahan penerimaan kemasan..."
                                    class="input-underline resize-none"
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

            <section
                v-if="poTerpilih"
                class="bg-white border border-slate-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden animate-fade-in"
            >
                <div class="px-4 py-4 md:px-6 md:py-5 border-b border-slate-100">
                    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                        <div class="flex items-center gap-3">
                            <div class="w-9 h-9 rounded-xl bg-slate-100 border border-slate-200 text-slate-700 flex items-center justify-center shrink-0">
                                <span class="text-xs font-black">02</span>
                            </div>

                            <div>
                                <h2 class="text-sm md:text-base font-bold text-slate-900">
                                    Pengecekan Fisik Kemasan
                                </h2>

                                <p class="text-[11px] md:text-xs text-slate-500 mt-0.5">
                                    Gunakan format PACK atau UNIT sesuai cara barang diterima.
                                </p>
                            </div>
                        </div>

                        <div class="grid grid-cols-3 gap-2 md:min-w-[360px]">
                            <div class="rounded-xl bg-slate-50 border border-slate-100 px-3 py-2.5">
                                <p class="text-[9px] uppercase font-bold tracking-wider text-slate-400">
                                    Terima
                                </p>

                                <p class="text-xs md:text-sm font-black text-emerald-600 mt-0.5">
                                    {{ formatAngka(totalDiterima) }}
                                </p>
                            </div>

                            <div class="rounded-xl bg-slate-50 border border-slate-100 px-3 py-2.5">
                                <p class="text-[9px] uppercase font-bold tracking-wider text-slate-400">
                                    Ditolak
                                </p>

                                <p class="text-xs md:text-sm font-black text-rose-600 mt-0.5">
                                    {{ formatAngka(totalDitolak) }}
                                </p>
                            </div>

                            <div class="rounded-xl bg-slate-50 border border-slate-100 px-3 py-2.5">
                                <p class="text-[9px] uppercase font-bold tracking-wider text-slate-400">
                                    Item
                                </p>

                                <p class="text-xs md:text-sm font-black text-slate-800 mt-0.5">
                                    {{ jumlahItemDiisi }}/{{ baris.length }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="p-3 md:p-5">
                    <div class="hidden xl:block overflow-x-auto custom-scrollbar">
                        <table class="w-full min-w-[1150px] text-left border-collapse">
                            <thead>
                                <tr class="bg-slate-50 border border-slate-100">
                                    <th class="px-3 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider w-[19%]">
                                        Nama Kemasan
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right w-[8%]">
                                        Sisa PO
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider w-[13%]">
                                        Format
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider w-[23%]">
                                        Kalkulasi Fisik
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-emerald-600 uppercase tracking-wider text-right w-[12%]">
                                        Total Terima
                                    </th>

                                    <th class="px-2 py-3 text-[10px] font-bold text-rose-500 uppercase tracking-wider text-right w-[10%]">
                                        Ditolak
                                    </th>

                                    <th class="px-3 py-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right w-[15%]">
                                        Selisih
                                    </th>
                                </tr>
                            </thead>

                            <tbody class="divide-y divide-slate-100">
                                <tr
                                    v-for="r in baris"
                                    :key="r.po_item_id"
                                    class="hover:bg-slate-50/60 transition-colors"
                                >
                                    <td class="px-3 py-4 align-top">
                                        <div class="flex items-start gap-2.5">
                                            <div class="w-8 h-8 shrink-0 rounded-lg bg-slate-100 border border-slate-200 text-slate-500 flex items-center justify-center">
                                                <i class="pi pi-box text-[10px]"></i>
                                            </div>

                                            <div class="min-w-0">
                                                <p class="text-xs font-bold text-slate-800 break-words">
                                                    {{ r.nama_item || '-' }}
                                                </p>

                                                <span
                                                    v-if="statusBaris(r) === 'complete'"
                                                    class="inline-flex items-center gap-1 mt-1 px-1.5 py-0.5 rounded-md bg-emerald-50 border border-emerald-100 text-emerald-700 text-[9px] font-bold"
                                                >
                                                    <i class="pi pi-check text-[8px]"></i>
                                                    Terisi
                                                </span>

                                                <span
                                                    v-else-if="statusBaris(r) === 'warning'"
                                                    class="inline-flex items-center gap-1 mt-1 px-1.5 py-0.5 rounded-md bg-amber-50 border border-amber-100 text-amber-700 text-[9px] font-bold"
                                                >
                                                    <i class="pi pi-exclamation-triangle text-[8px]"></i>
                                                    Perhatian
                                                </span>
                                            </div>
                                        </div>
                                    </td>

                                    <td class="px-2 py-4 text-right align-top">
                                        <span class="text-xs font-bold text-slate-600">
                                            {{ formatAngka(r.sisa_qty) }}
                                        </span>
                                    </td>

                                    <td class="px-2 py-4 align-top">
                                        <select
                                            v-model="r.tipe_input"
                                            @change="saatTipeBerubah(r)"
                                            class="w-full h-9 px-2 rounded-lg bg-white border border-slate-200 text-[10px] font-bold text-slate-700 focus:outline-none focus:border-slate-400 focus:ring-2 focus:ring-slate-100"
                                        >
                                            <option value="PACK">
                                                PACK / DUS
                                            </option>

                                            <option value="UNIT">
                                                UNIT / PCS
                                            </option>
                                        </select>
                                    </td>

                                    <td class="px-2 py-4 align-top">
                                        <div
                                            v-if="r.tipe_input === 'PACK'"
                                            class="grid grid-cols-[1fr_auto_1fr] items-start gap-1.5"
                                        >
                                            <div>
                                                <input
                                                    v-model.number="r.jumlah_koli"
                                                    type="number"
                                                    min="0"
                                                    step="1"
                                                    inputmode="numeric"
                                                    placeholder="0"
                                                    @input="hitungOtomatis(r)"
                                                    class="input-underline text-right font-semibold"
                                                />

                                                <span class="text-[8px] text-slate-400 block text-right mt-1">
                                                    Jml Pack
                                                </span>
                                            </div>

                                            <span class="text-slate-300 pt-2.5">
                                                ×
                                            </span>

                                            <div>
                                                <input
                                                    v-model.number="r.isi_per_koli"
                                                    type="number"
                                                    min="0"
                                                    step="1"
                                                    inputmode="numeric"
                                                    placeholder="0"
                                                    @input="hitungOtomatis(r)"
                                                    class="input-underline text-right font-semibold"
                                                />

                                                <span class="text-[8px] text-slate-400 block text-right mt-1">
                                                    Isi / Pack
                                                </span>
                                            </div>
                                        </div>

                                        <div
                                            v-else
                                            class="rounded-lg bg-slate-50 border border-slate-100 px-3 py-2.5"
                                        >
                                            <p class="text-[10px] text-slate-400">
                                                Masukkan jumlah unit secara langsung.
                                            </p>
                                        </div>
                                    </td>

                                    <td class="px-2 py-4 align-top">
                                        <input
                                            v-model.number="r.qty_diterima"
                                            type="number"
                                            min="0"
                                            step="1"
                                            :max="r.sisa_qty"
                                            inputmode="numeric"
                                            placeholder="0"
                                            :readonly="r.tipe_input === 'PACK'"
                                            :class="
                                                r.tipe_input === 'PACK'
                                                    ? 'input-readonly'
                                                    : 'input-emerald'
                                            "
                                            class="input-underline text-right font-black"
                                        />

                                        <span
                                            v-if="r.tipe_input === 'PACK'"
                                            class="text-[9px] text-emerald-600 font-semibold block text-right mt-1"
                                        >
                                            Otomatis
                                        </span>
                                    </td>

                                    <td class="px-2 py-4 align-top">
                                        <input
                                            v-model.number="r.qty_ditolak"
                                            type="number"
                                            min="0"
                                            step="1"
                                            inputmode="numeric"
                                            placeholder="0"
                                            class="input-underline input-rose text-right font-black"
                                        />
                                    </td>

                                    <td class="px-3 py-4 align-top text-right">
                                        <template v-if="selisih(r) !== null">
                                            <div
                                                class="inline-flex flex-col items-end px-2.5 py-1.5 rounded-lg border"
                                                :class="
                                                    selisih(r) > 0
                                                        ? 'bg-rose-50 border-rose-100 text-rose-600'
                                                        : selisih(r) < 0
                                                            ? 'bg-amber-50 border-amber-100 text-amber-700'
                                                            : 'bg-emerald-50 border-emerald-100 text-emerald-700'
                                                "
                                            >
                                                <span class="text-xs font-black">
                                                    {{ formatAngka(selisih(r)) }}
                                                </span>

                                                <span class="text-[9px] font-semibold mt-0.5 opacity-80">
                                                    {{
                                                        selisih(r) > 0
                                                            ? 'Lebih'
                                                            : selisih(r) < 0
                                                                ? 'Kurang'
                                                                : 'Sesuai'
                                                    }}
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
                        </table>
                    </div>

                    <div class="xl:hidden space-y-4">
                        <article
                            v-for="r in baris"
                            :key="'mobile-' + r.po_item_id"
                            class="rounded-2xl border border-slate-200 bg-slate-50/40 overflow-hidden"
                        >
                            <div class="p-4 bg-white border-b border-slate-100">
                                <div class="flex items-start justify-between gap-3">
                                    <div class="flex items-start gap-3 min-w-0">
                                        <div class="w-10 h-10 shrink-0 rounded-xl bg-slate-100 border border-slate-200 text-slate-500 flex items-center justify-center">
                                            <i class="pi pi-box text-sm"></i>
                                        </div>

                                        <div class="min-w-0">
                                            <p class="text-sm font-bold text-slate-900 break-words">
                                                {{ r.nama_item || '-' }}
                                            </p>

                                            <p class="text-[10px] text-slate-400 mt-1">
                                                Sisa PO:
                                                <span class="font-bold text-slate-600">
                                                    {{ formatAngka(r.sisa_qty) }}
                                                </span>
                                            </p>
                                        </div>
                                    </div>

                                    <span
                                        v-if="statusBaris(r) === 'complete'"
                                        class="shrink-0 inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-emerald-50 border border-emerald-100 text-emerald-700 text-[9px] font-bold"
                                    >
                                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                                        Terisi
                                    </span>

                                    <span
                                        v-else-if="statusBaris(r) === 'warning'"
                                        class="shrink-0 inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-amber-50 border border-amber-100 text-amber-700 text-[9px] font-bold"
                                    >
                                        <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                                        Perhatian
                                    </span>
                                </div>
                            </div>

                            <div class="p-4 space-y-4">
                                <div class="space-y-1.5">
                                    <label class="block text-[10px] font-bold uppercase tracking-wider text-slate-500">
                                        Format Input
                                    </label>

                                    <select
                                        v-model="r.tipe_input"
                                        @change="saatTipeBerubah(r)"
                                        class="w-full h-11 px-3 rounded-xl bg-white border border-slate-200 text-sm font-bold text-slate-700 focus:outline-none focus:border-slate-400 focus:ring-4 focus:ring-slate-100"
                                    >
                                        <option value="PACK">
                                            PACK / DUS
                                        </option>

                                        <option value="UNIT">
                                            UNIT / PCS
                                        </option>
                                    </select>
                                </div>

                                <div
                                    v-if="r.tipe_input === 'PACK'"
                                    class="rounded-2xl bg-white border border-slate-200 p-3"
                                >
                                    <p class="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-3">
                                        Kalkulasi Fisik
                                    </p>

                                    <div class="grid grid-cols-[1fr_auto_1fr_auto] items-end gap-2">
                                        <div class="space-y-1.5">
                                            <label class="text-[9px] font-bold text-slate-400">
                                                Jml Pack
                                            </label>

                                            <input
                                                v-model.number="r.jumlah_koli"
                                                type="number"
                                                min="0"
                                                step="1"
                                                inputmode="numeric"
                                                placeholder="0"
                                                @input="hitungOtomatis(r)"
                                                class="input-underline text-right font-bold"
                                            />
                                        </div>

                                        <span class="text-slate-300 pb-3">
                                            ×
                                        </span>

                                        <div class="space-y-1.5">
                                            <label class="text-[9px] font-bold text-slate-400">
                                                Isi / Pack
                                            </label>

                                            <input
                                                v-model.number="r.isi_per_koli"
                                                type="number"
                                                min="0"
                                                step="1"
                                                inputmode="numeric"
                                                placeholder="0"
                                                @input="hitungOtomatis(r)"
                                                class="input-underline text-right font-bold"
                                            />
                                        </div>

                                        <span class="text-slate-300 pb-3">
                                            =
                                        </span>
                                    </div>

                                    <div class="mt-3 rounded-xl bg-emerald-50 border border-emerald-100 p-3 flex items-center justify-between">
                                        <span class="text-[9px] uppercase tracking-wider font-bold text-emerald-600">
                                            Total Terima
                                        </span>

                                        <span class="text-base font-black text-emerald-700">
                                            {{ formatAngka(r.qty_diterima) }}
                                        </span>
                                    </div>
                                </div>

                                <div
                                    v-else
                                    class="space-y-1.5"
                                >
                                    <label class="block text-[10px] font-bold uppercase tracking-wider text-emerald-600">
                                        Total Terima
                                    </label>

                                    <input
                                        v-model.number="r.qty_diterima"
                                        type="number"
                                        min="0"
                                        step="1"
                                        :max="r.sisa_qty"
                                        inputmode="numeric"
                                        placeholder="Masukkan jumlah unit"
                                        class="input-underline input-emerald text-right font-black"
                                    />
                                </div>

                                <div class="grid grid-cols-2 gap-3">
                                    <div class="rounded-xl bg-slate-50 border border-slate-100 p-3">
                                        <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                            Sisa PO
                                        </p>

                                        <p class="text-sm font-black text-slate-700 mt-1">
                                            {{ formatAngka(r.sisa_qty) }}
                                        </p>
                                    </div>

                                    <div class="rounded-xl bg-rose-50 border border-rose-100 p-3">
                                        <p class="text-[9px] font-bold uppercase tracking-wider text-rose-500">
                                            Qty Ditolak
                                        </p>

                                        <input
                                            v-model.number="r.qty_ditolak"
                                            type="number"
                                            min="0"
                                            step="1"
                                            inputmode="numeric"
                                            placeholder="0"
                                            class="input-underline input-rose mt-1 text-right font-black"
                                        />
                                    </div>
                                </div>

                                <div
                                    v-if="selisih(r) !== null"
                                    class="rounded-xl border p-3"
                                    :class="
                                        selisih(r) > 0
                                            ? 'bg-rose-50 border-rose-200'
                                            : selisih(r) < 0
                                                ? 'bg-amber-50 border-amber-200'
                                                : 'bg-emerald-50 border-emerald-100'
                                    "
                                >
                                    <div class="flex items-center justify-between gap-3">
                                        <div>
                                            <p
                                                class="text-[9px] font-bold uppercase tracking-wider"
                                                :class="
                                                    selisih(r) > 0
                                                        ? 'text-rose-500'
                                                        : selisih(r) < 0
                                                            ? 'text-amber-600'
                                                            : 'text-emerald-600'
                                                "
                                            >
                                                Selisih
                                            </p>

                                            <p
                                                class="text-[10px] mt-0.5"
                                                :class="
                                                    selisih(r) > 0
                                                        ? 'text-rose-500'
                                                        : selisih(r) < 0
                                                            ? 'text-amber-600'
                                                            : 'text-emerald-600'
                                                "
                                            >
                                                {{
                                                    selisih(r) > 0
                                                        ? 'Melebihi sisa PO'
                                                        : selisih(r) < 0
                                                            ? 'Kurang dari sisa PO'
                                                            : 'Sesuai sisa PO'
                                                }}
                                            </p>
                                        </div>

                                        <span
                                            class="text-sm font-black"
                                            :class="
                                                selisih(r) > 0
                                                    ? 'text-rose-600'
                                                    : selisih(r) < 0
                                                        ? 'text-amber-700'
                                                        : 'text-emerald-700'
                                            "
                                        >
                                            {{ formatAngka(selisih(r)) }}
                                        </span>
                                    </div>
                                </div>

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
                                            maxlength="300"
                                            rows="3"
                                            required
                                            placeholder="Jelaskan alasan barang ditolak..."
                                            class="input-underline input-rose resize-none"
                                        ></textarea>
                                    </div>
                                </transition>
                            </div>
                        </article>
                    </div>

                    <div class="mt-5 space-y-3">
                        <div
                            v-for="r in barisLewatSisa"
                            :key="'sisa-' + r.po_item_id"
                            class="rounded-xl border border-red-200 bg-red-50 px-3.5 py-3 flex items-start gap-3"
                        >
                            <div class="w-8 h-8 shrink-0 rounded-lg bg-red-100 text-red-600 flex items-center justify-center">
                                <i class="pi pi-times-circle text-xs"></i>
                            </div>

                            <div class="text-xs text-red-800 leading-relaxed">
                                <strong>{{ r.nama_item }}:</strong>
                                Qty diterima melebihi sisa PO.
                                Maksimal:
                                <strong>{{ formatAngka(r.sisa_qty) }}</strong>.
                            </div>
                        </div>

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

                        <div
                            v-if="adaQtyDitolakTanpaTerima"
                            class="rounded-xl border border-amber-200 bg-amber-50 px-3.5 py-3 flex items-start gap-3"
                        >
                            <div class="w-8 h-8 shrink-0 rounded-lg bg-amber-100 text-amber-600 flex items-center justify-center">
                                <i class="pi pi-info-circle text-xs"></i>
                            </div>

                            <div class="text-xs text-amber-800 leading-relaxed">
                                Qty Ditolak harus memiliki Qty Terima pada item yang sama.
                            </div>
                        </div>
                    </div>

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

            <section
                v-if="poTerpilih"
                class="bg-white border border-slate-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden"
            >
                <div class="px-4 py-4 md:px-6 md:py-5 border-b border-slate-100 flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-emerald-50 border border-emerald-100 text-emerald-600 flex items-center justify-center shrink-0">
                        <span class="text-xs font-black">03</span>
                    </div>

                    <div>
                        <h2 class="text-sm md:text-base font-bold text-slate-900">
                            Ringkasan
                        </h2>

                        <p class="text-[11px] md:text-xs text-slate-500 mt-0.5">
                            Pastikan data penerimaan sudah sesuai sebelum disimpan.
                        </p>
                    </div>
                </div>

                <div class="p-4 md:p-6">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                        <div class="rounded-2xl bg-slate-50 border border-slate-100 p-4">
                            <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                Total Sisa PO
                            </p>

                            <p class="text-lg md:text-xl font-black text-slate-900 mt-2">
                                {{ formatAngka(totalSisa) }}
                            </p>
                        </div>

                        <div class="rounded-2xl bg-emerald-50 border border-emerald-100 p-4">
                            <p class="text-[9px] font-bold uppercase tracking-wider text-emerald-600">
                                Total Diterima
                            </p>

                            <p class="text-lg md:text-xl font-black text-emerald-700 mt-2">
                                {{ formatAngka(totalDiterima) }}
                            </p>
                        </div>

                        <div class="rounded-2xl bg-rose-50 border border-rose-100 p-4">
                            <p class="text-[9px] font-bold uppercase tracking-wider text-rose-500">
                                Total Ditolak
                            </p>

                            <p class="text-lg md:text-xl font-black text-rose-600 mt-2">
                                {{ formatAngka(totalDitolak) }}
                            </p>
                        </div>

                        <div
                            class="rounded-2xl border p-4"
                            :class="
                                validForm
                                    ? 'bg-blue-50 border-blue-100'
                                    : 'bg-amber-50 border-amber-200'
                            "
                        >
                            <p
                                class="text-[9px] font-bold uppercase tracking-wider"
                                :class="
                                    validForm
                                        ? 'text-blue-500'
                                        : 'text-amber-600'
                                "
                            >
                                Status
                            </p>

                            <p
                                class="text-sm md:text-base font-black mt-2"
                                :class="
                                    validForm
                                        ? 'text-blue-700'
                                        : 'text-amber-700'
                                "
                            >
                                {{ validForm ? 'Siap Disimpan' : 'Perlu Perbaikan' }}
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            <div
                v-if="poTerpilih"
                class="hidden lg:flex sticky bottom-4 z-20 items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-white/95 backdrop-blur-md p-3.5 shadow-xl shadow-slate-900/10"
            >
                <div class="min-w-0">
                    <p class="text-xs font-bold text-slate-800 truncate">
                        {{ poTerpilih.no_po }}
                    </p>

                    <p class="text-[10px] text-slate-400 mt-0.5">
                        {{ validForm ? 'Data telah memenuhi validasi.' : 'Periksa kembali input sebelum menyimpan.' }}
                    </p>
                </div>

                <div class="flex items-center gap-2 shrink-0">
                    <button
                        type="button"
                        @click="$emit('tutup')"
                        :disabled="sedangProses"
                        class="h-10 px-4 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Batal
                    </button>

                    <button
                        type="submit"
                        :disabled="!validForm || sedangProses"
                        class="h-10 px-5 rounded-xl bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 text-white text-xs font-bold transition-all shadow-sm disabled:cursor-not-allowed inline-flex items-center gap-2"
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

            <div
                v-if="poTerpilih"
                class="lg:hidden fixed bottom-0 left-0 right-0 z-40 px-3 py-3 bg-white/95 backdrop-blur-md border-t border-slate-200 shadow-[0_-8px_24px_rgba(15,23,42,0.08)]"
            >
                <div class="max-w-screen-xl mx-auto flex items-center gap-2">
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
                        :disabled="!validForm || sedangProses"
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
    watch,
    onMounted,
} from 'vue'

import { usePackageReceipt } from '../composables/usePackageReceipt'
import { hariIni, angka } from '@/utils/format'

defineEmits(['tutup'])

const {
    daftarPOKemasan,
    sedangProses,
    muatPOKemasan,
    simpanPenerimaan,
} = usePackageReceipt()

const pesanError = ref('')
const hasil = ref(null)
const poIdTerpilih = ref('')
const baris = ref([])

const form = reactive({
    no_surat_jalan: '',
    tanggal: hariIni(),
    catatan: '',
})

const poTerpilih = computed(() => {
    return daftarPOKemasan.value.find(
        (po) => String(po.id) === String(poIdTerpilih.value)
    ) ?? null
})

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
        const ditolak = Number(r.qty_ditolak) || 0

        return (
            ditolak > 0 &&
            !String(r.alasan_tolak || '').trim()
        )
    })
})

const adaQtyDitolakTanpaTerima = computed(() => {
    return baris.value.some((r) => {
        const diterima = Number(r.qty_diterima) || 0
        const ditolak = Number(r.qty_ditolak) || 0

        return ditolak > 0 && diterima <= 0
    })
})

const validForm = computed(() => {
    if (!poTerpilih.value) {
        return false
    }

    if (!String(form.no_surat_jalan || '').trim()) {
        return false
    }

    if (!form.tanggal) {
        return false
    }

    if (!baris.value.length) {
        return false
    }

    if (!jumlahItemDiisi.value) {
        return false
    }

    if (barisLewatSisa.value.length > 0) {
        return false
    }

    if (barisTanpaAlasan.value.length > 0) {
        return false
    }

    if (adaQtyDitolakTanpaTerima.value) {
        return false
    }

    return true
})

watch(poTerpilih, (po) => {
    pesanError.value = ''

    if (!po) {
        baris.value = []
        return
    }

    baris.value = (po.item || po.items || []).map((it) => ({
        po_item_id: it.id,
        nama_item: it.nama_item || it.nama,
        sisa_qty: Number(it.sisa_qty ?? it.qty ?? 0),
        tipe_input: 'PACK',
        jumlah_koli: null,
        isi_per_koli: null,
        qty_diterima: null,
        qty_ditolak: 0,
        alasan_tolak: '',
    }))
})

const hitungOtomatis = (r) => {
    if (r.tipe_input !== 'PACK') {
        return
    }

    const koli = Math.max(Number(r.jumlah_koli) || 0, 0)
    const isi = Math.max(Number(r.isi_per_koli) || 0, 0)

    r.qty_diterima = koli * isi
}

const saatTipeBerubah = (r) => {
    pesanError.value = ''

    if (r.tipe_input === 'UNIT') {
        r.jumlah_koli = null
        r.isi_per_koli = null
        r.qty_diterima = null
        return
    }

    r.qty_diterima = null
    hitungOtomatis(r)
}

const selisih = (r) => {
    if (
        r.qty_diterima == null ||
        r.qty_diterima === ''
    ) {
        return null
    }

    return Number(r.qty_diterima) - Number(r.sisa_qty)
}

const formatAngka = (num) => {
    if (num == null || num === '') {
        return '-'
    }

    return angka(num)
}

const statusBaris = (r) => {
    const diterima = Number(r.qty_diterima) || 0
    const ditolak = Number(r.qty_ditolak) || 0
    const overSisa = Number(r.qty_diterima) > Number(r.sisa_qty)

    if (
        overSisa ||
        (ditolak > 0 && !String(r.alasan_tolak || '').trim())
    ) {
        return 'warning'
    }

    if (diterima > 0) {
        return 'complete'
    }

    return 'empty'
}

const validasiForm = () => {
    if (!poTerpilih.value) {
        return 'Silakan pilih PO kemasan terlebih dahulu.'
    }

    if (!String(form.no_surat_jalan || '').trim()) {
        return 'Nomor surat jalan wajib diisi.'
    }

    if (!form.tanggal) {
        return 'Tanggal penerimaan wajib diisi.'
    }

    if (!baris.value.length) {
        return 'PO terpilih tidak memiliki item kemasan.'
    }

    if (!jumlahItemDiisi.value) {
        return 'Minimal satu kemasan harus memiliki Qty Terima.'
    }

    if (barisLewatSisa.value.length > 0) {
        return 'Terdapat Qty Terima yang melebihi sisa PO.'
    }

    if (barisTanpaAlasan.value.length > 0) {
        return 'Alasan penolakan wajib diisi untuk item yang memiliki Qty Ditolak.'
    }

    if (adaQtyDitolakTanpaTerima.value) {
        return 'Qty Ditolak tidak dapat diisi jika Qty Terima kosong.'
    }

    return ''
}

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
            jenis_kemasan: r.tipe_input === 'PACK'
                ? 'DUS'
                : 'CURAH',
            jumlah_koli: r.tipe_input === 'PACK'
                ? Number(r.jumlah_koli) || 0
                : null,
            isi_per_koli: r.tipe_input === 'PACK'
                ? Number(r.isi_per_koli) || 0
                : null,
            qty_diterima: String(
                Number(r.qty_diterima) || 0
            ),
            qty_ditolak: String(
                Number(r.qty_ditolak) || 0
            ),
            alasan_tolak: String(
                r.alasan_tolak || ''
            ).trim(),
        }))

    const res = await simpanPenerimaan({
        po_id: poTerpilih.value.id,
        no_surat_jalan: String(
            form.no_surat_jalan || ''
        ).trim(),
        tanggal: form.tanggal,
        catatan: String(
            form.catatan || ''
        ).trim(),
        baris: barisKirim,
    })

    if (res?.success) {
        hasil.value = res.data
        return
    }

    pesanError.value =
        res?.message ||
        'Gagal menyimpan penerimaan kemasan.'
}

const resetForm = async () => {
    poIdTerpilih.value = ''
    baris.value = []
    form.no_surat_jalan = ''
    form.tanggal = hariIni()
    form.catatan = ''
    pesanError.value = ''
    hasil.value = null

    await muatPOKemasan()
}

onMounted(() => {
    muatPOKemasan()
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

.slide-fade-enter-from,
.slide-fade-leave-to {
    opacity: 0;
    transform: translateY(-6px);
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

.input-underline {
    width: 100%;
    height: 2.75rem;
    border: 0;
    border-bottom: 2px solid #cbd5e1;
    border-radius: 0;
    background: transparent;
    padding: 0.5rem 0.25rem;
    color: #334155;
    outline: none;
    box-shadow: none;
    transition:
        border-color 0.2s ease,
        color 0.2s ease,
        background-color 0.2s ease;
}

.input-underline::placeholder {
    color: #94a3b8;
}

.input-underline:focus {
    border-bottom-color: #334155;
    outline: none;
    box-shadow: none;
}

.input-underline:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.input-underline.input-emerald {
    border-bottom-color: #86efac;
    color: #047857;
    background: transparent;
}

.input-underline.input-emerald:focus {
    border-bottom-color: #10b981;
}

.input-underline.input-rose {
    border-bottom-color: #fda4af;
    color: #e11d48;
    background: transparent;
}

.input-underline.input-rose:focus {
    border-bottom-color: #f43f5e;
}

.input-underline.input-readonly {
    border-bottom-color: #cbd5e1;
    background: transparent;
    color: #475569;
    cursor: not-allowed;
}

textarea.input-underline {
    height: auto;
    min-height: 5rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    line-height: 1.5;
}

input:focus,
select:focus,
textarea:focus,
button:focus {
    outline: none;
}
</style>