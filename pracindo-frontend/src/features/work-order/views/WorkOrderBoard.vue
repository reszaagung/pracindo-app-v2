<template>
    <div class="wo-board animate-fade-in">
        <header
            :class="[
                'flex justify-between gap-4 mb-8 pb-6 border-b border-slate-200',
                isMobile ? 'flex-col' : 'flex-row items-center'
            ]"
        >
            <div class="flex items-center gap-4">
                <div
                    :class="[
                        'bg-slate-900 rounded-xl flex items-center justify-center shrink-0 shadow-sm',
                        isMobile ? 'w-10 h-10' : 'w-12 h-12'
                    ]"
                >
                    <i
                        :class="[
                            'pi pi-desktop text-teal-400',
                            isMobile ? 'text-lg' : 'text-xl'
                        ]"
                    />
                </div>

                <div class="flex flex-col">
                    <h1
                        :class="[
                            'font-black text-slate-900 leading-tight m-0 tracking-tight',
                            isMobile ? 'text-2xl' : 'text-3xl'
                        ]"
                    >
                        Mading Operasional
                    </h1>

                    <p
                        :class="[
                            'text-slate-500 mt-1 m-0',
                            isMobile ? 'text-xs' : 'text-sm'
                        ]"
                    >
                        Kontrol pusat pesanan pabrik dan penugasan tim.
                    </p>
                </div>
            </div>

            <div :class="['flex gap-3', isMobile ? 'w-full' : 'w-auto']">
                <button
                    @click="bukaModalBuat"
                    class="btn-primary-tech"
                    :class="isMobile ? 'flex-1 justify-center' : ''"
                >
                    <i class="pi pi-plus" />
                    <span>{{ isMobile ? 'Tugas Baru' : 'Buat Tugas Baru' }}</span>
                </button>

                <button
                    @click="fetchMading"
                    class="btn-icon-tech shrink-0"
                    aria-label="Refresh"
                >
                    <i class="pi pi-refresh" :class="{ 'pi-spin': isLoading }" />
                </button>
            </div>
        </header>

        <div v-if="isLoading && madingList.length === 0" class="wo-loading">
            <div class="loader-pulse"></div>
            <p>Sinkronisasi data...</p>
        </div>

        <div v-else-if="!isLoading && madingList.length === 0" class="wo-empty">
            <div class="empty-glow">
                <i class="pi pi-check-circle"></i>
            </div>

            <h3>Panel Tugas</h3>
            <p>Tidak ada antrean pesanan atau tugas aktif. Ruang kerja bersih!</p>
        </div>

        <div
            v-else
            class="wo-grid"
            :data-count="madingList.length > 4 ? 'more' : madingList.length"
        >
            <PostWorkOrderCard
                v-for="wo in madingList"
                :key="wo.id"
                :wo="wo"
                :currentUserId="currentUserId"
                @open-chat="openChatModal"
                @approve="handleApprove"
                @close-session="handleCloseSession"
            />
        </div>

        <Dialog
            appendTo="body"
            v-model:visible="isCreateOpen"
            modal
            class="tech-modal create-modal"
            :style="{ width: '600px' }"
        >
            <template #header>
                <div>
                    <div class="p-dialog-title">Inisiasi Tugas Baru</div>
                    <p class="modal-subtitle">
                        Isi detail untuk menugaskan pekerjaan baru.
                    </p>
                </div>
            </template>

            <form @submit.prevent="handleCreate" class="tech-form">
                <div class="form-row">
                    <div class="input-wrap">
                        <label>Target Penerima Tugas (PIC)</label>

                        <MultiSelect
                            v-model="formCreate.staff_ids"
                            :options="staffTanpaPembuat"
                            optionLabel="nama_lengkap"
                            optionValue="id"
                            placeholder="Pilih pelaksana..."
                            display="chip"
                            filter
                            fluid
                        />
                    </div>

                    <div class="input-wrap">
                        <label>Tenggat Waktu</label>

                        <input
                            v-model="formCreate.deadline"
                            type="datetime-local"
                            class="neo-input"
                        />
                    </div>
                </div>

                <div class="input-wrap">
                    <label>Identifikasi Tugas</label>

                    <input
                        v-model="formCreate.judul"
                        type="text"
                        required
                        class="neo-input"
                        placeholder="Masukkan judul spesifik..."
                    />
                </div>

                <div class="input-wrap">
                    <label>Parameter Detail</label>

                    <textarea
                        v-model="formCreate.deskripsi"
                        rows="5"
                        class="neo-input resize-none"
                        placeholder="Uraikan instruksi pekerjaan di sini..."
                    ></textarea>
                </div>

                <div class="form-footer">
                    <button
                        type="button"
                        @click="isCreateOpen = false"
                        class="btn-ghost"
                        :disabled="isCreating"
                    >
                        Batalkan
                    </button>

                    <button
                        type="submit"
                        :disabled="isCreating"
                        class="btn-primary-tech"
                    >
                        <i
                            v-if="isCreating"
                            class="pi pi-spin pi-spinner"
                        ></i>

                        {{ isCreating ? 'Memproses...' : 'Eksekusi Tugas' }}
                    </button>
                </div>
            </form>
        </Dialog>

        <Dialog
            appendTo="body"
            v-model:visible="isChatOpen"
            modal
            header="Terminal Diskusi"
            :style="{ width: '450px' }"
            class="tech-modal"
        >
            <div v-if="activeWO" class="chat-wrapper">
                <div class="chat-feed custom-scroll" ref="chatBox">
                    <div
                        v-if="activeWO.pesan_chat.length === 0"
                        class="chat-blank"
                    >
                        <i class="pi pi-wave-pulse"></i>
                        <p>
                            Saluran komunikasi terbuka. Belum ada aktivitas.
                        </p>
                    </div>

                    <div
                        v-for="msg in activeWO.pesan_chat"
                        :key="msg.id"
                        class="message-block"
                    >
                        <span class="sender-id">
                            {{ msg.pengirim_nama }}
                        </span>

                        <div class="message-core">
                            {{ msg.teks }}
                        </div>
                    </div>
                </div>

                <div class="chat-control">
                    <input
                        v-model="chatInput"
                        type="text"
                        @keyup.enter="kirimPesan"
                        placeholder="Transmisikan pesan..."
                        class="neo-input"
                    />

                    <button
                        @click="kirimPesan"
                        :disabled="isSending || !chatInput.trim()"
                        class="btn-send-tech"
                    >
                        <i
                            class="pi pi-send"
                            :class="{ 'pi-spin pi-spinner': isSending }"
                        ></i>
                    </button>
                </div>
            </div>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, computed } from 'vue'
