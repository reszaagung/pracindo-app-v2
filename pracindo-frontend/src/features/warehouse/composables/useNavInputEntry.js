import { ref } from 'vue'

const judulHeader = ref('Input Entry')
const breadcrumb = ref('')

const menus = [
    {
        id: 'goods-receipt',
        label: 'Penerimaan',
        ikon: 'pi-download',
        rute: '/warehouse/input/receipt',
        activate: true,
    },
    {
        id: 'packing',
        label: 'Input Packing',
        ikon: 'pi-box',
        rute: '/warehouse/input/packing',
        activate: true,
    },
    {
        id: 'discrepancy',
        label: 'Selisih / Retur',
        ikon: 'pi-exclamation-triangle',
        rute: '/warehouse/input/discrepancy',
        activate: true,
    },
    {
        id: 'qc',
        label: 'Inspeksi QC',
        ikon: 'pi-check-square',
        rute: '/warehouse/input/qc',
        activate: true,
    },
]

export function useNavInputEntry() {
    const setNavInfo = (judulBaru, breadcrumbBaru = '') => {
        judulHeader.value = judulBaru || 'Input Entry'
        breadcrumb.value = breadcrumbBaru || ''
    }

    const resetNav = () => {
        judulHeader.value = 'Input Entry'
        breadcrumb.value = ''
    }

    return {
        menus,
        judulHeader,
        breadcrumb,
        setNavInfo,
        resetNav,
    }
}