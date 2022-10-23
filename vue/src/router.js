import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('./views/Home.vue')
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('./views/LoginPage.vue')
    },
    {
        path: '*',
        redirect: '/'
    }
];

const router = new VueRouter({
    mode: 'history',
    routes 
});

router.beforeEach((to, from, next) => {   
    return next();
});

export default router;