import { useWorkOrder } from '@/features/work-order/composables/useWorkOrder'
import Dialog from 'primevue/dialog'
import MultiSelect from 'primevue/multiselect'
import PostWorkOrderCard from '../components/PostWorkOrderCard.vue'
import { useDevice } from '@/composables/useDevice'
import { useAuth } from '@/composables/useAuth'

const { isMobile } = useDevice()
const { profil } = useAuth()

const {
    isLoading,
    isSending,
    isCreating,
    madingList,
    staffList,
    fetchMading,
    fetchStaff,
    approveTask,
    sendReply,
    createTask,
    fetchChat,
    // Kalau nama fungsi tutup-sesi di composable berbeda, sesuaikan di sini.
    closeTask
} = useWorkOrder()

const currentUserId = computed(() => profil.value?.id || 0)

const staffTanpaPembuat = computed(() =>
    staffList.value.filter(staff => staff.id !== currentUserId.value)
)

const isChatOpen = ref(false)
const isCreateOpen = ref(false)
const activeWO = ref(null)
const chatInput = ref('')
const chatBox = ref(null)

const formCreate = reactive({
    judul: '',
    deskripsi: '',
    kategori: 'UMUM',
    deadline: '',
    staff_ids: []
})

onMounted(() => {
    fetchMading()
    fetchStaff()
})

