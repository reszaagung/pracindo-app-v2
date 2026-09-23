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
                            Laporan Selisih
                        </span>
                    </div>

                    <div class="flex flex-wrap items-center gap-3">
                        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 tracking-tight">
                            Laporan Selisih
                        </h1>

                        <span class="inline-flex items-center justify-center min-w-7 h-7 px-2 rounded-full bg-slate-100 text-slate-700 border border-slate-200 text-xs font-bold">
                            {{ daftarSelisih.length }}
                        </span>
                    </div>

                    <p class="text-xs md:text-sm text-slate-500 mt-1 leading-relaxed">
                        Pantau perbedaan penerimaan, kekurangan barang, dan proses klaim supplier.
                    </p>
                </div>

                <button
                    type="button"
                    @click="muatSelisih"
                    :disabled="sedangProses"
                    class="h-10 px-3.5 rounded-xl border border-slate-200 bg-white text-slate-600 text-xs font-bold hover:bg-slate-50 hover:text-slate-900 hover:border-slate-300 transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center justify-center gap-2"
                >
                    <i
                        class="pi"
                        :class="sedangProses ? 'pi-spin pi-spinner' : 'pi-refresh'"
                    ></i>

                    <span class="hidden sm:inline">
                        Refresh
                    </span>
                </button>
            </div>
        </header>

        <transition name="slide-fade">
            <div
                v-if="galat"
                class="mb-5 rounded-2xl border border-red-200 bg-red-50 px-4 py-3.5 flex items-start gap-3 shadow-sm"
            >
                <div class="w-9 h-9 shrink-0 rounded-xl bg-red-100 text-red-600 flex items-center justify-center">
                    <i class="pi pi-exclamation-triangle text-sm"></i>
                </div>

                <div class="min-w-0 flex-1">
                    <p class="text-xs font-bold text-red-900">
                        Gagal memuat data
                    </p>

                    <p class="text-xs text-red-700 mt-0.5 break-words leading-relaxed">
                        {{ galat }}
                    </p>
                </div>

                <button
                    type="button"
                    @click="muatSelisih"
                    class="shrink-0 text-xs font-bold text-red-700 hover:text-red-900 underline underline-offset-2"
                >
                    Coba lagi
                </button>
            </div>
        </transition>

        <section class="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-5">
            <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
                <div class="flex items-center justify-between gap-2">
                    <div class="w-9 h-9 rounded-xl bg-slate-100 border border-slate-200 text-slate-500 flex items-center justify-center">
                        <i class="pi pi-list text-xs"></i>
                    </div>

                    <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                        Semua
                    </span>
                </div>

                <p class="text-xl md:text-2xl font-black text-slate-900 mt-3">
                    {{ totalSemua }}
                </p>

                <p class="text-[10px] text-slate-400 mt-0.5">
                    Total laporan
                </p>
            </div>

            <div class="bg-white border border-amber-200 rounded-2xl p-4 shadow-sm">
                <div class="flex items-center justify-between gap-2">
                    <div class="w-9 h-9 rounded-xl bg-amber-50 border border-amber-100 text-amber-600 flex items-center justify-center">
                        <i class="pi pi-exclamation-triangle text-xs"></i>
                    </div>

                    <span class="text-[10px] font-bold uppercase tracking-wider text-amber-600">
                        Dibuka
                    </span>
                </div>

                <p class="text-xl md:text-2xl font-black text-amber-700 mt-3">
                    {{ totalDibuka }}
                </p>

                <p class="text-[10px] text-amber-500 mt-0.5">
                    Menunggu tindakan
                </p>
            </div>

            <div class="bg-white border border-blue-200 rounded-2xl p-4 shadow-sm">
                <div class="flex items-center justify-between gap-2">
                    <div class="w-9 h-9 rounded-xl bg-blue-50 border border-blue-100 text-blue-600 flex items-center justify-center">
                        <i class="pi pi-send text-xs"></i>
                    </div>

                    <span class="text-[10px] font-bold uppercase tracking-wider text-blue-600">
                        Diajukan
                    </span>
                </div>

                <p class="text-xl md:text-2xl font-black text-blue-700 mt-3">
                    {{ totalDiajukan }}
                </p>

                <p class="text-[10px] text-blue-500 mt-0.5">
                    Dalam proses klaim
                </p>
            </div>

            <div class="bg-white border border-emerald-200 rounded-2xl p-4 shadow-sm">
                <div class="flex items-center justify-between gap-2">
                    <div class="w-9 h-9 rounded-xl bg-emerald-50 border border-emerald-100 text-emerald-600 flex items-center justify-center">
                        <i class="pi pi-check-circle text-xs"></i>
                    </div>

                    <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-600">
                        Selesai
                    </span>
                </div>

                <p class="text-xl md:text-2xl font-black text-emerald-700 mt-3">
                    {{ totalSelesai }}
                </p>

                <p class="text-[10px] text-emerald-500 mt-0.5">
                    Sudah ditangani
                </p>
            </div>
        </section>

        <section class="bg-white border border-slate-200 rounded-2xl md:rounded-3xl shadow-sm overflow-hidden">

            <div class="px-4 py-4 md:px-6 md:py-5 border-b border-slate-100">
                <div class="flex flex-col xl:flex-row xl:items-center xl:justify-between gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <h2 class="text-sm md:text-base font-bold text-slate-900">
                                Daftar Laporan
                            </h2>

                            <span
                                v-if="saring !== 'semua'"
                                class="inline-flex items-center px-2 py-0.5 rounded-md bg-slate-100 border border-slate-200 text-[10px] font-semibold text-slate-500"
                            >
                                Filter aktif
                            </span>
                        </div>

                        <p class="text-xs text-slate-500 mt-1">
                            {{ saring === 'semua'
                                ? 'Seluruh laporan selisih yang tercatat.'
                                : `Menampilkan laporan dengan status ${labelSaringan}.`
                            }}
                        </p>
                    </div>

                    <div class="flex bg-slate-50 border border-slate-100 p-1 rounded-xl overflow-x-auto custom-scrollbar w-full xl:w-auto">
                        <button
                            v-for="opt in SARINGAN"
                            :key="opt.nilai"
                            type="button"
                            @click="saring = opt.nilai"
                            :class="
                                saring === opt.nilai
                                    ? 'bg-white text-slate-800 shadow-sm font-bold border border-slate-200'
                                    : 'text-slate-500 hover:text-slate-700 border border-transparent'
                            "
                            class="min-h-9 px-3 md:px-4 py-2 rounded-lg text-[10px] md:text-xs whitespace-nowrap transition-all flex-1 xl:flex-none"
                        >
                            {{ opt.label }}

                            <span
                                v-if="jumlahStatus(opt.nilai) > 0"
                                class="ml-1.5 text-[9px] opacity-70"
                            >
                                {{ jumlahStatus(opt.nilai) }}
                            </span>
                        </button>
                    </div>
                </div>
            </div>

            <div
                v-if="sedangProses"
                class="p-4 md:p-6"
            >
                <div class="flex flex-col items-center justify-center py-10">
                    <div class="w-12 h-12 rounded-2xl bg-slate-100 flex items-center justify-center mb-4">
                        <i class="pi pi-spin pi-spinner text-slate-500 text-lg"></i>
                    </div>

                    <h3 class="text-sm font-bold text-slate-800">
                        Memuat laporan selisih
                    </h3>

                    <p class="text-xs text-slate-500 mt-1">
                        Mohon tunggu sebentar...
                    </p>
                </div>

                <div class="space-y-3 max-w-5xl mx-auto">
                    <div
                        v-for="n in 5"
                        :key="'skeleton-' + n"
                        class="h-16 rounded-xl bg-slate-50 border border-slate-100 animate-pulse"
                    ></div>
                </div>
            </div>

            <div
                v-else-if="tampil.length === 0"
                class="px-4 py-14 md:py-20"
            >
                <div class="max-w-md mx-auto text-center">
                    <div class="relative mx-auto w-16 h-16 mb-5">
                        <div class="absolute inset-0 rounded-2xl bg-emerald-50"></div>

                        <div class="relative w-16 h-16 rounded-2xl border border-emerald-100 bg-white flex items-center justify-center text-emerald-500">
                            <i class="pi pi-check-circle text-2xl"></i>
                        </div>
                    </div>

                    <h3 class="text-base md:text-lg font-bold text-slate-900">
                        {{ saring === 'semua'
                            ? 'Belum ada laporan selisih'
                            : 'Tidak ada laporan pada status ini'
                        }}
                    </h3>

                    <p class="text-xs md:text-sm text-slate-500 mt-1.5 leading-relaxed">
                        {{
                            saring === 'semua'
                                ? 'Belum ada perbedaan penerimaan yang tercatat.'
                                : 'Tidak terdapat data yang sesuai dengan filter yang dipilih.'
                        }}
                    </p>

                    <button
                        v-if="saring !== 'semua'"
                        type="button"
                        @click="saring = 'semua'"
                        class="mt-5 h-9 px-4 rounded-xl border border-slate-200 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 transition-colors"
                    >
                        Tampilkan Semua
                    </button>
                </div>
            </div>

            <div
                v-else
                class="hidden lg:block overflow-x-auto custom-scrollbar"
            >
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-slate-50/80 border-b border-slate-100">
                            <th class="px-6 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider w-[20%]">
                                Nomor Selisih
                            </th>

                            <th class="px-4 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider w-[24%]">
                                Jenis Laporan
                            </th>

                            <th class="px-4 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right w-[17%]">
                                Qty Selisih
                            </th>

                            <th class="px-4 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-center w-[19%]">
                                Status
                            </th>

                            <th class="px-6 py-3.5 text-[10px] font-bold text-slate-500 uppercase tracking-wider text-right w-[20%]">
                                Aksi
                            </th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-slate-100">
                        <tr
                            v-for="s in tampil"
                            :key="s.id"
                            class="group hover:bg-slate-50/70 transition-colors"
                        >
                            <td class="px-6 py-4 align-middle">
                                <div class="flex items-center gap-3">
                                    <div
                                        class="w-9 h-9 shrink-0 rounded-xl border flex items-center justify-center"
                                        :class="
                                            s.status === 'DIBUKA'
                                                ? 'bg-amber-50 border-amber-100 text-amber-600'
                                                : s.status === 'DIAJUKAN' || s.status === 'DISEPAKATI'
                                                    ? 'bg-blue-50 border-blue-100 text-blue-600'
                                                    : 'bg-slate-50 border-slate-200 text-slate-500'
                                        "
                                    >
                                        <i class="pi pi-file text-[10px]"></i>
                                    </div>

                                    <div class="min-w-0">
                                        <p class="text-sm font-bold text-slate-800 break-all">
                                            {{ s.nomor || '-' }}
                                        </p>

                                        <p class="text-[10px] text-slate-400 mt-1">
                                            Laporan selisih
                                        </p>
                                    </div>
                                </div>
                            </td>

                            <td class="px-4 py-4 align-middle">
                                <p class="text-sm font-semibold text-slate-700 break-words">
                                    {{ s.jenis || '-' }}
                                </p>
                            </td>

                            <td class="px-4 py-4 text-right align-middle">
                                <span class="inline-flex px-2.5 py-1 rounded-lg bg-rose-50 border border-rose-100 text-xs font-black text-rose-600">
                                    {{ angka(s.qty_selisih, 3) }}
                                </span>
                            </td>

                            <td class="px-4 py-4 text-center align-middle">
                                <span
                                    :class="badgeColor(s.status)"
                                    class="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-[10px] font-bold tracking-wide uppercase border"
                                >
                                    <span class="w-1.5 h-1.5 rounded-full bg-current"></span>
                                    {{ s.status || '-' }}
                                </span>
                            </td>

                            <td class="px-6 py-4 text-right align-middle">
                                <button
                                    v-if="s.status === 'DIBUKA'"
                                    type="button"
                                    :disabled="sedangProses"
                                    @click="ajukanKlaim(s)"
                                    class="h-9 px-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 active:bg-slate-950 text-white text-[10px] font-bold transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center justify-center gap-1.5"
                                >
                                    <i class="pi pi-send text-[9px]"></i>
                                    Ajukan Klaim
                                </button>

                                <span
                                    v-else
                                    class="inline-flex items-center gap-1.5 text-[10px] text-slate-400 font-medium"
                                >
                                    <i class="pi pi-check text-[9px]"></i>
                                    {{ actionLabel(s.status) }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div
                v-if="!sedangProses && tampil.length > 0"
                class="lg:hidden p-3 md:p-4 bg-slate-50/40 space-y-3"
            >
                <article
                    v-for="s in tampil"
                    :key="s.id"
                    class="rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden"
                >
                    <div class="p-4">
                        <div class="flex items-start justify-between gap-3">
                            <div class="flex items-start gap-3 min-w-0">
                                <div
                                    class="w-10 h-10 shrink-0 rounded-xl border flex items-center justify-center"
                                    :class="
                                        s.status === 'DIBUKA'
                                            ? 'bg-amber-50 border-amber-100 text-amber-600'
                                            : s.status === 'DIAJUKAN' || s.status === 'DISEPAKATI'
                                                ? 'bg-blue-50 border-blue-100 text-blue-600'
                                                : 'bg-slate-50 border-slate-200 text-slate-500'
                                    "
                                >
                                    <i class="pi pi-file text-xs"></i>
                                </div>

                                <div class="min-w-0">
                                    <p class="text-sm font-bold text-slate-900 break-all">
                                        {{ s.nomor || '-' }}
                                    </p>

                                    <p class="text-[10px] text-slate-400 mt-1">
                                        {{ s.jenis || '-' }}
                                    </p>
                                </div>
                            </div>

                            <span
                                :class="badgeColor(s.status)"
                                class="shrink-0 inline-flex items-center gap-1 px-2 py-1 rounded-lg text-[9px] font-bold uppercase border"
                            >
                                <span class="w-1.5 h-1.5 rounded-full bg-current"></span>
                                {{ s.status || '-' }}
                            </span>
                        </div>

                        <div class="grid grid-cols-2 gap-2 mt-4">
                            <div class="rounded-xl bg-rose-50 border border-rose-100 p-3">
                                <p class="text-[9px] font-bold uppercase tracking-wider text-rose-500">
                                    Qty Selisih
                                </p>

                                <p class="text-sm font-black text-rose-600 mt-1">
                                    {{ angka(s.qty_selisih, 3) }}
                                </p>
                            </div>

                            <div class="rounded-xl bg-slate-50 border border-slate-100 p-3">
                                <p class="text-[9px] font-bold uppercase tracking-wider text-slate-400">
                                    Jenis
                                </p>

                                <p class="text-xs font-bold text-slate-700 mt-1 break-words">
                                    {{ s.jenis || '-' }}
                                </p>
                            </div>
                        </div>

                        <div class="mt-3 pt-3 border-t border-slate-100">
                            <button
                                v-if="s.status === 'DIBUKA'"
                                type="button"
                                :disabled="sedangProses"
                                @click="ajukanKlaim(s)"
                                class="w-full h-10 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center justify-center gap-2"
                            >
                                <i class="pi pi-send text-[10px]"></i>
                                Ajukan ke Supplier
                            </button>

                            <div
                                v-else
                                class="h-10 rounded-xl bg-slate-50 border border-slate-100 text-slate-400 text-xs font-semibold inline-flex items-center justify-center gap-2 w-full"
                            >
                                <i class="pi pi-check-circle text-[10px]"></i>
                                {{ actionLabel(s.status) }}
                            </div>
                        </div>
                    </div>
                </article>
            </div>

            <div
                v-if="!sedangProses && tampil.length > 0"
                class="px-4 py-3.5 md:px-6 border-t border-slate-100 bg-white flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2"
            >
                <p class="text-[11px] text-slate-400">
                    Menampilkan
                    <span class="font-bold text-slate-600">
                        {{ tampil.length }}
                    </span>
                    laporan
                </p>

                <p class="text-[11px] text-slate-400">
                    Filter:
                    <span class="font-semibold text-slate-600">
                        {{ labelSaringan }}
                    </span>
                </p>
            </div>
        </section>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDiscrepancy } from '../composables/useDiscrepancy'
