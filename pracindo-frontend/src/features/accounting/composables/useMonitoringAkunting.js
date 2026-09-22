import {
    computed,
    onBeforeUnmount,
    onMounted,
    reactive,
    ref,
} from 'vue'

import { accountingApi } from '../api'

const REFRESH_MS = 30_000

export function useMonitoringAkunting() {
    const memuat = ref(false)
    const menyimpan = ref(false)
    const error = ref('')
    const terakhirDiperbarui = ref(null)
    const jamSekarang = ref(new Date())
    const autoRefresh = ref(true)

    const data = reactive({
        tanggal: null,
        peringatan_hari: 7,

        kas: {
            saldo_kas: 0,
            rekening: [],
        },

        tagihan: {
            ringkasan: {},
            data: [],
        },
    })

    const form = reactive({
        entitas: 'PT',
        kategori: '',
        keterangan: '',
        pemohon: '',
        nominal: '',
        bukti_nota: null,
    })

    let intervalRefresh = null
    let intervalJam = null

    function resetData() {
        data.tanggal = null
        data.peringatan_hari = 7

        data.kas = {
            saldo_kas: 0,
            rekening: [],
        }

        data.tagihan = {
            ringkasan: {},
            data: [],
        }
    }

    function normalisasiTagihan(response) {
        const list =
            response?.data ||
            response?.results ||
            []

        if (!Array.isArray(list)) {
            return []
        }

        return list.map((item) => ({
            ...item,

            id: item.id,

            supplier:
                item.supplier ||
                item.suplier ||
                item.nama_supplier ||
                '-',

            no_po:
                item.no_po ||
                item.nomor_po ||
                '-',

            sisa_hutang: Number(
                item.sisa_hutang ??
                item.sisa ??
                0,
            ),

            tanggal_jatuh_tempo:
                item.tanggal_jatuh_tempo ||
                item.jatuh_tempo ||
                null,

            hari_tersisa:
                item.hari_tersisa ??
                item.sisa_hari ??
                null,

            status_tempo:
                item.status_tempo ||
                item.status_monitoring ||
                'NORMAL',
        }))
    }

    function normalisasiSummary(response) {
        if (!response) {
            resetData()
            return
        }

        data.tanggal =
            response.tanggal || null

        data.peringatan_hari = Number(
            response.peringatan_hari ?? 7,
        )

        const kas = response.kas || {}

        data.kas = {
            saldo_kas: Number(
                kas.saldo_kas ??
                response.saldo_kas ??
                0,
            ),

            rekening: Array.isArray(
                kas.rekening,
            )
                ? kas.rekening
                : Array.isArray(
                      response.rekening,
                  )
                    ? response.rekening
                    : [],
        }

        const tagihan =
            response.tagihan || {}

        data.tagihan = {
            ringkasan:
                tagihan.ringkasan ||
                response.ringkasan ||
                {},

            data: normalisasiTagihan(
                tagihan,
            ),
        }
    }

    async function muatMonitoring() {
        if (memuat.value) {
            return
        }

        memuat.value = true
        error.value = ''

        try {
            const response =
                await accountingApi.monitoring.getSummary(
                    {
                        entitas: form.entitas,
                    },
                )

            normalisasiSummary(
                response.data,
            )

            terakhirDiperbarui.value =
                new Date()
        } catch (err) {
            error.value =
                err?.response?.data?.detail ||
                err?.message ||
                'Gagal memuat monitoring akunting.'
        } finally {
            memuat.value = false
        }
    }

    async function simpanPengeluaran() {
        if (menyimpan.value) {
            return
        }

        menyimpan.value = true
        error.value = ''

        try {
            const body = new FormData()

            body.append(
                'entitas',
                form.entitas,
            )

            body.append(
                'kategori',
                form.kategori,
            )

            body.append(
                'keterangan',
                form.keterangan,
            )

            body.append(
                'pemohon',
                form.pemohon,
            )

            body.append(
                'nominal',
                form.nominal,
            )

            if (form.bukti_nota) {
                body.append(
                    'bukti_nota',
                    form.bukti_nota,
                )
            }

            await accountingApi.monitoring.simpanPengeluaran(
                body,
            )

            resetForm()

            await muatMonitoring()
        } catch (err) {
            error.value =
                err?.response?.data?.detail ||
                err?.message ||
                'Gagal menyimpan pengeluaran.'
        } finally {
            menyimpan.value = false
        }
    }

    function resetForm() {
        form.kategori = ''
        form.keterangan = ''
        form.pemohon = ''
        form.nominal = ''
        form.bukti_nota = null
    }

    const tagihan = computed(() => {
        const prioritas = {
            TERLAMBAT: 0,
            JATUH_TEMPO: 1,
            PERINGATAN: 2,
            NORMAL: 3,
        }

        return [
            ...(data.tagihan.data || []),
        ].sort(
            (a, b) =>
                (
                    prioritas[
                        a.status_tempo
                    ] ?? 99
                ) -
                (
                    prioritas[
                        b.status_tempo
                    ] ?? 99
                ),
        )
    })

    const rekening = computed(() => {
        return data.kas.rekening || []
    })

    const saldoKas = computed(() => {
        return Number(
            data.kas.saldo_kas || 0,
        )
    })

    const jumlahTagihan = computed(() => {
        return Number(
            data.tagihan.ringkasan?.jumlah ??
            tagihan.value.length,
        )
    })

    const totalTagihan = computed(() => {
        const summary =
            data.tagihan.ringkasan

        const nilai =
            summary?.total_nilai ??
            summary?.total ??
            null

        if (nilai !== null) {
            return Number(nilai || 0)
        }

        return tagihan.value.reduce(
            (total, item) =>
                total +
                Number(
                    item.sisa_hutang || 0,
                ),
            0,
        )
    })

    function hitungStatus(status) {
        return tagihan.value.filter(
            (item) =>
                item.status_tempo ===
                status,
        ).length
    }

    const jumlahNormal = computed(() => {
        return hitungStatus('NORMAL')
    })

    const jumlahPeringatan = computed(() => {
        return Number(
            data.tagihan.ringkasan
                ?.peringatan ??
                hitungStatus('PERINGATAN'),
        )
    })

    const jumlahJatuhTempo = computed(() => {
        return Number(
            data.tagihan.ringkasan
                ?.jatuh_tempo ??
                hitungStatus('JATUH_TEMPO'),
        )
    })

    const jumlahTerlambat = computed(() => {
        return Number(
            data.tagihan.ringkasan
                ?.terlambat ??
                hitungStatus('TERLAMBAT'),
        )
    })

    const statusIDS = computed(() => {
        if (
            jumlahTerlambat.value > 0
        ) {
            return {
                key: 'KRITIS',
                label: 'PERHATIAN',
            }
        }

        if (
            jumlahJatuhTempo.value > 0
        ) {
            return {
                key: 'JATUH_TEMPO',
                label: 'PERLU TINDAKAN',
            }
        }

        if (
            jumlahPeringatan.value > 0
        ) {
            return {
                key: 'PERINGATAN',
                label: 'DALAM PEMANTAUAN',
            }
        }

        return {
            key: 'NORMAL',
            label: 'KONDISI NORMAL',
        }
    })

    const waktuDisplay = computed(() => {
        return new Intl.DateTimeFormat(
            'id-ID',
            {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
            },
        ).format(jamSekarang.value)
    })

    const tanggalDisplay = computed(() => {
        return new Intl.DateTimeFormat(
            'id-ID',
            {
                weekday: 'long',
                day: '2-digit',
                month: 'long',
                year: 'numeric',
            },
        ).format(jamSekarang.value)
    })

    const updateDisplay = computed(() => {
        if (
            !terakhirDiperbarui.value
        ) {
            return 'Belum diperbarui'
        }

        return new Intl.DateTimeFormat(
            'id-ID',
            {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
            },
        ).format(
            terakhirDiperbarui.value,
        )
    })

    function formatUang(nilai) {
        return new Intl.NumberFormat(
            'id-ID',
            {
                style: 'currency',
                currency: 'IDR',
                maximumFractionDigits: 0,
            },
        ).format(Number(nilai || 0))
    }

    function formatTanggal(tanggal) {
        if (!tanggal) {
            return '-'
        }

        return new Intl.DateTimeFormat(
            'id-ID',
            {
                day: '2-digit',
                month: 'short',
                year: 'numeric',
            },
        ).format(new Date(tanggal))
    }

    function labelStatus(status) {
        const map = {
            NORMAL: 'NORMAL',
            PERINGATAN: 'H-7',
            JATUH_TEMPO: 'JATUH TEMPO',
            TERLAMBAT: 'TERLAMBAT',
        }

        return (
            map[status] ||
            status ||
            '-'
        )
    }

    function labelHari(hari) {
        if (
            hari === null ||
            hari === undefined
        ) {
            return ''
        }

        const nilai = Number(hari)

        if (nilai < 0) {
            return `${Math.abs(nilai)} HARI TERLAMBAT`
        }

        if (nilai === 0) {
            return 'JATUH TEMPO HARI INI'
        }

        return `H-${nilai}`
    }

    function kelasStatus(status) {
        const map = {
            NORMAL:
                'bg-emerald-500/10 text-emerald-300 border-emerald-400/20',

            PERINGATAN:
                'bg-amber-500/10 text-amber-300 border-amber-400/20',

            JATUH_TEMPO:
                'bg-orange-500/10 text-orange-300 border-orange-400/20',

            TERLAMBAT:
                'bg-red-500/10 text-red-300 border-red-400/20',
        }

        return (
            map[status] ||
            'bg-slate-500/10 text-slate-300 border-slate-400/20'
        )
    }

    function toggleAutoRefresh() {
        autoRefresh.value =
            !autoRefresh.value

        if (autoRefresh.value) {
            mulaiRefresh()
        } else {
            hentikanRefresh()
        }
    }

    function mulaiRefresh() {
        hentikanRefresh()

        intervalRefresh =
            setInterval(() => {
                if (
                    !memuat.value &&
                    autoRefresh.value
                ) {
                    muatMonitoring()
                }
            }, REFRESH_MS)
    }

    function hentikanRefresh() {
        if (intervalRefresh) {
            clearInterval(
                intervalRefresh,
            )

            intervalRefresh = null
        }
    }

    function mulaiJam() {
        intervalJam = setInterval(() => {
            jamSekarang.value =
                new Date()
        }, 1000)
    }

    function gantiEntitas(kode) {
        if (!kode) {
            return
        }

        form.entitas = kode
        muatMonitoring()
    }

    onMounted(async () => {
        mulaiJam()
        mulaiRefresh()
        await muatMonitoring()
    })

    onBeforeUnmount(() => {
        hentikanRefresh()

        if (intervalJam) {
            clearInterval(
                intervalJam,
            )

            intervalJam = null
        }
    })

    return {
        data,
        form,

        memuat,
        menyimpan,
        error,
        autoRefresh,
        terakhirDiperbarui,

        tagihan,
        rekening,

        saldoKas,
        jumlahTagihan,
        totalTagihan,
        jumlahNormal,
        jumlahPeringatan,
        jumlahJatuhTempo,
        jumlahTerlambat,

        statusIDS,

        waktuDisplay,
        tanggalDisplay,
        updateDisplay,

        muatMonitoring,
        simpanPengeluaran,
        resetForm,
        toggleAutoRefresh,
        gantiEntitas,

        formatUang,
        formatTanggal,
        labelStatus,
        labelHari,
        kelasStatus,
    }
}