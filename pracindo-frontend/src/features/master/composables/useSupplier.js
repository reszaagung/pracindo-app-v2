import { computed, ref } from 'vue'
import api from '@/utils/api'
import {
    bacaError as bacaPesan,
    errorPerField,
} from '@/utils/error'

const PER_HALAMAN = 25

const bersih = (params = {}) =>
    Object.fromEntries(
        Object.entries(params).filter(
            ([, nilai]) =>
                nilai !== undefined &&
                nilai !== null &&
                nilai !== ''
        )
    )

const bacaError = (
    err,
    fallback = 'Terjadi kesalahan.'
) => {
    const data = err?.response?.data

    if (Array.isArray(data)) {
        return {
            pesanUmum: data.join(' '),
            errorField: {},
        }
    }

    if (Array.isArray(data?.detail)) {
        return {
            pesanUmum: data.detail.join(' '),
            errorField: {},
        }
    }

    const fieldErrors =
        errorPerField(err)

    if (
        !Object.keys(fieldErrors).length
    ) {
        return {
            pesanUmum: bacaPesan(
                err,
                fallback
            ),
            errorField: {},
        }
    }

    const umum =
        data?.non_field_errors

    return {
        pesanUmum: Array.isArray(umum)
            ? umum.join(' ')
            : 'Periksa kembali isian yang ditandai merah.',
        errorField: fieldErrors,
    }
}

export function useSupplier() {
    const daftarSuplier = ref([])

    const sedangProses = ref(false)
    const sedangMuat = ref(false)
    const sedangSimpan = ref(false)
    const sedangUbahStatus = ref(false)

    const pesanError = ref('')
    const errorField = ref({})

    const totalData = ref(0)
    const halaman = ref(1)

    const perHalaman =
        PER_HALAMAN

    const filterAktif = ref(null)
    const pencarian = ref('')


    const ambilSuplier = async (
        params = {}
    ) => {
        const ke =
            Number(params.halaman || 1)

        sedangMuat.value = true
        sedangProses.value = true
        pesanError.value = ''

        try {
            const response =
                await api.get(
                    'master/suplier/',
                    {
                        params: bersih({
                            search:
                                params.search ??
                                pencarian.value,
                            aktif:
                                params.aktif ??
                                filterAktif.value,
                            page: ke,
                        }),
                    }
                )

            const data =
                response?.data

            daftarSuplier.value =
                data?.results ||
                (Array.isArray(data)
                    ? data
                    : [])

            totalData.value =
                data?.count ??
                daftarSuplier.value.length

            halaman.value = ke
        } catch (err) {
            console.error(
                'Gagal memuat data suplier:',
                err
            )

            daftarSuplier.value = []

            pesanError.value =
                bacaPesan(
                    err,
                    'Gagal memuat data suplier.'
                )
        } finally {
            sedangMuat.value = false
            sedangProses.value = false
        }
    }


    const ambilSuplierRingkas =
        async () => {
            try {
                const response =
                    await api.get(
                        'master/suplier/',
                        {
                            params: {
                                ringkas: 1,
                                aktif: 'true',
                            },
                        }
                    )

                const data =
                    response?.data

                return (
                    data?.results ||
                    (Array.isArray(data)
                        ? data
                        : [])
                )
            } catch (err) {
                console.error(
                    'Gagal memuat dropdown suplier:',
                    err
                )

                return []
            }
        }


    const simpanSuplier = async (
        payload,
        id = null
    ) => {
        sedangSimpan.value = true
        sedangProses.value = true

        pesanError.value = ''
        errorField.value = {}

        try {
            const response = id
                ? await api.patch(
                      `master/suplier/${id}/`,
                      payload
                  )
                : await api.post(
                      'master/suplier/',
                      payload
                  )

            return {
                success: true,
                data:
                    response?.data ||
                    null,
            }
        } catch (err) {
            console.error(
                'Gagal menyimpan suplier:',
                err
            )

            const hasil =
                bacaError(
                    err,
                    'Gagal menyimpan data suplier.'
                )

            pesanError.value =
                hasil.pesanUmum

            errorField.value =
                hasil.errorField

            return {
                success: false,
                message:
                    hasil.pesanUmum,
                errorField:
                    hasil.errorField,
                data:
                    err?.response?.data ||
                    null,
            }
        } finally {
            sedangSimpan.value = false
            sedangProses.value = false
        }
    }


    const ubahStatusAktif = async (
        id,
        aktif
    ) => {
        if (!id) {
            const message =
                'ID suplier tidak ditemukan.'

            pesanError.value = message

            return {
                success: false,
                message,
            }
        }

        sedangUbahStatus.value = true
        sedangProses.value = true
        pesanError.value = ''

        try {
            const response =
                await api.patch(
                    `master/suplier/${id}/`,
                    {
                        aktif: Boolean(
                            aktif
                        ),
                    }
                )

            return {
                success: true,
                data:
                    response?.data ||
                    null,
            }
        } catch (err) {
            console.error(
                'Gagal mengubah status suplier:',
                err
            )

            const message =
                bacaPesan(
                    err,
                    'Gagal mengubah status suplier.'
                )

            pesanError.value =
                message

            return {
                success: false,
                message,
                data:
                    err?.response?.data ||
                    null,
            }
        } finally {
            sedangUbahStatus.value = false
            sedangProses.value = false
        }
    }


    const ubahHalaman = async (
        page,
        params = {}
    ) => {
        const target =
            Number(page)

        if (
            !Number.isInteger(target) ||
            target < 1
        ) {
            return
        }

        await ambilSuplier({
            ...params,
            halaman: target,
        })
    }


    const setPencarian = (
        value = ''
    ) => {
        pencarian.value =
            String(value)

        return ambilSuplier({
            search:
                pencarian.value,
            aktif:
                filterAktif.value,
            halaman: 1,
        })
    }


    const setFilterAktif = (
        value = null
    ) => {
        filterAktif.value =
            value === null
                ? null
                : String(value)

        return ambilSuplier({
            search:
                pencarian.value,
            aktif:
                filterAktif.value,
            halaman: 1,
        })
    }


    const jumlahHalaman =
        computed(() => {
            if (!totalData.value) {
                return 1
            }

            return Math.max(
                1,
                Math.ceil(
                    totalData.value /
                        perHalaman
                )
            )
        })


    const rangeMulai =
        computed(() => {
            if (!totalData.value) {
                return 0
            }

            return (
                (halaman.value - 1) *
                    perHalaman +
                1
            )
        })


    const rangeSelesai =
        computed(() => {
            if (!totalData.value) {
                return 0
            }

            return Math.min(
                halaman.value *
                    perHalaman,
                totalData.value
            )
        })


    const adaData =
        computed(() =>
            daftarSuplier.value.length >
            0
        )


    return {
        daftarSuplier,

        sedangProses,
        sedangMuat,
        sedangSimpan,
        sedangUbahStatus,

        pesanError,
        errorField,

        totalData,
        halaman,
        perHalaman,
        jumlahHalaman,
        rangeMulai,
        rangeSelesai,
        adaData,

        pencarian,
        filterAktif,

        ambilSuplier,
        ambilSuplierRingkas,
        simpanSuplier,
        ubahStatusAktif,
        ubahHalaman,
        setPencarian,
        setFilterAktif,
    }
}