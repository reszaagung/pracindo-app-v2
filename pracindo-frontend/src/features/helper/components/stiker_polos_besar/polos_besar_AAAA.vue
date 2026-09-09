<template>
  <div class="outer-container">
    <!-- Menggunakan v-for untuk membuat 4 kotak secara dinamis -->
    <div v-for="n in 4" :key="n" class="blue-box">
      A
    </div>
  </div>
</template>

<script setup>
// Anda bisa menambahkan state atau logika di sini jika nantinya diperlukan.
// Untuk tampilan statis ini, script bisa dibiarkan kosong.
</script>

<style scoped>
/* Kontainer paling luar dengan border tipis dan padding putih */
.outer-container {
  display: flex;
  flex-direction: column;
  width: 300px; /* Lebar bisa disesuaikan */
  padding: 8px; /* Jarak putih antara border luar dan kotak hitam-biru */
  border: 1px solid #000; /* Border tipis di bagian paling luar */
  background-color: #fff;
  box-sizing: border-box;
}

/* Styling untuk masing-masing kotak biru */
.blue-box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px; /* Tinggi masing-masing kotak */
  background-color: #3cb4ff; /* Warna biru terang yang senada dengan gambar */
  border: 5px solid #000; /* Border hitam tebal */
  color: #fff; /* Warna huruf putih */
  font-size: 4.5rem; /* Ukuran huruf besar */
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bold;
  box-sizing: border-box;
}

/* Mencegah border ganda yang terlalu tebal di antara kotak (opsional, sesuaikan dengan preferensi) */
.blue-box + .blue-box {
  margin-top: -5px; 
}
</style>