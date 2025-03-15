import {createRouter, createWebHistory} from "vue-router";
import mainView from "@/pages/mainView.vue";



const routes = [
    {
        path: '/',
        component: mainView
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes

})

export default router