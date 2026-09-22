<template>
    <div class="min-h-full w-full animate-fade-in">

        <!-- =========================================================
             HEADER
        ========================================================== -->
        <div class="mb-6 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
                <div class="mb-2 flex items-center gap-2 text-[11px] font-medium text-slate-400">
                    <span>Inventory</span>
                    <i class="pi pi-angle-right text-[9px]"></i>
                    <span class="font-semibold text-slate-600">Stok Gudang</span>
                </div>

                <div class="flex items-center gap-3">
                    <div
                        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-600 shadow-sm ring-1 ring-emerald-100"
                    >
                        <i class="pi pi-box text-lg"></i>
                    </div>

                    <div>
                        <h1 class="text-2xl font-black tracking-tight text-slate-900 md:text-3xl">
                            Posisi Stok
                        </h1>

                        <p class="mt-1 text-xs text-slate-500 md:text-sm">
                            Pantau posisi persediaan, mutasi entitas, saldo pool, dan stok barang jadi.
                        </p>
                    </div>
                </div>
            </div>

            <!-- STATUS -->
            <div
                class="inline-flex items-center gap-2 self-start rounded-full border border-slate-200 bg-white px-3.5 py-2 text-xs font-semibold text-slate-600 shadow-sm lg:self-auto"
            >
                <span
                    class="h-2 w-2 rounded-full"
                    :class="sedangProses ? 'animate-pulse bg-amber-400' : 'bg-emerald-500'"
                ></span>

                <span>
                    {{ sedangProses ? 'Memuat data' : 'Data terkini' }}
                </span>
            </div>
        </div>


        <!-- =========================================================
             ERROR
        ========================================================== -->
        <Transition name="slide">
            <div
                v-if="galat"
                class="mb-5 flex items-start gap-3 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-4 shadow-sm"
            >
                <div
                    class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white text-rose-500 shadow-sm"
                >
                    <i class="pi pi-exclamation-triangle"></i>
                </div>

                <div class="min-w-0">
                    <div class="text-sm font-bold text-rose-800">
                        Gagal memuat data
                    </div>

                    <div class="mt-0.5 text-xs leading-5 text-rose-600">
                        {{ galat }}
                    </div>
                </div>
            </div>
        </Transition>


        <!-- =========================================================
             MAIN CARD
        ========================================================== -->
        <div
            class="overflow-hidden rounded-[28px] border border-slate-200 bg-white shadow-[0_10px_40px_rgba(15,23,42,0.05)]"
        >

            <!-- TOP BAR -->
            <div
                class="border-b border-slate-100 bg-gradient-to-r from-white via-white to-slate-50/70 px-4 py-5 md:px-6"
            >
                <div class="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">

                    <div>
                        <div class="flex items-center gap-2">
                            <h2 class="text-sm font-black tracking-tight text-slate-800 md:text-base">
                                Daftar Persediaan
                            </h2>

                            <span
                                class="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-500"
                            >
                                {{ labelLapisAktif }}
                            </span>
                        </div>

                        <p class="mt-1 text-xs text-slate-500">
                            Pilih jenis laporan untuk melihat posisi stok yang relevan.
                        </p>
                    </div>


                    <!-- TABS -->
                    <div
                        class="flex w-full gap-1 overflow-x-auto rounded-2xl bg-slate-100/80 p-1.5 custom-scrollbar xl:w-auto"
                    >
                        <button
                            v-for="l in LAPIS"
                            :key="l.nilai"
                            type="button"
                            @click="pilihLapis(l.nilai)"
                            class="group flex min-w-[145px] items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-xs font-bold transition-all duration-200 md:min-w-[155px] md:text-sm"
                            :class="
                                lapis === l.nilai
                                    ? 'bg-white text-emerald-700 shadow-[0_4px_14px_rgba(15,23,42,0.08)] ring-1 ring-slate-200/80'
                                    : 'text-slate-500 hover:bg-white/60 hover:text-slate-700'
                            "
                        >
                            <i
                                class="text-xs transition-transform duration-200 group-hover:scale-110"
                                :class="getTabIcon(l.nilai)"
                            ></i>

                            <span>{{ l.label }}</span>
                        </button>
                    </div>
                </div>
            </div>


            <!-- =====================================================
                 SUMMARY CARDS
            ====================================================== -->
            <div class="grid grid-cols-1 gap-3 border-b border-slate-100 bg-slate-50/50 p-4 sm:grid-cols-2 xl:grid-cols-4 md:p-6">

                <!-- TOTAL -->
                <div
                    class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
                >
                    <div class="flex items-center justify-between gap-3">
                        <div>
                            <div class="text-[10px] font-bold uppercase tracking-[0.14em] text-slate-400">
                                {{ summaryLabel }}
                            </div>

                            <div class="mt-2 text-xl font-black text-slate-900">
                                {{ summaryValue }}
                            </div>
                        </div>

                        <div
                            class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-500"
                        >
                            <i :class="summaryIcon"></i>
                        </div>
                    </div>

                    <div class="mt-3 h-1 overflow-hidden rounded-full bg-slate-100">
                        <div
                            class="h-full rounded-full bg-emerald-500 transition-all duration-700"
                            :style="{ width: sedangProses ? '20%' : '100%' }"
                        ></div>
                    </div>
                </div>


                <!-- SECOND -->
                <div
                    class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
                >
                    <div class="flex items-center justify-between gap-3">
                        <div>
                            <div class="text-[10px] font-bold uppercase tracking-[0.14em] text-slate-400">
                                {{ secondaryLabel }}
                            </div>

                            <div class="mt-2 text-xl font-black text-emerald-600">
                                {{ secondaryValue }}
                            </div>
                        </div>

                        <div
                            class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600"
                        >
                            <i :class="secondaryIcon"></i>
                        </div>
                    </div>

                    <p class="mt-3 text-[11px] text-slate-400">
                        Ringkasan berdasarkan tampilan aktif.
                    </p>
                </div>


                <!-- THIRD -->
                <div
                    class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
                >
                    <div class="flex items-center justify-between gap-3">
                        <div>
                            <div class="text-[10px] font-bold uppercase tracking-[0.14em] text-slate-400">
                                {{ tertiaryLabel }}
                            </div>

                            <div class="mt-2 text-xl font-black text-slate-800">
                                {{ tertiaryValue }}
                            </div>
                        </div>

                        <div
                            class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-600"
                        >
                            <i :class="tertiaryIcon"></i>
                        </div>
                    </div>

                    <p class="mt-3 text-[11px] text-slate-400">
                        Data yang tersedia saat ini.
                    </p>
                </div>


                <!-- FOURTH -->
                <div
                    class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
                >
                    <div class="flex items-center justify-between gap-3">
                        <div>
                            <div class="text-[10px] font-bold uppercase tracking-[0.14em] text-slate-400">
                                {{ fourthLabel }}
                            </div>

                            <div
                                class="mt-2 text-xl font-black"
                                :class="fourthNegative ? 'text-rose-600' : 'text-slate-900'"
                            >
                                {{ fourthValue }}
                            </div>
                        </div>

                        <div
                            class="flex h-10 w-10 items-center justify-center rounded-xl"
                            :class="
                                fourthNegative
                                    ? 'bg-rose-50 text-rose-600'
                                    : 'bg-blue-50 text-blue-600'
                            "
                        >
                            <i :class="fourthIcon"></i>
                        </div>
                    </div>

                    <p class="mt-3 text-[11px] text-slate-400">
                        Nilai atau indikator utama.
                    </p>
                </div>
            </div>


            <!-- =====================================================
                 CONTENT
            ====================================================== -->
            <div class="p-4 md:p-6">

                <!-- LOADING -->
                <div v-if="sedangProses" class="py-10 md:py-16">
                    <div class="mx-auto flex max-w-md flex-col items-center text-center">

                        <div class="relative mb-5">
                            <div
                                class="flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-600"
                            >
                                <i class="pi pi-box text-2xl"></i>
                            </div>

                            <div
                                class="absolute -right-1 -top-1 flex h-6 w-6 items-center justify-center rounded-full border-2 border-white bg-emerald-500 text-white shadow-sm"
                            >
                                <i class="pi pi-spin pi-spinner text-[10px]"></i>
                            </div>
                        </div>

                        <div class="text-sm font-bold text-slate-700">
                            Memuat data persediaan
                        </div>

                        <div class="mt-1 text-xs text-slate-400">
                            Sedang mengambil data terbaru dari server...
                        </div>

                        <div class="mt-5 w-full max-w-xs overflow-hidden rounded-full bg-slate-100">
                            <div class="h-1.5 w-1/3 animate-loading-bar rounded-full bg-emerald-500"></div>
                        </div>
                    </div>
                </div>


                <!-- =================================================
                     ENTITAS
                ================================================== -->
                <div v-else-if="lapis === 'ENTITAS'">

                    <div class="mb-4 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                        <div>
                            <h3 class="text-sm font-black text-slate-800">
                                Rekap Mutasi Entitas
                            </h3>

                            <p class="mt-1 text-xs text-slate-500">
                                Ringkasan setoran, tarikan, kerugian, dan saldo setiap entitas.
                            </p>
                        </div>

                        <div
                            class="inline-flex w-fit items-center gap-2 rounded-xl bg-slate-50 px-3 py-2 text-[11px] font-semibold text-slate-500"
                        >
                            <i class="pi pi-database text-emerald-500"></i>
                            {{ daftarStok.length }} entitas
                        </div>
                    </div>


                    <div
                        v-if="daftarStok.length > 0"
                        class="overflow-hidden rounded-2xl border border-slate-200"
                    >
                        <div class="overflow-x-auto custom-scrollbar">
                            <table class="w-full min-w-[900px] text-left text-sm">
                                <thead class="bg-slate-50">
                                    <tr>
                                        <th class="px-4 py-3.5 text-left text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Entitas
                                        </th>

                                        <th class="px-4 py-3.5 text-right text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Qty Setor
                                        </th>

                                        <th class="px-4 py-3.5 text-right text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Qty Tarik
                                        </th>

                                        <th class="px-4 py-3.5 text-right text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Total Setor
                                        </th>

                                        <th class="px-4 py-3.5 text-right text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Total Tarik
                                        </th>

                                        <th class="px-4 py-3.5 text-right text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Total Rugi
                                        </th>

                                        <th class="px-4 py-3.5 text-right text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Saldo
                                        </th>

                                        <th class="px-4 py-3.5 text-center text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Status
                                        </th>
                                    </tr>
                                </thead>

                                <tbody class="divide-y divide-slate-100 bg-white">
                                    <tr
                                        v-for="s in daftarStok"
                                        :key="s.entitas_id"
                                        class="group transition-colors hover:bg-emerald-50/30"
                                    >
                                        <td class="px-4 py-4">
                                            <div class="flex items-center gap-3">
                                                <div
                                                    class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-xs font-black text-slate-600 group-hover:bg-emerald-100 group-hover:text-emerald-700"
                                                >
                                                    {{ String(s.kode || '-').slice(0, 2) }}
                                                </div>

                                                <div class="min-w-0">
                                                    <div class="truncate font-black uppercase text-slate-800">
                                                        {{ s.kode }}
                                                    </div>

                                                    <div class="mt-0.5 truncate text-[10px] text-slate-500">
                                                        {{ s.nama }}
                                                    </div>
                                                </div>
                                            </div>
                                        </td>

                                        <td class="px-4 py-4 text-right font-bold text-emerald-600">
                                            {{ angka(s.qty_setor, 3) }}
                                        </td>

                                        <td class="px-4 py-4 text-right font-bold text-amber-600">
                                            {{ angka(s.qty_tarik, 3) }}
                                        </td>

                                        <td class="px-4 py-4 text-right text-slate-500">
                                            {{ angka(s.total_setor) }}
                                        </td>

                                        <td class="px-4 py-4 text-right text-slate-500">
                                            {{ angka(s.total_tarik) }}
                                        </td>

                                        <td class="px-4 py-4 text-right font-semibold text-rose-500">
                                            {{ angka(s.total_rugi) }}
                                        </td>

                                        <td class="px-4 py-4 text-right">
                                            <div
                                                class="font-black"
                                                :class="
                                                    s.saldo > 0
                                                        ? 'text-emerald-600'
                                                        : s.saldo < 0
                                                            ? 'text-rose-600'
                                                            : 'text-slate-700'
                                                "
                                            >
                                                {{ angka(s.saldo) }}
                                            </div>
                                        </td>

                                        <td class="px-4 py-4 text-center">
                                            <span
                                                :class="getStatusBadge(s.status)"
                                                class="inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[10px] font-black"
                                            >
                                                <span class="h-1.5 w-1.5 rounded-full bg-current opacity-70"></span>
                                                {{ s.status }}
                                            </span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div
                        v-else
                        class="rounded-2xl border border-dashed border-slate-200 bg-slate-50/50 px-6 py-12 text-center"
                    >
                        <div
                            class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-slate-300 shadow-sm ring-1 ring-slate-200"
                        >
                            <i class="pi pi-building text-xl"></i>
                        </div>

                        <div class="mt-4 text-sm font-bold text-slate-700">
                            Belum ada data entitas
                        </div>

                        <div class="mx-auto mt-1 max-w-sm text-xs leading-5 text-slate-400">
                            Belum terdapat mutasi entitas yang dapat ditampilkan pada laporan ini.
                        </div>
                    </div>
                </div>


                <!-- =================================================
                     POOL
                ================================================== -->
                <div v-else-if="lapis === 'POOL'">

                    <div class="mb-4 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                        <div>
                            <h3 class="text-sm font-black text-slate-800">
                                Saldo Pool
                            </h3>

                            <p class="mt-1 text-xs text-slate-500">
                                Posisi fisik bahan baku yang tersedia di pool.
                            </p>
                        </div>

                        <div
                            class="inline-flex w-fit items-center gap-2 rounded-xl bg-slate-50 px-3 py-2 text-[11px] font-semibold text-slate-500"
                        >
                            <i class="pi pi-box text-blue-500"></i>
                            {{ daftarStok.length }} produk
                        </div>
                    </div>


                    <div
                        v-if="daftarStok.length > 0"
                        class="overflow-hidden rounded-2xl border border-slate-200"
                    >
                        <div class="overflow-x-auto custom-scrollbar">
                            <table class="w-full min-w-[650px] text-left text-sm">
                                <thead class="bg-slate-50">
                                    <tr>
                                        <th class="px-4 py-3.5 text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Produk (Raw)
                                        </th>

                                        <th class="px-4 py-3.5 text-right text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Qty
                                        </th>

                                        <th class="px-4 py-3.5 text-right text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Nilai
                                        </th>

                                        <th class="px-4 py-3.5 text-right text-[10px] font-black uppercase tracking-wider text-slate-500">
                                            Harga Rata / Kg
                                        </th>
                                    </tr>
                                </thead>

                                <tbody class="divide-y divide-slate-100 bg-white">
                                    <tr
                                        v-for="s in daftarStok"
                                        :key="s.produk_id"
                                        class="group transition-colors hover:bg-blue-50/30"
                                    >
                                        <td class="px-4 py-4">
                                            <div class="flex items-center gap-3">
                                                <div
                                                    class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600"
                                                >
                                                    <i class="pi pi-box text-sm"></i>
                                                </div>

                                                <div class="min-w-0">
                                                    <div class="truncate font-black uppercase text-slate-800">
                                                        {{ s.produk_kode }}
                                                    </div>

                                                    <div class="mt-0.5 truncate text-xs text-slate-500">
                                                        {{ s.produk_nama }}
                                                    </div>
                                                </div>
                                            </div>
                                        </td>

                                        <td class="px-4 py-4 text-right">
                                            <span class="text-base font-black text-slate-900">
                                                {{ angka(s.qty_kg, 3) }}
                                            </span>

                                            <span class="ml-1 text-[10px] font-semibold text-slate-400">
                                                Kg
                                            </span>
                                        </td>

                                        <td class="px-4 py-4 text-right font-black text-emerald-600">
                                            {{ angka(s.nilai) }}
                                        </td>

                                        <td class="px-4 py-4 text-right text-slate-500">
                                            {{ angka(s.harga_rata) }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div
                        v-else
                        class="rounded-2xl border border-dashed border-slate-200 bg-slate-50/50 px-6 py-12 text-center"
                    >
                        <div
                            class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-slate-300 shadow-sm ring-1 ring-slate-200"
                        >
                            <i class="pi pi-inbox text-xl"></i>
                        </div>

                        <div class="mt-4 text-sm font-bold text-slate-700">
                            Pool sedang kosong
                        </div>

                        <div class="mx-auto mt-1 max-w-sm text-xs leading-5 text-slate-400">
                            Belum ada saldo bahan baku yang tersedia di pool.
                        </div>
                    </div>
                </div>


                <!-- =================================================
                     BARANG JADI
                ================================================== -->
                <div v-else-if="lapis === 'JADI'">

                    <!-- TOOLBAR -->
                    <div class="mb-5 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">

                        <div>
                            <h3 class="text-sm font-black text-slate-800">
                                Stok Barang Jadi
                            </h3>

                            <p class="mt-1 text-xs text-slate-500">
                                Posisi barang jadi berdasarkan variasi kemasan.
                            </p>
                        </div>

                        <div class="flex w-full items-center gap-2 lg:w-auto">

                            <div
                                class="flex flex-1 items-center rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 shadow-sm transition-all focus-within:border-emerald-300 focus-within:ring-4 focus-within:ring-emerald-500/10 lg:w-[300px] lg:flex-none"
                            >
                                <i class="pi pi-search text-sm text-slate-400"></i>

                                <input
                                    v-model="pencarianBarang"
                                    type="text"
                                    class="min-w-0 flex-1 border-0 bg-transparent px-2.5 text-xs font-medium text-slate-700 outline-none placeholder:text-slate-400 focus:ring-0"
                                    placeholder="Cari nama barang..."
                                    list="saran-barang"
                                />

                                <button
                                    v-if="pencarianBarang"
                                    type="button"
                                    @click="pencarianBarang = ''"
                                    class="flex h-6 w-6 items-center justify-center rounded-lg text-slate-400 transition hover:bg-slate-100 hover:text-slate-600"
                                >
                                    <i class="pi pi-times text-[10px]"></i>
                                </button>

                                <datalist id="saran-barang">
                                    <option
                                        v-for="nama in saranNamaBarang"
                                        :key="nama"
                                        :value="nama"
                                    />
                                </datalist>
                            </div>

                            <div
                                class="hidden shrink-0 rounded-xl bg-slate-100 px-3 py-2.5 text-[11px] font-bold text-slate-500 sm:block"
                            >
                                {{ dataYangDitampilkan.length }} / {{ stokPivot.length }}
                            </div>
                        </div>
                    </div>


                    <!-- LEGEND -->
                    <div class="mb-4 flex flex-wrap items-center gap-2">
                        <span
                            v-for="kemasan in kemasanUnik"
                            :key="`legend-${kemasan}`"
                            class="rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1 text-[10px] font-bold text-slate-500"
                        >
                            {{ kemasan }}
                        </span>
                    </div>


                    <!-- TABLE -->
                    <div
                        v-if="dataYangDitampilkan.length > 0"
                        class="overflow-hidden rounded-2xl border border-slate-200"
                    >
                        <div class="overflow-x-auto custom-scrollbar">
                            <table class="w-full min-w-[900px] border-collapse text-sm">
                                <thead class="bg-slate-50">
                                    <tr>
                                        <th
                                            class="sticky left-0 z-10 w-[260px] bg-slate-50 px-4 py-3.5 text-left text-[10px] font-black uppercase tracking-wider text-slate-500"
                                        >
                                            Nama Barang
                                        </th>

                                        <th
                                            v-for="(kemasan, index) in kemasanUnik"
                                            :key="kemasan"
                                            class="px-4 py-3.5 text-center text-[10px] font-black uppercase tracking-wider text-blue-600"
                                        >
                                            {{ kemasan }}
                                        </th>
                                    </tr>
                                </thead>

                                <tbody class="divide-y divide-slate-100 bg-white">
                                    <tr
                                        v-for="baris in dataYangDitampilkan"
                                        :key="baris.nama"
                                        class="group transition-colors hover:bg-slate-50"
                                    >
                                        <td
                                            class="sticky left-0 z-[1] bg-white px-4 py-4 transition-colors group-hover:bg-slate-50"
                                        >
                                            <div class="flex items-center gap-3">
                                                <div
                                                    class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-500 transition-colors group-hover:bg-emerald-100 group-hover:text-emerald-700"
                                                >
                                                    <i class="pi pi-box text-sm"></i>
                                                </div>

                                                <div class="min-w-0">
                                                    <div class="truncate font-black uppercase text-slate-800">
                                                        {{ baris.nama }}
                                                    </div>
                                                </div>
                                            </div>
                                        </td>

                                        <td
                                            v-for="kemasan in kemasanUnik"
                                            :key="kemasan"
                                            class="px-4 py-4 text-center"
                                        >
                                            <span
                                                class="inline-flex min-w-[72px] items-center justify-center rounded-xl bg-slate-50 px-2.5 py-1.5 text-xs font-bold text-slate-700 ring-1 ring-slate-200/80 transition-all group-hover:bg-white"
                                            >
                                                {{ renderCell(kemasan, baris[kemasan]) }}
                                            </span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>


                    <!-- EMPTY SEARCH -->
                    <div
                        v-else-if="pencarianBarang"
                        class="rounded-2xl border border-dashed border-slate-200 bg-slate-50/50 px-6 py-12 text-center"
                    >
                        <div
                            class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-slate-300 shadow-sm ring-1 ring-slate-200"
                        >
                            <i class="pi pi-search text-xl"></i>
                        </div>

                        <div class="mt-4 text-sm font-bold text-slate-700">
                            Barang tidak ditemukan
                        </div>

                        <div class="mt-1 text-xs text-slate-400">
                            Tidak ada barang yang cocok dengan pencarian
                            <span class="font-semibold text-slate-500">
                                "{{ pencarianBarang }}"
                            </span>.
                        </div>

                        <button
                            type="button"
                            @click="pencarianBarang = ''"
                            class="mt-4 rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-white transition hover:bg-slate-800"
                        >
                            Reset pencarian
                        </button>
                    </div>


                    <!-- EMPTY DATA -->
                    <div
                        v-else
                        class="rounded-2xl border border-dashed border-slate-200 bg-slate-50/50 px-6 py-12 text-center"
                    >
                        <div
                            class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-white text-slate-300 shadow-sm ring-1 ring-slate-200"
                        >
                            <i class="pi pi-inbox text-xl"></i>
                        </div>

                        <div class="mt-4 text-sm font-bold text-slate-700">
                            Belum ada stok barang jadi
                        </div>

                        <div class="mx-auto mt-1 max-w-sm text-xs leading-5 text-slate-400">
                            Belum ada data barang jadi yang dapat ditampilkan.
                        </div>
                    </div>


                    <!-- FOOTER INFO -->
                    <div
                        v-if="stokPivot.length > 10"
                        class="mt-3 flex flex-col gap-1 text-[10px] text-slate-400 sm:flex-row sm:items-center sm:justify-between"
                    >
                        <span>
                            Menampilkan maksimal 10 barang pada tampilan ini.
                        </span>

                        <span v-if="!pencarianBarang">
                            Total {{ stokPivot.length }} barang tersedia.
                        </span>

                        <span v-else>
                            Hasil pencarian untuk
                            <span class="font-semibold text-slate-500">
                                "{{ pencarianBarang }}"
                            </span>
                        </span>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStock } from '../composables/useStock'
