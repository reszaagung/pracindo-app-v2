<template>
    <div class="dashboard-wrapper">
        <header class="topbar">
            <div class="topbar__left">
                <div class="logo-box">PC</div>
                <span class="brand-text">PRACINDO &middot; SISTEM RETAIL</span>
            </div>
            <div class="topbar__right">
                <div class="user-info">
                    <span class="user-name">{{ pengguna?.nama || pengguna?.username || 'Staf Retail' }}</span>
                    <span class="user-role">{{ pengguna?.role_display || 'Kasir / SPG' }} &middot; {{ pengguna?.cabang?.nama || 'Cabang' }}</span>
                </div>
                <button @click="prosesLogout" class="btn-logout">Keluar</button>
            </div>
        </header>

        <main class="main-content">
            <div class="greeting-section">
                <h1 class="greeting-title">Selamat {{ waktuSapaan }}, {{ pengguna?.username || 'Staf' }}</h1>
                <p class="greeting-subtitle">Pilih modul atau selesaikan tugas operasional cabang hari ini.</p>
            </div>

            <section class="mb-10">
                <h2 class="section-title">Modul Toko</h2>
                <div class="modules-grid">
                    <!-- 👇 Memanggil data RETAIL_MODUL langsung dari config -->
                    <ModuleCard 
                        v-for="m in RETAIL_MODUL" 
                        :key="m.id" 
                        :modul="m" 
                    />
                </div>
            </section>

            <section class="work-order-section">
                <div class="section-header">
                    <h2 class="section-title">Tugas & Instruksi Cabang</h2>
                    <span class="task-badge">{{ daftarTugas.length }} Tugas Aktif</span>
                </div>
                <div v-if="daftarTugas.length > 0" class="wo-grid">
                    <WorkOrderCard 
                        v-for="wo in daftarTugas" 
                        :key="wo.id" 
                        :wo="wo" 
                        :staffId="pengguna?.id" 
                        :sibuk="sedangMenyimpan"
                        @approve="handleApproveTugas" 
                    />
                </div>
                <div v-else class="empty-task">
                    <i class="pi pi-check-circle text-green-500 text-3xl mb-2"></i>
                    <p class="text-slate-600 font-medium">Belum ada tugas operasional baru untuk cabang ini.</p>
                </div>
            </section>
        </main>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
// 👇 Import data modul dari file config/modules.js
import { RETAIL_MODUL } from '@/config/modules'
import ModuleCard from '@/components/ModuleCard.vue'
import WorkOrderCard from '@/components/WorkOrderCard.vue'

const router = useRouter()
const pengguna = ref(null)
const sedangMenyimpan = ref(false)
const daftarTugas = ref([]) // Dikosongkan sementara sampai API siap

onMounted(() => {
    const userData = localStorage.getItem('retail_user')
    if (userData) {
        pengguna.value = JSON.parse(userData)
    }
})

const waktuSapaan = computed(() => {
    const jam = new Date().getHours()
    if (jam < 11) return 'pagi'
    if (jam < 15) return 'siang'
    if (jam < 18) return 'sore'
    return 'malam'
})

const handleApproveTugas = async (wo) => {
    sedangMenyimpan.value = true
    try {
        await new Promise(resolve => setTimeout(resolve, 800))
        daftarTugas.value = daftarTugas.value.filter(item => item.id !== wo.id)
    } finally {
        sedangMenyimpan.value = false
    }
}

const prosesLogout = () => {
    if (confirm("Apakah Anda yakin ingin keluar dari sistem?")) {
        localStorage.removeItem('retail_token')
        localStorage.removeItem('retail_user')
        router.push('/login')
    }
}
</script>

<style scoped>
.dashboard-wrapper { min-height: 100vh; background-color: #f8fafc; font-family: 'Inter', system-ui, sans-serif; color: #0f172a; }
.topbar { display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 3rem; background: #ffffff; border-bottom: 1px solid #e2e8f0; }
.topbar__left { display: flex; align-items: center; gap: 1rem; }
.logo-box { background-color: #0f172a; color: white; font-weight: 800; font-size: 0.85rem; padding: 0.4rem 0.6rem; border-radius: 6px; letter-spacing: 1px; }
.brand-text { font-size: 0.85rem; font-weight: 600; color: #64748b; letter-spacing: 0.05em; }
.topbar__right { display: flex; align-items: center; gap: 1.5rem; }
.user-info { display: flex; flex-direction: column; align-items: flex-end; }
.user-name { font-size: 0.95rem; font-weight: 700; color: #334155; }
.user-role { font-size: 0.75rem; color: #94a3b8; }
.btn-logout { background: transparent; border: 1px solid #e2e8f0; padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: #475569; cursor: pointer; transition: all 0.2s; }
.btn-logout:hover { background: #f1f5f9; color: #0f172a; }
.main-content { max-width: 1200px; margin: 0 auto; padding: 2.5rem 3rem; }
.greeting-section { margin-bottom: 2.5rem; }
.greeting-title { font-size: 2.25rem; font-weight: 700; letter-spacing: -0.03em; color: #0f172a; margin-bottom: 0.35rem; }
.greeting-subtitle { font-size: 1rem; color: #64748b; }
.section-title { font-size: 1.125rem; font-weight: 700; color: #1e293b; margin-bottom: 1rem; }
.modules-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 1.25rem; }
.work-order-section { margin-top: 2.5rem; padding-top: 2rem; border-top: 1px solid #e2e8f0; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.task-badge { background: #eff6ff; color: #2563eb; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.75rem; border-radius: 999px; }
.wo-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 1.25rem; }
.empty-task { background: #ffffff; border: 1px dashed #cbd5e1; border-radius: 12px; padding: 2.5rem; text-align: center; }
@media (max-width: 768px) {
    .topbar { padding: 1.25rem; flex-direction: column; gap: 1rem; align-items: flex-start; }
    .topbar__right { width: 100%; justify-content: space-between; }
    .main-content { padding: 1.5rem; }
    .greeting-title { font-size: 1.75rem; }
    .modules-grid, .wo-grid { grid-template-columns: 1fr; }
}
</style>