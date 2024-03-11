import HomeView from './components/Home.vue';
import SignUp from './components/SignUp.vue';
import LogIn from './components/LogIn.vue';
import ProfileDash from './components/ProfileDash.vue';
import {createRouter, createWebHistory} from 'vue-router';
import store from './store.js';
console.log(store);


const routes=[
    {name:'Home',
    component:HomeView,
    path:'/'
    },

    {name:'SignUp',
    component:SignUp,
    path:'/sign-up',
    meta:{requiresGuest:true}
    },
    {name:'Login',
    component:LogIn,
    path:'/login',
    meta:{requiresGuest:true}
    },
    {name:'ProfileDash',
    component:ProfileDash,
    path:'/profileDash',
    meta:{requiresAuth:true},
  }

];

const router = createRouter({
    history:createWebHistory(),
    routes,

});

router.beforeEach((to, from, next) => {
    const isLoggedIn = store.state.isLoggedIn; 
  
    if (to.meta.requiresGuest && isLoggedIn) {
      next({ name: 'Home' });
    } else {
      next();
    }
    if(to.meta.requiresAuth && !isLoggedIn){
        next({name:'Login'});
    }
});


export default router;
