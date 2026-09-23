<template>
    <div
        class="procurement-create-root flex flex-col w-full animate-fade-in relative p-5 md:p-6 lg:p-8 bg-white/50"
    >
        <div
            class="mb-5 md:mb-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-4 md:gap-0"
        >
            <div>
                <p class="text-[11px] text-slate-400 mb-2">
                    <router-link
                        to="/"
                        class="hover:text-slate-700 transition-colors"
                    >
                        Dashboard
                    </router-link>
                    ›
                    <router-link
                        to="/accounting/input/po"
                        class="hover:text-slate-700 transition-colors"
                    >
                        Input Entry
                    </router-link>
                    › Buat PO
                </p>

                <div class="flex items-center gap-3">
                    <h2
                        class="text-lg md:text-xl font-bold text-slate-800 tracking-tight"
                    >
                        Create Purchase Order
                    </h2>

                    <span
                        class="bg-slate-100 text-slate-600 text-[9px] font-semibold px-2.5 py-1 rounded-md tracking-wide uppercase"
                    >
                        DRAFT
                    </span>
                </div>
            </div>

            <div
                class="relative z-20 flex items-center gap-2 w-full md:w-auto mt-2 md:mt-0"
            >
                <button
                    type="button"
                    @click.stop.prevent="bukaModalProduct"
                    class="relative z-20 flex-1 md:flex-none justify-center px-4 py-2.5 bg-blue-50 hover:bg-blue-100 active:bg-blue-200 border border-blue-200 text-blue-700 text-xs font-semibold rounded-lg transition-all flex items-center gap-2 cursor-pointer select-none"
                >
                    <i class="pi pi-box text-sm"></i>

                    <span class="hidden sm:inline">
                        Produk Baru
                    </span>

                    <span class="sm:hidden">
                        Produk
                    </span>
                </button>

                <button
                    type="button"
                    @click.stop.prevent="bukaModalSupplier"
                    class="relative z-20 flex-1 md:flex-none justify-center px-4 py-2.5 bg-slate-100 hover:bg-slate-200 active:bg-slate-300 border border-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition-all flex items-center gap-2 cursor-pointer select-none"
                >
                    <i class="pi pi-users text-sm"></i>

                    <span class="hidden sm:inline">
                        Supplier Baru
                    </span>

                    <span class="sm:hidden">
                        Supplier
                    </span>
                </button>
            </div>
        </div>

        <div class="mb-6 flex items-center">
            <SelectButton
                v-model="jenisPo"
                :options="opsiJenisPo"
                optionLabel="label"
                optionValue="value"
                :allowEmpty="false"
                class="jenis-po-select bg-slate-50 p-1 rounded-xl border border-slate-200"
            >
                <template #option="slotProps">
                    <div
                        class="flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-colors"
                        :class="
                            jenisPo ===
                            slotProps.option.value
                                ? 'bg-teal-600 text-white shadow-sm'
                                : 'text-slate-500'
                        "
                    >
                        <i
                            class="pi"
                            :class="slotProps.option.icon"
                            style="font-size: 0.7rem"
                        ></i>

                        <span class="text-[11px] font-semibold">
                            {{ slotProps.option.label }}
                        </span>

                        <i
                            v-if="
                                jenisPo ===
                                slotProps.option.value
                            "
                            class="pi pi-check text-[9px]"
                        ></i>
                    </div>
                </template>
            </SelectButton>
        </div>

        <div
            v-if="pesanError"
            class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600 font-medium flex items-start gap-3 shadow-sm"
        >
            <i
                class="pi pi-exclamation-triangle mt-0.5 text-lg"
            ></i>

            <span>
                {{ pesanError }}
            </span>
        </div>

        <form
            @submit.prevent="kirim"
            class="bg-white border border-slate-200 rounded-2xl p-5 md:p-8 shadow-[0_4px_20px_rgba(0,0,0,0.03)] w-full"
        >
            <div
                class="flex flex-col md:flex-row md:items-center justify-between mb-8 border-b border-slate-100 pb-5 gap-4"
            >
                <h3
                    class="text-xs md:text-sm font-semibold text-slate-800 flex items-center gap-2"
                >
                    <i
                        class="pi pi-building text-slate-400"
                    ></i>

                    Entitas Pembeli
                </h3>

                <SelectButton
                    v-model="draf.entitas_id"
                    :options="listEntitas"
                    optionLabel="kode"
                    optionValue="id"
                    :allowEmpty="false"
                    class="entitas-select bg-slate-50 p-1 rounded-xl border border-slate-200"
                >
                    <template #option="slotProps">
                        <div
                            class="flex items-center gap-1.5 px-4 py-1.5 rounded-lg transition-colors"
                            :class="
                                draf.entitas_id ===
                                slotProps.option.id
                                    ? 'bg-teal-600 text-white shadow-sm'
                                    : 'text-slate-500'
                            "
                        >
                            <span
                                class="text-[11px] font-semibold"
                            >
                                {{
                                    slotProps
                                        .option
                                        .kode
                                }}
                            </span>

                            <i
                                v-if="
                                    draf.entitas_id ===
                                    slotProps.option.id
                                "
                                class="pi pi-check text-[9px]"
                            ></i>
                        </div>
                    </template>
                </SelectButton>
            </div>

            <div
                class="grid grid-cols-1 md:grid-cols-[1fr_0.8fr_1.3fr] gap-6 md:gap-8 mb-8"
            >
                <div class="flex flex-col gap-1.5">
                    <label
                        class="text-[10px] font-semibold text-slate-500 uppercase tracking-wider"
                    >
                        No. PO (Preview)
                    </label>

                    <input
                        :value="previewNomor"
                        type="text"
                        readonly
                        class="w-full px-1 py-2 bg-transparent border-b-2 border-slate-200 rounded-none focus:outline-none text-sm text-slate-500 font-semibold cursor-not-allowed"
                    />
                </div>

                <div class="flex flex-col gap-1.5">
                    <label
                        class="text-[10px] font-semibold text-slate-500 uppercase tracking-wider"
                    >
                        Tanggal PO
                    </label>

                    <input
                        v-model="draf.tanggal"
                        type="date"
                        required
                        class="w-full px-1 py-2 bg-transparent border-b-2 border-slate-200 rounded-none focus:outline-none focus:border-teal-500 text-sm text-slate-800 font-medium transition-colors"
                    />
                </div>

                <div class="flex flex-col gap-1.5">
                    <label
                        class="text-[10px] font-semibold text-slate-500 uppercase tracking-wider"
                    >
                        Pilih Supplier
                    </label>

                    <Select
                        v-model="draf.suplier_id"
                        :options="listSupplier"
                        optionLabel="nama"
                        optionValue="id"
                        filter
                        appendTo="body"
                        placeholder="-- Pilih Supplier --"
                        class="w-full"
                        :pt="{
                            root: {
                                class: 'w-full h-[38px] bg-transparent border-b-2 border-slate-200 rounded-none flex items-center hover:border-teal-400 transition-colors'
                            },
                            input: {
                                class: 'text-sm px-2 text-slate-800 font-medium'
                            },
                            trigger: {
                                class: 'w-8 flex items-center justify-center text-slate-400'
                            }
                        }"
                    >
                        <template #empty>
                            <div
                                class="p-2 text-center text-slate-500 text-xs"
                            >
                                Supplier tidak ditemukan.
                            </div>
                        </template>
                    </Select>
                </div>
            </div>

            <div class="w-full mb-8">
                <div
                    class="flex justify-between items-center mb-5 pb-3 mt-8 border-b border-slate-100"
                >
                    <h3
                        class="text-xs md:text-sm font-semibold text-slate-800 flex items-center gap-2"
                    >
                        <i
                            class="pi pi-box"
                            :class="
                                jenisPo === 'BAHAN_BAKU'
                                    ? 'text-teal-500'
                                    : 'text-blue-500'
                            "
                        ></i>

                        Item Pesanan

                        <span class="text-slate-400 font-normal">
                            ({{
                                jenisPo === 'BAHAN_BAKU'
                                    ? 'Bahan'
                                    : 'Kemasan'
                            }})
                        </span>
                    </h3>

                    <button
                        type="button"
                        @click="tambahItem"
                        class="px-4 py-2.5 bg-teal-50 hover:bg-teal-100 active:bg-teal-200 text-teal-700 text-xs font-semibold rounded-lg transition-colors flex items-center gap-2 border border-teal-100 cursor-pointer"
                    >
                        <i class="pi pi-plus"></i>
                        Tambah Item
                    </button>
                </div>

                <div
                    class="hidden md:block w-full overflow-x-auto bg-slate-50/20 border border-slate-200 rounded-xl p-2 shadow-sm custom-scrollbar"
                >
                    <table class="w-full text-left table-fixed">
                        <thead
                            class="border-b-2 border-slate-200"
                        >
                            <tr>
                                <th
                                    style="width: 40%"
                                    class="py-3 px-3 text-[10px] font-semibold text-slate-500 uppercase tracking-wider"
                                >
                                    {{
                                        jenisPo === 'BAHAN_BAKU'
                                            ? 'Bahan Baku'
                                            : 'Kemasan'
                                    }}
                                </th>

                                <th
                                    style="width: 17%"
                                    class="py-3 px-3 text-[10px] font-semibold text-slate-500 uppercase tracking-wider text-right"
                                >
                                    {{
                                        jenisPo === 'BAHAN_BAKU'
                                            ? 'Qty (Kg)'
                                            : 'Qty (Pcs)'
                                    }}
                                </th>

                                <th
                                    style="width: 20%"
                                    class="py-3 px-3 text-[10px] font-semibold text-slate-500 uppercase tracking-wider text-right"
                                >
                                    Harga
                                </th>

                                <th
                                    style="width: 18%"
                                    class="py-3 px-3 text-[10px] font-semibold text-slate-500 uppercase tracking-wider text-right"
                                >
                                    Subtotal
                                </th>

                                <th
                                    style="width: 5%"
                                    class="py-3 px-3"
                                ></th>
                            </tr>
                        </thead>

                        <tbody
                            class="divide-y divide-slate-100 bg-transparent"
                        >
                            <tr
                                v-for="(
                                    item, index
                                ) in draf.items"
                                :key="'d-' + index"
                                class="hover:bg-slate-50/80 transition-colors group"
                            >
                                <td class="py-3 px-3 align-middle">
                                    <Dropdown
                                        v-model="item.produk"
                                        :options="produkBerdasarkanSuplier"
                                        optionLabel="label"
                                        appendTo="body"
                                        :placeholder="
                                            draf.suplier_id
                                                ? 'Pilih produk...'
                                                : 'Pilih supplier'
                                        "
                                        class="w-full"
                                        :disabled="!draf.suplier_id"
                                        filter
                                        :loading="loadingProduk"
                                        :pt="{
                                            root: {
                                                class: 'w-full h-[40px] bg-transparent border-b-2 border-slate-200 rounded-none flex items-center hover:border-teal-400 transition-colors'
                                            },
                                            input: {
                                                class: 'text-sm pl-2 text-slate-800 font-medium'
                                            },
                                            trigger: {
                                                class: 'w-8 flex items-center justify-center text-slate-400'
                                            }
                                        }"
                                    />
                                </td>

                                <td class="py-3 px-3 align-middle">
                                    <input
                                        :value="item.qty"
                                        @input="
                                            item.qty =
                                                angkaInteger(
                                                    $event.target.value
                                                )
                                        "
                                        type="number"
                                        min="0"
                                        step="1"
                                        inputmode="numeric"
                                        required
                                        class="input-angka w-full px-1 py-2 bg-transparent border-b-2 border-slate-200 rounded-none text-sm font-medium text-right text-slate-800 focus:outline-none focus:border-teal-500 transition-colors"
                                        placeholder="0"
                                    />
                                </td>

                                <td class="py-3 px-3 align-middle">
                                    <div class="relative w-full">
                                        <span
                                            class="absolute left-0 top-1/2 -translate-y-1/2 text-slate-400 font-semibold text-sm"
                                        >
                                            Rp
                                        </span>

                                        <input
                                            :value="item.harga_per_kg"
                                            @input="
                                                item.harga_per_kg =
                                                    angkaInteger(
                                                        $event.target.value
                                                    )
                                            "
                                            type="number"
                                            min="0"
                                            step="1"
                                            inputmode="numeric"
                                            class="input-angka w-full pl-7 pr-1 py-2 bg-transparent border-b-2 border-slate-200 rounded-none text-sm font-medium text-right text-slate-800 focus:outline-none focus:border-teal-500 transition-colors"
                                            placeholder="0"
                                        />
                                    </div>
                                </td>

                                <td
                                    class="py-3 px-3 align-middle text-right"
                                >
                                    <span
                                        class="text-sm font-semibold text-slate-800 whitespace-nowrap"
                                    >
                                        Rp
                                        {{
                                            subtotal(item).toLocaleString(
                                                'id-ID'
                                            )
                                        }}
                                    </span>
                                </td>

                                <td
                                    class="py-3 px-3 align-middle text-center"
                                >
                                    <button
                                        type="button"
                                        @click="hapusItem(index)"
                                        :disabled="
                                            draf.items.length === 1
                                        "
                                        class="w-8 h-8 rounded-full text-slate-400 hover:text-red-500 hover:bg-red-50 disabled:opacity-30 disabled:hover:bg-transparent transition-colors flex items-center justify-center mx-auto cursor-pointer disabled:cursor-not-allowed"
                                    >
                                        <i class="pi pi-times"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div
                    class="md:hidden flex flex-col gap-6"
                >
                    <div
                        v-for="(
                            item, index
                        ) in draf.items"
                        :key="'m-' + index"
                        class="p-5 border border-slate-200 bg-white relative flex flex-col gap-4 shadow-sm rounded-xl"
                    >
                        <div
                            class="flex justify-between items-center border-b border-slate-100 pb-2"
                        >
                            <span
                                class="text-[10px] font-semibold text-slate-400 uppercase tracking-wide"
                            >
                                Item #{{ index + 1 }}
                            </span>

                            <button
                                type="button"
                                @click="hapusItem(index)"
                                :disabled="
                                    draf.items.length === 1
                                "
                                class="text-red-500 hover:text-red-700 text-xs font-semibold disabled:opacity-30 flex items-center gap-1 cursor-pointer disabled:cursor-not-allowed"
                            >
                                <i class="pi pi-trash text-xs"></i>
                                Hapus
                            </button>
                        </div>

                        <div class="flex flex-col gap-1">
                            <label
                                class="text-[10px] font-semibold text-slate-500 uppercase tracking-wider"
                            >
                                {{
                                    jenisPo === 'BAHAN_BAKU'
                                        ? 'Bahan Baku'
                                        : 'Kemasan'
                                }}
                            </label>

                            <Dropdown
                                v-model="item.produk"
                                :options="
                                    produkBerdasarkanSuplier
                                "
                                optionLabel="label"
                                appendTo="body"
                                :placeholder="
                                    draf.suplier_id
                                        ? 'Pilih produk...'
                                        : 'Pilih supplier dulu'
                                "
                                class="w-full"
                                :disabled="!draf.suplier_id"
                                filter
                                :loading="loadingProduk"
                                :pt="{
                                    root: {
                                        class: 'w-full h-[40px] bg-transparent border-b-2 border-slate-200 rounded-none flex items-center hover:border-teal-400 transition-colors'
                                    },
                                    input: {
                                        class: 'text-sm pl-1 text-slate-800 font-medium'
                                    },
                                    trigger: {
                                        class: 'w-8 flex items-center justify-center text-slate-400'
                                    }
                                }"
                            />
                        </div>

                        <div class="grid grid-cols-2 gap-6 mt-1">
                            <div class="flex flex-col gap-1">
                                <label
                                    class="text-[10px] font-semibold text-slate-500 uppercase tracking-wider"
                                >
                                    {{
                                        jenisPo === 'BAHAN_BAKU'
                                            ? 'Qty (Kg)'
                                            : 'Qty (Pcs)'
                                    }}
                                </label>

                                <input
                                    :value="item.qty"
                                    @input="
                                        item.qty =
                                            angkaInteger(
                                                $event.target.value
                                            )
                                    "
                                    type="number"
                                    min="0"
                                    step="1"
                                    inputmode="numeric"
                                    required
                                    class="input-angka w-full px-1 py-2 bg-transparent border-b-2 border-slate-200 rounded-none text-sm font-medium text-slate-800 focus:outline-none focus:border-teal-500 transition-colors"
                                    placeholder="0"
                                />
                            </div>

                            <div class="flex flex-col gap-1">
                                <label
                                    class="text-[10px] font-semibold text-slate-500 uppercase tracking-wider"
                                >
                                    Harga Satuan
                                </label>

                                <div class="relative">
                                    <span
                                        class="absolute left-0 top-1/2 -translate-y-1/2 text-slate-400 font-semibold text-sm"
                                    >
                                        Rp
                                    </span>

                                    <input
                                        :value="
                                            item.harga_per_kg
                                        "
                                        @input="
                                            item.harga_per_kg =
                                                angkaInteger(
                                                    $event.target.value
                                                )
                                        "
                                        type="number"
                                        min="0"
                                        step="1"
                                        inputmode="numeric"
                                        class="input-angka w-full pl-6 pr-1 py-2 bg-transparent border-b-2 border-slate-200 rounded-none text-sm font-medium text-right text-slate-800 focus:outline-none focus:border-teal-500 transition-colors"
                                        placeholder="0"
                                    />
                                </div>
                            </div>
                        </div>

                        <div
                            class="flex justify-between items-center pt-3 mt-1"
                        >
                            <span
                                class="text-xs font-semibold text-slate-500 uppercase tracking-wider"
                            >
                                Subtotal
                            </span>

                            <span
                                class="text-sm font-bold text-slate-800"
                            >
                                Rp
                                {{
                                    subtotal(item).toLocaleString(
                                        'id-ID'
                                    )
                                }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <div
                class="flex flex-col md:flex-row justify-between items-start bg-slate-50 p-6 md:p-8 rounded-2xl border border-slate-200 shadow-inner"
            >
                <div
                    class="ppn-toggle-wrapper flex items-center gap-4 bg-white p-4 rounded-xl border border-slate-200 w-full md:w-auto mb-6 md:mb-0 shadow-sm"
                >
                    <ToggleSwitch
                        v-model="isPpnAktif"
                    />

                    <div class="flex flex-col">
                        <label
                            class="text-sm font-semibold cursor-pointer select-none"
                            :class="
                                isPpnAktif
                                    ? 'text-teal-700'
                                    : 'text-slate-600'
                            "
                            @click="
                                isPpnAktif =
                                    !isPpnAktif
                            "
                        >
                            Kenakan PPN 11%
                        </label>

                        <p
                            class="text-[10px] text-slate-500 font-medium mt-1"
                        >
                            <i
                                class="pi pi-info-circle text-[9px] mr-1"
                            ></i>
                            PPN Masukan (Beban Pembeli).
                        </p>
                    </div>
                </div>

                <div
                    class="flex flex-col w-full md:w-80 gap-3 border-t md:border-none border-slate-200 pt-6 md:pt-0"
                >
                    <div
                        class="flex justify-between items-center text-sm px-1"
                    >
                        <span
                            class="font-semibold text-slate-500"
                        >
                            Subtotal
                        </span>

                        <span class="font-bold text-slate-700">
                            Rp
                            {{
                                subtotalSemua.toLocaleString(
                                    'id-ID'
                                )
                            }}
                        </span>
                    </div>

                    <div
                        v-if="draf.ppn_persen > 0"
                        class="flex justify-between items-center text-sm px-1 animate-fade-in"
                    >
                        <span
                            class="font-semibold text-teal-600"
                        >
                            PPN (11%)
                        </span>

                        <span
                            class="font-bold text-teal-700"
                        >
                            Rp
                            {{
                                ppnNominal.toLocaleString(
                                    'id-ID'
                                )
                            }}
                        </span>
                    </div>

                    <div
                        class="flex justify-between items-end mt-3 pb-2 border-b border-slate-200 px-1"
                    >
                        <span
                            class="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-1.5"
                        >
                            Grand Total
                        </span>

                        <span
                            class="text-xl md:text-2xl font-bold text-slate-900 tracking-tight"
                        >
                            Rp
                            {{
                                grandTotal.toLocaleString(
                                    'id-ID'
                                )
                            }}
                        </span>
                    </div>
                </div>
            </div>

            <div
                class="flex flex-col-reverse sm:flex-row justify-end items-stretch sm:items-center gap-3 w-full mt-6 pt-5 border-t border-slate-100"
            >
                <button
                    type="button"
                    @click="$emit('close')"
                    :disabled="sedangProses"
                    class="w-full sm:w-auto px-6 py-3.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-sm font-semibold rounded-xl transition-colors text-center cursor-pointer disabled:cursor-not-allowed disabled:opacity-50"
                >
                    Batal
                </button>

                <button
                    type="submit"
                    :disabled="
                        sedangProses ||
                        periodeDitutup
                    "
                    class="w-full sm:w-auto px-10 py-3.5 bg-teal-600 hover:bg-teal-700 disabled:bg-slate-300 text-white text-sm font-semibold rounded-xl shadow-[0_4px_15px_rgba(13,148,136,0.25)] hover:shadow-[0_6px_20px_rgba(13,148,136,0.4)] transition-all flex items-center justify-center gap-2 cursor-pointer disabled:cursor-not-allowed"
                >
                    <i
                        class="pi text-lg"
                        :class="
                            sedangProses
                                ? 'pi-spin pi-spinner'
                                : 'pi-check-circle'
                        "
                    ></i>

                    {{
                        sedangProses
                            ? 'Menyimpan...'
                            : 'Simpan PO'
                    }}
                </button>
            </div>
        </form>

        <Dialog
            v-model:visible="showModalSupplier"
            modal
            appendTo="body"
            :draggable="false"
            :dismissableMask="true"
            :closable="true"
            :style="{
                width: 'min(92vw, 760px)'
            }"
            :breakpoints="{
                '768px': '94vw'
            }"
            :pt="{
                root: {
                    class: 'rounded-3xl overflow-hidden border border-slate-200 shadow-2xl'
                },
                header: {
                    class: 'bg-white border-b border-slate-100 px-5 py-4'
                },
                content: {
                    class: 'p-0 bg-white'
                }
            }"
        >
            <template #header>
                <div>
                    <div
                        class="text-lg font-black text-slate-900"
                    >
                        Tambah Supplier
                    </div>

                    <div
                        class="mt-1 text-xs text-slate-500"
                    >
                        Tambahkan supplier baru ke master data.
                    </div>
                </div>
            </template>

            <SupplierForm
                @close="showModalSupplier = false"
                @saved="handleSupplierSaved"
            />
        </Dialog>

        <Dialog
            v-model:visible="showModalProduct"
            modal
            appendTo="body"
            :draggable="false"
            :dismissableMask="true"
            :closable="true"
            :style="{
                width: 'min(92vw, 760px)'
            }"
            :breakpoints="{
                '768px': '94vw'
            }"
            :pt="{
                root: {
                    class: 'rounded-3xl overflow-hidden border border-slate-200 shadow-2xl'
                },
                header: {
                    class: 'bg-white border-b border-slate-100 px-5 py-4'
                },
                content: {
                    class: 'p-0 bg-white'
                }
            }"
        >
            <template #header>
                <div>
                    <div
                        class="text-lg font-black text-slate-900"
                    >
                        Tambah Produk
                    </div>

                    <div
                        class="mt-1 text-xs text-slate-500"
                    >
                        Tambahkan produk baru ke master data.
                    </div>
                </div>
            </template>

            <ProductEntry
                @close="showModalProduct = false"
                @saved="handleProductSaved"
            />
        </Dialog>
    </div>
