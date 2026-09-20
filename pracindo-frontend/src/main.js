import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/index.css'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import { definePreset } from '@primevue/themes'
import 'primeicons/primeicons.css'
import ToastService from 'primevue/toastservice'
import Tooltip from 'primevue/tooltip'
import './assets/styles/tech-theme.css'
import '@/assets/tema.css'
import { assertBreakpointSync } from '@/utils/assertBreakpointSync'

const TealPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{teal.50}',
            100: '{teal.100}',
            200: '{teal.200}',
            300: '{teal.300}',
            400: '{teal.400}',
            500: '{teal.500}',
            600: '{teal.600}',
            700: '{teal.700}',
            800: '{teal.800}',
            900: '{teal.900}',
            950: '{teal.950}'
        }
    }
})

const app = createApp(App)

app.config.errorHandler = (err, instance, info) => {
    const nama = instance?.$options?.name || instance?.$options?.__name || 'komponen tidak dikenal'
    console.error(`[errorHandler] ${nama} (${info}):`, err)
}

app.use(createPinia())
app.use(router)
app.use(ToastService)

app.use(PrimeVue, {
    theme: {
        preset: TealPreset,
        options: {
            darkModeSelector: 'none',
            cssLayer: {
                name: 'primevue'
            }
        }
    }
})

app.directive('tooltip', Tooltip)

app.mount('#app')

assertBreakpointSync()