import { angka } from '@/utils/format'


const LAPIS = [
    {
        nilai: 'ENTITAS',
        label: 'Mutasi Entitas',
    },
    {
        nilai: 'POOL',
        label: 'Saldo Pool',
    },
    {
        nilai: 'JADI',
        label: 'Barang Jadi',
    },
]


const { daftarStok, sedangProses, galat, muatStok } = useStock()

const lapis = ref('ENTITAS')
const pencarianBarang = ref('')


const STANDAR_KEMASAN = [
    'PCS@1KG',
    'GALON@5KG',
    'DUS@12KG',
    'PAIL@20KG',
    'PAIL@25KG',
    'PAIL@30KG',
]


/* =========================================================
   BASIC HELPERS
========================================================= */

const pilihLapis = (l) => {
    lapis.value = l
    pencarianBarang.value = ''
    muatStok({ lapis: l })
}


const getTabIcon = (nilai) => {
    if (nilai === 'ENTITAS') return 'pi pi-building'
    if (nilai === 'POOL') return 'pi pi-box'
    if (nilai === 'JADI') return 'pi pi-shopping-bag'

    return 'pi pi-circle'
}


const getStatusBadge = (status) => {
    const s = String(status || '').toUpperCase()

    if (s === 'KLAIM') {
        return 'bg-emerald-50 text-emerald-700 border-emerald-200'
    }

    if (s === 'HUTANG') {
        return 'bg-rose-50 text-rose-700 border-rose-200'
    }

    return 'bg-slate-100 text-slate-600 border-slate-200'
}


