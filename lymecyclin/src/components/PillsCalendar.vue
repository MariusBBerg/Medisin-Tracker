<template>
    <div class="calendar">
      <div class="header">
        <button @click="prevMonth">«</button>
        <h2>{{ currentMonthName }} {{ currentYear }}</h2>
        <button @click="nextMonth">»</button>
      </div>
      <div class="weekdays">
        <div v-for="day in weekdays" :key="day">{{ day }}</div>
      </div>
      <div class="days">
        <div
          v-for="day in daysInMonth"
          :key="day.date"
          :class="{'marked': day.isMarked, 'not-current-month': !day.isCurrentMonth, 'today': day.isToday}"
          >
          {{ day.number }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PillsCalendar',
    data() {
      return {
        currentMonth: new Date().getMonth(),
        currentYear: new Date().getFullYear(),
        weekdays: ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'],
        markedDays: [], // Datoer for merkede dager
      };
    },
    computed: {
      currentMonthName() {
        return new Date(this.currentYear, this.currentMonth).toLocaleString('default', { month: 'long' });
      },
      daysInMonth() {
        const days = [];
        // Få første dag i måneden
        const firstDay = new Date(this.currentYear, this.currentMonth, 1);
        // Få siste dag i måneden
        const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0);
        // Fyll ut dagene før første dag i måneden
        for (let i = firstDay.getDay(); i > 1; i--) {
          days.push({ number: '', isCurrentMonth: false });
        }

        const today =  new Date();
        const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
        // Legg til alle dagene i måneden
        for (let day = 1; day <= lastDay.getDate(); day++) {
          const dateStr = `${this.currentYear}-${String(this.currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
          days.push({
            number: day,
            date: dateStr,
            isCurrentMonth: true,
            isMarked: this.markedDays.includes(dateStr),
            isToday: dateStr === todayStr,
          });
        }
        return days;
      }
    },
    methods: {
      prevMonth() {
        if (this.currentMonth === 0) {
          this.currentMonth = 11;
          this.currentYear--;
        } else {
          this.currentMonth--;
        }
      },
      nextMonth() {
        if (this.currentMonth === 11) {
          this.currentMonth = 0;
          this.currentYear++;
        } else {
          this.currentMonth++;
        }
      },
      async getTwoPillsDays(){
            try {
                let response = await this.$axios.get('/two_pills_days');
                this.markedDays = response.data.two_pills_days;
                console.log(this.twoPillsDays)
            } catch (error) {
                console.error('Failed to get two pills days:', error);
            }
        } 
    },
    created() {
      this.getTwoPillsDays();
    }
  };
  </script>
  
  <style>
.calendar {
  max-width: 400px;
  margin: 2rem auto;
  background-color: #4a90e2; /* Juster etter din stilguide */
  color: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #3278b3; /* Mørkere blå for header */
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.today {
    color: #04d1a1 !important; /* Endrer tekstfargen til rød */
  }
.header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.header button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.5rem;
}

.weekdays {
  background-color: #3278b3; /* Mørkere blå for weekdays */
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  padding: 0.5rem 0;
}

.weekdays div {
  padding: 0.5rem 0;
}

.days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
}

.days div {
  padding: 1rem 0;
  border-bottom: 1px solid #3278b3; /* Border farge */
  border-right: 1px solid #3278b3; /* Border farge */
}

.days div:nth-child(7n) {
  border-right: none;
}

.marked {
  background-color: #ff6868; /* Markert farge */
  color: white;
}

.not-current-month {
  color: #ccc;
}

@media (min-width: 600px) {
  .calendar {
    max-width: 600px;
  }
}
</style>

  