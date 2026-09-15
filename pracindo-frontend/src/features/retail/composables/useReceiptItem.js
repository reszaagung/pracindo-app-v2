import { ref, onMounted } from 'vue';
import axios from 'axios';

export function useReceiptItem(dokumen, emit) {
  const isLoading = ref(false);
  const localItems = ref([]);

  onMounted(() => {
    localItems.value = dokumen.items.map(item => ({
      ...item,
      unit_diterima: item.unit_diterima === 0 ? item.unit_dikirim : item.unit_diterima
    }));
  });

  const formatTanggal = (isoString) => {
    if (!isoString) return '-';
    return new Date(isoString).toLocaleDateString('id-ID', {
      day: '2-digit', month: 'short', year: 'numeric'
    });
  };

  const submitPenerimaan = async () => {
    const adaMinus = localItems.value.some(item => item.unit_diterima < 0);
    if (adaMinus) {
      alert("Jumlah barang diterima tidak boleh kurang dari 0.");
      return;
    }

    isLoading.value = true;
    try {
      const payload = {
        items: localItems.value.map(item => ({
          id: item.id,
          unit_diterima: item.unit_diterima
        }))
      };

      await axios.post(`/api/retail/penerimaan/${dokumen.id}/proses/`, payload);
      emit('sukses'); 
    } catch (error) {
      console.error("Gagal memproses penerimaan:", error);
      alert("Terjadi kesalahan sistem saat menyimpan data.");
    } finally {
      isLoading.value = false;
    }
  };

  return {
    localItems,
    isLoading,
    formatTanggal,
    submitPenerimaan
  };
}