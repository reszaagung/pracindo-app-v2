<template>
  <div
    class="flex flex-col w-full animate-fade-in relative p-4 sm:p-5 md:p-6 lg:p-8 bg-slate-50/30"
  >
    <!-- =====================================================
         HEADER
    ====================================================== -->
    <div
      class="mb-5 md:mb-8 flex flex-col lg:flex-row justify-between items-start lg:items-end gap-4"
    >
      <div class="min-w-0">
        <div
          class="flex flex-wrap items-center gap-2 text-xs text-slate-400 mb-2"
        >
          <router-link
            to="/"
            class="hover:text-slate-700 transition-colors"
          >
            Dashboard
          </router-link>

          <span>›</span>

          <router-link
            to="/accounting/input/so"
            class="hover:text-slate-700 transition-colors"
          >
            Input Entry
          </router-link>

          <span>›</span>

          <span class="text-slate-500">
            Buat SO
          </span>
        </div>

        <div class="flex flex-wrap items-center gap-3">
          <h2
            class="text-xl md:text-2xl font-black text-slate-800 tracking-tight"
          >
            Create Sales Order
          </h2>

          <span
            class="inline-flex items-center bg-blue-100 text-blue-700 text-[10px] font-bold px-2.5 py-1 rounded-md tracking-wide"
          >
            PENJUALAN
          </span>
        </div>

        <p class="text-xs text-slate-500 mt-1">
          Buat pesanan penjualan dan terbitkan SO.
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-2 w-full lg:w-auto">
        <button
          type="button"
          @click="showModalCustomer = true"
          class="w-full lg:w-auto justify-center px-4 py-2.5 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 text-xs font-bold rounded-xl transition-colors flex items-center gap-2 shadow-sm"
        >
          <i class="pi pi-user-plus text-sm"></i>
          Pelanggan Baru
        </button>
      </div>
    </div>

    <!-- =====================================================
         ERROR
    ====================================================== -->
    <Transition name="fade">
      <div
        v-if="pesanError"
        class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600 font-medium flex items-start gap-3 shadow-sm"
      >
        <i
          class="pi pi-exclamation-triangle mt-0.5 text-lg shrink-0"
        ></i>

        <div class="flex-1 min-w-0">
          <p>{{ pesanError }}</p>
        </div>
      </div>
    </Transition>

    <!-- =====================================================
         MAIN FORM
    ====================================================== -->
    <form
      @submit.prevent="kirim"
      class="bg-white border border-slate-200 rounded-2xl md:rounded-[24px] p-4 sm:p-5 md:p-8 shadow-[0_4px_20px_rgba(0,0,0,0.03)] w-full"
    >
      <!-- ===================================================
           ENTITAS PENJUAL
      ==================================================== -->
      <section
        class="mb-8 pb-5 border-b border-slate-100"
      >
        <div
          class="flex flex-col lg:flex-row lg:items-center justify-between gap-4"
        >
          <div>
            <h3
              class="text-sm md:text-base font-bold text-slate-800 flex items-center gap-2"
            >
              <i class="pi pi-building text-slate-400"></i>
              Entitas Penjual
            </h3>

            <p class="text-[11px] text-slate-400 mt-1">
              Tentukan entitas yang menerbitkan Sales Order.
            </p>
          </div>

          <div
            class="w-full lg:w-auto overflow-x-auto pb-1"
          >
            <SelectButton
              v-model="draf.entitas_id"
              :options="listEntitas"
              optionLabel="kode"
              optionValue="id"
              :allowEmpty="false"
              class="min-w-max"
              :disabled="sedangProses"
            >
              <template #option="slotProps">
                <span
                  class="text-xs font-bold px-4 py-1.5 block"
                >
                  {{ slotProps.option.kode }}
                </span>
              </template>
            </SelectButton>
          </div>
        </div>
      </section>

      <!-- ===================================================
           INFORMASI SO
      ==================================================== -->
      <section class="mb-8">
        <div
          class="grid grid-cols-1 md:grid-cols-3 gap-5 md:gap-8"
        >
          <!-- NO SO -->
          <div class="flex flex-col gap-1.5">
            <label
              class="text-[11px] font-bold text-slate-500 uppercase tracking-wider"
            >
              No. SO
            </label>

            <div class="relative">
              <input
                :value="previewNomor"
                type="text"
                readonly
                class="w-full px-1 py-2.5 bg-transparent border-b-2 border-slate-200 rounded-none focus:outline-none text-sm text-slate-500 font-bold cursor-not-allowed"
              />

              <i
                class="pi pi-file-edit absolute right-1 top-1/2 -translate-y-1/2 text-slate-300 text-sm pointer-events-none"
              ></i>
            </div>
          </div>

          <!-- TANGGAL -->
          <div class="flex flex-col gap-1.5">
            <label
              for="so-tanggal"
              class="text-[11px] font-bold text-slate-500 uppercase tracking-wider"
            >
              Tanggal Transaksi
            </label>

            <input
              id="so-tanggal"
              v-model="draf.tanggal"
              type="date"
              required
              :disabled="sedangProses"
              class="w-full px-1 py-2.5 bg-transparent border-b-2 border-slate-200 rounded-none focus:outline-none focus:border-blue-500 text-sm text-slate-800 font-medium transition-colors disabled:opacity-50"
            />
          </div>

          <!-- PELANGGAN -->
          <div class="flex flex-col gap-1.5">
            <label
              for="so-pelanggan"
              class="text-[11px] font-bold text-slate-500 uppercase tracking-wider"
            >
              Pelanggan
            </label>

            <Dropdown
              id="so-pelanggan"
              v-model="draf.pelanggan_id"
              :options="listPelanggan"
              optionLabel="nama"
              optionValue="id"
              placeholder="Pilih pelanggan..."
              filter
              filterPlaceholder="Cari pelanggan..."
              class="w-full"
              :disabled="sedangProses"
            >
              <template #value="slotProps">
                <span
                  v-if="slotProps.value"
                  class="text-sm font-semibold text-slate-800"
                >
                  {{
                    getNamaPelanggan(slotProps.value)
                  }}
                </span>

                <span
                  v-else
                  class="text-sm text-slate-400"
                >
                  {{ slotProps.placeholder }}
                </span>
              </template>

              <template #option="slotProps">
                <div class="flex flex-col py-1">
                  <span
                    class="text-sm font-bold text-slate-700"
                  >
                    {{ slotProps.option.nama }}
                  </span>

                  <span
                    v-if="slotProps.option.kota"
                    class="text-[11px] text-slate-400 mt-0.5"
                  >
                    {{ slotProps.option.kota }}
                  </span>
                </div>
              </template>
            </Dropdown>
          </div>
        </div>
      </section>

      <!-- ===================================================
           RINCIAN PESANAN
      ==================================================== -->
      <section class="w-full mb-8">
        <div
          class="flex flex-col sm:flex-row justify-between sm:items-center gap-3 mb-5 pb-3 mt-2 border-b border-slate-100"
        >
          <div>
            <h3
              class="text-sm md:text-base font-bold text-slate-800 flex items-center gap-2"
            >
              <i class="pi pi-box text-blue-500"></i>
              Rincian Pesanan
            </h3>

            <p class="text-[11px] text-slate-400 mt-1">
              Tambahkan produk, jumlah, dan harga jual.
            </p>
          </div>

          <button
            type="button"
            @click="tambahItem"
            :disabled="sedangProses"
            class="w-full sm:w-auto px-4 py-2.5 bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-bold rounded-xl transition-colors flex items-center justify-center gap-2 border border-blue-100 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <i class="pi pi-plus"></i>
            Tambah Item
          </button>
        </div>

        <!-- =================================================
             DESKTOP TABLE
        ================================================== -->
        <div
          class="hidden md:block w-full overflow-x-auto bg-white border border-slate-200 rounded-xl shadow-sm custom-scrollbar"
        >
          <table class="w-full min-w-[900px] text-left">
            <thead
              class="bg-slate-50 border-b border-slate-200"
            >
              <tr>
                <th
                  class="py-3 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider"
                >
                  Barang
                </th>

                <th
                  class="py-3 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider w-[14%] text-right"
                >
                  Qty
                </th>

                <th
                  class="py-3 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider w-[20%] text-right"
                >
                  Harga Jual
                </th>

                <th
                  class="py-3 px-4 text-[11px] font-bold text-slate-500 uppercase tracking-wider w-[20%] text-right"
                >
                  Subtotal
                </th>

                <th
                  class="py-3 px-4 w-[60px]"
                ></th>
              </tr>
            </thead>

            <tbody
              class="divide-y divide-slate-100"
            >
              <tr
                v-for="(item, index) in draf.items"
                :key="item._key"
                class="hover:bg-slate-50/60 transition-colors"
              >
                <!-- PRODUK -->
                <td class="py-3 px-4 align-middle">
                  <Dropdown
                    v-model="item.produk"
                    :options="produkTersediaUntukRow(item)"
                    optionLabel="nama"
                    placeholder="Pilih produk..."
                    class="w-full"
                    filter
                    filterPlaceholder="Cari produk..."
                    :disabled="sedangProses"
                  >
                    <template #value="slotProps">
                      <div
                        v-if="slotProps.value"
                        class="flex items-center gap-2 min-w-0"
                      >
                        <div class="min-w-0">
                          <span
                            class="block text-sm text-slate-800 font-semibold truncate"
                          >
                            {{ slotProps.value.nama }}
                          </span>

                          <span
                            class="block text-[10px] text-slate-400 mt-0.5"
                          >
                            Stok:
                            {{
                              formatQty(
                                slotProps.value.stok
                              )
                            }}
                            {{
                              slotProps.value.satuan_kode ||
                              ''
                            }}
                          </span>
                        </div>
                      </div>

                      <span
                        v-else
                        class="text-sm text-slate-400"
                      >
                        {{ slotProps.placeholder }}
                      </span>
                    </template>

                    <template #option="slotProps">
                      <div
                        class="flex items-center justify-between gap-4 py-1.5"
                      >
                        <div
                          class="flex flex-col min-w-0"
                        >
                          <span
                            class="text-sm font-bold text-slate-700 truncate"
                          >
                            {{ slotProps.option.nama }}
                          </span>

                          <span
                            class="text-[11px] text-slate-400 mt-0.5"
                          >
                            {{
                              slotProps.option.kode ||
                              '-'
                            }}
                          </span>
                        </div>

                        <span
                          class="text-[11px] font-bold whitespace-nowrap"
                          :class="
                            Number(
                              slotProps.option.stok
                            ) > 0
                              ? 'text-emerald-600'
                              : 'text-red-500'
                          "
                        >
                          Stok:
                          {{
                            formatQty(
                              slotProps.option.stok
                            )
                          }}
                          {{
                            slotProps.option.satuan_kode ||
                            ''
                          }}
                        </span>
                      </div>
                    </template>
                  </Dropdown>
                </td>

                <!-- QTY -->
                <td
                  class="py-3 px-4 align-middle"
                >
                  <div class="relative">
                    <input
                      v-model.number="item.qty"
                      type="number"
                      min="0.01"
                      step="0.01"
                      required
                      :disabled="
                        !item.produk ||
                        sedangProses
                      "
                      :class="[
                        'w-full px-2 py-2 bg-transparent border-b-2 rounded-none text-sm font-semibold text-right focus:outline-none focus:border-blue-500 transition-colors',
                        stokRowError(item)
                          ? 'border-red-400 text-red-600'
                          : 'border-slate-200 text-slate-800'
                      ]"
                      placeholder="0"
                    />

                    <span
                      v-if="stokRowError(item)"
                      class="block mt-1 text-[10px] font-bold text-red-500 text-right"
                    >
                      Stok tidak cukup
                    </span>
                  </div>
                </td>

                <!-- HARGA -->
                <td
                  class="py-3 px-4 align-middle"
                >
                  <div
                    class="relative w-full"
                  >
                    <span
                      class="absolute left-1 top-1/2 -translate-y-1/2 text-slate-400 font-bold text-sm"
                    >
                      Rp
                    </span>

                    <input
                      v-model.number="item.harga_jual"
                      type="number"
                      min="0"
                      step="1"
                      required
                      :disabled="sedangProses"
                      class="w-full pl-7 pr-2 py-2 bg-transparent border-b-2 border-slate-200 rounded-none text-sm font-semibold text-right focus:outline-none focus:border-blue-500 text-slate-800 transition-colors"
                      placeholder="0"
                    />
                  </div>
                </td>

                <!-- SUBTOTAL -->
                <td
                  class="py-3 px-4 align-middle text-right"
                >
                  <span
                    class="text-[14px] font-black text-slate-800"
                  >
                    Rp
                    {{
                      formatRupiah(
                        subtotal(item)
                      )
                    }}
                  </span>
                </td>

                <!-- DELETE -->
                <td
                  class="py-3 px-4 align-middle text-center"
                >
                  <button
                    type="button"
                    @click="hapusItem(index)"
                    :disabled="
                      draf.items.length === 1 ||
                      sedangProses
                    "
                    class="w-8 h-8 rounded-full text-slate-400 hover:text-red-600 hover:bg-red-50 disabled:opacity-30 flex items-center justify-center mx-auto transition-colors"
                    title="Hapus item"
                  >
                    <i class="pi pi-times"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- =================================================
             MOBILE
        ================================================== -->
        <div
          class="md:hidden flex flex-col gap-4"
        >
          <div
            v-for="(item, index) in draf.items"
            :key="item._key"
            class="border border-slate-200 bg-white rounded-xl p-4 shadow-sm"
          >
            <!-- HEADER CARD -->
            <div
              class="flex justify-between items-center border-b border-slate-100 pb-3 mb-4"
            >
              <div class="flex items-center gap-2">
                <span
                  class="w-7 h-7 rounded-full bg-blue-50 text-blue-700 text-xs font-black flex items-center justify-center"
                >
                  {{ index + 1 }}
                </span>

                <span
                  class="text-[10px] font-bold text-slate-400 uppercase tracking-wide"
                >
                  Item Pesanan
                </span>
              </div>

              <button
                type="button"
                @click="hapusItem(index)"
                :disabled="
                  draf.items.length === 1 ||
                  sedangProses
                "
                class="text-red-500 hover:text-red-700 text-xs font-semibold disabled:opacity-30 flex items-center gap-1"
              >
                <i class="pi pi-trash text-xs"></i>
                Hapus
              </button>
            </div>

            <!-- PRODUCT -->
            <div class="flex flex-col gap-1 mb-5">
              <label
                class="text-[11px] font-bold text-slate-500 uppercase tracking-wider"
              >
                Barang
              </label>

              <Dropdown
                v-model="item.produk"
                :options="produkTersediaUntukRow(item)"
                optionLabel="nama"
                placeholder="Pilih produk..."
                class="w-full"
                filter
                filterPlaceholder="Cari produk..."
                :disabled="sedangProses"
              >
                <template #value="slotProps">
                  <div
                    v-if="slotProps.value"
                    class="min-w-0"
                  >
                    <span
                      class="block text-sm font-semibold text-slate-800 truncate"
                    >
                      {{ slotProps.value.nama }}
                    </span>

                    <span
                      class="block text-[10px] text-slate-400 mt-0.5"
                    >
                      Stok:
                      {{
                        formatQty(
                          slotProps.value.stok
                        )
                      }}
                      {{
                        slotProps.value.satuan_kode ||
                        ''
                      }}
                    </span>
                  </div>

                  <span
                    v-else
                    class="text-sm text-slate-400"
                  >
                    {{ slotProps.placeholder }}
                  </span>
                </template>

                <template #option="slotProps">
                  <div class="flex flex-col py-1">
                    <span
                      class="text-sm font-bold text-slate-700"
                    >
                      {{ slotProps.option.nama }}
                    </span>

                    <span
                      class="text-[11px] font-semibold mt-0.5"
                      :class="
                        Number(
                          slotProps.option.stok
                        ) > 0
                          ? 'text-emerald-600'
                          : 'text-red-500'
                      "
                    >
                      Stok:
                      {{
                        formatQty(
                          slotProps.option.stok
                        )
                      }}
                      {{
                        slotProps.option.satuan_kode ||
                        ''
                      }}
                    </span>
                  </div>
                </template>
              </Dropdown>
            </div>

            <!-- QTY + PRICE -->
            <div
              class="grid grid-cols-2 gap-4"
            >
              <!-- QTY -->
              <div>
                <label
                  class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1 block"
                >
                  Qty
                </label>

                <input
                  v-model.number="item.qty"
                  type="number"
                  min="0.01"
                  step="0.01"
                  required
                  :disabled="
                    !item.produk ||
                    sedangProses
                  "
                  :class="[
                    'w-full px-1 py-2 bg-transparent border-b-2 rounded-none text-sm font-semibold focus:outline-none focus:border-blue-500',
                    stokRowError(item)
                      ? 'border-red-400 text-red-600'
                      : 'border-slate-200 text-slate-800'
                  ]"
                  placeholder="0"
                />

                <span
                  v-if="stokRowError(item)"
                  class="block mt-1 text-[10px] font-bold text-red-500"
                >
                  Stok tidak cukup
                </span>
              </div>

              <!-- HARGA -->
              <div>
                <label
                  class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1 block"
                >
                  Harga Jual
                </label>

                <div class="relative">
                  <span
                    class="absolute left-1 top-1/2 -translate-y-1/2 text-slate-400 font-bold text-sm"
                  >
                    Rp
                  </span>

                  <input
                    v-model.number="item.harga_jual"
                    type="number"
                    min="0"
                    step="1"
                    required
                    :disabled="sedangProses"
                    class="w-full pl-6 pr-1 py-2 bg-transparent border-b-2 border-slate-200 rounded-none text-sm font-semibold text-right focus:outline-none focus:border-blue-500 text-slate-800"
                    placeholder="0"
                  />
                </div>
              </div>
            </div>

            <!-- SUBTOTAL -->
            <div
              class="flex justify-between items-center pt-4 mt-4 border-t border-slate-100"
            >
              <span
                class="text-xs font-bold text-slate-500 uppercase tracking-wider"
              >
                Subtotal
              </span>

              <span
                class="text-base font-black text-slate-800"
              >
                Rp
                {{
                  formatRupiah(
                    subtotal(item)
                  )
                }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- ===================================================
           REKAP
      ==================================================== -->
      <section
        class="flex flex-col lg:flex-row justify-between items-stretch bg-slate-50 p-4 sm:p-5 md:p-6 lg:p-8 rounded-2xl border border-slate-200 shadow-inner gap-6"
      >
        <!-- PPN -->
        <div
          class="flex items-center gap-4 bg-white p-4 rounded-xl border border-slate-200 w-full lg:w-auto shadow-sm"
        >
          <ToggleSwitch
            v-model="isPpnAktif"
            :disabled="sedangProses"
          />

          <button
            type="button"
            @click="isPpnAktif = !isPpnAktif"
            :disabled="sedangProses"
            class="text-left disabled:cursor-not-allowed"
          >
            <span
              class="text-sm font-bold block"
              :class="
                isPpnAktif
                  ? 'text-blue-700'
                  : 'text-slate-600'
              "
            >
              Kenakan PPN
              {{ draf.ppn_persen }}%
              (Keluaran)
            </span>

            <span
              class="text-[10px] text-slate-500 font-medium mt-1 block"
            >
              <i
                class="pi pi-info-circle text-[9px] mr-1"
              ></i>
              Opsional untuk transaksi kena pajak.
            </span>
          </button>
        </div>

        <!-- TOTAL -->
        <div
          class="flex flex-col w-full lg:w-[380px] gap-3 border-t lg:border-t-0 border-slate-200 pt-5 lg:pt-0"
        >
          <div
            class="flex justify-between items-center text-sm px-1"
          >
            <span class="font-bold text-slate-500">
              Subtotal
            </span>

            <span
              class="font-black text-slate-700"
            >
              Rp
              {{
                formatRupiah(
                  subtotalSemua
                )
              }}
            </span>
          </div>

          <div
            v-if="draf.ppn_persen > 0"
            class="flex justify-between items-center text-sm px-1"
          >
            <span
              class="font-bold text-blue-600"
            >
              PPN
              {{ draf.ppn_persen }}%
            </span>

            <span
              class="font-black text-blue-700"
            >
              Rp
              {{
                formatRupiah(
                  ppnNominal
                )
              }}
            </span>
          </div>

          <div
            class="flex justify-between items-end mt-2 pt-4 border-t border-slate-200 px-1"
          >
            <div>
              <span
                class="text-[10px] font-bold text-slate-400 uppercase tracking-widest block"
              >
                Total Tagihan
              </span>

              <span
                class="text-[10px] text-slate-400 mt-1 block"
              >
                {{ draf.items.length }}
                item pesanan
              </span>
            </div>

            <span
              class="text-2xl md:text-3xl font-black text-slate-900 tracking-tight text-right"
            >
              Rp
              {{
                formatRupiah(
                  grandTotal
                )
              }}
            </span>
          </div>
        </div>
      </section>

      <!-- ===================================================
           ACTION
      ==================================================== -->
      <div
        class="flex flex-col-reverse sm:flex-row justify-end items-stretch sm:items-center gap-3 w-full mt-6 pt-5 border-t border-slate-100"
      >
        <button
          type="button"
          @click="$emit('close')"
          :disabled="sedangProses"
          class="w-full sm:w-auto px-6 py-3.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-sm font-bold rounded-xl transition-colors text-center disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Batal
        </button>

        <button
          type="submit"
          :disabled="
            sedangProses ||
            periodeDitutup ||
            hasErrorStok ||
            !formSiap
          "
          class="w-full sm:w-auto px-10 py-3.5 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white text-sm font-bold rounded-xl shadow-[0_4px_15px_rgba(37,99,235,0.25)] hover:shadow-[0_6px_20px_rgba(37,99,235,0.4)] transition-all flex items-center justify-center gap-2 cursor-pointer disabled:cursor-not-allowed"
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
              ? 'Menyimpan SO...'
              : 'Simpan & Terbitkan'
          }}
        </button>
      </div>
    </form>

    <!-- =====================================================
         CUSTOMER MODAL
    ====================================================== -->
    <Teleport to="body">
      <CustomerForm
        v-if="showModalCustomer"
        @close="showModalCustomer = false"
        @saved="handleCustomerSaved"
      />
    </Teleport>
  </div>