const bukaModalBuat = () => {
    Object.assign(formCreate, {
        judul: '',
        deskripsi: '',
        kategori: 'UMUM',
        deadline: '',
        staff_ids: []
    })

    isCreateOpen.value = true
}

const handleCreate = async () => {
    const payload = { ...formCreate }

    if (!payload.deadline) {
        delete payload.deadline
    } else {
        // <input type="datetime-local"> menghasilkan string "2026-09-20T14:30".
        // Kirim tanggal + jam lengkap (ISO). Kalau backend field-nya DateField
        // (tanggal saja), ganti baris ini jadi: payload.deadline = payload.deadline.slice(0, 10)
        payload.deadline = payload.deadline.length === 16
            ? payload.deadline + ':00'
            : payload.deadline
    }

    const res = await createTask(payload)
    if (res.success) {
        isCreateOpen.value = false
    } else {
        alert(`Gagal: ${res.message}`)
    }
}

const handleApprove = async (wo) => {
    if (wo.pembuat_id === currentUserId.value) {
        alert(
            'Akses Ditolak: Anda adalah pemberi tugas. Hanya penerima tugas (PIC) yang dapat menyelesaikan tugas ini.'
        )
        return
    }

    if (confirm('Konfirmasi: Tandai tugas ini sebagai selesai?')) {
        await approveTask(wo.id)
    }
}

const handleCloseSession = async (wo) => {
    if (confirm('Tutup sesi tugas ini? Kartu akan disembunyikan dari Mading.')) {
        await closeTask(wo.id)
    }
}

const openChatModal = async (wo) => {
    activeWO.value = {
        ...wo,
        pesan_chat: []
    }

    isChatOpen.value = true
    activeWO.value.pesan_chat = await fetchChat(wo.id)

    scrollToBottom()
}

const kirimPesan = async () => {
    if (!activeWO.value || !chatInput.value.trim()) return

    const pesanBaru = await sendReply(
        activeWO.value.id,
        chatInput.value
    )

    if (pesanBaru) {
        activeWO.value.pesan_chat.push(pesanBaru)
        chatInput.value = ''
        scrollToBottom()
        fetchMading()
    }
}

const scrollToBottom = () => {
    nextTick(() => {
        if (chatBox.value) {
            chatBox.value.scrollTop = chatBox.value.scrollHeight
        }
    })
}
</script>

<style scoped>
.wo-board {
    box-sizing: border-box;
    padding: 2rem;
    max-width: 1440px;
    margin: 0 auto;
    font-family: 'Inter', -apple-system, sans-serif;
    color: #0f172a;
}

