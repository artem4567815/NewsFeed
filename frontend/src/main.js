import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "@/router/router";
import components from '@/components/UI';
import mitt from 'mitt'
import axios from 'axios'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

axios.defaults.withCredentials = true

const emitter = mitt()


const app = createApp(App)

app.use(Toast, {
    transition: "Vue-Toastification__bounce",
    maxToasts: 3,
    newestOnTop: true,
    position: "top-right",
    timeout: 5000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: false,
    closeButton: "button",
    icon: true,
    rtl: false
})

components.forEach(component => {
    app.component(component.name, component)
})

app
    .use(router)
    .mount('#app')

export default emitter