</template>

<script setup>
import {
  reactive,
  computed,
  ref,
  watch,
  onMounted
} from 'vue'

import Dropdown from 'primevue/dropdown'
import SelectButton from 'primevue/selectbutton'
import ToggleSwitch from 'primevue/toggleswitch'

import CustomerForm from './CustomerForm.vue'

import {
  useSalesOrder
} from '@/features/accounting/composables/useSalesOrder'

// =========================================================
// EMITS
// =========================================================

const emit = defineEmits([
  'close',
  'saved'
])

// =========================================================
// SALES ORDER COMPOSABLE
// =========================================================

const {
  listEntitas,
  listPelanggan,
  listProduk,

  sedangProses,
  pesanError,
  previewNomor,

  periodeDitutup,

  muatDataMaster,
  muatPreviewNomor,
  simpanSO,
  muatStokEntitas
} = useSalesOrder()

// =========================================================
// STATE
// =========================================================

const showModalCustomer =
  ref(false)

const isPpnAktif =
  ref(false)

let itemSequence = 0

// =========================================================
// DATE
// =========================================================

function hariIni() {
  const tanggalLocal =
    new Date(
      Date.now() -
        new Date().getTimezoneOffset() *
          60_000
    )

  return tanggalLocal
    .toISOString()
    .slice(0, 10)
}