/* =========================================================
   LABEL TAB
========================================================= */

const labelLapisAktif = computed(() => {
    return (
        LAPIS.find(
            item => item.nilai === lapis.value
        )?.label || '-'
    )
})


/* =========================================================
   SUMMARY CARDS
========================================================= */

const summaryLabel = computed(() => {
    if (lapis.value === 'ENTITAS') {
        return 'Total Entitas'
    }

    if (lapis.value === 'POOL') {
        return 'Total Produk Raw'
    }

    return 'Total Barang'
})


const summaryValue = computed(() => {
    return angka(daftarStok.value?.length || 0)
})


const summaryIcon = computed(() => {
    if (lapis.value === 'ENTITAS') {
        return 'pi pi-building'
    }

    if (lapis.value === 'POOL') {
        return 'pi pi-box'
    }

    return 'pi pi-shopping-bag'
})


const secondaryLabel = computed(() => {
    if (lapis.value === 'ENTITAS') {
        return 'Qty Setor'
    }

    if (lapis.value === 'POOL') {
        return 'Total Qty'
    }

    return 'Total Unit'
})


const secondaryValue = computed(() => {
    if (lapis.value === 'ENTITAS') {
        return angka(
            daftarStok.value.reduce(
                (sum, item) =>
                    sum + Number(item.qty_setor || 0),
                0
            ),
            3
        )
    }

    if (lapis.value === 'POOL') {
        return angka(
            daftarStok.value.reduce(
                (sum, item) =>
                    sum + Number(item.qty_kg || 0),
                0
            ),
            3
        )
    }

    return angka(
        daftarStok.value.reduce(
            (sum, item) =>
                sum + Number(item.qty_unit || 0),
            0
        )
    )
})


