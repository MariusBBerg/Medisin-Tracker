<template>
    <div class="login">
        <img src="../assets/logo.png" class="logo" @click="$router.push('/')" />
        <h1>Log In</h1>
        <input type="text" v-model="username" placeholder="Username">
        <input type="password" v-model="password" placeholder="Password">

        <FlashMessage v-if="flashMessage" :message="flashMessage" :type="flashMessageType" />

        <button id="login-b1" @click="login">Log In</button>
        <button id="register-b2" @click="$router.push('/sign-up')">Sign Up</button>

    </div>
</template>

<script>

import FlashMessage from './FlashMessage.vue'

export default {
    name: 'LogIn',
    components: {
        FlashMessage,
    },
    data() {
        return {
            username: '',
            password: '',
            flashMessage: '',  // Updated from errorMessage
            flashMessageType: '',      
            showModal: false,  
        };
    },
    methods: {
        async login() {
            if (!this.username || !this.password) {
                this.flashMessage = "Username and password are required";
                this.flashMessageType = "error";
                return;
            }

            try {
                let result = await this.$axios.post('/login', {
                    username: this.username,
                    password: this.password,
                });

                if(result.status == 200){
                    console.log("User logged in successfully")
                    this.$store.commit('setLoggedIn', true)
                    this.$router.push('/')
                }
            } catch (error) {
                if (error.response && error.response.status == 401) {
                    this.flashMessage = "Invalid credentials";
                    this.flashMessageType = "error";
                }
            }
        },
    },
};

</script>

<style>
.logo{
    width: 100px;   
}
.login {
    display:flex;
    flex-direction: column;
    align-items: center;
}

.login input{
    width:300px;
    height:40px;
    padding-left:20px;
    display:block;
    margin-bottom: 30px;
    margin-right: auto;
    margin-left:auto;
    border: 1px solid #ea5736;
}

#login-b1{
    width: 320px;
    height: 40px;
    background-color: #ea5736;
    border: 1px solid #ea5736;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
}
#login-b1:hover {
    background-color: #ff7043; /* Lysere oransje farge på hover */
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2); /* Legger til en skyggeeffekt */
    transform: translateY(-2px); /* Løfter knappen litt opp */
}
#register-b2 {
    width: 320px;
    height: 40px;
    background-color: #fff;
    border: 1px solid #ea5736;
    color: #ea5736;
    cursor: pointer;
    margin-top: 10px;
    transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
}

#register-b2:hover {
    background-color: #f7b299; /* En lysere nyanse som komplementerer #ea5736 */
    color: #fff; /* Inverter tekstfarge til hvit for kontrast */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Legg til en subtil boks-skygge */
    transform: scale(1.05); /* Skalere knappen litt opp for å gi en følelse av interaktivitet */
}
</style>