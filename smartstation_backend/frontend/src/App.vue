<template>
<!-- <div id="app"> -->
<!-- 
 <p>welcome:: {{this.user}}</p> -->

  <PtwMainpage :user=this.user>MainPage</PtwMainpage>
<!-- </div> -->

  
</template>

<script>

import PtwMainpage from './components/PtwMainpage.vue'

export default {
  name: 'App',
  // props:{user:Object},
  data() 
    {
      return {
        user: ""
      }
      },

  components: {
    PtwMainpage
  },
  mounted() {
    this.user= window.user
    // console.log(this.user)
  }
}



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