const secondaryIcon = computed(() => {
    if (lapis.value === 'ENTITAS') {
        return 'pi pi-arrow-down-left'
    }

    if (lapis.value === 'POOL') {
        return 'pi pi-weight'
    }

    return 'pi pi-box'
})


const tertiaryLabel = computed(() => {
    if (lapis.value === 'ENTITAS') {
        return 'Qty Tarik'
    }

    if (lapis.value === 'POOL') {
        return 'Nilai Pool'
    }

    return 'Jenis Kemasan'
})


const tertiaryValue = computed(() => {
    if (lapis.value === 'ENTITAS') {
        return angka(
            daftarStok.value.reduce(
                (sum, item) =>
                    sum + Number(item.qty_tarik || 0),
                0
            ),
            3
        )
    }

    if (lapis.value === 'POOL') {
        return angka(
            daftarStok.value.reduce(
                (sum, item) =>
                    sum + Number(item.nilai || 0),
                0
            )
        )
    }

    return angka(kemasanUnik.value.length)
})


const tertiaryIcon = computed(() => {
    if (lapis.value === 'ENTITAS') {
        return 'pi pi-arrow-up-right'
    }

    if (lapis.value === 'POOL') {
        return 'pi pi-wallet'
    }

    return 'pi pi-tag'
})


