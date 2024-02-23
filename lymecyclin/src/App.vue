<template>
  <router-view/>
</template>

<script>
//import axios from 'axios';

export default {
  name: 'App',
  created() {
    this.checkAuthStatus();
  },
  methods: {
    async checkAuthStatus() {
      try {
        const response = await this.$axios.get('/api/auth/check');
        if (response.data.authenticated) {
          this.$store.dispatch('logIn', true);
        } else {
          this.$store.dispatch('logout');
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        this.$store.dispatch('logout');
      }
    }
  }

 
}
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
