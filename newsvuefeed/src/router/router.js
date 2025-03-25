import {createRouter, createWebHistory} from "vue-router";
import mainView from "@/pages/mainView.vue";
import detailedNews from "@/pages/detailedNews.vue";
import profile from "@/pages/profile.vue";
import createPage from "@/pages/createPage.vue";
import createCover from "@/pages/createCover.vue";




const routes = [
    {
        path: '/',
        component: mainView
    },
    {
        path: '/Post/:id',
        component: detailedNews
    },
    {
        path: '/Profile',
        component: profile
    },
    {
        path: '/Profile/Create',
        component: createPage
    },
    {
        path: '/Profile/Create/Cover',
        component: createCover
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes

})

export default router