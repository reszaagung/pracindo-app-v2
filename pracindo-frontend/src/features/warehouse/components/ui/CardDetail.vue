<template>
    <div class="w-full min-w-0 animate-fade-in relative">

        <!-- =========================================================
             ERROR STATE
        ========================================================== -->
        <transition name="slide-fade">
            <div
                v-if="error"
                class="mb-5 rounded-2xl border border-red-200 bg-red-50 px-4 py-3.5 md:px-5 md:py-4 flex items-start gap-3 shadow-sm"
            >
                <div class="w-9 h-9 shrink-0 rounded-xl bg-red-100 text-red-600 flex items-center justify-center">
                    <i class="pi pi-exclamation-triangle text-sm"></i>
                </div>

                <div class="min-w-0 flex-1">
                    <p class="text-xs md:text-sm font-bold text-red-900">
                        Gagal memuat data
                    </p>

                    <p class="text-xs text-red-700 mt-0.5 leading-relaxed break-words">
                        {{ error }}
                    </p>
                </div>
            </div>
        </transition>

        <!-- =========================================================
             LOADING STATE
        ========================================================== -->
        <div
            v-if="loading && !error"
            class="rounded-2xl md:rounded-3xl border border-slate-200 bg-white shadow-sm overflow-hidden"
        >
            <!-- Header Skeleton -->
            <div class="p-4 md:p-6 border-b border-slate-100">
                <div class="flex items-start justify-between gap-4">
                    <div class="flex items-start gap-3 min-w-0 flex-1">
                        <div class="w-10 h-10 rounded-xl bg-slate-100 animate-pulse shrink-0"></div>

                        <div class="min-w-0 flex-1 space-y-2">
                            <div class="h-3 bg-slate-100 rounded w-24 animate-pulse"></div>
                            <div class="h-6 bg-slate-100 rounded w-48 md:w-72 animate-pulse"></div>
                            <div class="h-3 bg-slate-100 rounded w-64 md:w-96 animate-pulse"></div>
                        </div>
                    </div>

                    <div class="h-7 w-24 bg-slate-100 rounded-full animate-pulse shrink-0"></div>
                </div>
            </div>

            <!-- Content Skeleton -->
            <div class="p-4 md:p-6 space-y-4">
                <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div
                        v-for="n in 4"
                        :key="'summary-skeleton-' + n"
                        class="h-24 rounded-2xl bg-slate-50 border border-slate-100 animate-pulse"
                    ></div>
                </div>

                <div class="rounded-2xl border border-slate-100 overflow-hidden">
                    <div class="h-12 bg-slate-50 animate-pulse"></div>

                    <div class="p-4 space-y-3">
                        <div
                            v-for="n in 5"
                            :key="'row-skeleton-' + n"
                            class="h-12 rounded-xl bg-slate-50 animate-pulse"
                        ></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- =========================================================
             EMPTY STATE
        ========================================================== -->
        <div
            v-else-if="!hasData && !error"
            class="rounded-2xl md:rounded-3xl border border-slate-200 bg-white shadow-sm p-8 md:p-12"
        >
            <div class="max-w-md mx-auto text-center">
                <div class="relative mx-auto w-16 h-16 mb-5">
                    <div class="absolute inset-0 rounded-2xl bg-slate-100"></div>

                    <div class="relative w-16 h-16 rounded-2xl border border-slate-200 bg-white flex items-center justify-center text-slate-400">
                        <i class="pi pi-file text-2xl"></i>
                    </div>
                </div>

                <h2 class="text-base md:text-lg font-bold text-slate-900">
                    Data tidak ditemukan
                </h2>

                <p class="text-xs md:text-sm text-slate-500 mt-1.5 leading-relaxed">
                    Detail yang diminta tidak tersedia atau sudah tidak dapat diakses.
                </p>

                <router-link
                    v-if="backRoute"
                    :to="backRoute"
                    class="mt-5 h-10 px-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold inline-flex items-center justify-center gap-2 transition-all shadow-sm"
                >
                    <i class="pi pi-arrow-left text-[10px]"></i>
                    {{ backLabel }}
                </router-link>
            </div>
        </div>

        <!-- =========================================================
             DATA STATE
        ========================================================== -->
        <template v-else-if="hasData">

            <!-- =====================================================
                 PAGE HEADER
            ====================================================== -->
            <header class="mb-5 md:mb-6">
                <div class="flex flex-col xl:flex-row xl:items-start xl:justify-between gap-4">

                    <!-- Left -->
                    <div class="flex items-start gap-3 min-w-0 flex-1">

                        <!-- Back -->
                        <router-link
                            v-if="backRoute"
                            :to="backRoute"
                            :aria-label="`Kembali ke ${backLabel}`"
                            class="group w-10 h-10 shrink-0 rounded-xl border border-slate-200 bg-white flex items-center justify-center text-slate-500 hover:text-slate-900 hover:border-slate-300 hover:bg-slate-50 transition-all duration-200 shadow-sm"
                        >
                            <i class="pi pi-arrow-left text-sm group-hover:-translate-x-0.5 transition-transform"></i>
                        </router-link>

                        <div class="min-w-0 flex-1">

                            <!-- Breadcrumb -->
                            <div
                                v-if="backRoute"
                                class="flex items-center gap-2 mb-1.5 min-w-0"
                            >
                                <router-link
                                    :to="backRoute"
                                    class="text-xs text-slate-400 hover:text-slate-700 transition-colors truncate max-w-[180px]"
                                >
                                    {{ backLabel }}
                                </router-link>

                                <i class="pi pi-angle-right text-[9px] text-slate-300 shrink-0"></i>

                                <span class="text-xs font-semibold text-slate-600 truncate">
                                    {{ title }}
                                </span>
                            </div>

                            <!-- Title -->
                            <div class="flex flex-wrap items-center gap-2.5">
                                <h1
                                    class="text-xl md:text-2xl lg:text-3xl font-bold text-slate-900 tracking-tight break-words"
                                >
                                    {{ title }}
                                </h1>

                                <span
                                    v-if="badge"
                                    :class="badgeClass"
                                    class="shrink-0 px-2.5 py-1.5 rounded-lg text-[10px] md:text-[11px] font-bold tracking-wide uppercase inline-flex items-center gap-1.5 border"
                                >
                                    <i
                                        v-if="badgeIcon"
                                        :class="['pi', badgeIcon, 'text-[9px]']"
                                    ></i>

                                    {{ badge }}
                                </span>
                            </div>

                            <!-- Subtitle -->
                            <p
                                v-if="subtitle"
                                class="text-xs md:text-sm text-slate-500 mt-1.5 leading-relaxed break-words"
                            >
                                {{ subtitle }}
                            </p>
                        </div>
                    </div>

                    <!-- Right Header Slot -->
                    <div
                        v-if="$slots.actions"
                        class="w-full xl:w-auto shrink-0"
                    >
                        <slot name="actions" />
                    </div>
                </div>

                <!-- Secondary Meta Slot -->
                <div
                    v-if="$slots.meta"
                    class="mt-4"
                >
                    <slot name="meta" />
                </div>
            </header>

            <!-- =====================================================
                 MAIN CONTENT
            ====================================================== -->
            <main class="w-full min-w-0">
                <slot />
            </main>
        </template>
    </div>
</template>

<script setup>
defineProps({
    loading: {
        type: Boolean,
        default: false,
    },

    error: {
        type: String,
        default: '',
    },

    hasData: {
        type: Boolean,
        default: true,
    },

    title: {
        type: String,
        required: true,
    },

    subtitle: {
        type: String,
        default: '',
    },

    backRoute: {
        type: String,
        default: '',
    },

    backLabel: {
        type: String,
        default: 'Kembali',
    },

    badge: {
        type: String,
        default: '',
    },

    badgeClass: {
        type: String,
        default: 'bg-slate-50 text-slate-600 border-slate-200',
    },

    badgeIcon: {
        type: String,
        default: '',
    },
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

button:focus-visible,
a:focus-visible {
    outline: 2px solid #64748b;
    outline-offset: 2px;
}
</style>