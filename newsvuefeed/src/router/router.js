import {createRouter, createWebHistory} from "vue-router";
import mainView from "@/pages/mainView.vue";
import detailedNews from "@/pages/detailedNews.vue";


const routes = [
    {
        path: '/',
        component: mainView
    },
    {
        path: '/Post/:id',
        component: detailedNews
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes

})

export default router