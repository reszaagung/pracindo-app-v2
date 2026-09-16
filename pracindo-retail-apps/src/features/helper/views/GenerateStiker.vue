<script setup>
import { ref, reactive, computed, shallowRef, defineAsyncComponent, watch } from 'vue'
import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Calendar from 'primevue/calendar'
import { useToast } from 'primevue/usetoast'

// 1. Import Composable yang sudah kita perbaiki
import { useSticker } from '../composables/useSticker'

const toast = useToast()

// 2. Destructure state dan fungsi dari useSticker
const { sedangProses, galat, hasilCetak, buatDanCetakStiker } = useSticker()

const opsiJenis = [
    { label: 'Polos Besar', value: 'polos_besar' },
    { label: 'CV Besar', value: 'cv_besar' }
]

const masterTemplates = {
    polos_besar: [
        { id: 1, nama_file: 'stiker_polos_besar_AAAA', pola: 'AAAA', jumlah_input: 1 },
        { id: 2, nama_file: 'stiker_polos_besar_AAAB', pola: 'AAAB', jumlah_input: 2 },
        { id: 3, nama_file: 'stiker_polos_besar_AABB', pola: 'AABB', jumlah_input: 2 },
        { id: 4, nama_file: 'stiker_polos_besar_AABC', pola: 'AABC', jumlah_input: 3 },
        { id: 5, nama_file: 'stiker_polos_besar_ABCD', pola: 'ABCD', jumlah_input: 4 },
    ],
    cv_besar: [
        { id: 6, nama_file: 'stiker_cv_besar_AAAA', pola: 'AAAA', jumlah_input: 1 },
        { id: 7, nama_file: 'stiker_cv_besar_AAAC', pola: 'AAAC', jumlah_input: 2 },
        { id: 8, nama_file: 'stiker_cv_besar_AABB', pola: 'AABB', jumlah_input: 2 },
        { id: 9, nama_file: 'stiker_cv_besar_AABC', pola: 'AABC', jumlah_input: 3 },
        { id: 10, nama_file: 'stiker_cv_besar_ABCD', pola: 'ABCD', jumlah_input: 4 },
    ]
}

const fileTerpilih = ref(null)
const PreviewComponent = shallowRef(null)

const form = reactive({
    jenis: null,
    items: []
})

const getPolaFromFilename = (filename) => {
    const cleanName = filename.replace('.docx', '')
    const parts = cleanName.split('_')
    return parts[parts.length - 1].toUpperCase()
}

const daftarFileAktif = computed(() => {
    if (!form.jenis) return []
    return (masterTemplates[form.jenis] || []).map(file => ({
        ...file,
        pola: file.pola || getPolaFromFilename(file.nama_file)
    }))
})

const resetPilihan = () => {
    fileTerpilih.value = null
    form.items = []
    PreviewComponent.value = null
}

const pilihFile = (file) => {
    fileTerpilih.value = file
    form.items = Array.from({ length: file.jumlah_input }, () => ({
        nama_item: '',
        tipe: '',
        lot: null,
        net: null
    }))

    const folderJenis = form.jenis
    const namaKomponen = `${folderJenis}_${file.pola}`

    // 3. Perbaikan Path Import Dinamis
    PreviewComponent.value = defineAsyncComponent(() =>
        import(`../components/stiker_besar/${namaKomponen}.vue`)
            .catch(() => ({ template: '<div class="text-slate-400 text-xs text-center p-4">File komponen preview (<b>' + namaKomponen + '.vue</b>) belum dibuat.</div>' }))
    )
}

const formatTanggalLokal = (date) => {
    if (!date) return null
    const tahun = date.getFullYear()
    const bulan = String(date.getMonth() + 1).padStart(2, '0')
    const hari = String(date.getDate()).padStart(2, '0')
    return `${tahun}-${bulan}-${hari}`
}

const validasiForm = () => {
    for (const [idx, item] of form.items.entries()) {
        const netKosong = item.net === null || item.net === undefined
        if (!item.nama_item?.trim() || !item.tipe?.trim() || !item.lot || netKosong) {
            toast.add({
                severity: 'warn',
                summary: 'Data belum lengkap',
                detail: `Grup Input ${idx + 1} masih ada field yang kosong`,
                life: 3000
            })
            return false
        }
    }
    return true
}

const submitStiker = async () => {
    if (!fileTerpilih.value || sedangProses.value) return
    if (!validasiForm()) return

    const payload = {
        jenis: form.jenis,
        template_id: fileTerpilih.value.id,
        items: form.items.map(item => ({
            nama_item: item.nama_item,
            tipe: item.tipe,
            lot: formatTanggalLokal(item.lot),
            net: item.net
        }))
    }

    // 4. Eksekusi fungsi dari composable, bukan nembak api langsung
    await buatDanCetakStiker(payload)

    if (galat.value) {
        toast.add({ severity: 'error', summary: 'Gagal', detail: galat.value, life: 5000 })
    }
}

// 5. Watcher untuk otomatis membuka PDF ketika polling berhasil
watch(hasilCetak, (newVal) => {
    if (newVal && newVal.file_hasil) {
        toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Stiker berhasil dibuat!', life: 3000 })
        window.open(newVal.file_hasil, '_blank')
    }
})
</script>