<!-- features/warehouse/views/ReceiptIndex.vue -->
<template>
    <div class="w-full min-w-0 animate-fade-in relative">

        <header class="mb-5 md:mb-6">
            <div class="flex flex-col xl:flex-row xl:items-end xl:justify-between gap-4">
                <div class="min-w-0">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="text-xs font-medium text-slate-400">
                            Warehouse
                        </span>

                        <i class="pi pi-angle-right text-[9px] text-slate-300"></i>

                        <span class="text-xs font-semibold text-slate-600">
                            Penerimaan
                        </span>
                    </div>

                    <h1 class="text-2xl md:text-3xl font-bold text-slate-900 tracking-tight">
                        Penerimaan Barang
                    </h1>

                    <p class="text-xs md:text-sm text-slate-500 mt-1 leading-relaxed">
                        Pilih jenis dokumen untuk memproses penerimaan barang masuk.
                    </p>
                </div>

                <div class="hidden sm:flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-50 border border-slate-100 text-[10px] text-slate-500">
                    <i class="pi pi-info-circle text-slate-400"></i>
                    <span>Gunakan tab sesuai kategori barang.</span>
                </div>
            </div>
        </header>

        <section class="mb-5 md:mb-6">
            <div class="bg-white border border-slate-200 rounded-2xl md:rounded-3xl shadow-sm p-2">
                <div class="grid grid-cols-2 gap-2">

                    <button
                        type="button"
                        @click="ubahTab('bahan_baku')"
                        :aria-selected="tabAktif === 'bahan_baku'"
                        role="tab"
                        class="group relative min-w-0 rounded-xl md:rounded-2xl px-3 py-3.5 md:px-5 md:py-4 text-left transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-400"
                        :class="
                            tabAktif === 'bahan_baku'
                                ? 'bg-slate-900 text-white shadow-md shadow-slate-200'
                                : 'bg-white text-slate-600 hover:bg-slate-50'
                        "
                    >
                        <div class="flex items-center gap-3">
                            <div
                                class="w-10 h-10 md:w-11 md:h-11 shrink-0 rounded-xl flex items-center justify-center transition-colors"
                                :class="
                                    tabAktif === 'bahan_baku'
                                        ? 'bg-white/10 text-white'
                                        : 'bg-slate-100 text-slate-500 group-hover:bg-slate-200'
                                "
                            >
                                <i class="pi pi-box text-sm md:text-base"></i>
                            </div>

                            <div class="min-w-0 flex-1">
                                <p
                                    class="text-xs md:text-sm truncate"
                                    :class="
                                        tabAktif === 'bahan_baku'
                                            ? 'font-bold text-white'
                                            : 'font-semibold text-slate-700'
                                    "
                                >
                                    Bahan Baku
                                </p>

                                <p
                                    class="text-[10px] md:text-[11px] mt-0.5 truncate"
                                    :class="
                                        tabAktif === 'bahan_baku'
                                            ? 'text-slate-300'
                                            : 'text-slate-400'
                                    "
                                >
                                    Material produksi
                                </p>
                            </div>

                            <i
                                v-if="tabAktif === 'bahan_baku'"
                                class="pi pi-check text-xs shrink-0"
                            ></i>
                        </div>
                    </button>

                    <button
                        type="button"
                        @click="ubahTab('kemasan')"
                        :aria-selected="tabAktif === 'kemasan'"
                        role="tab"
                        class="group relative min-w-0 rounded-xl md:rounded-2xl px-3 py-3.5 md:px-5 md:py-4 text-left transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-violet-400"
                        :class="
                            tabAktif === 'kemasan'
                                ? 'bg-violet-600 text-white shadow-md shadow-violet-200'
                                : 'bg-white text-slate-600 hover:bg-slate-50'
                        "
                    >
                        <div class="flex items-center gap-3">
                            <div
                                class="w-10 h-10 md:w-11 md:h-11 shrink-0 rounded-xl flex items-center justify-center transition-colors"
                                :class="
                                    tabAktif === 'kemasan'
                                        ? 'bg-white/10 text-white'
                                        : 'bg-violet-50 text-violet-500 group-hover:bg-violet-100'
                                "
                            >
                                <i class="pi pi-shopping-bag text-sm md:text-base"></i>
                            </div>

                            <div class="min-w-0 flex-1">
                                <p
                                    class="text-xs md:text-sm truncate"
                                    :class="
                                        tabAktif === 'kemasan'
                                            ? 'font-bold text-white'
                                            : 'font-semibold text-slate-700'
                                    "
                                >
                                    Kemasan
                                </p>

                                <p
                                    class="text-[10px] md:text-[11px] mt-0.5 truncate"
                                    :class="
                                        tabAktif === 'kemasan'
                                            ? 'text-violet-100'
                                            : 'text-slate-400'
                                    "
                                >
                                    Aset packaging
                                </p>
                            </div>

                            <i
                                v-if="tabAktif === 'kemasan'"
                                class="pi pi-check text-xs shrink-0"
                            ></i>
                        </div>
                    </button>
                </div>
            </div>
        </section>

        <transition
            name="content-fade"
            mode="out-in"
        >
            <GoodsReceiptList
                v-if="tabAktif === 'bahan_baku'"
                key="bahan_baku"
            />

            <PackageReceiptList
                v-else
                key="kemasan"
            />
        </transition>
    </div>
</template>

<script setup>
import { useReceiptIndex } from '../composables/useReceiptIndex'
import GoodsReceiptList from './GoodsReceiptList.vue'
import PackageReceiptList from './PackageReceiptList.vue'

const {
    tabAktif,
    ubahTab,
} = useReceiptIndex()
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

.content-fade-enter-active,
.content-fade-leave-active {
    transition:
        opacity 0.2s ease,
        transform 0.2s ease;
}

.content-fade-enter-from {
    opacity: 0;
    transform: translateY(6px);
}

.content-fade-leave-to {
    opacity: 0;
    transform: translateY(-6px);
}

button:focus-visible {
    outline: 2px solid #64748b;
    outline-offset: 2px;
}
</style>