const fourthLabel = computed(() => {
    if (lapis.value === 'ENTITAS') {
        return 'Saldo'
    }

    if (lapis.value === 'POOL') {
        return 'Harga Rata-rata'
    }

    return 'Kemasan Aktif'
})


const fourthValue = computed(() => {
    if (lapis.value === 'ENTITAS') {
        const saldo = daftarStok.value.reduce(
            (sum, item) =>
                sum + Number(item.saldo || 0),
            0
        )

        return angka(saldo)
    }

    if (lapis.value === 'POOL') {
        const qty = daftarStok.value.reduce(
            (sum, item) =>
                sum + Number(item.qty_kg || 0),
            0
        )

        const nilai = daftarStok.value.reduce(
            (sum, item) =>
                sum + Number(item.nilai || 0),
            0
        )

        return qty > 0
            ? angka(nilai / qty)
            : angka(0)
    }

    return angka(kemasanUnik.value.length)
})


const fourthNegative = computed(() => {
    if (lapis.value !== 'ENTITAS') {
        return false
    }

    const saldo = daftarStok.value.reduce(
        (sum, item) =>
            sum + Number(item.saldo || 0),
        0
    )

    return saldo < 0
})


const fourthIcon = computed(() => {
    if (lapis.value === 'ENTITAS') {
        return 'pi pi-wallet'
    }

    if (lapis.value === 'POOL') {
        return 'pi pi-chart-line'
    }

    return 'pi pi-tags'
})