</template>

<script setup>
import {
    computed,
    onMounted,
    reactive,
    ref,
    watch
} from 'vue'

import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import Select from 'primevue/select'
import SelectButton from 'primevue/selectbutton'
import ToggleSwitch from 'primevue/toggleswitch'

import SupplierForm from '@/features/master/views/SupplierForm.vue'
import ProductEntry from '@/features/master/views/ProductEntry.vue'

import {
    usePurchaseOrder
} from '@/features/accounting/composables/usePurchaseOrder'

import api from '@/utils/api'

const emit = defineEmits([
    'close',
    'saved'
])

const {
    listEntitas,
    listSupplier,
    sedangProses,
    pesanError,
    previewNomor,
    periodeDitutup,
    muatDataMaster,
    muatPreviewNomor,
    simpanPO,
    cekStatusPeriode
} = usePurchaseOrder()

const showModalSupplier =
    ref(false)

const showModalProduct =
    ref(false)

const produkBerdasarkanSuplier =
    ref([])

const loadingProduk =
    ref(false)

const jenisPo =
    ref('BAHAN_BAKU')

const opsiJenisPo = [
    {
        label: 'Bahan Baku',
        value: 'BAHAN_BAKU',
        icon: 'pi-box'
    },
    {
        label: 'Kemasan',
        value: 'KEMASAN',
        icon: 'pi-shopping-bag'
    }
]

