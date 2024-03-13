<template>
  <div class="home">
    <img src="../assets/logo.png" class="logo" @click="$router.push('/')" />
    <div class="status">
      <p>Last milk time: {{ lastMilkTime }}</p>
      <p>Can drink milk: {{ canDrinkMilk }}</p>
      <p>Can take pill: {{ canTakePill }}</p>
    </div>

    <div class="logs">
      <h2>Milk Logs</h2>
      <div v-for="log in milkLogs" :key="log">
        <template v-if="editingMilkLog === log">
          <input type="datetime-local" v-model="editingMilkLogTime" />
          <button @click="saveEditingMilkLog(editingMilkLogTime)">Save</button>
          <button @click="cancelEditingMilkLog">Cancel</button>
        </template>
        <template v-else>
          {{ formatDate(log) }}
          <button @click="deleteMilkLog(log)">Delete</button>
          <button @click="startEditingMilkLog(log)">Edit</button>
        </template>
      </div>
      <FlashMessage :message="milkFlashMessage" :type="flashType" />

      <h2>Add Milk Log</h2>
      <button @click="addingMilkLog = !addingMilkLog">Add Milk Log</button>
      <div v-if="addingMilkLog">
        <input type="datetime-local" v-model="newMilkLogTime" />
        <button @click="addMilkLog(newMilkLogTime)">Add</button>
        <button @click="addingMilkLog = false">Cancel</button>
      </div>



      <h2>Pill Logs</h2>
      <div v-for="log in pillLogs" :key="log">
        <template v-if="editingPillLog === log">
          <input type="datetime-local" v-model="editingPillLogTime" />
          <button @click="saveEditingPillLog(editingPillLogTime)">Save</button>
          <button @click="cancelEditingPillLog">Cancel</button>
        </template>
        <template v-else>
          {{ formatDate(log) }}
          <button @click="deletePillLog(log)">Delete</button>
          <button @click="startEditingPillLog(log)">Edit</button>
        </template>
      </div>
      <FlashMessage :message="pillFlashMessage" :type="flashType" />
      <h2>Add Pill Log</h2>
      <button @click="addingPillLog = !addingPillLog">Add Pill Log</button>
      <div v-if="addingPillLog">
        <input type="datetime-local" v-model="newPillLogTime" />
        <button @click="addPillLog(newPillLogTime)">Add</button>
        <button @click="addingPillLog = false">Cancel</button>
      </div>
    </div>

    <button class="logout-button" @click="logOut">Log Out</button>
  </div>
</template>

<script>
import moment from "moment";
import FlashMessage from "./FlashMessage.vue";

