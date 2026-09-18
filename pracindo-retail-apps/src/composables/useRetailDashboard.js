import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export function useRetailDashboard() {
    const router = useRouter()
    const pengguna = ref(null)

    // 1. Logika Tarik Profil dari LocalStorage
    const muatProfil = () => {
        const userData = localStorage.getItem('retail_user')
        if (userData) {
            pengguna.value = JSON.parse(userData)
        }
    }

    // 2. Logika Sapaan Dinamis berdasarkan Jam
    const waktuSapaan = computed(() => {
        const jam = new Date().getHours()
        if (jam < 11) return 'pagi'
        if (jam < 15) return 'siang'
        if (jam < 18) return 'sore'
        return 'malam'
    })

    // 3. Konfigurasi Daftar Modul Retail
    const daftarModul = ref([
        {
            id: 'pos',
            nama: 'Mesin Kasir (POS)',
            deskripsi: 'Antarmuka Point of Sale untuk melayani transaksi pelanggan.',
            ikon: 'pi pi-desktop',
            warnaBg: 'bg-blue',
            rute: '/kasir',
            siap: true
        },
        {
            id: 'riwayat',
            nama: 'Riwayat Transaksi',
            deskripsi: 'Cek struk, retur barang, dan pembatalan transaksi kasir.',
            ikon: 'pi pi-receipt',
            warnaBg: 'bg-green',
            rute: '/kasir/riwayat',
            siap: true
        },
        {
            id: 'pembukuan',
            nama: 'Pembukuan Cabang',
            deskripsi: 'Input jurnal, kas kecil, dan mutasi pengeluaran toko.',
            ikon: 'pi pi-book',
            warnaBg: 'bg-purple',
            rute: '/pembukuan/jurnal',
            siap: true
        },
        {
            id: 'stok',
            nama: 'Stok & Opname',
            deskripsi: 'Modul untuk cek stok warna dan stok opname harian cabang.',
            ikon: 'pi pi-box',
            warnaBg: 'bg-gray',
            rute: '',
            siap: false // Otomatis bikin kartu jadi redup dan ada tulisan SEGERA
        }
    ])

    // 4. Logika Logout
    const prosesLogout = () => {
        const konfirmasi = confirm("Apakah Anda yakin ingin keluar dari sistem?")
        if (konfirmasi) {
            localStorage.removeItem('retail_token')
            localStorage.removeItem('retail_user')
            router.push('/login')
        }
    }

    // Jalankan muatProfil saat komponen yang memakai composable ini di-mount
    onMounted(() => {
        muatProfil()
    })

    return {
        pengguna,
        waktuSapaan,
        daftarModul,
        prosesLogout
    }
}