const isPpnAktif =
    ref(false)

const hariIni = () => {
    const tanggal =
        new Date(
            Date.now() -
                new Date().getTimezoneOffset() *
                    60_000
        )

    return tanggal
        .toISOString()
        .slice(0, 10)
}

const itemKosong = () => ({
    produk: null,
    qty: null,
    harga_per_kg: null
})

const draf = reactive({
    entitas_id: '',
    suplier_id: '',
    tanggal: hariIni(),
    tanggal_kirim_diminta: '',
    catatan: '',
    ppn_persen: 0,
    items: [
        itemKosong()
    ]
})

const angkaInteger = (
    value
) => {
    const hanyaAngka =
        String(
            value ?? ''
        ).replace(
            /\D/g,
            ''
        )

    if (!hanyaAngka) {
        return null
    }

    return Number.parseInt(
        hanyaAngka,
        10
    )
}

const bukaModalSupplier = () => {
    showModalProduct.value = false
    showModalSupplier.value = true
}

const bukaModalProduct = () => {
    showModalSupplier.value = false
    showModalProduct.value = true
}

onMounted(
    async () => {
        await muatDataMaster()

        previewNomor.value =
            'Pilih entitas & tanggal'

        if (
            listEntitas.value.length
        ) {
            draf.entitas_id =
                listEntitas.value[0].id
        }
    }
)