// =========================================================
// ITEM
// =========================================================

function itemKosong() {
  itemSequence += 1

  return {
    _key: `so-item-${itemSequence}`,

    produk: null,

    qty: null,

    harga_jual: null
  }
}

// =========================================================
// DRAFT
// =========================================================

const draf = reactive({
  entitas_id: '',
  pelanggan_id: '',
  tanggal: hariIni(),
  catatan: '',
  ppn_persen: 0,

  items: [
    itemKosong()
  ]
})

// =========================================================
// INIT
// =========================================================

onMounted(
  async () => {
    try {
      await muatDataMaster()

      previewNomor.value =
        'Pilih entitas & tanggal'

      if (
        listEntitas.value.length > 0
      ) {
        draf.entitas_id =
          listEntitas.value[0].id
      }
    } catch (error) {
      console.error(
        'Init Sales Order:',
        error
      )
    }
  }
)

// =========================================================
// PPN
// =========================================================

watch(
  isPpnAktif,
  (aktif) => {
    draf.ppn_persen =
      aktif
        ? 11
        : 0
  },
  {
    immediate: true
  }
)

// =========================================================
// PREVIEW NOMOR
// =========================================================

watch(
  [
    () => draf.entitas_id,
    () => draf.tanggal
  ],
  async (
    [entitas, tanggal]
  ) => {
    if (
      entitas &&
      tanggal
    ) {
      await muatPreviewNomor(
        entitas,
        tanggal
      )
    } else {
      previewNomor.value =
        'Pilih entitas & tanggal'
    }
  }
)

