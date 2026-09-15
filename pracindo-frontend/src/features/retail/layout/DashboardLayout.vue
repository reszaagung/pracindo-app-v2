<template>
  <div class="dashboard-container">
    <!-- Overlay Transparan untuk Mobile (Menutup sidebar jika area luar diklik) -->
    <div 
      v-if="isSidebarOpen" 
      class="sidebar-overlay"
      @click="toggleSidebar"
    ></div>

    <!-- Sidebar Menu -->
    <aside :class="['sidebar', { 'open': isSidebarOpen }]">
      <div class="sidebar-brand">
        <h3>Pracindo Retail</h3>
        <button class="btn-close-sidebar" @click="toggleSidebar">✕</button>
      </div>
      
      <nav class="sidebar-nav">
        <!-- Gunakan <router-link> jika menggunakan Vue Router -->
        <a href="#/pos" class="nav-item">💻 POS Kasir</a>
        <a href="#/penerimaan" class="nav-item">📦 Terima Barang</a>
        <a href="#/stok" class="nav-item">📊 Stok Gudang</a>
        <a href="#/piutang" class="nav-item">📒 Buku Piutang</a>
      </nav>

      <div class="sidebar-footer">
        <button class="btn-logout">🚪 Keluar</button>
      </div>
    </aside>

    <!-- Area Konten Utama -->
    <main class="main-content">
      <!-- Topbar (Header) -->
      <header class="topbar">
        <div class="topbar-left">
          <button class="btn-menu" @click="toggleSidebar">☰</button>
          <h4 class="page-title">Dashboard</h4>
        </div>
        <div class="topbar-right">
          <span class="user-badge">👤 Kasir Aktif</span>
        </div>
      </header>

      <!-- Slot Dinamis untuk Komponen Halaman (misal: PenerimaanBarang.vue) -->
      <div class="content-wrapper">
        <slot></slot>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isSidebarOpen = ref(false);

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};
</script>

<style scoped>
/* Variabel Warna & Ukuran */
:root {
  --sidebar-width: 250px;
  --topbar-height: 60px;
  --bg-color: #f4f6f9;
  --primary-color: #2c3e50;
  --hover-color: #34495e;
}

.dashboard-container {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-color);
  overflow-x: hidden;
}

/* --- SIDEBAR --- */
.sidebar {
  width: var(--sidebar-width);
  background-color: var(--primary-color);
  color: white;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  z-index: 1000;
  transition: transform 0.3s ease-in-out;
}

.sidebar-brand {
  height: var(--topbar-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  background-color: #1a252f;
}

.btn-close-sidebar {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
}

.sidebar-nav {
  flex: 1;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
}

.nav-item {
  padding: 12px 20px;
  color: #adb5bd;
  text-decoration: none;
  transition: 0.2s;
}

.nav-item:hover, .nav-item.active {
  background-color: var(--hover-color);
  color: white;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #34495e;
}

.btn-logout {
  width: 100%;
  padding: 10px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* --- MAIN CONTENT & TOPBAR --- */
.main-content {
  flex: 1;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s ease-in-out;
  width: 100%;
}

.topbar {
  height: var(--topbar-height);
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.btn-menu {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.content-wrapper {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.sidebar-overlay {
  display: none;
}

/* --- ADAPTASI MOBILE (Media Query) --- */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%); /* Sembunyikan sidebar ke kiri */
  }
  
  .sidebar.open {
    transform: translateX(0); /* Munculkan saat state open */
  }
  
  .btn-close-sidebar {
    display: block; /* Tampilkan tombol silang di mobile */
  }

  .main-content {
    margin-left: 0; /* Penuhi layar */
  }

  .btn-menu {
    display: block; /* Tampilkan tombol hamburger */
  }

  .sidebar-overlay {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0,0,0,0.5);
    z-index: 999;
  }
}
</style>