import {
  ref,
  reactive,
  computed,
  watch
} from 'vue'

import {
  apiTangki,
  apiBatch,
  apiPratinjau,
  apiRawUntukProduksi
} from '../api'

export function useBlendingForm() {
  const loadingForm = ref(false)
  const submitting = ref(false)
  const errorMsg = ref('')

  const daftarTangki = ref([])
  const daftarRaw = ref([])
  const pratinjau = ref(null)
  const isNamaHasilReadonly = ref(false)

  const form = reactive({
    nama_hasil: '',
    tangki_tujuan: '',
    batch: '',
    tekor_kg: 0
  })

  const bomRows = ref([])
  const wipRows = ref([])

  let seqBom = 0
  let seqWip = 0

  function buatBarisBom() {
    seqBom += 1

    return {
      _id: `bom-${seqBom}`,
      raw: '',
      qty: 0,
      saldo: 0,
      harga: 0,
      subtotal: 0
    }
  }

  function buatBarisWip() {
    seqWip += 1

    return {
      _id: `wip-${seqWip}`,
      tangki_asal: '',
      nama_hasil: '',
      qty: 0,
      tersedia: 0,
      harga: 0
    }
  }

  function cariTangki(id) {
    if (!id) {
      return null
    }

    return (
      daftarTangki.value.find(
        tangki =>
          String(tangki.id) ===
          String(id)
      ) || null
    )
  }

  function kodeTangki(tangki) {
    return String(
      tangki?.kode ??
      tangki?.nama ??
      ''
    )
      .trim()
      .toUpperCase()
  }

  function tangkiAdalahBlending(tangki) {
    return kodeTangki(tangki).startsWith(
      'TK-BLD-'
    )
  }

  function tangkiAdalahMixing(tangki) {
    return kodeTangki(tangki).startsWith(
      'TK-MIX-'
    )
  }

  function tangkiProsesValid(tangki) {
    return (
      tangkiAdalahBlending(tangki) ||
      tangkiAdalahMixing(tangki)
    )
  }

  function updateNamaHasilDariTangki() {
    const tangki =
      cariTangki(
        form.tangki_tujuan
      )

    if (!tangki) {
      form.nama_hasil = ''
      isNamaHasilReadonly.value = false
      return
    }

    const namaHasil =
      tangki.nama_hasil ||
      tangki.isi_saat_ini ||
      ''

    if (
      Number(
        tangki.saldo_kg ?? 0
      ) > 0 &&
      namaHasil
    ) {
      form.nama_hasil =
        namaHasil

      isNamaHasilReadonly.value =
        true
    } else {
      form.nama_hasil = ''
      isNamaHasilReadonly.value = false
    }
  }

  function normalisasiSaldoTangki(res) {
    const data =
      res?.results ??
      res?.data?.results ??
      res?.data ??
      res?.saldo ??
      res ??
      []

    if (Array.isArray(data)) {
      let totalQty = 0
      let totalNilai = 0

      for (const item of data) {
        const qty =
          Number(
            item?.saldo_kg ??
            item?.qty_kg ??
            item?.sisa_qty ??
            item?.saldo_qty ??
            item?.tersedia ??
            item?.qty ??
            0
          )

        const harga =
          Number(
            item?.harga_per_kg ??
            item?.harga_rata ??
            item?.harga ??
            0
          )

        if (qty > 0) {
          totalQty += qty
          totalNilai += qty * harga
        }
      }

      return {
        tersedia: totalQty,
        harga:
          totalQty > 0
            ? totalNilai / totalQty
            : 0
      }
    }

    const tersedia =
      Number(
        data?.saldo_kg ??
        data?.qty_kg ??
        data?.sisa_qty ??
        data?.saldo_qty ??
        data?.tersedia ??
        data?.qty ??
        0
      )

    const harga =
      Number(
        data?.harga_per_kg ??
        data?.harga_rata ??
        data?.harga ??
        0
      )

    return {
      tersedia,
      harga
    }
  }

  async function muatSaldoTangki(
    tangkiId
  ) {
    if (!tangkiId) {
      return {
        tersedia: 0,
        harga: 0
      }
    }

    try {
      const res =
        await apiTangki.saldo(
          tangkiId
        )

      return normalisasiSaldoTangki(
        res
      )
    } catch (error) {
      console.error(error)

      return {
        tersedia: 0,
        harga: 0
      }
    }
  }

  async function muatTangki() {
    try {
      const res =
        await apiTangki.daftar()

      const list =
        res?.results ??
        res?.data?.results ??
        res?.data ??
        res ??
        []

      if (!Array.isArray(list)) {
        daftarTangki.value = []
        return
      }

      const hasil =
        await Promise.all(
          list.map(
            async tangki => {
              let saldoKg =
                Number(
                  tangki.saldo_kg ??
                  tangki.qty_kg ??
                  0
                )

              let saldoNilai =
                Number(
                  tangki.saldo_nilai ??
                  0
                )

              let hargaPerKg =
                Number(
                  tangki.harga_per_kg ??
                  0
                )

              try {
                const saldoResponse =
                  await apiTangki.saldo(
                    tangki.id
                  )

                const saldoData =
                  saldoResponse?.results ??
                  saldoResponse?.data?.results ??
                  saldoResponse?.data ??
                  saldoResponse?.saldo ??
                  saldoResponse ??
                  null

                if (
                  Array.isArray(
                    saldoData
                  )
                ) {
                  let totalQty = 0
                  let totalNilai = 0

                  for (
                    const item of
                    saldoData
                  ) {
                    const qty =
                      Number(
                        item?.saldo_kg ??
                        item?.qty_kg ??
                        item?.sisa_qty ??
                        item?.saldo_qty ??
                        item?.tersedia ??
                        item?.qty ??
                        0
                      )

                    const harga =
                      Number(
                        item?.harga_per_kg ??
                        item?.harga_rata ??
                        item?.harga ??
                        0
                      )

                    if (qty > 0) {
                      totalQty += qty
                      totalNilai +=
                        qty * harga
                    }
                  }

                  saldoKg =
                    totalQty

                  saldoNilai =
                    totalQty > 0
                      ? totalNilai
                      : 0

                  hargaPerKg =
                    totalQty > 0
                      ? totalNilai /
                        totalQty
                      : 0
                } else if (
                  saldoData &&
                  typeof saldoData ===
                    'object'
                ) {
                  saldoKg =
                    Number(
                      saldoData.saldo_kg ??
                      saldoData.qty_kg ??
                      saldoData.sisa_qty ??
                      saldoData.saldo_qty ??
                      saldoData.tersedia ??
                      saldoData.qty ??
                      saldoKg
                    )

                  saldoNilai =
                    Number(
                      saldoData.saldo_nilai ??
                      saldoData.nilai ??
                      saldoNilai
                    )

                  hargaPerKg =
                    Number(
                      saldoData.harga_per_kg ??
                      saldoData.harga_rata ??
                      saldoData.harga ??
                      hargaPerKg
                    )
                }
              } catch (errorSaldo) {
                console.warn(
                  `Gagal memuat saldo tangki ${tangki.kode}`,
                  errorSaldo
                )
              }

              if (
                saldoKg > 0 &&
                saldoNilai > 0
              ) {
                hargaPerKg =
                  saldoNilai /
                  saldoKg
              }

              return {
                ...tangki,
                saldo_kg:
                  saldoKg,
                saldo_nilai:
                  saldoNilai,
                harga_per_kg:
                  hargaPerKg,
                nama_hasil:
                  tangki.nama_hasil ||
                  tangki.isi_saat_ini ||
                  ''
              }
            }
          )
        )

      daftarTangki.value =
        hasil
    } catch (error) {
      console.error(error)

      errorMsg.value =
        'Gagal memuat daftar tangki'
    }
  }

  const opsiTangkiSumber =
    computed(() => {
      const tujuanId =
        String(
          form.tangki_tujuan || ''
        )

      const sumberTerpakai =
        new Set(
          wipRows.value
            .map(
              row =>
                row.tangki_asal
                  ? String(
                      row.tangki_asal
                    )
                  : null
            )
            .filter(Boolean)
        )

      return daftarTangki.value
        .filter(
          tangki => {
            const id =
              String(
                tangki.id
              )

            const kode =
              kodeTangki(
                tangki
              )

            const saldo =
              Number(
                tangki.saldo_kg ??
                0
              )

            const kodeValid =
              kode.startsWith(
                'TK-MIX-'
              ) ||
              kode.startsWith(
                'TK-BLD-'
              )

            return (
              tangki.aktif !== false &&
              kodeValid &&
              id !== tujuanId &&
              saldo > 0
            )
          }
        )
        .map(
          tangki => {
            const saldo =
              Number(
                tangki.saldo_kg ??
                0
              )

            const nilai =
              Number(
                tangki.saldo_nilai ??
                0
              )

            const harga =
              Number(
                tangki.harga_per_kg ||
                (
                  saldo > 0
                    ? nilai / saldo
                    : 0
                )
              )

            const namaHasil =
              tangki.nama_hasil ||
              tangki.isi_saat_ini ||
              '-'

            return {
              id: tangki.id,
              kode: tangki.kode,
              nama: tangki.nama,
              nama_hasil:
                namaHasil,
              saldo_kg:
                saldo,
              saldo_nilai:
                nilai,
              harga_per_kg:
                harga,
              disabled:
                sumberTerpakai.has(
                  String(
                    tangki.id
                  )
                ),
              label:
                `${tangki.kode} — ${namaHasil} — Tersedia ${saldo.toLocaleString(
                  'id-ID',
                  {
                    minimumFractionDigits: 3,
                    maximumFractionDigits: 3
                  }
                )} Kg`
            }
          }
        )
    })

  async function muatRawPool() {
    try {
      const res =
        await apiRawUntukProduksi.daftar()

      const list =
        res?.rincian ??
        res?.data?.rincian ??
        res?.results ??
        res?.data ??
        res ??
        []

      daftarRaw.value =
        Array.isArray(list)
          ? list
              .filter(
                item =>
                  Number(
                    item.qty_kg
                  ) > 0
              )
              .map(
                item => ({
                  ...item,
                  raw:
                    item.produk_id ??
                    item.raw ??
                    item.produk
                })
              )
          : []
    } catch (error) {
      console.error(error)

      errorMsg.value =
        'Gagal memuat saldo bahan baku'
    }
  }

  async function bukaFormBaru() {
    form.nama_hasil = ''
    form.tangki_tujuan = ''
    form.batch = ''
    form.tekor_kg = 0

    isNamaHasilReadonly.value =
      false

    pratinjau.value = null
    errorMsg.value = ''

    loadingForm.value = true

    try {
      await Promise.all([
        muatTangki(),
        muatRawPool()
      ])

      bomRows.value = [
        buatBarisBom()
      ]

      wipRows.value = [
        buatBarisWip()
      ]
    } finally {
      loadingForm.value = false
    }
  }

  async function bukaFormEdit(
    batchId
  ) {
    loadingForm.value = true
    errorMsg.value = ''

    try {
      await Promise.all([
        muatTangki(),
        muatRawPool()
      ])

      const detail =
        await apiBatch.detail(
          batchId
        )

      form.nama_hasil =
        detail.nama_hasil ||
        ''

      form.tangki_tujuan =
        detail.tangki_tujuan ??
        detail.tangki ??
        ''

      form.batch =
        detail.batch ||
        detail.nomor_batch ||
        ''

      form.tekor_kg =
        Number(
          detail.tekor_kg ||
          0
        )

      updateNamaHasilDariTangki()

      bomRows.value =
        (
          detail.materials ||
          detail.bahan_baku ||
          []
        ).map(
          material => {
            const row =
              buatBarisBom()

            row.raw =
              material.raw ??
              material.produk_id ??
              material.produk

            row.qty =
              Number(
                material.qty_kg ??
                0
              )

            row.harga =
              Number(
                material.harga_per_kg ??
                0
              )

            row.subtotal =
              row.qty *
              row.harga

            perbaruiTelemetriBom(
              row
            )

            return row
          }
        )

      if (
        bomRows.value.length ===
        0
      ) {
        bomRows.value = [
          buatBarisBom()
        ]
      }

      const wipSources =
        detail.wip_sources ||
        detail.info_blending ||
        []

      wipRows.value =
        await Promise.all(
          wipSources.map(
            async wip => {
              const row =
                buatBarisWip()

              row.tangki_asal =
                wip.tangki_sumber_id ??
                wip.tangki_asal

              row.qty =
                Number(
                  wip.qty_kg ??
                  wip.qty ??
                  0
                )

              const tangki =
                cariTangki(
                  row.tangki_asal
                )

              const saldo =
                await muatSaldoTangki(
                  row.tangki_asal
                )

              row.nama_hasil =
                tangki?.nama_hasil ||
                tangki?.isi_saat_ini ||
                ''

              row.tersedia =
                saldo.tersedia

              row.harga =
                Number(
                  wip.harga_per_kg ??
                  saldo.harga ??
                  tangki?.harga_per_kg ??
                  0
                )

              return row
            }
          )
        )

      if (
        wipRows.value.length ===
        0
      ) {
        wipRows.value = [
          buatBarisWip()
        ]
      }
    } catch (error) {
      console.error(error)

      errorMsg.value =
        'Gagal memuat detail batch blending'
    } finally {
      loadingForm.value = false
    }
  }

  function saatTangkiTujuanDipilih() {
    const tangki =
      cariTangki(
        form.tangki_tujuan
      )

    if (!tangki) {
      form.nama_hasil = ''
      isNamaHasilReadonly.value =
        false
      return
    }

    if (
      !tangkiAdalahBlending(
        tangki
      )
    ) {
      errorMsg.value =
        'Tangki tujuan Blending harus menggunakan kode TK-BLD-*'

      form.tangki_tujuan = ''
      form.nama_hasil = ''
      isNamaHasilReadonly.value =
        false

      return
    }

    errorMsg.value = ''

    updateNamaHasilDariTangki()

    const tujuanId =
      String(
        form.tangki_tujuan
      )

    for (
      const row of
      wipRows.value
    ) {
      if (
        row.tangki_asal &&
        String(
          row.tangki_asal
        ) === tujuanId
      ) {
        row.tangki_asal = ''
        row.nama_hasil = ''
        row.qty = 0
        row.tersedia = 0
        row.harga = 0
      }
    }

    if (
      wipRows.value.length ===
      0
    ) {
      wipRows.value = [
        buatBarisWip()
      ]
    }
  }

  async function saatTangkiAsalDipilih(
    row
  ) {
    row.nama_hasil = ''
    row.tersedia = 0
    row.harga = 0

    if (
      !row.tangki_asal
    ) {
      return
    }

    if (
      String(
        row.tangki_asal
      ) ===
      String(
        form.tangki_tujuan
      )
    ) {
      row.tangki_asal = ''
      return
    }

    const tangki =
      cariTangki(
        row.tangki_asal
      )

    if (!tangki) {
      return
    }

    if (
      !tangkiProsesValid(
        tangki
      )
    ) {
      row.tangki_asal = ''
      return
    }

    row.nama_hasil =
      tangki.nama_hasil ||
      tangki.isi_saat_ini ||
      ''

    const saldo =
      await muatSaldoTangki(
        row.tangki_asal
      )

    row.tersedia =
      saldo.tersedia

    row.harga =
      saldo.harga ||
      Number(
        tangki.harga_per_kg ||
        0
      )
  }

  function saatBatchWipDipilih() {
    return
  }

  function tambahBomRow() {
    bomRows.value.push(
      buatBarisBom()
    )
  }

  function hapusBomRow(id) {
    if (
      bomRows.value.length <=
      1
    ) {
      return
    }

    bomRows.value =
      bomRows.value.filter(
        row =>
          row._id !== id
      )
  }

  function tambahWipRow() {
    wipRows.value.push(
      buatBarisWip()
    )
  }

  function hapusWipRow(id) {
    if (
      wipRows.value.length <=
      1
    ) {
      wipRows.value = [
        buatBarisWip()
      ]

      return
    }

    wipRows.value =
      wipRows.value.filter(
        row =>
          row._id !== id
      )
  }

  function perbaruiTelemetriBom(
    row
  ) {
    const item =
      daftarRaw.value.find(
        raw =>
          String(
            raw.raw
          ) ===
          String(
            row.raw
          )
      )

    row.saldo =
      item
        ? Number(
            item.qty_kg ??
            0
          )
        : 0

    row.harga =
      item
        ? Number(
            item.harga_rata ??
            item.harga_per_kg ??
            0
          )
        : 0

    row.subtotal =
      (
        Number(
          row.qty
        ) || 0
      ) *
      (
        Number(
          row.harga
        ) || 0
      )
  }

  const totalQtyBom =
    computed(() =>
      bomRows.value.reduce(
        (sum, row) =>
          sum +
          (
            Number(
              row.qty
            ) || 0
          ),
        0
      )
    )

  const totalNilaiBom =
    computed(() =>
      bomRows.value.reduce(
        (sum, row) =>
          sum +
          (
            Number(
              row.qty
            ) || 0
          ) *
          (
            Number(
              row.harga
            ) || 0
          ),
        0
      )
    )

  const totalQtyWip =
    computed(() =>
      wipRows.value.reduce(
        (sum, row) =>
          sum +
          (
            Number(
              row.qty
            ) || 0
          ),
        0
      )
    )

  const totalNilaiWip =
    computed(() =>
      wipRows.value.reduce(
        (sum, row) =>
          sum +
          (
            Number(
              row.qty
            ) || 0
          ) *
          (
            Number(
              row.harga
            ) || 0
          ),
        0
      )
    )

  const totalInputKg =
    computed(
      () =>
        totalQtyBom.value +
        totalQtyWip.value
    )

  const totalInputNilai =
    computed(
      () =>
        totalNilaiBom.value +
        totalNilaiWip.value
    )

  const proyeksiYield =
    computed(
      () =>
        totalInputKg.value -
        (
          Number(
            form.tekor_kg
          ) || 0
        )
    )

  const proyeksiHargaRata =
    computed(() =>
      proyeksiYield.value > 0
        ? totalInputNilai.value /
          proyeksiYield.value
        : 0
    )

  function susunPayload() {
    return {
      nama_hasil:
        form.nama_hasil.trim(),

      tangki_tujuan:
        Number(
          form.tangki_tujuan
        ),

      batch:
        form.batch.trim(),

      tekor_kg:
        Number(
          form.tekor_kg
        ) || 0,

      materials:
        bomRows.value
          .filter(
            row =>
              row.raw &&
              Number(
                row.qty
              ) > 0
          )
          .map(
            row => ({
              raw:
                String(
                  row.raw
                ),
              qty_kg:
                Number(
                  row.qty
                )
            })
          ),

      wip_sources:
        wipRows.value
          .filter(
            row =>
              row.tangki_asal &&
              Number(
                row.qty
              ) > 0
          )
          .map(
            row => ({
              tangki_sumber_id:
                Number(
                  row.tangki_asal
                ),

              qty_kg:
                Number(
                  row.qty
                )
            })
          )
    }
  }

  function validasiForm() {
    if (
      !form.nama_hasil.trim()
    ) {
      return (
        'Nama hasil produksi wajib diisi'
      )
    }

    if (
      !form.tangki_tujuan
    ) {
      return (
        'Tangki tujuan wajib dipilih'
      )
    }

    const tangkiTujuan =
      cariTangki(
        form.tangki_tujuan
      )

    if (!tangkiTujuan) {
      return (
        'Tangki tujuan tidak ditemukan'
      )
    }

    if (
      !tangkiAdalahBlending(
        tangkiTujuan
      )
    ) {
      return (
        'Tangki tujuan Blending harus menggunakan kode TK-BLD-*'
      )
    }

    if (
      !form.batch.trim()
    ) {
      return (
        'Batch ID wajib diisi'
      )
    }

    const adaBom =
      bomRows.value.some(
        row =>
          row.raw &&
          Number(
            row.qty
          ) > 0
      )

    const adaWip =
      wipRows.value.some(
        row =>
          row.tangki_asal &&
          Number(
            row.qty
          ) > 0
      )

    if (
      !adaBom &&
      !adaWip
    ) {
      return (
        'Minimal satu sumber WIP atau bahan baku harus diisi'
      )
    }

    for (
      const row of
      bomRows.value
    ) {
      if (
        row.raw &&
        Number(
          row.qty
        ) >
        Number(
          row.saldo
        ) + 0.001
      ) {
        return (
          'Saldo pool bahan baku tidak cukup'
        )
      }
    }

    const tujuanId =
      String(
        form.tangki_tujuan
      )

    const sumberIds = []

    for (
      const row of
      wipRows.value
    ) {
      if (
        !row.tangki_asal
      ) {
        continue
      }

      const sumberId =
        String(
          row.tangki_asal
        )

      if (
        sumberId ===
        tujuanId
      ) {
        return (
          'Tangki tujuan tidak boleh digunakan sebagai tangki sumber WIP.'
        )
      }

      const tangkiSumber =
        cariTangki(
          row.tangki_asal
        )

      if (
        !tangkiSumber
      ) {
        return (
          'Tangki sumber WIP tidak ditemukan.'
        )
      }

      if (
        !tangkiProsesValid(
          tangkiSumber
        )
      ) {
        return (
          `Kode tangki ${kodeTangki(
            tangkiSumber
          )} tidak valid sebagai sumber WIP.`
        )
      }

      const qty =
        Number(
          row.qty
        ) || 0

      const tersedia =
        Number(
          row.tersedia
        ) || 0

      if (
        qty >
        tersedia + 0.001
      ) {
        return (
          `Saldo WIP pada ${kodeTangki(
            tangkiSumber
          )} tidak cukup. ` +
          `Diminta ${qty.toFixed(
            3
          )} Kg, tersedia ${tersedia.toFixed(
            3
          )} Kg.`
        )
      }

      sumberIds.push(
        sumberId
      )
    }

    if (
      new Set(
        sumberIds
      ).size !==
      sumberIds.length
    ) {
      return (
        'Satu tangki sumber hanya boleh digunakan satu kali.'
      )
    }

    if (
      proyeksiYield.value <=
      0
    ) {
      return (
        'Yield harus positif setelah dikurangi tekor'
      )
    }

    return ''
  }

  async function mintaPratinjau() {
    errorMsg.value =
      validasiForm()

    if (
      errorMsg.value
    ) {
      return null
    }

    try {
      const res =
        await apiPratinjau(
          susunPayload()
        )

      pratinjau.value =
        res

      if (
        res &&
        res.valid === false
      ) {
        errorMsg.value =
          res.galat
            ?.map(
              item =>
                item.pesan
            )
            .join(
              ' | '
            ) ||
          'Kalkulasi ditolak server.'
      }

      return res
    } catch (error) {
      console.error(error)

      errorMsg.value =
        error?.response?.data?.pesan ||
        error?.response?.data?.detail ||
        'Gagal kalkulasi pratinjau.'

      return null
    }
  }

  async function simpanDanPosting(
    batchId = null
  ) {
    errorMsg.value =
      validasiForm()

    if (
      errorMsg.value
    ) {
      return false
    }

    submitting.value =
      true

    try {
      const payload =
        susunPayload()

      if (
        batchId
      ) {
        await apiBatch.ubah(
          batchId,
          payload
        )
      } else {
        await apiBatch.buat(
          payload
        )
      }

      return true
    } catch (error) {
      console.error(error)

      const data =
        error?.response?.data

      errorMsg.value =
        data?.detail ||
        data?.pesan ||
        'Gagal memposting batch produksi'

      return false
    } finally {
      submitting.value =
        false
    }
  }

  async function tambahTangkiBaru(
    nama
  ) {
    const namaBersih =
      String(
        nama || ''
      )
        .trim()
        .toUpperCase()

    if (
      !namaBersih
    ) {
      return null
    }

    if (
      !namaBersih.startsWith(
        'TK-BLD-'
      )
    ) {
      errorMsg.value =
        'Tangki tujuan Blending harus menggunakan kode TK-BLD-*'

      return null
    }

    const existing =
      daftarTangki.value.find(
        tangki =>
          String(
            tangki.kode ??
            tangki.nama ??
            ''
          )
            .trim()
            .toUpperCase() ===
          namaBersih
      )

    if (
      existing
    ) {
      return existing
    }

    try {
      const dibuat =
        await apiTangki.buat({
          nama:
            namaBersih,
          kode:
            namaBersih
        })

      await muatTangki()

      return dibuat
    } catch (error) {
      console.error(error)

      errorMsg.value =
        'Gagal membuat tangki baru'

      return null
    }
  }

  async function generateNomorBatch() {
    if (
      !form.tangki_tujuan
    ) {
      errorMsg.value =
        'Pilih tangki tujuan terlebih dahulu'

      return
    }

    const tangki =
      cariTangki(
        form.tangki_tujuan
      )

    if (
      !tangki ||
      !tangkiAdalahBlending(
        tangki
      )
    ) {
      errorMsg.value =
        'Tangki tujuan harus TK-BLD-*'

      return
    }

    try {
      const res =
        await apiBatch.nomorBaru(
          'BLENDING'
        )

      form.batch =
        res?.nomor ??
        res?.batch ??
        ''
    } catch (error) {
      console.error(error)

      errorMsg.value =
        'Gagal membuat nomor batch otomatis'
    }
  }

  watch(
    () =>
      form.tangki_tujuan,
    () => {
      saatTangkiTujuanDipilih()
    }
  )

  watch(
    bomRows,
    rows => {
      rows.forEach(
        row => {
          row.subtotal =
            (
              Number(
                row.qty
              ) || 0
            ) *
            (
              Number(
                row.harga
              ) || 0
            )
        }
      )
    },
    {
      deep: true
    }
  )

  return {
    loadingForm,
    submitting,
    errorMsg,

    daftarTangki,
    daftarRaw,
    opsiTangkiSumber,

    form,
    bomRows,
    wipRows,
    pratinjau,

    isNamaHasilReadonly,

    proyeksiYield,
    proyeksiHargaRata,

    totalQtyWip,
    totalNilaiWip,

    bukaFormBaru,
    bukaFormEdit,

    tambahTangkiBaru,
    generateNomorBatch,

    saatTangkiTujuanDipilih,
    saatTangkiAsalDipilih,
    saatBatchWipDipilih,

    tambahBomRow,
    hapusBomRow,

    tambahWipRow,
    hapusWipRow,

    perbaruiTelemetriBom,

    mintaPratinjau,
    simpanDanPosting
  }
}