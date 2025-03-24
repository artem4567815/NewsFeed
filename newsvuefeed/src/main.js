import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "@/router/router";
import components from '@/components/UI';
import mitt from 'mitt'

const emitter = mitt()


const app = createApp(App)

components.forEach(component => {
    app.component(component.name, component)
})

app
    .use(router)
    .mount('#app')

export default emitter



