<template>
    <section
        class="rounded-3xl border border-slate-800 bg-slate-900 overflow-hidden"
    >
        <div class="px-4 sm:px-5 py-4 border-b border-slate-800">
            <h2 class="text-lg sm:text-xl font-black">
                POSISI KAS
            </h2>

            <p class="text-xs text-slate-500 mt-1">
                Saldo rekening operasional.
            </p>
        </div>

        <div class="p-4 space-y-3">
            <article
                v-for="item in rekening"
                :key="item.id"
                class="rounded-2xl border border-slate-800 bg-slate-950 p-4"
            >
                <div
                    class="flex items-start justify-between gap-3"
                >
                    <div>
                        <div class="font-bold text-slate-200">
                            {{
                                item.nama ||
                                item.nama_bank ||
                                'Kas'
                            }}
                        </div>

                        <div
                            class="mt-1 text-[10px] font-black tracking-widest text-slate-600"
                        >
                            {{ item.jenis || 'KAS_KECIL' }}
                        </div>
                    </div>

                    <div class="text-right">
                        <div
                            class="text-lg sm:text-xl font-black tabular-nums"
                        >
                            {{ formatUang(item.saldo) }}
                        </div>
                    </div>
                </div>
            </article>

            <div
                v-if="!rekening.length"
                class="py-12 text-center text-sm text-slate-600"
            >
                Belum ada rekening kas.
            </div>
        </div>
    </section>
</template>

<script setup>
defineProps({
    rekening: {
        type: Array,
        default: () => [],
    },
})

function formatUang(nilai) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        maximumFractionDigits: 0,
    }).format(Number(nilai || 0))
}
</script>