/* =========================================================
   BARANG JADI
========================================================= */

const kemasanUnik = computed(() => {
    if (lapis.value !== 'JADI') {
        return []
    }

    const unik = new Set(STANDAR_KEMASAN)

    daftarStok.value.forEach(item => {
        if (item.kemasan_nama) {
            unik.add(
                String(item.kemasan_nama)
                    .trim()
                    .toUpperCase()
            )
        }
    })

    return Array.from(unik)
})


const stokPivot = computed(() => {
    if (lapis.value !== 'JADI') {
        return []
    }

    const pivotMap = {}
    const headers = kemasanUnik.value

    daftarStok.value.forEach(item => {
        const namaBarang =
            item.item_nama ||
            item.produk_nama ||
            '-'

        const namaKemasan = item.kemasan_nama
            ? String(item.kemasan_nama)
                .trim()
                .toUpperCase()
            : '-'

        if (!pivotMap[namaBarang]) {
            pivotMap[namaBarang] = {
                nama: namaBarang,
            }

            headers.forEach(k => {
                pivotMap[namaBarang][k] = {
                    qty: 0,
                }
            })
        }

        if (
            pivotMap[namaBarang][namaKemasan] !==
            undefined
        ) {
            pivotMap[namaBarang][namaKemasan].qty +=
                Number(item.qty_unit || 0)
        } else {
            pivotMap[namaBarang][namaKemasan] = {
                qty: Number(item.qty_unit || 0),
            }
        }
    })

    return Object.values(pivotMap).sort(
        (a, b) =>
            a.nama.localeCompare(b.nama)
    )
})


