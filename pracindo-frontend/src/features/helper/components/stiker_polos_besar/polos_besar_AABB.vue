<template>
  <div class="page-wrapper">
    <div class="modern-container">
      <!-- Mengiterasi array items dan menerapkan class warna dinamis berdasarkan nilai item -->
      <div 
        v-for="(item, index) in items" 
        :key="index" 
        class="modern-box"
        :class="item === 'A' ? 'box-blue' : 'box-green'"
      >
        {{ item }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Data reaktif berisi A, A, B, B
const items = ref(['A', 'A', 'B', 'B'])
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&display=swap');

/* Pembungkus halaman / centered layout */
.page-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f3f4f6;
  font-family: 'Inter', sans-serif;
}

/* Kontainer Kartu (Glassmorphism) */
.modern-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 320px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05), 
              inset 0 1px 0 rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

/* Styling Dasar Kotak */
.modern-box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  border-radius: 16px;
  color: #ffffff;
  font-size: 4rem;
  font-weight: 800;
  cursor: pointer;
  user-select: none;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* Efek Interaktif Saat Hover & Klik */
.modern-box:hover {
  transform: translateY(-5px) scale(1.02);
}

.modern-box:active {
  transform: translateY(2px) scale(0.98);
}

/* --- Variasi Warna Biru (Untuk "A") --- */
.box-blue {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  box-shadow: 0 10px 20px rgba(79, 172, 254, 0.3), 
              inset 0 -3px 0 rgba(0, 0, 0, 0.1);
}

.box-blue:hover {
  box-shadow: 0 15px 25px rgba(79, 172, 254, 0.4), 
              inset 0 -3px 0 rgba(0, 0, 0, 0.1);
}

/* --- Variasi Warna Hijau (Untuk "B") --- */
.box-green {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  box-shadow: 0 10px 20px rgba(67, 233, 123, 0.3), 
              inset 0 -3px 0 rgba(0, 0, 0, 0.1);
}

.box-green:hover {
  box-shadow: 0 15px 25px rgba(67, 233, 123, 0.4), 
              inset 0 -3px 0 rgba(0, 0, 0, 0.1);
}
</style>