watch(
    isPpnAktif,
    (value) => {
        draf.ppn_persen =
            value ? 11 : 0
    }
)

const handleSupplierSaved =
    async (
        supplierBaru
    ) => {
        showModalSupplier.value =
            false

        await muatDataMaster()

        if (
            supplierBaru?.id
        ) {
            draf.suplier_id =
                supplierBaru.id
        }
    }

const handleProductSaved =
    async (
        produkBaru
    ) => {
        showModalProduct.value =
            false

        if (
            !produkBaru?.id
        ) {
            return
        }

        if (
            !draf.suplier_id
        ) {
            return
        }

        await tarikProdukDariAPI(
            draf.suplier_id
        )

        const produkTerpilih =
            produkBerdasarkanSuplier.value.find(
                (produk) =>
                    String(
                        produk.id
                    ) ===
                    String(
                        produkBaru.id
                    )
            )

        if (
            produkTerpilih
        ) {
            const barisTerakhir =
                draf.items[
                    draf.items.length -
                        1
                ]

            if (
                barisTerakhir &&
                !barisTerakhir.produk
            ) {
                barisTerakhir.produk =
                    produkTerpilih
            }
        }
    }

watch(
    [
        () =>
            draf.entitas_id,
        () =>
            draf.tanggal
    ],
    async (
        [
            entitas,
            tanggal
        ]
    ) => {
        if (
            entitas &&
            tanggal
        ) {
            await Promise.all([
                muatPreviewNomor(
                    entitas,
                    tanggal
                ),
                cekStatusPeriode(
                    entitas,
                    tanggal
                )
            ])

            return
        }

        previewNomor.value =
            'Pilih entitas & tanggal'

        periodeDitutup.value =
            false
    }
)