const saranNamaBarang = computed(() => {
    return stokPivot.value.map(
        row => row.nama
    )
})


const dataYangDitampilkan = computed(() => {
    let hasil = stokPivot.value

    if (pencarianBarang.value) {
        const keyword =
            pencarianBarang.value
                .toLowerCase()
                .trim()

        hasil = hasil.filter(row =>
            String(row.nama)
                .toLowerCase()
                .includes(keyword)
        )
    }

    return hasil.slice(0, 10)
})


const renderCell = (namaKemasan, cellData) => {
    const qty =
        cellData && cellData.qty
            ? cellData.qty
            : 0

    let satuan = 'unit'

    const str =
        String(namaKemasan)
            .toUpperCase()

    if (
        str.includes('DUS') ||
        str.includes('DS')
    ) {
        satuan = 'dus'
    }

    return `${qty} ${satuan}`
}


/* =========================================================
   INIT
========================================================= */

onMounted(() => {
    muatStok({
        lapis: lapis.value,
    })
})
</script>


<style scoped>
.animate-fade-in {
    animation: fadeIn 0.35s ease-out forwards;
}

.slide-enter-active,
.slide-leave-active {
    transition:
        opacity 0.2s ease,
        transform 0.2s ease;
}

.slide-enter-from,
.slide-leave-to {
    opacity: 0;
    transform: translateY(-6px);
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

.animate-loading-bar {
    animation: loadingBar 1.2s ease-in-out infinite;
}

@keyframes loadingBar {
    0% {
        transform: translateX(-120%);
    }

    50% {
        transform: translateX(120%);
    }

    100% {
        transform: translateX(320%);
    }
}

.custom-scrollbar::-webkit-scrollbar {
    height: 7px;
    width: 7px;
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

input[type="text"]::-webkit-search-cancel-button {
    display: none;
}
</style>