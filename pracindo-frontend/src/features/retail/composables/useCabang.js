import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { retailApi } from '../api'

export function useCabang() {
  const router = useRouter()
  const isLoading = ref(false)
  const errors = ref({}) 

  const simpanCabang = async (formPayload) => {
    isLoading.value = true
    errors.value = {}
    
    try {
      await retailApi.createCabang(formPayload)
      alert('Cabang dan akun login berhasil didaftarkan!')
      router.push('/retail')
    } catch (error) {
      if (error.response && error.response.status === 400) {
        errors.value = error.response.data
      } else {
        alert("Terjadi kesalahan sistem. Pastikan Username atau Kode Cabang belum digunakan.")
      }
    } finally {
      isLoading.value = false
    }
  }

  return { isLoading, errors, simpanCabang }
}