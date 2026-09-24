import {
  ref,
  reactive,
  computed,
  watch,
  onMounted
} from 'vue'

import {
  apiTangki,
  apiBatch,
  apiPratinjau,
  apiRawUntukProduksi
} from '../api'

const JENIS = {
  MIXING: 'MIXING',
  BLENDING: 'BLENDING'
}

export function useInputProduksi() {
  const mode = ref('list')
  const editingBatchId = ref(null)

  const loadingList = ref(false)
  const loadingForm = ref(false)
  const submitting = ref(false)
  const errorMsg = ref('')

  const daftarTangki = ref([])
  const daftarRaw = ref([])
  const daftarBatch = ref([])

  const isNamaHasilReadonly = ref(false)

  const filter = reactive({
    jenis: '',
    tangki: '',
    search: ''
  })

  const form = reactive({
    nama_hasil: '',
    tangki_tujuan: '',
    batch: '',
    tekor_kg: 0
  })

  const bomRows = ref([])
  const wipRows = ref([])
  const pratinjau = ref(null)

  let seqBom = 0
  let seqWip = 0

  // =========================================================
  // JENIS PROSES
  // =========================================================
  //
  // JENIS TIDAK DISIMPAN SEBAGAI INPUT.
  // JENIS DITENTUKAN DARI KODE TANGKI TUJUAN.
  //
  // TK-BLD-*  -> BLENDING
  // TK-MIX-*  -> MIXING
  // =========================================================

  function normalisasiKodeTangki(tangki) {
    return String(
      tangki?.kode ??
      tangki?.nama ??
      ''
    )
      .trim()
      .toUpperCase()
  }

  function tentukanJenisDariTangki(tangki) {
    const kode =
      normalisasiKodeTangki(tangki)

    if (
      kode.startsWith('TK-BLD-')
    ) {
      return JENIS.BLENDING
    }

    if (
      kode.startsWith('TK-MIX-')
    ) {
      return JENIS.MIXING
    }

    return ''
  }

  const jenisProduksi = computed(() => {
    const tangki =
      daftarTangki.value.find(
        (t) =>
          String(t.id) ===
          String(form.tangki_tujuan)
      )

    return tentukanJenisDariTangki(
      tangki
    )
  })

  const isBlending = computed(() =>
    jenisProduksi.value ===
    JENIS.BLENDING
  )

  const isMixing = computed(() =>
    jenisProduksi.value ===
    JENIS.MIXING
  )

  // =========================================================
  // ROW BOM
  // =========================================================

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

  // =========================================================
  // ROW WIP
  // =========================================================
  //
  // WIP TIDAK MEMILIKI BATCH SUMBER.
  // SUMBER HANYA TANGKI.
  // =========================================================

  function buatBarisWip() {
    seqWip += 1

    return {
      _id: `wip-${seqWip}`,
      tangki_asal: '',
      nama_hasil: '',
      qty: 0,
      tersedia: 0,
      nilai: 0,
      harga: 0
    }
  }

  // =========================================================
  // LOAD TANGKI
  // =========================================================

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

      daftarTangki.value =
        Array.isArray(list)
          ? list.map((t) => {
              const saldoKg =
                Number(
                  t.saldo_kg ?? 0
                )

              const saldoNilai =
                Number(
                  t.saldo_nilai ?? 0
                )

              const harga =
                saldoKg > 0
                  ? Number(
                      t.harga_per_kg ??
                      (
                        saldoNilai /
                        saldoKg
                      )
                    )
                  : 0

              return {
                ...t,

                saldo_kg:
                  saldoKg,

                saldo_nilai:
                  saldoNilai,

                harga_per_kg:
                  harga,

                nama_hasil:
                  t.nama_hasil ||
                  t.isi_saat_ini ||
                  ''
              }
            })
          : []

    } catch (error) {
      console.error(error)

      errorMsg.value =
        'Gagal memuat daftar tangki'
    }
  }

  // =========================================================
  // LOAD RAW POOL
  // =========================================================

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
                (item) =>
                  Number(
                    item.qty_kg
                  ) > 0
              )
              .map((item) => ({
                ...item,

                raw:
                  item.produk_id ??
                  item.raw ??
                  item.produk
              }))
          : []

    } catch (error) {
      console.error(error)

      errorMsg.value =
        'Gagal memuat saldo bahan baku'
    }
  }

  // =========================================================
  // LOAD DAFTAR BATCH
  // =========================================================

  async function muatDaftarBatch() {
    loadingList.value = true

    try {
      const params = {}

      /*
       * Filter jenis masih boleh dipakai
       * untuk LIST jika backend mendukung.
       *
       * Ini bukan field produksi.
       */

      if (filter.jenis) {
        params.jenis =
          filter.jenis
      }

      if (filter.tangki) {
        params.tangki =
          filter.tangki
      }

      if (filter.search) {
        params.search =
          filter.search
      }

      const res =
        await apiBatch.daftar(
          params
        )

      daftarBatch.value =
        res?.results ??
        res?.data?.results ??
        res?.data ??
        res ??
        []

    } catch (error) {
      console.error(error)

      errorMsg.value =
        'Gagal memuat daftar batch produksi'

    } finally {
      loadingList.value = false
    }
  }

  // =========================================================
  // INIT
  // =========================================================

  async function initHalaman() {
    await Promise.all([
      muatTangki(),
      muatDaftarBatch()
    ])
  }

  // =========================================================
  // PILIH TANGKI TUJUAN
  // =========================================================

  function saatTangkiTujuanDipilih() {
    const tangki =
      daftarTangki.value.find(
        (t) =>
          String(t.id) ===
          String(
            form.tangki_tujuan
          )
      )

    if (!tangki) {
      form.nama_hasil = ''

      isNamaHasilReadonly.value =
        false

      wipRows.value = []

      return
    }

    const jenis =
      tentukanJenisDariTangki(
        tangki
      )

    const namaHasil =
      tangki.nama_hasil ||
      tangki.isi_saat_ini ||
      ''

    // =======================================================
    // NAMA HASIL
    // =======================================================

    if (
      Number(
        tangki.saldo_kg
      ) > 0 &&
      namaHasil
    ) {
      form.nama_hasil =
        namaHasil

      isNamaHasilReadonly.value =
        true
    } else {
      form.nama_hasil = ''

      isNamaHasilReadonly.value =
        false
    }

    // =======================================================
    // WIP BERDASARKAN JENIS TANGKI
    // =======================================================

    if (
      jenis === JENIS.BLENDING
    ) {
      if (
        wipRows.value.length ===
        0
      ) {
        wipRows.value = [
          buatBarisWip()
        ]
      }
    } else {
      wipRows.value = []
    }

    // =======================================================
    // TANGKI TUJUAN TIDAK BOLEH JADI SUMBER
    // =======================================================

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
        row.nilai = 0
        row.harga = 0
      }
    }
  }

  // =========================================================
  // OPSI TANGKI SUMBER
  // =========================================================

  const opsiTangkiSumber =
    computed(() => {
      const tujuanId =
        String(
          form.tangki_tujuan || ''
        )

      const terpakai =
        new Set(
          wipRows.value
            .map((row) =>
              row.tangki_asal
                ? String(
                    row.tangki_asal
                  )
                : null
            )
            .filter(Boolean)
        )

      return daftarTangki.value
        .filter((t) => {
          const id =
            String(t.id)

          const saldo =
            Number(
              t.saldo_kg || 0
            )

          const kode =
            normalisasiKodeTangki(
              t
            )

          /*
           * Sumber WIP harus berasal dari
           * tangki yang memiliki identitas
           * proses yang valid.
           */

          const tangkiValid =
            kode.startsWith(
              'TK-MIX-'
            ) ||
            kode.startsWith(
              'TK-BLD-'
            )

          return (
            t.aktif !== false &&
            tangkiValid &&
            id !== tujuanId &&
            saldo > 0
          )
        })
        .map((t) => {
          const saldo =
            Number(
              t.saldo_kg || 0
            )

          const nilai =
            Number(
              t.saldo_nilai || 0
            )

          const harga =
            Number(
              t.harga_per_kg ||
              (
                saldo > 0
                  ? nilai / saldo
                  : 0
              )
            )

          const namaHasil =
            t.nama_hasil ||
            t.isi_saat_ini ||
            '-'

          const sudahDipakai =
            terpakai.has(
              String(t.id)
            )

          return {
            id: t.id,
            kode: t.kode,
            nama: t.nama,
            nama_hasil:
              namaHasil,

            saldo_kg:
              saldo,

            saldo_nilai:
              nilai,

            harga_per_kg:
              harga,

            disabled:
              sudahDipakai,

            label:
              `${t.kode} • ${namaHasil} • ` +
              `Tersedia ${saldo.toLocaleString(
                'id-ID',
                {
                  minimumFractionDigits: 3,
                  maximumFractionDigits: 3
                }
              )} Kg`
          }
        })
    })

  // =========================================================
  // FORM BARU
  // =========================================================

  async function bukaFormBaru() {
    resetForm()

    editingBatchId.value =
      null

    mode.value =
      'form'

    loadingForm.value =
      true

    try {
      await Promise.all([
        muatTangki(),
        muatRawPool()
      ])

      bomRows.value = [
        buatBarisBom()
      ]

      /*
       * Jangan langsung menentukan WIP.
       *
       * WIP akan dibuat setelah user memilih
       * tangki tujuan TK-BLD-*.
       */

      wipRows.value = []

    } finally {
      loadingForm.value =
        false
    }
  }

  // =========================================================
  // EDIT
  // =========================================================

  async function bukaFormEdit(
    batchId
  ) {
    editingBatchId.value =
      batchId

    mode.value =
      'form'

    loadingForm.value =
      true

    errorMsg.value = ''

    try {
      const [
        detail,
        komposisi
      ] = await Promise.all([
        apiBatch.detail(
          batchId
        ),

        apiBatch.komposisi(
          batchId
        ),

        muatTangki(),
        muatRawPool()
      ])

      form.nama_hasil =
        detail.nama_hasil ||
        ''

      form.tangki_tujuan =
        detail.tangki_tujuan ??
        detail.tangki ??
        ''

      form.batch =
        detail.batch ??
        detail.nomor ??
        detail.nomor_batch ??
        ''

      form.tekor_kg =
        Number(
          detail.tekor_kg ?? 0
        )

      isNamaHasilReadonly.value =
        Boolean(
          form.nama_hasil
        )

      // =====================================================
      // BOM
      // =====================================================

      bomRows.value =
        (
          komposisi?.materials ??
          komposisi?.bahan_baku ??
          []
        ).map(
          (material) => {
            const row =
              buatBarisBom()

            row.raw =
              material.raw ??
              material.produk_id ??
              material.produk

            row.qty =
              Number(
                material.qty_kg ?? 0
              )

            row.saldo =
              Number(
                material.saldo ??
                material.qty_tersedia ??
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

            return row
          }
        )

      if (
        !bomRows.value.length
      ) {
        bomRows.value = [
          buatBarisBom()
        ]
      }

      // =====================================================
      // JENIS OTOMATIS DARI TANGKI
      // =====================================================

      const tangkiTujuan =
        daftarTangki.value.find(
          (t) =>
            String(t.id) ===
            String(
              form.tangki_tujuan
            )
        )

      const jenis =
        tentukanJenisDariTangki(
          tangkiTujuan
        )

      // =====================================================
      // WIP
      // =====================================================

      if (
        jenis === JENIS.BLENDING
      ) {
        const wipSources =
          komposisi?.wip_sources ??
          komposisi?.info_blending ??
          []

        wipRows.value =
          wipSources.map(
            (wip) => {
              const row =
                buatBarisWip()

              /*
               * Backend baru:
               * tangki_sumber_id
               *
               * Compatibility:
               * tangki_asal
               */

              row.tangki_asal =
                wip.tangki_sumber_id ??
                wip.tangki_asal

              row.qty =
                Number(
                  wip.qty_kg ?? 0
                )

              const tangki =
                daftarTangki.value.find(
                  (t) =>
                    String(
                      t.id
                    ) ===
                    String(
                      row.tangki_asal
                    )
                )

              if (tangki) {
                row.nama_hasil =
                  tangki.nama_hasil ||
                  tangki.isi_saat_ini ||
                  ''

                row.tersedia =
                  Number(
                    tangki.saldo_kg ??
                    0
                  )

                row.nilai =
                  Number(
                    tangki.saldo_nilai ??
                    0
                  )

                row.harga =
                  Number(
                    tangki.harga_per_kg ??
                    0
                  )

              } else {
                row.nama_hasil =
                  wip.nama_hasil ||
                  ''

                row.tersedia =
                  Number(
                    wip.tersedia ??
                    wip.sisa_qty ??
                    0
                  )

                row.nilai =
                  Number(
                    wip.nilai ??
                    0
                  )

                row.harga =
                  Number(
                    wip.harga_per_kg ??
                    0
                  )
              }

              return row
            }
          )

        if (
          !wipRows.value.length
        ) {
          wipRows.value = [
            buatBarisWip()
          ]
        }

      } else {
        wipRows.value = []
      }

      pratinjau.value =
        null

    } catch (error) {
      console.error(error)

      errorMsg.value =
        'Gagal memuat detail batch'

    } finally {
      loadingForm.value =
        false
    }
  }

  // =========================================================
  // TUTUP FORM
  // =========================================================

  function tutupForm() {
    mode.value = 'list'

    resetForm()
  }

  // =========================================================
  // RESET
  // =========================================================

  function resetForm() {
    form.nama_hasil = ''
    form.tangki_tujuan = ''
    form.batch = ''
    form.tekor_kg = 0

    editingBatchId.value =
      null

    isNamaHasilReadonly.value =
      false

    bomRows.value = []
    wipRows.value = []

    pratinjau.value =
      null

    errorMsg.value =
      ''
  }

  // =========================================================
  // TAMBAH TANGKI
  // =========================================================

  async function tambahTangkiBaru(
    nama
  ) {
    const namaBersih =
      String(
        nama || ''
      )
        .trim()
        .toUpperCase()

    if (!namaBersih) {
      return null
    }

    const existing =
      daftarTangki.value.find(
        (t) =>
          String(
            t.nama ||
            t.kode ||
            ''
          ).toUpperCase() ===
          namaBersih
      )

    if (existing) {
      return existing
    }

    try {
      const dibuat =
        await apiTangki.buat({
          nama: namaBersih,
          kode: namaBersih
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

  // =========================================================
  // GENERATE BATCH
  // =========================================================
  //
  // Untuk generate nomor batch, jenis masih ditentukan
  // dari tangki tujuan.
  //
  // BUKAN dari state jenisProduksi manual.
  // =========================================================

  async function generateNomorBatch() {
    const jenis =
      jenisProduksi.value

    if (!jenis) {
      errorMsg.value =
        'Pilih tangki tujuan terlebih dahulu'

      return
    }

    try {
      const res =
        await apiBatch.nomorBaru(
          jenis
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

  // =========================================================
  // BOM
  // =========================================================

  function tambahBomRow() {
    bomRows.value.push(
      buatBarisBom()
    )
  }

  function hapusBomRow(id) {
    if (
      bomRows.value.length <= 1
    ) {
      return
    }

    bomRows.value =
      bomRows.value.filter(
        (row) =>
          row._id !== id
      )
  }

  function perbaruiTelemetriBom(
    row
  ) {
    const item =
      daftarRaw.value.find(
        (item) =>
          String(item.raw) ===
          String(row.raw)
      )

    row.saldo =
      item
        ? Number(
            item.qty_kg || 0
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
        Number(row.qty) || 0
      ) *
      (
        Number(row.harga) || 0
      )
  }

  // =========================================================
  // WIP
  // =========================================================

  function tambahWipRow() {
    if (
      !isBlending.value
    ) {
      return
    }

    wipRows.value.push(
      buatBarisWip()
    )
  }

  function hapusWipRow(id) {
    wipRows.value =
      wipRows.value.filter(
        (row) =>
          row._id !== id
      )
  }

  // =========================================================
  // PILIH TANGKI SUMBER
  // =========================================================
  //
  // TIDAK ADA PEMILIHAN BATCH SUMBER.
  // Saldo dan harga langsung berasal dari tangki.
  // =========================================================

  function saatTangkiAsalDipilih(
    row
  ) {
    row.nama_hasil = ''
    row.tersedia = 0
    row.nilai = 0
    row.harga = 0

    if (!row.tangki_asal) {
      return
    }

    const tujuanId =
      String(
        form.tangki_tujuan
      )

    if (
      String(
        row.tangki_asal
      ) === tujuanId
    ) {
      row.tangki_asal = ''

      return
    }

    const tangki =
      daftarTangki.value.find(
        (t) =>
          String(t.id) ===
          String(
            row.tangki_asal
          )
      )

    if (!tangki) {
      return
    }

    row.nama_hasil =
      tangki.nama_hasil ||
      tangki.isi_saat_ini ||
      ''

    row.tersedia =
      Number(
        tangki.saldo_kg || 0
      )

    row.nilai =
      Number(
        tangki.saldo_nilai || 0
      )

    row.harga =
      Number(
        tangki.harga_per_kg ||
        (
          row.tersedia > 0
            ? row.nilai /
              row.tersedia
            : 0
        )
      )
  }

  // =========================================================
  // TOTAL BOM
  // =========================================================

  const totalQtyBom =
    computed(() =>
      bomRows.value.reduce(
        (sum, row) =>
          sum +
          (
            Number(row.qty) || 0
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
            Number(row.qty) || 0
          ) *
          (
            Number(row.harga) || 0
          ),
        0
      )
    )

  // =========================================================
  // TOTAL WIP
  // =========================================================

  const totalQtyWip =
    computed(() => {
      if (
        !isBlending.value
      ) {
        return 0
      }

      return wipRows.value.reduce(
        (sum, row) =>
          sum +
          (
            Number(row.qty) || 0
          ),
        0
      )
    })

  const totalNilaiWip =
    computed(() => {
      if (
        !isBlending.value
      ) {
        return 0
      }

      return wipRows.value.reduce(
        (sum, row) =>
          sum +
          (
            Number(row.qty) || 0
          ) *
          (
            Number(row.harga) || 0
          ),
        0
      )
    })

  // =========================================================
  // TOTAL INPUT
  // =========================================================

  const totalInputKg =
    computed(() =>
      totalQtyBom.value +
      totalQtyWip.value
    )

  const totalInputNilai =
    computed(() =>
      totalNilaiBom.value +
      totalNilaiWip.value
    )

  const proyeksiYield =
    computed(() =>
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

  // =========================================================
  // PAYLOAD
  // =========================================================
  //
  // PENTING:
  // TIDAK ADA `jenis`
  //
  // Jenis proses diketahui dari kode tangki tujuan.
  //
  // WIP source hanya:
  // tangki_sumber_id + qty_kg
  //
  // Tidak ada batch source.
  // =========================================================

  function susunPayload() {
    const payload = {
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
            (row) =>
              row.raw &&
              Number(row.qty) > 0
          )
          .map((row) => ({
            raw:
              String(row.raw),

            qty_kg:
              Number(row.qty)
          })),

      wip_sources: []
    }

    // =======================================================
    // WIP HANYA UNTUK TANGKI TK-BLD-*
    // =======================================================

    if (
      isBlending.value
    ) {
      payload.wip_sources =
        wipRows.value
          .filter(
            (row) =>
              row.tangki_asal &&
              Number(row.qty) > 0
          )
          .map((row) => ({
            tangki_sumber_id:
              Number(
                row.tangki_asal
              ),

            qty_kg:
              Number(
                row.qty
              )
          }))
    }

    return payload
  }

  // =========================================================
  // VALIDASI
  // =========================================================

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
      daftarTangki.value.find(
        (t) =>
          String(t.id) ===
          String(
            form.tangki_tujuan
          )
      )

    if (!tangkiTujuan) {
      return (
        'Tangki tujuan tidak ditemukan'
      )
    }

    const jenis =
      tentukanJenisDariTangki(
        tangkiTujuan
      )

    if (!jenis) {
      return (
        'Kode tangki tujuan tidak dikenali. Gunakan TK-MIX-* atau TK-BLD-*'
      )
    }

    if (
      !form.batch.trim()
    ) {
      return (
        'Nomor batch wajib diisi'
      )
    }

    const adaBom =
      bomRows.value.some(
        (row) =>
          row.raw &&
          Number(row.qty) > 0
      )

    const adaWip =
      jenis === JENIS.BLENDING &&
      wipRows.value.some(
        (row) =>
          row.tangki_asal &&
          Number(row.qty) > 0
      )

    // =======================================================
    // MIXING
    // =======================================================

    if (
      jenis === JENIS.MIXING &&
      !adaBom
    ) {
      return (
        'Minimal satu baris bahan baku harus diisi'
      )
    }

    // =======================================================
    // BLENDING
    // =======================================================

    if (
      jenis === JENIS.BLENDING &&
      !adaBom &&
      !adaWip
    ) {
      return (
        'Minimal satu sumber WIP atau bahan baku harus diisi'
      )
    }

    // =======================================================
    // TANGKI SUMBER
    // =======================================================

    const tujuanId =
      String(
        form.tangki_tujuan
      )

    for (
      const row of
      wipRows.value
    ) {
      if (
        !row.tangki_asal
      ) {
        continue
      }

      if (
        String(
          row.tangki_asal
        ) === tujuanId
      ) {
        return (
          'Tangki tujuan tidak boleh digunakan sebagai tangki sumber WIP.'
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
          `Saldo WIP tangki sumber tidak cukup. ` +
          `Diminta ${qty.toFixed(
            3
          )} Kg, ` +
          `tersedia ${tersedia.toFixed(
            3
          )} Kg.`
        )
      }
    }

    // =======================================================
    // SALDO BOM
    // =======================================================

    for (
      const row of
      bomRows.value
    ) {
      if (
        row.raw &&
        Number(row.qty) >
          Number(
            row.saldo
          ) + 0.001
      ) {
        return (
          `Saldo pool tidak cukup. ` +
          `Diminta ${Number(
            row.qty
          ).toFixed(
            3
          )} Kg, ` +
          `tersedia ${Number(
            row.saldo
          ).toFixed(
            3
          )} Kg.`
        )
      }
    }

    // =======================================================
    // DUPLIKASI TANGKI SUMBER
    // =======================================================

    const sumberIds =
      wipRows.value
        .filter(
          (row) =>
            row.tangki_asal &&
            Number(
              row.qty
            ) > 0
        )
        .map(
          (row) =>
            String(
              row.tangki_asal
            )
        )

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

    // =======================================================
    // YIELD
    // =======================================================

    if (
      proyeksiYield.value <= 0
    ) {
      return (
        'Yield harus positif setelah dikurangi tekor/shrinkage'
      )
    }

    return ''
  }

  // =========================================================
  // PREVIEW
  // =========================================================

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
              (item) =>
                item.pesan
            )
            .join(' | ') ||
          'Kalkulasi ditolak server.'
      }

      return res

    } catch (error) {
      console.error(error)

      errorMsg.value =
        error?.response
          ?.data
          ?.pesan ||
        error?.response
          ?.data
          ?.detail ||
        'Gagal terhubung ke server untuk kalkulasi.'

      return null
    }
  }

  // =========================================================
  // SAVE
  // =========================================================

  async function simpanDanPosting() {
    errorMsg.value =
      validasiForm()

    if (
      errorMsg.value
    ) {
      return false
    }

    submitting.value = true

    try {
      const payload =
        susunPayload()

      if (
        editingBatchId.value
      ) {
        await apiBatch.ubah(
          editingBatchId.value,
          payload
        )
      } else {
        await apiBatch.buat(
          payload
        )
      }

      await Promise.all([
        muatDaftarBatch(),
        muatTangki(),
        muatRawPool()
      ])

      tutupForm()

      return true

    } catch (error) {
      console.error(error)

      const data =
        error?.response?.data

      if (
        typeof data ===
        'object' &&
        data !== null
      ) {
        const firstError =
          Object.values(
            data
          )[0]

        errorMsg.value =
          typeof firstError ===
          'string'
            ? firstError
            : JSON.stringify(
                firstError
              )
      } else {
        errorMsg.value =
          error?.message ||
          'Gagal menyimpan batch produksi'
      }

      return false

    } finally {
      submitting.value =
        false
    }
  }

  // =========================================================
  // WATCH
  // =========================================================

  watch(
    bomRows,
    (rows) => {
      rows.forEach(
        (row) => {
          row.subtotal =
            (
              Number(row.qty) ||
              0
            ) *
            (
              Number(row.harga) ||
              0
            )
        }
      )
    },
    {
      deep: true
    }
  )

  watch(
    () => form.tangki_tujuan,
    () => {
      saatTangkiTujuanDipilih()
    }
  )

  onMounted(() => {
    initHalaman()
  })

  return {
    JENIS,

    mode,
    jenisProduksi,
    isBlending,
    isMixing,

    editingBatchId,

    loadingList,
    loadingForm,
    submitting,
    errorMsg,

    daftarTangki,
    daftarRaw,
    daftarBatch,

    filter,

    form,

    bomRows,
    wipRows,
    pratinjau,

    isNamaHasilReadonly,
    opsiTangkiSumber,

    totalQtyBom,
    totalNilaiBom,
    totalQtyWip,
    totalNilaiWip,
    totalInputKg,
    totalInputNilai,
    proyeksiYield,
    proyeksiHargaRata,

    muatTangki,
    muatRawPool,
    muatDaftarBatch,

    bukaFormBaru,
    bukaFormEdit,
    tutupForm,
    resetForm,

    tambahTangkiBaru,
    generateNomorBatch,

    tambahBomRow,
    hapusBomRow,
    perbaruiTelemetriBom,

    tambahWipRow,
    hapusWipRow,
    saatTangkiAsalDipilih,
    saatTangkiTujuanDipilih,

    mintaPratinjau,
    simpanDanPosting
  }
}