import { useToast } from '@/composables/useToast'
import { angka } from '@/utils/format'

const SARINGAN = [
    { nilai: 'semua', label: 'Semua' },
    { nilai: 'DIBUKA', label: 'Dibuka' },
    { nilai: 'DIAJUKAN', label: 'Diajukan' },
    { nilai: 'DISELESAIKAN', label: 'Diselesaikan' },
    { nilai: 'DITUTUP', label: 'Ditutup' },
]

const {
    daftarSelisih,
    sedangProses,
    galat,
    muatSelisih,
    ajukan,
} = useDiscrepancy()

const toast = useToast()
const saring = ref('semua')

const tampil = computed(() => {
    if (saring.value === 'semua') {
        return daftarSelisih.value
    }

    return daftarSelisih.value.filter(
        (s) => String(s.status).toUpperCase() === saring.value
    )
})

const totalSemua = computed(() => {
    return daftarSelisih.value.length
})

const totalDibuka = computed(() => {
    return daftarSelisih.value.filter(
        (s) => String(s.status).toUpperCase() === 'DIBUKA'
    ).length
})

const totalDiajukan = computed(() => {
    return daftarSelisih.value.filter((s) => {
        const status = String(s.status).toUpperCase()

        return status === 'DIAJUKAN' || status === 'DISEPAKATI'
    }).length
})

