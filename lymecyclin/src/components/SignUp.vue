<template>
    <div class="container">
      <img src="../assets/logo.png" class="logo" @click="$router.push('/')" />
      <h1>Sign Up</h1>
        

      <!-- Burde kanskje legge til en validering av passord f.eks både her og i backend.
            Per nå kan passord og brukernavn være hva som helst. 
        
        -->
      <div class="register">
        <input type="text" v-model="username" placeholder="Enter username">
        <input type="password" v-model="password" placeholder="Enter password">
        <select v-model="timezone" class="timezone-select">
          <option disabled value="">Please select your timezone</option>
          <option value="UTC">UTC</option>
          <option value="Europe/Oslo">Europe/Oslo</option>
          <option value="America/New_York">America/New_York</option>
        </select>
  
        <FlashMessage v-if="flashMessage" :message="flashMessage" :type="flashMessageType" />
  
        <button id="register-b" @click="register">Sign Up</button>
        <button id="login-b" @click="$router.push('/login')">Log In</button>
      </div>
    </div>
  </template>
  
  <script>

    import FlashMessage from './FlashMessage.vue'

    export default {
    name: 'SignUp',
    components: {
    FlashMessage // Registrer FlashMessage komponenten for bruk
  },

    data() {
        return {
        username: '',
        password: '',
        timezone: 'UTC',
        flashMessage: '',  // Oppdatert fra errorMessage
        flashMessageType: '',        };
    },
    methods: {
        async register() {

        if (!this.username || !this.password || !this.timezone) {
            this.flashMessage = "All fields are required";
            this.flashMessageType = "error";
            return;
        }

        try {
            let result = await this.$axios.post('/register', {
            username: this.username,
            password: this.password,
            timezone: this.timezone,
            });

            console.warn(result)

            if(result.status == 201){
            this.flashMessage = "User registered successfully";
            this.flashMessageType = "success";
            this.$store.commit('setLoggedIn', true)
            this.$router.push('/')


            }
        } catch (error) {
            if (error.response && error.response.status == 409) {
                this.flashMessage = "User already exists";
                this.flashMessageType = "error";
            }
            else{
                this.flashMessage = "An error occurred. Please try again.";
                this.flashMessageType = "error";
            }
        }
        },
    },
    };
</script>
  
<style>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
  }
.logo {
    width: 100px;   
}
.register {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.register input, .timezone-select {
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-right: auto;
    margin-left: auto;
    border: 1px solid #ea5736;
}
#register-b, #login-b {
    width: 320px;
    height: 40px;
    background-color: #fff;
    border: 1px solid #ea5736;
    color: #ea5736;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
}
#register-b:hover, #login-b:hover {
    background-color: #f7b299; /* En lysere nyanse som komplementerer #ea5736 */
    color: #fff; /* Inverter tekstfarge til hvit for kontrast */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Legg til en subtil boks-skygge */
    transform: scale(1.05); /* Skalere knappen litt opp */
}
#login-b {
    background-color: #ea5736;
    color: #fff;
    margin-top: 10px; /* Sikrer litt avstand mellom registrerings- og innloggingsknappene */
}
#login-b:hover {
    background-color: #ff7043; /* Lysere oransje farge på hover */
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2); /* Legger til en skyggeeffekt */
    transform: translateY(-2px); /* Løfter knappen litt opp */
}
.timezone-select {
    width: 300px;
    height: 40px;
    padding-left: 20px;
    display: block;
    margin-bottom: 30px;
    margin-right: auto;
    margin-left: auto;
    border: 1px solid #ea5736;
  }
</style>