// =========================================================
// GANTI ENTITAS
// =========================================================

watch(
  () => draf.entitas_id,
  async (
    entitasBaru,
    entitasLama
  ) => {
    if (
      !entitasBaru ||
      entitasBaru ===
        entitasLama
    ) {
      return
    }

    try {
      await muatStokEntitas(
        entitasBaru
      )

      /*
       * Stok berbeda antar entitas.
       * Karena itu produk draft lama harus dibersihkan.
       */
      draf.items = [
        itemKosong()
      ]
    } catch (error) {
      console.error(
        'Ganti entitas:',
        error
      )
    }
  }
)

// =========================================================
// CUSTOMER SAVED
// =========================================================

async function handleCustomerSaved() {
  showModalCustomer.value =
    false

  await muatDataMaster()
}

// =========================================================
// CUSTOMER LABEL
// =========================================================

function getNamaPelanggan(id) {
  const pelanggan =
    listPelanggan.value.find(
      (item) =>
        String(item.id) ===
        String(id)
    )

  if (!pelanggan) {
    return ''
  }

  return pelanggan.kota
    ? `${pelanggan.nama} — ${pelanggan.kota}`
    : pelanggan.nama
}

// =========================================================
// FORMAT QTY
// =========================================================

function formatQty(value) {
  return Number(
    value || 0
  ).toLocaleString(
    'id-ID',
    {
      maximumFractionDigits: 2
    }
  )
}