const totalSelesai = computed(() => {
    return daftarSelisih.value.filter((s) => {
        const status = String(s.status).toUpperCase()

        return status === 'DISELESAIKAN' || status === 'DITUTUP'
    }).length
})

const labelSaringan = computed(() => {
    return SARINGAN.find(
        (item) => item.nilai === saring.value
    )?.label || 'Semua'
})

const jumlahStatus = (status) => {
    if (status === 'semua') {
        return daftarSelisih.value.length
    }

    return daftarSelisih.value.filter(
        (s) => String(s.status).toUpperCase() === status
    ).length
}

const badgeColor = (status) => {
    const st = String(status).toUpperCase()

    if (st === 'DIBUKA') {
        return 'bg-amber-50 text-amber-700 border-amber-200'
    }

    if (st === 'DIAJUKAN' || st === 'DISEPAKATI') {
        return 'bg-blue-50 text-blue-700 border-blue-200'
    }

    if (st === 'DISELESAIKAN') {
        return 'bg-emerald-50 text-emerald-700 border-emerald-200'
    }

    if (st === 'DITUTUP') {
        return 'bg-slate-50 text-slate-500 border-slate-200'
    }

    return 'bg-slate-50 text-slate-500 border-slate-200'
}

const actionLabel = (status) => {
    const st = String(status).toUpperCase()

    if (st === 'DIAJUKAN') {
        return 'Menunggu Supplier'
    }

    if (st === 'DISEPAKATI') {
        return 'Disepakati'
    }

    if (st === 'DISELESAIKAN') {
        return 'Selesai'
    }

    if (st === 'DITUTUP') {
        return 'Ditutup'
    }

    return 'Tidak ada tindakan'
}

const ajukanKlaim = async (laporan) => {
    if (!laporan?.id || sedangProses.value) {
        return
    }

    const hasil = await ajukan(laporan.id)

    if (hasil.success) {
        toast.success('Klaim berhasil diajukan ke supplier.')
        await muatSelisih()
        return
    }

    toast.error(
        hasil.message || 'Gagal mengajukan klaim.'
    )
}

onMounted(() => {
    muatSelisih()
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

button:focus-visible {
    outline: 2px solid #64748b;
    outline-offset: 2px;
}
</style>