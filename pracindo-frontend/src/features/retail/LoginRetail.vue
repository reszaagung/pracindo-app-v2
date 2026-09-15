<!--
  src/features/retail/LoginRetail.vue
  ====================================
  Halaman login khusus modul Retail.
  - Route: '/retail/login' (name: 'LoginRetail'), didaftarkan di
    features/retail/routes.js dengan meta { perluLogin: false, modul: 'retail' }.
  - Logika akses memakai composable `useRetailAuth()` — pembungkus
    `useAuth()` global, validasi akses modul 'retail' ada di dalam
    composable itu sendiri.
  - Redirect setelah login: pakai `next` dari query kalau ada, kalau
    tidak fallback ke '/retail' (route 'retail-portal' → DashboardView.vue).
  - "Lupa kata sandi?" mengarah ke hubungiAdmin() karena reset password
    modul retail ditangani manual oleh admin pusat, bukan self-service.
  - Ilustrasi dipakai sebagai background penuh (desktop), form melayang
    di atasnya lewat panel kanan yang transparan. Overlay dibuat tipis +
    text-shadow di teks kiri supaya ilustrasi tetap kelihatan jelas.
-->
<template>
    <div class="login-wrapper">

        <!-- Background: ilustrasi jadi latar penuh (desktop only) -->
        <img :src="ilustrationImg" alt="" class="bg-illustration" />
        <div class="bg-overlay"></div>

        <!-- ── kiri: teks & brand (desktop) ─────────────────── -->
        <div class="panel-left">
            <div class="brand-top">
                <img :src="logoPracindo" alt="Logo Pracindo" class="logo-img" />
                <span class="brand-text">Pracindo Supply Chain Management</span>
            </div>

            <div class="hero-content">
                <h1 class="hero-title">
                    Dari Pabrik <br>
                    hingga ke Toko, <br>
                    <span class="text-accent">Warna Selalu Terkendali.</span>
                </h1>

                <p class="hero-subtitle">
                    Portal khusus staf Retail untuk mengelola transaksi kasir,
                    stok warna di toko, hingga laporan penjualan harian.
                </p>
            </div>
        </div>

        <!-- ── kanan: form login ───────────────────────────────── -->
        <div class="panel-right">
            <div class="login-box animate-fade-in">

                <!-- Tampil hanya di Mobile -->
                <div class="mobile-brand">
                    <img :src="logoPracindo" alt="Logo Pracindo" class="logo-img-mobile" />
                    <span class="brand-text-mobile">Pracindo Jaya Mandiri</span>
                </div>

                <!-- Badge modul -->
                <div class="module-info">
                    <div class="module-icon">
                        <i class="pi pi-shopping-cart"></i>
                    </div>
                    <div class="module-text">
                        <h2 class="form-title">Retail</h2>
                        <p class="module-desc">Akses ke sistem penjualan retail dan manajemen toko.</p>
                    </div>
                </div>

                <form class="login-form" @submit.prevent="handleLogin">
                    <div class="input-group">
                        <i class="pi pi-user input-icon"></i>
                        <input ref="isianPertama" v-model="form.username" type="text"
                            placeholder="Username" autocomplete="username" required :disabled="sedangProses"
                            class="form-input pl-icon" />
                    </div>

                    <div class="input-group">
                        <i class="pi pi-lock input-icon"></i>
                        <input v-model="form.password" :type="showPassword ? 'text' : 'password'"
                            placeholder="Kata Sandi" autocomplete="current-password" required :disabled="sedangProses"
                            class="form-input pl-icon pr-icon" />
                        <span class="btn-toggle-pass"
                            :title="showPassword ? 'Sembunyikan sandi' : 'Tampilkan sandi'"
                            @click="showPassword = !showPassword">
                            <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
                        </span>
                    </div>

                    <div class="forgot-pass-wrap">
                        <span class="forgot-pass-link" @click="hubungiAdmin">Lupa kata sandi?</span>
                    </div>

                    <!-- Pesan Error / Notifikasi Sesi -->
                    <p v-if="pesan" role="alert" class="error-msg">
                        {{ pesan }}
                    </p>

                    <button type="submit" class="btn-submit" :disabled="sedangProses">
                        <i v-if="sedangProses" class="pi pi-spin pi-spinner" style="margin-right: 8px;"></i>
                        <i v-else class="pi pi-sign-in" style="margin-right: 8px;"></i>
                        {{ sedangProses ? 'Memeriksa...' : 'Masuk' }}
                    </button>
                </form>

                <div class="divider"></div>

                <!-- Tautan ke Halaman Pendaftaran -->
                <p class="register-link-wrap">
                    Belum punya akun? <br>
                    <router-link to="/register" class="register-link">
                        Registrasi Staff
                    </router-link>
                </p>

                <p class="session-warning">
                    Satu sesi aktif per akun — masuk di perangkat lain akan menutup sesi ini.
                </p>
            </div>

            <div class="footer-note">
                <i class="pi pi-shield"></i> Sistem Terintegrasi • Aman • Terpercaya
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRetailAuth } from './composables/useRetailAuth'

