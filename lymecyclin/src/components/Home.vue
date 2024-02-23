<template>
  <div class="home">
    <img src="../assets/logo.png" alt="Logo" class="logo" @click="$router.push('/')" />
    <div v-if="!isLoggedIn">
      <h2>Marius' melke- og medisintracker</h2>
      <p>Holde styr på når melk og medisinen lymecyclin tas.</p>
      <router-link to="/sign-up">
        <button class="action-button">Sign Up</button>
      </router-link>
      <router-link to="/login">
        <button class="action-button">Log In</button>
      </router-link>
    </div>
    <div v-if="isLoggedIn">
      <h1>Hello {{ username }}</h1>
      <div class="actions">
        <button class="action-button" @click="drinkMilk">Drink Milk</button>
        <button class="action-button" @click="takePill">Take Pill</button>
      </div>
      <div class="status">
        <p>When can I drink milk: {{ milkCountdown }}</p>
        <p>When can I take next pill: {{ pillCountdown }}</p>
      </div>
      <PillsCalendar :key="pillTakenCount"/>
      <button class="logout-button" @click="$router.push('/profileDash')">Profile</button>
      <button class="logout-button" @click="logOut">Log Out</button>
    </div>
  </div>
</template>



<script>
import PillsCalendar from "./PillsCalendar.vue";
import moment from "moment";

export default {
  name: "HomeView",

  components: {
    PillsCalendar,
  },

  data() {
    return {
      username: "",
      lastMilkTime: "",
      lastPillTime: "",
      canDrinkMilk: false,
      canTakePill: false,
      pillCountdown: "",
      milkCountdown: "",
      pillTakenCount: 0, // Forcing re-render of PillsCalendar

    };
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.isLoggedIn;
    },
    lastMilkTimeDisplay() {
      return this.lastMilkTime
        ? moment(this.lastMilkTime).local().format("YYYY-MM-DD HH:mm:ss")
        : "N/A";
    },
    lastPillTimeDisplay() {
      return this.lastPillTime
        ? moment(this.lastPillTime).local().format("YYYY-MM-DD HH:mm:ss")
        : "N/A";
    },
  },

  async created() {
    if (this.isLoggedIn) {
      try {
        let response = await this.$axios.get("/");
        this.username = response.data.username;
        this.checkStatus();
        this.startCountdowns();
      } catch (error) {
        console.error("Failed to get user:", error);
      }
    }
  },

  methods: {
    async logOut() {
      console.log(this.$store.state.isLoggedIn);

      // Check if the user is logged in
      if (this.$store.state.isLoggedIn) {
        try {
          // Log out the user on the server
          await this.$axios.post("/logout");

          // Log out the user on the client
          this.$store.dispatch("logout");
          this.$router.push("/login");
        } catch (error) {
          console.error("Failed to log out:", error);
        }
      } else {
        console.log("User is not logged in");
      }
    },

    async drinkMilk() {
      if (!this.canDrinkMilk) {
        alert("Cannot drink milk since you have taken a pill");
        return;
      } else {
        try {
          let response = await this.$axios.post("/drink_milk");
          alert(response.data.message);
          this.checkStatus();
        } catch (error) {
          alert(error.response.data.message);
        }
      }
    },

    async takePill() {
      if (!this.canTakePill) {
        alert("Cannot take pill less than 5 hours apart");
        return;
      }
      try {
        await this.$axios.post("/take_pill");
        this.checkStatus();
        this.pillTakenCount++;
      } catch (error) {
        console.error("Failed to log pill:", error);
      }
    },

    async checkStatus() {
      try {
        let response = await this.$axios.get("/can_i");
        // Antar at backend returnerer UTC tidspunkt som ISO string
        this.lastMilkTime = this.convertUtcToLocal(
          response.data.last_milk_time_utc
        );
        this.lastPillTime = this.convertUtcToLocal(
          response.data.last_pill_time_utc
        );
        this.canDrinkMilk = response.data.can_drink_milk;
        this.canTakePill = response.data.can_take_pill;

        // Oppdater nedtelling basert på nye tider fra server
        this.startCountdowns();
      } catch (error) {
        console.error("Failed to check status:", error);
      }
    },
    convertUtcToLocal(utcTime) {
      return moment.utc(utcTime).local().format("YYYY-MM-DD HH:mm:ss");
    },

    // Eksempel på konvertering fra lokal tid til UTC før sending til backend
    convertLocalToUtc(localTime) {
      return moment(localTime).utc().format();
    },

    startCountdowns() {
      setInterval(() => {
        const now = moment().unix(); // Get current time in UNIX timestamp
        const updateCountdown = (time) => {
          if (!time || !moment(time).isValid()) {
            return "Now";
          }
          const duration = moment.duration(
            moment(time).unix() - now,
            "seconds"
          );
          if (duration.asSeconds() <= 0) {
            return "Now";
          }
          return `${duration.hours()} hours, ${duration.minutes()} minutes, ${duration.seconds()} seconds`;
        };

        this.milkCountdown = this.lastPillTime
          ? updateCountdown(moment(this.lastPillTime).add(1, "hours"))
          : "Now";
        this.pillCountdown =
          this.lastPillTime && this.lastMilkTime
            ? updateCountdown(
                moment.max(
                  moment(this.lastPillTime).add(5, "hours"),
                  moment(this.lastMilkTime).add(1, "hours")
                )
              )
            : this.lastPillTime
            ? updateCountdown(moment(this.lastPillTime).add(5, "hours"))
            : "Now";
      }, 1000);
    },
  },
};
</script>

