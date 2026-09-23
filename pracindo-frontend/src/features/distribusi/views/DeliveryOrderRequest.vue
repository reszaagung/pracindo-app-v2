<template>
    <div
        class="min-h-screen w-full animate-fade-in bg-[#F8FAFC] p-4 text-slate-700 sm:p-5 lg:p-6"
    >
        <div class="mx-auto flex w-full max-w-7xl flex-col">
            <header
                class="mb-5 flex flex-col gap-5 border-b border-slate-200 pb-5 md:mb-7 md:flex-row md:items-end md:justify-between"
            >
                <div class="min-w-0">
                    <div
                        class="mb-2 flex flex-wrap items-center gap-1.5 text-[10px] font-semibold uppercase tracking-[0.1em] text-slate-400"
                    >
                        <span class="transition-colors hover:text-slate-600">
                            Logistics
                        </span>

                        <span
                            class="text-slate-300"
                            aria-hidden="true"
                        >
                            /
                        </span>

                        <span class="text-slate-600">
                            Delivery Order
                        </span>
                    </div>

                    <div class="flex items-start gap-3">
                        <div
                            class="mt-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-white shadow-sm sm:h-11 sm:w-11"
                            aria-hidden="true"
                        >
                            <i class="pi pi-truck text-base sm:text-lg"></i>
                        </div>

                        <div class="min-w-0">
                            <h1
                                class="text-xl font-extrabold tracking-tight text-slate-800 sm:text-2xl lg:text-3xl"
                            >
                                Delivery Request Order
                            </h1>

                            <p
                                class="mt-1 max-w-3xl text-xs leading-5 text-slate-500 sm:text-sm"
                            >
                                {{
                                    activeTab === 'DISTRIBUSI'
                                        ? 'Permintaan pengiriman stok internal ke cabang retail.'
                                        : 'Permintaan pengiriman B2C langsung ke kustomer (SO).'
                                }}
                            </p>
                        </div>
                    </div>
                </div>

                <div
                    class="grid w-full grid-cols-2 overflow-hidden rounded-2xl border border-slate-200 bg-white p-1 shadow-sm md:w-auto md:min-w-[430px]"
                    role="tablist"
                    aria-label="Jenis delivery order"
                >
                    <button
                        type="button"
                        role="tab"
                        :aria-selected="activeTab === 'DISTRIBUSI'"
                        :tabindex="activeTab === 'DISTRIBUSI' ? 0 : -1"
                        @click="activeTab = 'DISTRIBUSI'"
                        class="relative flex min-h-12 items-center justify-center gap-2 rounded-xl px-3 py-2.5 text-[11px] font-extrabold uppercase tracking-wide transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 sm:px-5 sm:text-xs"
                        :class="
                            activeTab === 'DISTRIBUSI'
                                ? 'bg-slate-900 text-white shadow-md shadow-slate-900/10'
                                : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
                        "
                    >
                        <i
                            class="pi pi-building text-xs sm:text-sm"
                            aria-hidden="true"
                        ></i>

                        <span>Distribusi</span>
                    </button>

                    <button
                        type="button"
                        role="tab"
                        :aria-selected="activeTab === 'DELIVERY'"
                        :tabindex="activeTab === 'DELIVERY' ? 0 : -1"
                        @click="activeTab = 'DELIVERY'"
                        class="relative flex min-h-12 items-center justify-center gap-2 rounded-xl px-3 py-2.5 text-[11px] font-extrabold uppercase tracking-wide transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2 sm:px-5 sm:text-xs"
                        :class="
                            activeTab === 'DELIVERY'
                                ? 'bg-slate-900 text-white shadow-md shadow-slate-900/10'
                                : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
                        "
                    >
                        <i
                            class="pi pi-send text-xs sm:text-sm"
                            aria-hidden="true"
                        ></i>

                        <span>Delivery</span>
                    </button>
                </div>
            </header>

            <main
                class="relative overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_10px_35px_rgba(15,23,42,0.05)] sm:rounded-3xl"
            >
                <div
                    class="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-slate-300 to-transparent"
                    aria-hidden="true"
                ></div>

                <div class="p-4 sm:p-5 lg:p-6">
                    <Transition
                        name="tab-fade"
                        mode="out-in"
                    >
                        <div
                            :key="activeTab"
                            class="w-full"
                            role="tabpanel"
                            :aria-label="
                                activeTab === 'DISTRIBUSI'
                                    ? 'Form Distribusi Retail'
                                    : 'Form Delivery B2C'
                            "
                        >
                            <DistribusiCreate
                                v-if="activeTab === 'DISTRIBUSI'"
                            />

                            <DeliveryCreate
                                v-else
                            />
                        </div>
                    </Transition>
                </div>
            </main>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import DistribusiCreate from './DistribusiCreate.vue'
import DeliveryCreate from './DeliveryCreate.vue'

const activeTab = ref('DISTRIBUSI')
</script>

<style scoped>
.animate-fade-in {
    animation: pageFadeIn 0.35s ease-out forwards;
}

.tab-fade-enter-active,
.tab-fade-leave-active {
    transition:
        opacity 0.2s ease,
        transform 0.2s ease;
}

.tab-fade-enter-from {
    opacity: 0;
    transform: translateY(6px);
}

.tab-fade-leave-to {
    opacity: 0;
    transform: translateY(-6px);
}

@keyframes pageFadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (prefers-reduced-motion: reduce) {
    .animate-fade-in,
    .tab-fade-enter-active,
    .tab-fade-leave-active {
        animation: none !important;
        transition: none !important;
    }
}
</style>
