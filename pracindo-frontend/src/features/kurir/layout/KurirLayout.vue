<template>
    <div class="min-h-screen bg-slate-50 text-slate-900">
        <main class="min-h-screen pb-[92px]">
            <router-view v-slot="{ Component }">
                <transition name="kurir-page" mode="out-in">
                    <component :is="Component" />
                </transition>
            </router-view>
        </main>

        <nav
            aria-label="Navigasi utama kurir"
            class="fixed inset-x-0 bottom-0 z-50 px-3 pb-safe-area"
        >
            <div
                class="mx-auto flex h-[76px] max-w-md items-center rounded-t-[24px] border border-slate-200 bg-white/95 px-3 shadow-[0_-12px_35px_rgba(15,23,42,0.08)] backdrop-blur-xl"
            >
                <router-link
                    to="/kurir/permintaan"
                    aria-label="Buka halaman Permintaan"
                    :aria-current="$route.path.includes('/kurir/permintaan') ? 'page' : undefined"
                    class="group relative flex h-full flex-1 flex-col items-center justify-center gap-1.5 text-slate-400 transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    active-class="text-blue-600"
                >
                    <div
                        aria-hidden="true"
                        class="nav-icon"
                        :class="{
                            'nav-icon-active': $route.path.includes('/kurir/permintaan')
                        }"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-[21px] w-[21px]"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            stroke-width="1.8"
                            focusable="false"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                            />
                        </svg>
                    </div>

                    <span class="nav-label">Permintaan</span>

                    <span
                        v-if="$route.path.includes('/kurir/permintaan')"
                        aria-hidden="true"
                        class="absolute bottom-1 h-1 w-7 rounded-full bg-blue-600"
                    />
                </router-link>

                <router-link
                    to="/kurir/tugas-saya"
                    aria-label="Buka halaman Tugas Saya"
                    :aria-current="$route.path.includes('/kurir/tugas-saya') ? 'page' : undefined"
                    class="group relative flex h-full flex-1 flex-col items-center justify-center gap-1.5 text-slate-400 transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    active-class="text-blue-600"
                >
                    <div
                        aria-hidden="true"
                        class="nav-icon"
                        :class="{
                            'nav-icon-active': $route.path.includes('/kurir/tugas-saya')
                        }"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-[21px] w-[21px]"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            stroke-width="1.8"
                            focusable="false"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z"
                            />
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a2 2 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0"
                            />
                        </svg>
                    </div>

                    <span class="nav-label">Tugas Saya</span>

                    <span
                        v-if="$route.path.includes('/kurir/tugas-saya')"
                        aria-hidden="true"
                        class="absolute bottom-1 h-1 w-7 rounded-full bg-blue-600"
                    />
                </router-link>

                <router-link
                    to="/kurir/profil"
                    aria-label="Buka halaman Profil"
                    :aria-current="$route.path.includes('/kurir/profil') ? 'page' : undefined"
                    class="group relative flex h-full flex-1 flex-col items-center justify-center gap-1.5 text-slate-400 transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                    active-class="text-blue-600"
                >
                    <div
                        aria-hidden="true"
                        class="nav-icon"
                        :class="{
                            'nav-icon-active': $route.path.includes('/kurir/profil')
                        }"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-[21px] w-[21px]"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            stroke-width="1.8"
                            focusable="false"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                            />
                        </svg>
                    </div>

                    <span class="nav-label">Profil</span>

                    <span
                        v-if="$route.path.includes('/kurir/profil')"
                        aria-hidden="true"
                        class="absolute bottom-1 h-1 w-7 rounded-full bg-blue-600"
                    />
                </router-link>
            </div>
        </nav>
    </div>
</template>

<script setup>
</script>

<style scoped>
.nav-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 32px;
    border-radius: 12px;
    transition:
        background-color 0.2s ease,
        color 0.2s ease,
        transform 0.2s ease;
}

.nav-icon-active {
    background: #eff6ff;
    color: #2563eb;
}

.nav-label {
    font-size: 10px;
    font-weight: 600;
    line-height: 1;
    letter-spacing: -0.01em;
}

.router-link-active .nav-icon {
    transform: translateY(-1px);
}

.router-link:focus-visible {
    border-radius: 12px;
}

.pb-safe-area {
    padding-bottom: max(0px, env(safe-area-inset-bottom));
}

.kurir-page-enter-active,
.kurir-page-leave-active {
    transition:
        opacity 0.18s ease,
        transform 0.18s ease;
}

.kurir-page-enter-from {
    opacity: 0;
    transform: translateY(6px);
}

.kurir-page-leave-to {
    opacity: 0;
    transform: translateY(-4px);
}
</style>