// =========================================================
// FORMAT RUPIAH
// =========================================================

function formatRupiah(value) {
  return Number(
    value || 0
  ).toLocaleString(
    'id-ID',
    {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }
  )
}

// =========================================================
// SUBTOTAL
// =========================================================

function subtotal(item) {
  return (
    Number(item.qty) || 0
  ) *
  (
    Number(
      item.harga_jual
    ) || 0
  )
}

const subtotalSemua =
  computed(() =>
    draf.items.reduce(
      (
        total,
        item
      ) =>
        total +
        subtotal(item),
      0
    )
  )

const ppnNominal =
  computed(
    () =>
      subtotalSemua.value *
      (
        Number(
          draf.ppn_persen
        ) || 0
      ) /
      100
  )

const grandTotal =
  computed(
    () =>
      subtotalSemua.value +
      ppnNominal.value
  )

// =========================================================
// TOTAL QTY PRODUK
//
// Penting untuk validasi produk duplikat.
// =========================================================

function totalQtyProduk(
  produkId
) {
  return draf.items.reduce(
    (
      total,
      item
    ) => {
      if (
        item.produk &&
        String(
          item.produk.id
        ) ===
          String(
            produkId
          )
      ) {
        return (
          total +
          (
            Number(
              item.qty
            ) || 0
          )
        )
      }

      return total
    },
    0
  )
}