import logoPracindo from '@/assets/logo_pt.svg'
import ilustrationImg from './src/asset_retail/retail_ilustration.png'

const route = useRoute()
const router = useRouter()
const { login, sedangProses } = useRetailAuth()

const form = reactive({ username: '', password: '' })
const showPassword = ref(false)
const pesan = ref('')
const isianPertama = ref(null)

onMounted(() => {
    isianPertama.value?.focus?.()
    if (route.query.sesi === 'berakhir') {
        pesan.value = 'Sesi Anda telah berakhir. Silakan login kembali.'
        router.replace({ query: {} })
    }
})

const handleLogin = async () => {
    pesan.value = ''
    const hasil = await login(form.username.trim(), form.password)

    if (!hasil.success) {
        pesan.value = hasil.message 
        form.password = ''
        return
    }

    const tujuan = route.query.next || '/retail'
    router.push(tujuan)
}

const hubungiAdmin = () => {
    alert('Silakan hubungi administrator pusat untuk bantuan pemulihan akun retail.')
}
</script>

<style scoped>
/* =========================================
   STYLE HALAMAN LOGIN RETAIL (AKSEN BIRU)
   Ilustrasi = background penuh, form melayang
   di atasnya (desktop only, ≥1024px).
========================================= */

* {
    box-sizing: border-box;
}

.login-wrapper {
    position: relative;
    display: flex;
    min-height: 100vh;
    width: 100%;
    font-family: inherit;
    color: #1e293b;
    background: #fff;
    overflow: hidden;
}

/* Background: gambar ilustrasi, full-bleed, desktop only */
.bg-illustration {
    display: none;
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    z-index: 0;
}

@media (min-width: 1024px) {
    .bg-illustration {
        display: block;
    }
}

/* Overlay tipis, hanya buat bantu kontras teks — bukan wash tebal */
.bg-overlay {
    display: none;
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to right,
        rgba(255, 255, 255, 0.55) 0%,
        rgba(255, 255, 255, 0.38) 22%,
        rgba(255, 255, 255, 0.12) 42%,
        rgba(255, 255, 255, 0) 60%
    );
    z-index: 1;
}

@media (min-width: 1024px) {
    .bg-overlay {
        display: block;
    }
}

/* --- KIRI: TEKS & BRAND (desktop) --- */
.panel-left {
    display: none;
    width: 55%;
    flex-direction: column;
    justify-content: center;
    position: relative;
    z-index: 2;
    padding: 4rem 6rem;
}

@media (min-width: 1024px) {
    .panel-left {
        display: flex;
    }
}

.brand-top {
    position: absolute;
    top: 3rem;
    left: 6rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.logo-img {
    width: 4.5rem;
    height: 4.5rem;
    object-fit: contain;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
    padding: 0.25rem;
    background: #fff;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.12);
}

.brand-text {
    font-weight: 800;
    font-size: 1.5rem;
    color: #1e40af;
    letter-spacing: -0.025em;
    line-height: 1.15;
    text-shadow: 0 1px 3px rgba(255, 255, 255, 0.85), 0 0 18px rgba(255, 255, 255, 0.65);
}

.hero-content {
    width: 100%;
    z-index: 10;
    margin-top: 2rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.1;
    letter-spacing: -0.025em;
    margin-bottom: 1rem;
    text-shadow: 0 2px 6px rgba(255, 255, 255, 0.85), 0 0 32px rgba(255, 255, 255, 0.7);
}

.text-accent {
    color: #2563eb;
}

.hero-subtitle {
    font-size: 1rem;
    color: #475569;
    margin-bottom: 2rem;
    font-weight: 500;
    line-height: 1.625;
    max-width: 32rem;
    text-shadow: 0 1px 4px rgba(255, 255, 255, 0.9), 0 0 16px rgba(255, 255, 255, 0.8);
}

/* --- KANAN: PANEL FORM LOGIN --- */
.panel-right {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    position: relative;
    z-index: 2;
    background: #f8fafc;
}

@media (min-width: 1024px) {
    .panel-right {
        width: 45%;
        background: transparent;
    }
}

.login-box {
    width: 100%;
    max-width: 400px;
    background: #fff;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.15);
    border: 1px solid #e2e8f0;
}

/* Brand Khusus Mobile */
.mobile-brand {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}

@media (min-width: 1024px) {
    .mobile-brand {
        display: none;
    }
}

.logo-img-mobile {
    width: 5rem;
    height: 5rem;
    object-fit: contain;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
    padding: 0.375rem;
}

.brand-text-mobile {
    font-weight: 700;
    font-size: 1.5rem;
    color: #1e40af;
    letter-spacing: -0.025em;
}

/* Badge Modul */
.module-info {
    display: flex;
    align-items: flex-start;
    gap: 0.875rem;
    background: #eff6ff;
    border: 1px solid #dbeafe;
    border-radius: 0.875rem;
    padding: 1rem;
    margin-bottom: 1.5rem;
}

.module-icon {
    flex-shrink: 0;
    width: 2.75rem;
    height: 2.75rem;
    border-radius: 50%;
    background: #dbeafe;
    color: #2563eb;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.125rem;
}

.module-text {
    flex: 1;
}

.form-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: #1e293b;
    margin: 0 0 0.125rem 0;
    text-align: left;
}