const tarikProdukDariAPI =
    async (
        idSuplier
    ) => {
        if (
            !idSuplier
        ) {
            produkBerdasarkanSuplier.value =
                []

            return
        }

        loadingProduk.value =
            true

        try {
            const response =
                await api.get(
                    'master/produk/',
                    {
                        params: {
                            suplier:
                                idSuplier,
                            jenis:
                                jenisPo.value,
                            aktif: true,
                            ringkas: 1
                        }
                    }
                )

            const hasil =
                response?.data?.results ||
                response?.data ||
                []

            produkBerdasarkanSuplier.value =
                Array.isArray(
                    hasil
                )
                    ? hasil.map(
                          (
                              produk
                          ) => ({
                              ...produk,
                              label: `${produk.kode} - ${produk.nama}`
                          })
                      )
                    : []
        } catch (err) {
            console.error(
                'Gagal menarik produk:',
                err
            )

            produkBerdasarkanSuplier.value =
                []
        } finally {
            loadingProduk.value =
                false
        }
    }

watch(
    () =>
        jenisPo.value,
    async () => {
        draf.items = [
            itemKosong()
        ]

        if (
            draf.suplier_id
        ) {
            await tarikProdukDariAPI(
                draf.suplier_id
            )
        }
    }
)

watch(
    () =>
        draf.suplier_id,
    async (
        newVal,
        oldVal
    ) => {
        if (
            oldVal &&
            newVal !== oldVal
        ) {
            draf.items = [
                itemKosong()
            ]
        }

        await tarikProdukDariAPI(
            newVal
        )
    },
    {
        immediate: true
    }
)

