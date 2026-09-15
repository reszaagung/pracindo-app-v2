<template>
  <div class="page-wrapper">
    <div class="modern-container">
      <div 
        v-for="(item, index) in items" 
        :key="index" 
        class="modern-box"
        :class="[`box-${item.toLowerCase()}`, { 'box-aktif': hurufAktif === item }]"
        @click="setHurufAktif(item)"
      >
        {{ item }}
        <span v-if="formData[item]?.is_saved" class="badge-tersimpan">
          <i class="pi pi-check"></i>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStiker } from '../../composables/useStiker'

const items = ref(['A', 'A', 'A', 'A'])
const { formData, hurufAktif, setHurufAktif } = useStiker()
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&display=swap');

.page-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  font-family: 'Inter', sans-serif;
}

.modern-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 320px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05), 
              inset 0 1px 0 rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.modern-box {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: clamp(56px, 22vw, 100px);
  border-radius: 14px;
  color: #ffffff;
  font-size: clamp(1.5rem, 9vw, 4rem);
  font-weight: 800;
  cursor: pointer;
  user-select: none;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.modern-box:hover { transform: translateY(-5px) scale(1.02); }
.modern-box:active { transform: translateY(2px) scale(0.98); }

.box-aktif { outline: 3px solid #1e293b; outline-offset: 2px; }

.badge-tersimpan {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 28px;
  height: 28px;
  background: #ffffff;
  border: 2px solid #10b981;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.badge-tersimpan .pi-check { color: #10b981; font-size: 0.85rem; }

.box-a {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  box-shadow: 0 10px 20px rgba(79, 172, 254, 0.3), inset 0 -3px 0 rgba(0, 0, 0, 0.1);
}
.box-a:hover { box-shadow: 0 15px 25px rgba(79, 172, 254, 0.4), inset 0 -3px 0 rgba(0, 0, 0, 0.1); }
</style>