<style scoped>

:root {
  --primary-color: #4a90e2; /* Lys blå for primære handlinger */
  --secondary-color: #ea5736; /* Original farge bevart for kontrast */
  --text-color: #333; /* Mørkere tekst for bedre lesbarhet */
  --background-color: #f5f5f5; /* Lys bakgrunnsfarge */
  --font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

body {
  font-family: var(--font-family);
  background-color: var(--background-color);
  color: var(--text-color);
}

.logo {
  width: 120px; /* Større logo */
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05); /* Liten zoom-effekt ved hover */
}

.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 20px;
  max-width: 1200px; /* Sentrerer innholdet med maks bredde */
  margin: auto;
}

.action-button, .logout-button {
  width: 90%; /* Responsiv bredde */
  max-width: 300px; /* Maks bredde for å unngå for store knapper */
  height: 50px;
  margin: 10px 0;
  border-radius: 5px; /* Runde hjørner */
  transition: background-color 0.3s ease;
}

.action-button {
  background-color: var(--primary-color);
  border: 1px solid var(--primary-color);
  color: #fff;
}

.action-button:hover, .logout-button:hover {
  background-color: var(--secondary-color);
  color: #fff;
}

.logout-button {
  background-color: transparent;
  color: var(--secondary-color);
  border: 1px solid var(--secondary-color);
}

.actions, .status {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%; /* Full bredde for bedre layout-kontroll */
}

.status p {
  background-color: #fff; /* Legger til en bakgrunnsfarge for å skille teksten */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Subtil skygge for dybde */
  border-radius: 5px; /* Runde hjørner */
}
.logo {
  width: 150px;
  cursor: pointer;
  margin-bottom: 20px;
}



.home p {
  width: 100%;
  padding: 10px;
  border: 1px solid #ea5736;
  margin-bottom: 10px;
  background-color: #fff;
  border-radius: 5px;
  text-align: center;
}

.action-button, .logout-button {
  width: 100%;
  height: 40px;
  background-color: #ea5736;
  border: none;
  color: #fff;
  cursor: pointer;
  margin-bottom: 10px;
  border-radius: 5px;
  text-align: center;
  line-height: 40px;
  align-items: center;
}


.welcome-content, .user-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}



</style>