.btn-primary-tech {
    background: linear-gradient(180deg, #0d9488 0%, #0f766e 100%);
    color: #fff;
    border: 1px solid #115e59;
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.875rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    box-shadow: 0 2px 4px rgba(13, 148, 136, 0.2);
    transition: 0.2s;
}

.btn-primary-tech:hover:not(:disabled) {
    background: linear-gradient(180deg, #14b8a6 0%, #0d9488 100%);
    transform: translateY(-1px);
}

.btn-icon-tech {
    background: #fff;
    border: 1px solid #e2e8f0;
    color: #475569;
    padding: 0.6rem 0.8rem;
    border-radius: 8px;
    cursor: pointer;
}

.wo-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding: 5rem 0;
    color: #64748b;
}

.loader-pulse {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background: #14b8a6;
    animation: pulse-glow 1.5s infinite;
}

@keyframes pulse-glow {
    0% {
        transform: scale(0.9);
        box-shadow: 0 0 0 0 rgba(20, 184, 166, 0.5);
    }

    70% {
        transform: scale(1);
        box-shadow: 0 0 0 15px rgba(20, 184, 166, 0);
    }

    100% {
        transform: scale(0.9);
        box-shadow: 0 0 0 0 rgba(20, 184, 166, 0);
    }
}

.wo-empty {
    padding: 5rem 2rem;
    text-align: center;
    background: linear-gradient(to bottom, #fff, #f8fafc);
    border: 1px dashed #cbd5e1;
    border-radius: 16px;
}

.empty-glow {
    width: 5rem;
    height: 5rem;
    margin: 0 auto 1.5rem;
    background: #f0fdfa;
    color: #0d9488;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
}

.wo-empty h3 {
    font-size: 1.25rem;
    font-weight: 700;
    margin: 0 0 0.5rem;
}

.wo-empty p {
    color: #64748b;
    margin: 0;
}

.wo-grid {
    display: grid;
    gap: 1.5rem;
}

.wo-grid[data-count="1"] {
    grid-template-columns: 1fr;
    max-width: 450px;
}

.wo-grid[data-count="2"] {
    grid-template-columns: repeat(2, 1fr);
    max-width: 900px;
}

.wo-grid[data-count="3"] {
    grid-template-columns: repeat(3, 1fr);
}

.wo-grid[data-count="4"],
.wo-grid[data-count="more"] {
    grid-template-columns: repeat(4, 1fr);
}

.tech-form {
    display: flex;
    flex-direction: column;
    gap: 1.75rem;
    padding-top: 0.5rem;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
}

.input-wrap {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.input-wrap label {
    font-size: 0.75rem;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.neo-input {
    width: 100%;
    box-sizing: border-box;
    background: #fff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    font-size: 0.95rem;
    color: #0f172a;
    font-family: inherit;
}

.neo-input:focus {
    outline: none;
    border-color: #14b8a6;
    box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1);
}

.resize-none {
    resize: none;
}

.form-footer {
    display: flex;
    justify-content: flex-end;
    gap: 0.75rem;
    margin-top: 0.5rem;
}

.btn-ghost {
    background: transparent;
    color: #64748b;
    font-weight: 600;
    border: none;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    cursor: pointer;
}

.chat-wrapper {
    display: flex;
    flex-direction: column;
    height: 420px;
}

.chat-feed {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.chat-blank {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #94a3b8;
}

.chat-blank i {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.message-block {
    display: flex;
    flex-direction: column;
}

.sender-id {
    font-size: 0.65rem;
    font-weight: 700;
    color: #64748b;
    margin: 0 0 0.2rem 0.5rem;
    text-transform: uppercase;
}

.message-core {
    background: #fff;
    border: 1px solid #e2e8f0;
    padding: 0.75rem 1rem;
    border-radius: 12px;
    border-top-left-radius: 2px;
    font-size: 0.875rem;
    color: #1e293b;
    width: fit-content;
    max-width: 90%;
}

.chat-control {
    margin-top: 1.25rem;
    display: flex;
    gap: 0.5rem;
}

.btn-send-tech {
    background: #0f172a;
    color: #fff;
    width: 2.75rem;
    height: 2.75rem;
    border: none;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.custom-scroll::-webkit-scrollbar {
    width: 5px;
}

.custom-scroll::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
}

@media (max-width: 1024px) {
    .wo-grid[data-count="3"],
    .wo-grid[data-count="4"],
    .wo-grid[data-count="more"] {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .wo-board {
        padding: 1rem;
    }

    .wo-grid[data-count] {
        grid-template-columns: 1fr;
        max-width: 100%;
    }

    .form-row {
        grid-template-columns: 1fr;
    }
}

.animate-fade-in {
    animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>

<style>
.tech-modal.p-dialog {
    border-radius: 14px;
    overflow: hidden;
}

.tech-modal .p-dialog-header {
    background: #fff;
    border-bottom: 1px solid #f1f5f9;
    padding: 1.5rem 2rem;
}

.tech-modal .p-dialog-content {
    padding: 2rem;
    background: #fafaf9;
}

.tech-modal .p-dialog-title {
    font-weight: 700;
    font-size: 1.125rem;
    color: #0f172a;
}

.tech-modal .modal-subtitle {
    margin: 0.25rem 0 0;
    font-size: 0.8rem;
    color: #64748b;
}

/* MultiSelect */
.tech-modal .p-multiselect {
    min-height: 48px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    background: #fff;
}

.tech-modal .p-multiselect.p-focus,
.tech-modal .p-multiselect:focus-within {
    border-color: #14b8a6 !important;
    box-shadow: 0 0 0 3px rgba(20, 184, 166, .1) !important;
}

/* Search */
.p-multiselect-overlay .p-multiselect-filter,
.p-multiselect-panel .p-multiselect-filter {
    width: 100% !important;
    height: 38px !important;
    box-sizing: border-box !important;
    padding: .5rem .75rem !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 6px !important;
    background: #fff !important;
}

/* Checkbox */
.p-multiselect-overlay .p-checkbox,
.p-multiselect-panel .p-checkbox {
    width: 20px !important;
    height: 20px !important;
    min-width: 20px !important;
    flex: 0 0 20px !important;
}

.p-multiselect-overlay .p-checkbox-input,
.p-multiselect-panel .p-checkbox-input {
    width: 20px !important;
    height: 20px !important;
    margin: 0 !important;
    padding: 0 !important;
    opacity: 0 !important;
}

.p-multiselect-overlay .p-checkbox-box,
.p-multiselect-panel .p-checkbox-box {
    width: 20px !important;
    height: 20px !important;
    border-radius: 5px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
}

.p-multiselect-overlay .p-checkbox-checked .p-checkbox-box,
.p-multiselect-panel .p-checkbox-checked .p-checkbox-box {
    background: #14b8a6 !important;
    border-color: #14b8a6 !important;
}

/* Option */
.p-multiselect-overlay .p-multiselect-option,
.p-multiselect-panel .p-multiselect-option {
    display: flex !important;
    align-items: center !important;
    gap: .65rem !important;
    min-height: 42px !important;
    padding: .65rem 1rem !important;
}

.tech-modal .p-chip {
    background: #f0fdfa !important;
    color: #0f766e !important;
    border: 1px solid #ccfbf1 !important;
}

/* ============================================================
   MOBILE MODAL
   ============================================================ */

.create-modal.p-dialog {
    width: 600px !important;
    max-width: calc(100vw - 24px) !important;
    max-height: calc(100dvh - 24px) !important;
    margin: 12px !important;
}

.create-modal .p-dialog-content {
    overflow-y: auto !important;
}

@media (max-width: 768px) {
    .create-modal.p-dialog {
        width: calc(100vw - 24px) !important;
        max-width: calc(100vw - 24px) !important;
        max-height: calc(100dvh - 16px) !important;
        margin: 8px !important;
        border-radius: 16px !important;
    }

    .create-modal .p-dialog-header {
        padding: 1.25rem !important;
    }

    .create-modal .p-dialog-content {
        padding: 1.25rem !important;
        background: #fafaf9;
    }

    .create-modal .tech-form {
        gap: 1.25rem;
    }

    .create-modal .form-row {
        grid-template-columns: 1fr;
        gap: 1.25rem;
    }

    .create-modal .input-wrap {
        gap: 0.4rem;
    }

    .create-modal .form-footer {
        position: sticky;
        bottom: 0;
        z-index: 5;

        margin: 0 -1.25rem -1.25rem;
        padding: 1rem 1.25rem;

        background: rgba(250, 250, 249, 0.96);
        border-top: 1px solid #e2e8f0;
        backdrop-filter: blur(8px);
    }

    .create-modal .btn-primary-tech {
        min-height: 44px;
    }

    .create-modal .btn-ghost {
        min-height: 44px;
    }
}

@media (max-width: 768px) {
    .create-modal .p-multiselect,
    .create-modal .neo-input {
        width: 100% !important;
        min-height: 48px;
    }

    .create-modal textarea.neo-input {
        min-height: 130px;
    }
}
</style>