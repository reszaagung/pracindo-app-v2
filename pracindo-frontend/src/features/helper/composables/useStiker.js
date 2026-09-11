import { ref, reactive } from 'vue'

const hurufAktif = ref(null)
const formData = reactive({
    A: { nama_item: '', tipe: '', lot: null, net: null, is_saved: false },
    B: { nama_item: '', tipe: '', lot: null, net: null, is_saved: false },
    C: { nama_item: '', tipe: '', lot: null, net: null, is_saved: false },
    D: { nama_item: '', tipe: '', lot: null, net: null, is_saved: false },
})

export function useStiker() {
    const setHurufAktif = (huruf) => {
        hurufAktif.value = huruf
        setTimeout(() => {
            const formElement = document.getElementById('form-input-stiker')
            if (formElement) {
                formElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
            }
        }, 100)
    }

    const tutupForm = () => {
        hurufAktif.value = null
    }

    const resetData = () => {
        hurufAktif.value = null
        Object.keys(formData).forEach(key => {
            formData[key] = { nama_item: '', tipe: '', lot: null, net: null, is_saved: false }
        })
    }

    return {
        hurufAktif,
        formData,
        setHurufAktif,
        tutupForm,
        resetData
    }
}