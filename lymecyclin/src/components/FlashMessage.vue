<template>
    <transition name="fade">
      <div v-if="message" :class="`flash-message ${type}`">{{ message }}</div>
    </transition>
  </template>
  
  <script>
  export default {
    name: 'FlashMessage',
    props: {
      message: String,
      type: {
        type: String,
        default: 'info' // Kan være 'success', 'error', 'info'
      }
    }
  }
  </script>
  
  <style scoped>
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    opacity: 0;
  }
  
  .flash-message {
    padding: 10px !important;
    margin-bottom: 10px !important;
    border-radius: 5px !important;
    text-align: center !important;
    color: #fff !important
  }
  .success {
    background-color: #4CAF50 !important;
  }
  .error {
    background-color: #F44336 !important;
  }
  .info {
    background-color: #2196F3 !important;
  }
  </style>
  