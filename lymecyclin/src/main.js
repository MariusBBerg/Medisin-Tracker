import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import router from './routers';
import store from './store';
import './main.css' //Kan bruke Tailwindcss

// Sett opp axios
axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.withCredentials = true;

const app = createApp(App);

// Gjør axios tilgjengelig i hele applikasjonen som $axios
app.config.globalProperties.$axios = axios;

// Bruk router og store
app.use(router).use(store);

app.mount('#app');
