<template>
    <div class="flex flex-col w-full animate-fade-in relative">
        <div v-if="error" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600 font-medium flex items-start gap-3 shadow-sm">
            <i class="pi pi-exclamation-triangle mt-0.5"></i>
            <span>{{ error }}</span>
        </div>

        <div v-if="loading && !error" class="flex flex-col items-center justify-center py-12 text-slate-400">
            <i class="pi pi-spin pi-spinner text-3xl mb-3"></i>
            <p class="text-sm font-medium">Memuat data...</p>
        </div>

        <template v-if="!loading && hasData">
            <div class="mb-6 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
                <div>
                    <p v-if="backRoute" class="text-xs text-slate-400 mb-1">
                        <router-link :to="backRoute" class="hover:text-slate-700 transition-colors">{{ backLabel }}</router-link>
                        <span class="mx-1">/</span>
                        <span class="text-slate-600 font-semibold">{{ title }}</span>
                    </p>
                    <h2 class="text-xl md:text-2xl font-bold text-slate-800 tracking-tight">{{ title }}</h2>
                    <p v-if="subtitle" class="text-xs md:text-sm text-slate-500 mt-1">{{ subtitle }}</p>
                </div>
                
                <span v-if="badge" :class="badgeClass" class="px-3 py-1 rounded-full text-xs font-bold tracking-wide uppercase inline-flex items-center gap-1.5 shadow-sm border">
                    <i v-if="badgeIcon" :class="['pi', badgeIcon]"></i> {{ badge }}
                </span>
            </div>

            <slot />
        </template>
    </div>
</template>

<script setup>
defineProps({
    loading: { type: Boolean, default: false },
    error: { type: String, default: '' },
    hasData: { type: Boolean, default: true },
    title: { type: String, required: true },
    subtitle: { type: String, default: '' },
    backRoute: { type: String, default: '' },
    backLabel: { type: String, default: 'Kembali' },
    badge: { type: String, default: '' },
    badgeClass: { type: String, default: 'bg-slate-50 text-slate-600 border-slate-200' },
    badgeIcon: { type: String, default: '' }
})
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>