<template>
<div id="app">


  <PtwMainpage>MainPage</PtwMainpage>
</div>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  
</template>

<script>
// import * as Vue from 'vue'

// import HelloWorld from './components/HelloWorld.vue'
import PtwMainpage from './components/PtwMainpage.vue'

export default {
  name: 'App',
  components: {
    // HelloWorld,
    PtwMainpage
  }
}

// export default Vue.component('app', {
//     components: {
//     // HelloWorld,
//     PtwMainpage
//   }
// }
// )

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