const subtotal = (
    item
) =>
    (Number(
        item?.qty
    ) || 0) *
    (Number(
        item?.harga_per_kg
    ) || 0)

const subtotalSemua =
    computed(() =>
        draf.items.reduce(
            (
                total,
                item
            ) =>
                total +
                subtotal(
                    item
                ),
            0
        )
    )

const ppnNominal =
    computed(
        () =>
            subtotalSemua.value *
            (
                draf.ppn_persen /
                100
            )
    )

const grandTotal =
    computed(
        () =>
            subtotalSemua.value +
            ppnNominal.value
    )

const tambahItem = () => {
    draf.items.push(
        itemKosong()
    )
}

const hapusItem = (
    index
) => {
    if (
        draf.items.length >
        1
    ) {
        draf.items.splice(
            index,
            1
        )
    }
}

const kirim = async () => {
    if (
        periodeDitutup.value
    ) {
        return
    }

    pesanError.value = ''

    if (
        !draf.entitas_id
    ) {
        pesanError.value =
            'Entitas pembeli wajib dipilih.'

        return
    }

    if (
        !draf.suplier_id
    ) {
        pesanError.value =
            'Supplier wajib dipilih.'

        return
    }

    const itemTidakValid =
        draf.items.some(
            (
                item
            ) =>
                !item
                    ?.produk
                    ?.id ||
                !(
                    Number(
                        item?.qty
                    ) > 0
                )
        )

    if (
        itemTidakValid
    ) {
        pesanError.value =
            'Setiap item membutuhkan produk yang valid dan Qty minimal 1.'

        return
    }

    const payload = {
        entitas_id:
            draf.entitas_id,

        suplier_id:
            draf.suplier_id,

        tanggal:
            draf.tanggal,

        tanggal_kirim_diminta:
            draf.tanggal_kirim_diminta ||
            null,

        catatan:
            draf.catatan,

        pakai_ppn:
            draf.ppn_persen >
            0,

        ppn_persen:
            draf.ppn_persen ||
            0,

        kategori_po:
            jenisPo.value,

        items:
            draf.items.map(
                (
                    item
                ) => {
                    const idSatuan =
                        item
                            ?.produk
                            ?.satuan
                            ?.id ||
                        item
                            ?.produk
                            ?.satuan_id ||
                        item
                            ?.produk
                            ?.satuan

                    return {
                        produk_id:
                            item
                                .produk
                                .id,

                        qty_pesan:
                            Number(
                                item.qty
                            ) ||
                            0,

                        harga_per_kg:
                            Number(
                                item.harga_per_kg
                            ) ||
                            0,

                        satuan:
                            idSatuan
                    }
                }
            )
    }

    const hasil =
        await simpanPO(
            payload,
            true
        )

    if (
        hasil.success
    ) {
        alert(
            'Purchase Order baru berhasil disimpan dan diajukan.'
        )

        emit(
            'saved',
            hasil.data
        )

        return
    }

    pesanError.value =
        hasil.message ||
        'Gagal menyimpan Purchase Order.'

    alert(
        'Gagal menyimpan PO:\n' +
            (
                hasil.message ||
                'Terjadi kesalahan.'
            )
    )
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.procurement-create-root {
    font-family:
        'Inter',
        ui-sans-serif,
        system-ui,
        -apple-system,
        sans-serif;
}

.animate-fade-in {
    animation:
        fadeIn
        0.3s
        ease-out
        forwards;
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

.custom-scrollbar::-webkit-scrollbar {
    height: 6px;
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 6px;
}

.jenis-po-select
    :deep(.p-togglebutton),
.entitas-select
    :deep(.p-togglebutton) {
    background: transparent;
    border: none;
    padding: 0;
    border-radius: 0.5rem;
    overflow: hidden;
}

.input-angka {
    appearance: textfield;
    -moz-appearance: textfield;
}

.input-angka::-webkit-outer-spin-button,
.input-angka::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

.ppn-toggle-wrapper {
    --p-toggleswitch-width: 2.75rem;
    --p-toggleswitch-height: 1.5rem;
    --p-toggleswitch-border-radius: 999px;
    --p-toggleswitch-background: #e2e8f0;
    --p-toggleswitch-hover-background: #cbd5e1;
    --p-toggleswitch-checked-background: #0d9488;
    --p-toggleswitch-checked-hover-background: #0f766e;
    --p-toggleswitch-handle-background: #ffffff;
    --p-toggleswitch-handle-size: 1.1rem;
}

.ppn-toggle-wrapper
    :deep(.p-toggleswitch-input) {
    appearance: none;
    -webkit-appearance: none;
    opacity: 0;
    position: absolute;
    inset: 0;
    margin: 0;
    cursor: pointer;
}

.ppn-toggle-wrapper
    :deep(.p-toggleswitch-slider) {
    border: none;
    outline: none;
}

.ppn-toggle-wrapper
    :deep(.p-toggleswitch-handle) {
    box-shadow:
        0 1px 2px
            rgba(
                0,
                0,
                0,
                0.15
            );
}
</style>