export default {
  name: "ProfileDash",
  components: {
    FlashMessage,
  },

  data() {
    return {
      username: "",
      lastMilkTime: "",
      canDrinkMilk: false,
      canTakePill: false,
      milkLogs: [],
      pillLogs: [],
      editingMilkLog: null,
      newMilkLogTime: null,
      editingMilkLogTime: null, 
      editingPillLog: null, 
      newPillLogTime: null, 
      editingPillLogTime: null, 
      milkFlashMessage: "",
      pillFlashMessage: "",
      addingMilkLog: false,
      addingPillLog: false,
      flashType: "info",
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
  },

  async created() {
    if (this.isLoggedIn) {
      try {
        let response = await this.$axios.get("/");
        this.username = response.data.username;
        this.checkStatus();
        this.getMilkLogs();
        this.getPillLogs();
      } catch (error) {
        console.error("Failed to get user:", error);
      }
    }
  },

  methods: {
    formatDate(date) {
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      const utcDate = new Date(date + "Z"); // Legger til 'Z' for å indikere at det er en UTC tid
      return utcDate.toLocaleString(undefined, options);
    },
    isFutureDate(date) {
      return moment(date).isAfter(moment());
    },

    async logOut() {
      if (this.$store.state.isLoggedIn) {
        try {
          await this.$axios.post("/logout");
          this.$store.dispatch("logout");
          this.$router.push("/login");
        } catch (error) {
          console.error("Failed to log out:", error);
        }
      } else {
        console.log("User is not logged in");
      }
    },
    async getMilkLogs() {
      let response = await this.$axios.get("/milk_logs");
      this.milkLogs = response.data.milk_logs;
    },

    async getPillLogs() {
      let response = await this.$axios.get("/pill_logs");
      this.pillLogs = response.data.pill_logs;
    },

    /*Må kanskje legge til en logikk som godtar å legge til melk i fortiden.
      Sånn det er nå kan jeg ikke legge til melk for en dag siden hvis jeg har tatt pillen,
      altså hvis candrinkmilk er false.
      Samme gjelder piller over
      */
    async addMilkLog(newTimestamp) {
      this.milkFlashMessage = "";
      this.pillFlashMessage = "";
      if (!this.canDrinkMilk) {
        this.milkFlashMessage =
          "Cannot add milk log since you have taken a pill";
        this.flashType = "error";
        return;
      }
      else if(this.isFutureDate(newTimestamp)){
        this.pillFlashMessage = "Cannot set a date in the future";
        this.flashType = "error";
        return;
      }
      let newTimestampUTC = moment(newTimestamp)
        .utc()
        .format("YYYY-MM-DDTHH:mm:ss");
        console.log(newTimestampUTC)
      await this.$axios.post("/milk_logs", { timestamp: newTimestampUTC });
      this.getMilkLogs();
      this.checkStatus();
      this.milkFlashMessage = "Milk log added successfully";
      this.flashType = "success";
      this.addingMilkLog = false;
    },

    async deleteMilkLog(log) {
      await this.$axios.delete("/milk_logs", { data: { timestamp: log } });
      this.getMilkLogs();
      this.checkStatus();
    },

    async addPillLog(newTimestamp) {
      this.milkFlashMessage = "";
      this.pillFlashMessage = "";
      if (!this.canTakePill) {
        this.pillFlashMessage = "Cannot add pill log less than 5 hours apart";
        this.flashType = "error";
        return;
      }
      else if(this.isFutureDate(newTimestamp)){
        this.pillFlashMessage = "Cannot set a date in the future";
        this.flashType = "error";
        return;
      }
      let newTimestampUTC = moment(newTimestamp)
        .utc()
        .format("YYYY-MM-DDTHH:mm:ss");
      await this.$axios.post("/pill_logs", { timestamp: newTimestampUTC });
      this.getPillLogs();
      this.checkStatus();
      this.pillFlashMessage = "Pill log added successfully";
      this.flashType = "success";
      this.addingPillLog = false;
    },

    async deletePillLog(log) {
      await this.$axios.delete("/pill_logs", { data: { timestamp: log } });
      this.getPillLogs();
    },

    async checkStatus() {
      try {
        let response = await this.$axios.get("/can_i");
        this.lastMilkTime = this.convertUtcToLocal(
          response.data.last_milk_time_utc
        );
        this.canDrinkMilk = response.data.can_drink_milk;
        this.canTakePill = response.data.can_take_pill;
      } catch (error) {
        console.error("Failed to check status:", error);
      }
    },
    convertUtcToLocal(utcTime) {
      return moment.utc(utcTime).local().format("YYYY-MM-DD HH:mm:ss");
    },

    startEditingMilkLog(log) {
      this.editingMilkLog = log;
      this.newMilkLogTime = log;
    },
    async saveEditingMilkLog(newTimestamp) {
      this.milkFlashMessage = "";
      this.pillFlashMessage = "";
      if (this.isFutureDate(newTimestamp)) {
        this.milkFlashMessage = "Cannot set a date in the future";
        this.flashType = "error";
        return;
      }
      let newTimestampUTC = moment(newTimestamp)
        .utc()
        .format("YYYY-MM-DDTHH:mm:ss");
      await this.$axios.put("/milk_logs", {
        old_timestamp: this.editingMilkLog,
        new_timestamp: newTimestampUTC,
      });
      this.getMilkLogs();
      this.checkStatus();
      this.editingMilkLog = null;
      this.newMilkLogTime = null;
    },
    cancelEditingMilkLog() {
      this.editingMilkLog = null;
      this.newMilkLogTime = null;
    },
    startEditingPillLog(log) {
      this.editingPillLog = log;
      this.newPillLogTime = log; // Set the new time to the current time of the log
    },
    async saveEditingPillLog(newTimestamp) {
      this.milkFlashMessage = "";
      this.pillFlashMessage = "";
      if (this.isFutureDate(newTimestamp)) {
        this.pillFlashMessage = "Cannot set a date in the future";
        this.flashType = "error";
        return;
      }
      let newTimestampUTC = moment(newTimestamp)
        .utc()
        .format("YYYY-MM-DDTHH:mm:ss");

      await this.$axios.put("/pill_logs", {
        old_timestamp: this.editingPillLog,
        new_timestamp: newTimestampUTC,
      });
      this.getPillLogs();
      this.checkStatus();
      this.editingPillLog = null;
      this.newPillLogTime = null; // Reset the new time
    },
    cancelEditingPillLog() {
      this.editingPillLog = null;
      this.newPillLogTime = null; // Reset the new time
    },
  },
};
</script>

<style>
.logo {
  width: 150px;
  cursor: pointer;
  margin-bottom: 20px;
}

.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  max-width: 500px;
  margin: 0 auto;
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

.action-button,
.logout-button {
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
}

.logout-button {
  background-color: #fff;
  border: 1px solid #ea5736;
  color: #ea5736;
  margin-top: 10px;
}

.logs {
  width: 100%;
  margin-bottom: 20px;
}

.logs h2 {
  text-align: center;
  color: #ea5736;
}

.logs div {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ea5736;
  border-radius: 5px;
  margin-bottom: 10px;
}

.logs button {
  background-color: #ea5736;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}
</style>
