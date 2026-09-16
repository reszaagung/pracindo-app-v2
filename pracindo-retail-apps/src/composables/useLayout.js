import { ref } from 'vue'
import { useRouter } from 'vue-router'

const isSidebarOpen = ref(false)

export function useLayout() {
    const router = useRouter()

    const toggleSidebar = () => {
        isSidebarOpen.value = !isSidebarOpen.value
    }

    const closeSidebar = () => {
        isSidebarOpen.value = false
    }

    const prosesLogout = () => {
        const konfirmasi = confirm("Apakah Anda yakin ingin keluar dari sistem?")
        if (konfirmasi) {
            localStorage.removeItem('retail_access_token')
            localStorage.removeItem('retail_refresh_token')
            localStorage.removeItem('retail_user_data')

            router.push('/login')
        }
    }

    return {
        isSidebarOpen,
        toggleSidebar,
        closeSidebar,
        prosesLogout
    }
}