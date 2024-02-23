import { createStore } from 'vuex';
import VuexPersist from 'vuex-persist';


// Opprett en instans av VuexPersist
const vuexLocal  = new VuexPersist({
  key: 'erLoggetInn', // Nøkkelen som brukes for å lagre data i localStorage
  storage: window.localStorage, // Angir at localStorage skal brukes for lagring
  // Du kan også velge å kun persistere bestemte deler av tilstanden ved å bruke `reducer`-egenskapen
});



export default createStore({
  plugins: [vuexLocal.plugin], // Bruk vuexLocal.plugin her
  state: {
    isLoggedIn: false,
    // other state...
  },
  mutations: {
    setLoggedIn(state, value) {
      state.isLoggedIn = value;
    },
    logOut(state){
      state.isLoggedIn = false;
    }
  },
  actions: {
    logIn({ commit }, value) {
      commit('setLoggedIn', value);
    },
    logout({ commit }){
      commit('logOut')
    }
    // other actions...
  },
  getters: {
    isLoggedIn: state => state.isLoggedIn,
    isLoggedOut: state => !state.isLoggedIn,
    // other getters...
  },
});