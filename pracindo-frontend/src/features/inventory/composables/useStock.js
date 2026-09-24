import {
    computed,
    onMounted,
    onUnmounted,
    ref,
} from 'vue'

import api from '@/utils/api'
import { bacaError } from '@/utils/error'


export function useStock() {
    /* =========================================================
       STOK UMUM
    ========================================================= */

    const daftarStok = ref([])
    const stokDetail = ref(null)
    const daftarMutasi = ref([])

    const loadingStok = ref(false)
    const loadingDetail = ref(false)
    const loadingMutasi = ref(false)

    const galat = ref('')


    /* =========================================================
       POOL KEMASAN
    ========================================================= */

    const poolKemasan = ref([])
    const totalNilaiPoolKemasan = ref(0)

    const loadingPoolKemasan = ref(false)
    const galatPoolKemasan = ref('')
    const terakhirDiperbaruiPoolKemasan = ref('')

    const cariPoolKemasan = ref('')
    const filterKategoriPoolKemasan = ref('SEMUA')

    const poolKemasanRealtimeAktif = ref(false)

    let intervalPoolKemasan = null
    let poolKemasanSedangRequest = false


    /* =========================================================
       STATUS LOADING
    ========================================================= */

    const sedangProses = computed(() => {
        return (
            loadingStok.value ||
            loadingDetail.value ||
            loadingMutasi.value
        )
    })


    /* =========================================================
       MUAT STOK
    ========================================================= */

const muatStok = async (params = {}) => {
    if (params.lapis === 'KEMASAN') {
        await muatPoolKemasan()
        return
    }

    loadingStok.value = true
    galat.value = ''

    try {
        if (params.lapis === 'ENTITAS') {
            const { data } = await api.get(
                'inventory/mutasi/rekap/',
                { params }
            )

            daftarStok.value =
                data?.entitas || []

        } else if (params.lapis === 'POOL') {
            const { data } = await api.get(
                'inventory/pool/',
                { params }
            )

            daftarStok.value =
                data?.rincian || []

        } else if (params.lapis === 'JADI') {
            const { data } = await api.get(
                'inventory/barang-jadi/',
                { params }
            )

            daftarStok.value =
                data?.rincian ||
                data?.results ||
                data ||
                []

        } else {
            daftarStok.value = []
        }
    } catch (err) {
        console.error(
            'Gagal memuat data persediaan:',
            err
        )

        daftarStok.value = []

        galat.value = bacaError(
            err,
            'Gagal memuat data persediaan stok.'
        )
    } finally {
        loadingStok.value = false
    }
}


const muatPoolKemasan = async (
    silent = false
) => {
    if (poolKemasanSedangRequest) {
        return
    }

    poolKemasanSedangRequest = true

    if (!silent) {
        loadingPoolKemasan.value = true
    }

    galatPoolKemasan.value = ''

    try {
        const response = await api.get(
            'inventory/pool/kemasan/'
        )

        const data = response?.data

        /* =====================================================
           PAYLOAD DEBUG
        ====================================================== */

        console.group(
            '%c[POOL KEMASAN]',
            'color:#059669;font-weight:bold'
        )

        console.log(
            'URL:',
            response?.config?.url
        )

        console.log(
            'STATUS:',
            response?.status
        )

        console.log(
            'PAYLOAD RAW:',
            data
        )

        console.log(
            'TIPE:',
            Array.isArray(data)
                ? 'ARRAY'
                : typeof data
        )

        if (Array.isArray(data)) {
            console.table(data)
        }

        console.groupEnd()


        /* =====================================================
           NORMALISASI PAYLOAD
        ====================================================== */

        const rincian = Array.isArray(data)
            ? data
            : Array.isArray(data?.rincian)
                ? data.rincian
                : Array.isArray(data?.results)
                    ? data.results
                    : []


        poolKemasan.value = rincian


        /* =====================================================
           TOTAL NILAI
        ====================================================== */

        if (
            data &&
            !Array.isArray(data) &&
            data.total_nilai_pool !== undefined
        ) {
            totalNilaiPoolKemasan.value =
                Number(
                    data.total_nilai_pool || 0
                )
        } else {
            totalNilaiPoolKemasan.value =
                rincian.reduce(
                    (total, item) =>
                        total +
                        Number(
                            item.nilai || 0
                        ),
                    0
                )
        }


        /* =====================================================
           UPDATE TIME
        ====================================================== */

        terakhirDiperbaruiPoolKemasan.value =
            new Date().toLocaleTimeString(
                'id-ID',
                {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                }
            )

    } catch (err) {
        console.error(
            '[POOL KEMASAN] ERROR:',
            err
        )

        console.error(
            '[POOL KEMASAN] RESPONSE:',
            err?.response?.data
        )

        galatPoolKemasan.value =
            bacaError(
                err,
                'Gagal memuat data pool kemasan.'
            )
    } finally {
        poolKemasanSedangRequest = false

        if (!silent) {
            loadingPoolKemasan.value = false
        }
    }
}


    const kategoriPoolKemasan = computed(() => {
        const daftar = new Set()

        poolKemasan.value.forEach(
            item => {
                const kategori =
                    item.kategori_label ||
                    item.kategori

                if (kategori) {
                    daftar.add(
                        String(kategori)
                    )
                }
            }
        )

        return Array.from(
            daftar
        ).sort()
    })


    /* =========================================================
       FILTER POOL KEMASAN
    ========================================================= */

    const poolKemasanTampil =
        computed(() => {
            let hasil = [
                ...poolKemasan.value,
            ]

            const keyword =
                cariPoolKemasan.value
                    .toLowerCase()
                    .trim()

            if (keyword) {
                hasil =
                    hasil.filter(
                        item => {
                            const kode =
                                String(
                                    item.produk_kode ||
                                    ''
                                ).toLowerCase()

                            const nama =
                                String(
                                    item.produk_nama ||
                                    ''
                                ).toLowerCase()

                            return (
                                kode.includes(
                                    keyword
                                ) ||
                                nama.includes(
                                    keyword
                                )
                            )
                        }
                    )
            }

            if (
                filterKategoriPoolKemasan.value !==
                'SEMUA'
            ) {
                hasil =
                    hasil.filter(
                        item => {
                            const kategori =
                                String(
                                    item.kategori_label ||
                                    item.kategori ||
                                    ''
                                )

                            return (
                                kategori ===
                                filterKategoriPoolKemasan.value
                            )
                        }
                    )
            }

            return hasil
        })


    /* =========================================================
       REALTIME POOL KEMASAN
    ========================================================= */

    const mulaiRealtimePoolKemasan = () => {
        berhentiRealtimePoolKemasan()

        poolKemasanRealtimeAktif.value = true

        intervalPoolKemasan =
            window.setInterval(
                () => {
                    if (
                        !poolKemasanRealtimeAktif.value ||
                        document.hidden
                    ) {
                        return
                    }

                    muatPoolKemasan(true)
                },
                3000
            )
    }


    const berhentiRealtimePoolKemasan = () => {
        poolKemasanRealtimeAktif.value = false

        if (
            intervalPoolKemasan !== null
        ) {
            window.clearInterval(
                intervalPoolKemasan
            )

            intervalPoolKemasan = null
        }
    }


    const handleVisibilityPoolKemasan =
        () => {
            if (
                !poolKemasanRealtimeAktif.value
            ) {
                return
            }

            if (!document.hidden) {
                muatPoolKemasan(true)
            }
        }


    /* =========================================================
       DETAIL STOK
    ========================================================= */

    const muatStokDetail = async (
        id,
        params = {}
    ) => {
        if (!id) {
            stokDetail.value = null

            galat.value =
                'ID stok tidak ditemukan.'

            return
        }

        loadingDetail.value = true
        galat.value = ''

        try {
            stokDetail.value = null

            const { data } = await api.get(
                `inventory/stok/${id}/`,
                { params }
            )

            stokDetail.value =
                data || null
        } catch (err) {
            console.error(
                'Gagal memuat detail stok:',
                err
            )

            stokDetail.value = null

            galat.value = bacaError(
                err,
                'Gagal memuat detail stok.'
            )
        } finally {
            loadingDetail.value = false
        }
    }


    /* =========================================================
       MUTASI
    ========================================================= */

    const muatMutasi = async (
        params = {}
    ) => {
        loadingMutasi.value = true
        galat.value = ''

        try {
            daftarMutasi.value = []

            const { data } = await api.get(
                'inventory/mutasi/',
                { params }
            )

            daftarMutasi.value =
                data?.results ||
                data ||
                []
        } catch (err) {
            console.error(
                'Gagal memuat riwayat mutasi:',
                err
            )

            daftarMutasi.value = []

            galat.value = bacaError(
                err,
                'Gagal memuat riwayat mutasi.'
            )
        } finally {
            loadingMutasi.value = false
        }
    }


    /* =========================================================
       LIFECYCLE
    ========================================================= */

    onMounted(() => {
        document.addEventListener(
            'visibilitychange',
            handleVisibilityPoolKemasan
        )
    })


    onUnmounted(() => {
        berhentiRealtimePoolKemasan()

        document.removeEventListener(
            'visibilitychange',
            handleVisibilityPoolKemasan
        )
    })


    /* =========================================================
       RETURN
    ========================================================= */

    return {
        /* STOK */
        daftarStok,
        stokDetail,
        daftarMutasi,

        sedangProses,
        loadingStok,
        loadingDetail,
        loadingMutasi,

        galat,

        muatStok,
        muatStokDetail,
        muatMutasi,

        /* POOL KEMASAN */
        poolKemasan,
        totalNilaiPoolKemasan,

        loadingPoolKemasan,
        galatPoolKemasan,
        terakhirDiperbaruiPoolKemasan,

        cariPoolKemasan,
        filterKategoriPoolKemasan,
        kategoriPoolKemasan,
        poolKemasanTampil,

        muatPoolKemasan,
        mulaiRealtimePoolKemasan,
        berhentiRealtimePoolKemasan,

        poolKemasanRealtimeAktif,
    }
}
