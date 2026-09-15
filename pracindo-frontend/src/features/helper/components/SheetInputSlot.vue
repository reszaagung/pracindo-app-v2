<template>
  <Teleport to="body">
    <Transition name="sheet">
      <div v-if="visible" class="fixed inset-0 z-[60] flex items-end lg:hidden">
        <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" @click="$emit('tutup')"></div>
        <div class="relative w-full bg-white rounded-t-3xl shadow-2xl p-5 pb-8 max-h-[85vh] overflow-y-auto">
          <div class="w-10 h-1.5 bg-slate-200 rounded-full mx-auto mb-4"></div>

          <div class="relative mb-5 pr-10">
            <button
              type="button"
              @click="$emit('tutup')"
              class="absolute top-0 right-0 w-9 h-9 flex items-center justify-center text-slate-400 hover:text-red-500 rounded-full hover:bg-red-50 transition-colors"
            >
              <i class="pi pi-times text-base"></i>
            </button>
            <h3 class="text-lg font-black text-slate-800 leading-snug break-words">
              Slot {{ nomorSlot }} <span class="text-blue-600">· Pola {{ huruf }}</span>
            </h3>
            <p class="text-xs text-slate-400 mt-1">Isi data untuk grup huruf {{ huruf }}</p>
          </div>

          <div class="flex flex-col gap-4">
            <div class="flex flex-col gap-2">
              <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Nama Barang</label>
              <InputText class="p-3 border-slate-300 rounded-xl w-full" placeholder="Misal: SUPER WHITE" v-model="item.nama_item"/>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Tipe Barang</label>
              <InputText class="p-3 border-slate-300 rounded-xl w-full" placeholder="Misal: SC SC" v-model="item.tipe"/>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Tanggal Lot</label>
              <Calendar :pt="{ input: { class: 'p-3 border-slate-300 rounded-xl w-full' } }" class="w-full" dateFormat="yy-mm-dd" placeholder="Pilih Tanggal" v-model="item.lot"/>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs font-bold text-slate-600 uppercase tracking-wide">Net (KGS)</label>
              <InputNumber :maxFractionDigits="2" :minFractionDigits="2" :pt="{ input: { class: 'p-3 border-slate-300 rounded-xl w-full' } }" class="w-full" mode="decimal" placeholder="0.00" v-model="item.net"/>
            </div>
          </div>

          <button
            type="button"
            @click="simpan"
            class="mt-6 w-full bg-slate-900 hover:bg-slate-800 text-white font-bold py-3.5 rounded-xl flex items-center justify-center gap-2 transition-colors shadow-md"
          >
            <i class="pi pi-check"></i>
            {{ item.is_saved ? `Perbarui Slot ${nomorSlot}` : `Simpan Slot ${nomorSlot}` }}
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Calendar from 'primevue/calendar'
import { useToast } from 'primevue/usetoast'

const props = defineProps({
  visible: { type: Boolean, default: false },
  huruf: { type: String, default: '' },
  nomorSlot: { type: Number, default: 1 },
  item: { type: Object, required: true }
})
const emit = defineEmits(['tutup', 'simpan'])

const toast = useToast()

const simpan = () => {
  const netKosong = props.item.net === null || props.item.net === undefined
  if (!props.item.nama_item?.trim() || !props.item.tipe?.trim() || !props.item.lot || netKosong) {
    toast.add({
      severity: 'warn',
      summary: 'Data belum lengkap',
      detail: `Lengkapi semua field untuk Slot ${props.nomorSlot} terlebih dahulu`,
      life: 3000
    })
    return
  }
  props.item.is_saved = true
  emit('simpan')
  emit('tutup')
}
</script>

<style scoped>
.sheet-enter-active, .sheet-leave-active { transition: opacity 0.22s ease; }
.sheet-enter-from, .sheet-leave-to { opacity: 0; }
.sheet-enter-active .relative, .sheet-leave-active .relative { transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1); }
.sheet-enter-from .relative, .sheet-leave-to .relative { transform: translateY(24px); }
</style>