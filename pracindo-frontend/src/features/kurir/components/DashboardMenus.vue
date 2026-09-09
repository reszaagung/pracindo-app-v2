<template>
    <div class="mt-8 mx-5 grid grid-cols-4 gap-y-6 gap-x-2">
        <button @click="$router.push('/kurir/available-tasks')" class="flex flex-col items-center gap-2 group">
            <div class="w-14 h-14 bg-emerald-100 rounded-2xl flex items-center justify-center relative shadow-sm border border-emerald-200">
                <div class="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full border-2 border-white z-10">Baru</div>
                <span class="text-2xl">📦</span>
            </div>
            <span class="text-[11px] font-semibold text-slate-700 text-center leading-tight">Kolam<br>Tugas</span>
        </button>

        <button @click="$router.push('/kurir/my-deliveries')" class="flex flex-col items-center gap-2 group">
            <div class="w-14 h-14 bg-blue-100 rounded-2xl flex items-center justify-center shadow-sm border border-blue-200">
                <span class="text-2xl">🚚</span>
            </div>
            <span class="text-[11px] font-semibold text-slate-700 text-center leading-tight">Tugas<br>Saya</span>
        </button>

        <button class="flex flex-col items-center gap-2 opacity-60">
            <div class="w-14 h-14 bg-purple-100 rounded-2xl flex items-center justify-center shadow-sm border border-purple-200">
                <span class="text-2xl">📜</span>
            </div>
            <span class="text-[11px] font-semibold text-slate-700 text-center leading-tight">Riwayat</span>
        </button>

        <button class="flex flex-col items-center gap-2 opacity-60">
            <div class="w-14 h-14 bg-orange-100 rounded-2xl flex items-center justify-center shadow-sm border border-orange-200">
                <span class="text-2xl">🚐</span>
            </div>
            <span class="text-[11px] font-semibold text-slate-700 text-center leading-tight">Armada</span>
        </button>
    </div>
</template>