// =========================================================
// STOK ERROR PER ROW
// =========================================================

function stokRowError(item) {
  if (!item.produk) {
    return false
  }

  const stok =
    Number(
      item.produk.stok
    ) || 0

  const totalQty =
    totalQtyProduk(
      item.produk.id
    )

  return (
    totalQty >
    stok
  )
}

// =========================================================
// GLOBAL STOCK ERROR
// =========================================================

const hasErrorStok =
  computed(() =>
    draf.items.some(
      (item) =>
        stokRowError(item)
    )
  )

// =========================================================
// PRODUK YANG BOLEH DIPILIH
//
// Produk yang sudah dipakai di row lain dibuat disabled
// supaya satu produk tidak masuk beberapa row.
// =========================================================

function produkTersediaUntukRow(
  currentRow
) {
  return listProduk.value.map(
    (produk) => {
      const dipakaiDiRowLain =
        draf.items.some(
          (item) =>
            item._key !==
              currentRow._key &&
            item.produk &&
            String(
              item.produk.id
            ) ===
              String(
                produk.id
              )
        )

      return {
        ...produk,
        disabled:
          dipakaiDiRowLain
      }
    }
  )
}

// =========================================================
// FORM READY
// =========================================================

const formSiap =
  computed(() => {
    if (
      !draf.entitas_id ||
      !draf.pelanggan_id ||
      !draf.tanggal
    ) {
      return false
    }

    if (
      !draf.items.length
    ) {
      return false
    }

    return draf.items.every(
      (item) =>
        item.produk?.id &&
        Number(item.qty) > 0 &&
        Number(
          item.harga_jual
        ) >= 0
    )
  })

