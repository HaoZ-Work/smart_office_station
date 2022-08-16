<template>

  <!-- <header> <meta http-equiv= refresh content=10></header> -->
  <hr size=20 color=#b90f22> <hr size=4 color=#000000>


  <CENTER> <img src='https://www.ptw.tu-darmstadt.de/media/fachgebietptw/grafikenundfotos/logos_2/PTW-Logo.png' width=140 height=92> </center>

  <center><h1>Smart Office Station</h1></center>
  <hr size=4 color=#000000>

  <center>
    <div class="row">
      <div class="col">
        <!-- <button type="button " class="btn btn-primary" >Station 01
        </button> -->
        <center><h3>Smart Station 01</h3>
        <SmartStation ></SmartStation>
        </center>
      </div>
      <!-- <div class="col">Station 02</div>
      <div class="col">Station 03</div> -->
    </div>
    
  </center>



</template>

<script>
// import * as Vue from 'vue'

import SmartStation from './SmartStation.vue'



export default {
    name: "PtwMainpage",
    components: { SmartStation }
}

// export default Vue.component("PtwMainpage",{
//       components: { SmartStation }

// }

// )

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style >

</style>
