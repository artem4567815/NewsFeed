import {createRouter, createWebHistory} from "vue-router";
import mainView from "@/pages/mainView.vue";
import detailedNews from "@/pages/detailedNews.vue";
import profile from "@/pages/profile.vue";
import createPage from "@/pages/createPage.vue";
import createCover from "@/pages/createCover.vue";
import formAuth from "@/pages/formAuth.vue";
import formReg from "@/pages/formReg.vue";
import formRegAdmin from "@/pages/formRegAdmin.vue";





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
        path: '/Create',
        component: createPage
    },
    {
        path: '/Create/Cover',
        component: createCover
    },
    {
        path: '/auth',
        component: formAuth
    },
    {
        path: '/registration',
        component: formReg
    },
    {
        path: '/registration/admin',
        component: formRegAdmin
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes

})

let previousRoute = null;

router.beforeEach((to, from, next) => {
    previousRoute = from;
    next();
});

// потом экспортировать или сохранять в глобальное хранилище

export default router
export { previousRoute };
