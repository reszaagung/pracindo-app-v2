<template>
    <div class="mx-5 -mt-8 bg-white rounded-2xl shadow-md p-4 flex items-center justify-between border-2 border-slate-100 z-10 relative">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </div>
            <div>
                <p class="text-xs text-slate-500 font-semibold">Selesai</p>
                <p class="text-lg font-bold text-slate-800">{{ selesai }} <span class="text-sm font-normal text-slate-500">Tugas</span></p>
            </div>
        </div>
        
        <div class="h-10 w-px bg-slate-200"></div> <!-- Garis Pemisah -->
        
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center text-orange-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </div>
            <div>
                <p class="text-xs text-slate-500 font-semibold">Aktif</p>
                <p class="text-lg font-bold text-slate-800">{{ aktif }} <span class="text-sm font-normal text-slate-500">Jalan</span></p>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    selesai: { type: Number, default: 0 },
    aktif: { type: Number, default: 0 }
})
</script>