.module-desc {
    font-size: 0.8125rem;
    color: #64748b;
    line-height: 1.4;
    margin: 0;
}

/* Form Styling */
.login-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.input-group {
    position: relative;
    width: 100%;
}

.input-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
    font-size: 1rem;
    pointer-events: none;
}

.form-input {
    width: 100%;
    border-radius: 0.75rem;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    padding: 0.875rem 1rem;
    font-size: 0.9375rem;
    color: #334155;
    transition: all 0.2s;
    outline: none;
    font-family: inherit;
}

.form-input.pl-icon {
    padding-left: 2.75rem;
}

.form-input.pr-icon {
    padding-right: 3rem;
}

.form-input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    background: #fff;
}

.btn-toggle-pass {
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    font-size: 1.125rem;
    width: auto !important;
    height: auto !important;
    padding: 0.25rem !important;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    z-index: 10;
}

.btn-toggle-pass:hover {
    color: #475569;
}

/* Lupa Kata Sandi */
.forgot-pass-wrap {
    display: flex;
    justify-content: flex-end;
}

.forgot-pass-link {
    font-size: 0.8125rem;
    color: #2563eb;
    font-weight: 600;
    cursor: pointer;
    user-select: none;
}

.forgot-pass-link:hover {
    color: #1d4ed8;
    text-decoration: underline;
}

/* Error Message */
.error-msg {
    background: #fef2f2;
    border: 1px solid #fee2e2;
    color: #dc2626;
    font-size: 0.875rem;
    line-height: 1.5;
    border-radius: 0.75rem;
    padding: 0.75rem 1rem;
    margin: 0;
    white-space: pre-line;
}

/* Tombol Submit */
.btn-submit {
    width: 100%;
    background: #2563eb;
    color: #fff;
    border: none;
    border-radius: 0.75rem;
    padding: 0.875rem;
    font-size: 1.0625rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.2s;
    margin-top: 0.5rem;
    font-family: inherit;
    display: flex;
    justify-content: center;
    align-items: center;
}

.btn-submit:hover:not(:disabled) {
    background: #1d4ed8;
}

.btn-submit:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.divider {
    border-bottom: 1px solid #e2e8f0;
    width: 100%;
    margin: 1.5rem 0 1.25rem 0;
}

/* Register Link & Text Bawah */
.register-link-wrap {
    text-align: center;
    font-size: 0.875rem;
    color: #64748b;
    font-weight: 500;
    margin: 0;
    line-height: 1.5;
}

.register-link {
    color: #2563eb;
    font-weight: 700;
    text-decoration: none;
    transition: color 0.2s;
}

.register-link:hover {
    color: #1d4ed8;
}

.session-warning {
    margin-top: 1.25rem;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
    font-size: 0.75rem;
    color: #94a3b8;
    text-align: center;
    line-height: 1.5;
}

.footer-note {
    position: absolute;
    bottom: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.375rem;
    color: #475569;
    font-size: 0.875rem;
    font-weight: 500;
    background: rgba(255, 255, 255, 0.85);
    padding: 0.5rem 1.125rem;
    border-radius: 999px;
    backdrop-filter: blur(4px);
}

/* --- ANIMASI --- */
.animate-fade-in {
    animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (prefers-reduced-motion: reduce) {
    .animate-fade-in {
        animation: none;
    }
}
</style>