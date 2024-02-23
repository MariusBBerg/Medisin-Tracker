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
    // Replace `isLoggedIn` with your own logic to check if the user is logged in
    const isLoggedIn = store.state.isLoggedIn; // assuming you're using Vuex for state management
  
    if (to.meta.requiresGuest && isLoggedIn) {
      // If the user is logged in and the route requires a guest (not logged in), redirect to home page
      next({ name: 'Home' });
    } else {
      next();
    }
    if(to.meta.requiresAuth && !isLoggedIn){
        next({name:'Login'});
    }
});


export default router;