// =========================================================
// TAMBAH ITEM
// =========================================================

function tambahItem() {
  draf.items.push(
    itemKosong()
  )
}

// =========================================================
// HAPUS ITEM
// =========================================================

function hapusItem(index) {
  if (
    draf.items.length <= 1
  ) {
    return
  }

  draf.items.splice(
    index,
    1
  )
}

// =========================================================
// SUBMIT
// =========================================================

async function kirim() {
  pesanError.value = ''

  // -------------------------------------------------------
  // BASIC
  // -------------------------------------------------------

  if (!draf.entitas_id) {
    pesanError.value =
      'Entitas penjual wajib dipilih.'
    return
  }

  if (!draf.pelanggan_id) {
    pesanError.value =
      'Pelanggan wajib dipilih.'
    return
  }

  if (!draf.tanggal) {
    pesanError.value =
      'Tanggal transaksi wajib diisi.'
    return
  }

  // -------------------------------------------------------
  // ITEM
  // -------------------------------------------------------

  const itemTidakValid =
    draf.items.some(
      (item) =>
        !item.produk?.id ||
        !(
          Number(
            item.qty
          ) > 0
        ) ||
        !(
          Number(
            item.harga_jual
          ) >= 0
        )
    )

  if (itemTidakValid) {
    pesanError.value =
      'Setiap item harus memiliki produk, Qty lebih dari 0, dan harga jual yang valid.'
    return
  }

  // -------------------------------------------------------
  // DUPLIKAT PRODUK
  // -------------------------------------------------------

  const produkIds =
    draf.items
      .map(
        (item) =>
          item.produk?.id
      )
      .filter(Boolean)

  const uniqueProdukIds =
    new Set(
      produkIds.map(
        (id) =>
          String(id)
      )
    )

  if (
    uniqueProdukIds.size !==
    produkIds.length
  ) {
    pesanError.value =
      'Produk yang sama tidak boleh dimasukkan pada lebih dari satu baris.'
    return
  }

  // -------------------------------------------------------
  // STOK
  // -------------------------------------------------------

  if (
    hasErrorStok.value
  ) {
    pesanError.value =
      'Terdapat produk dengan jumlah pesanan melebihi ketersediaan stok.'
    return
  }

  // -------------------------------------------------------
  // PERIODE
  // -------------------------------------------------------

  if (
    periodeDitutup
  ) {
    pesanError.value =
      'Periode transaksi sedang ditutup.'
    return
  }

  // -------------------------------------------------------
  // PAYLOAD
  // -------------------------------------------------------

  const payload = {
    entitas:
      draf.entitas_id,

    pelanggan:
      draf.pelanggan_id,

    tanggal:
      draf.tanggal,

    catatan:
      draf.catatan,

    ppn_persen:
      Number(
        draf.ppn_persen
      ) || 0,

    items:
      draf.items.map(
        (item) => ({
          produk:
            item.produk.id,

          qty:
            Number(
              item.qty
            ),

          harga_jual:
            Number(
              item.harga_jual
            ) || 0
        })
      )
  }

  const hasil =
    await simpanSO(
      payload
    )

  if (
    hasil?.success
  ) {
    emit('saved')
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
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

.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}
</style>