import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNavInputEntry } from './useNavInputEntry'

const TAB_BAHAN_BAKU = 'bahan_baku'
const TAB_KEMASAN = 'kemasan'

export function useReceiptIndex() {
    const route = useRoute()
    const router = useRouter()
    const { setNavInfo, resetNav } = useNavInputEntry()

    const getTabFromRoute = () => {
        return route.query.tab === TAB_KEMASAN
            ? TAB_KEMASAN
            : TAB_BAHAN_BAKU
    }

    const tabAktif = ref(getTabFromRoute())

    const ubahTab = async (tabBaru) => {
        const tabValid = [TAB_BAHAN_BAKU, TAB_KEMASAN].includes(tabBaru)

        if (!tabValid || tabAktif.value === tabBaru) {
            return
        }

        tabAktif.value = tabBaru

        await router.replace({
            query: {
                ...route.query,
                tab: tabBaru,
            },
        })
    }

    watch(
        () => route.query.tab,
        () => {
            tabAktif.value = getTabFromRoute()
        }
    )

    onMounted(() => {
        setNavInfo(
            'Penerimaan Barang',
            'Warehouse > Penerimaan > Index'
        )
    })

    onUnmounted(() => {
        resetNav()
    })

    return {
        tabAktif,
        ubahTab,
    }
}