<template>
    <div class="w-full p-4 flex flex-col gap-4 pb-24 bg-slate-50 min-h-screen">
        <h1 class="text-xl font-bold text-slate-800">Riwayat Pengiriman</h1>
        <p class="text-xs text-slate-500 mb-2">Daftar tugas yang telah diselesaikan.</p>

        <div class="flex flex-col gap-3">
            <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex items-center justify-between opacity-80">
                <div>
                    <span class="text-[10px] font-bold bg-slate-100 text-slate-600 px-2 py-1 rounded">DO-2023-088</span>
                    <h3 class="text-sm font-bold mt-2 text-slate-700">Selesai: 12 Okt 2023</h3>
                    <p class="text-xs text-slate-500">3 Perhentian Toko</p>
                </div>
                <div class="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600">
                    <span>✔️</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
// Placeholder untuk fetch history API
</script>