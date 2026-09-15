import { ref, reactive } from 'vue'

const DAFTAR_HURUF = ['A','B','C','D','E','F','G','H','I','J','K','L']

const hurufAktif = ref(null)
const formData = reactive(
    Object.fromEntries(DAFTAR_HURUF.map(h => [h, { nama_item: null, tipe: '', lot: null, net: null, is_saved: false }]))
)

export function useStikerKecil12() {
    const setHurufAktif = (huruf) => {
        hurufAktif.value = huruf
        setTimeout(() => {
            const formElement = document.getElementById('form-input-stiker-kecil-12')
            if (formElement) {
                formElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
            }
        }, 100)
    }

    const tutupForm = () => { hurufAktif.value = null }

    const resetData = () => {
        hurufAktif.value = null
        DAFTAR_HURUF.forEach(h => {
            formData[h] = { nama_item: null, tipe: '', lot: null, net: null, is_saved: false }
        })
    }

    return { hurufAktif, formData, setHurufAktif, tutupForm, resetData, DAFTAR_HURUF }
}