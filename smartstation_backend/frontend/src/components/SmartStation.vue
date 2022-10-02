<template>

<!-- <P>Data for {{this.user}}</P> -->
<table class="table">
  <thead>
    <tr>
      <th scope="col">Data</th>
      <th scope="col">Value</th>
      <!-- <th scope="col">Last</th>
      <th scope="col">Handle</th> -->
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Temperature</th>
      <td>{{this.temp}}</td>
 
    </tr>
    <tr>
      <th scope="row">Humidity</th>
      <td>{{this.humi}}</td>

    </tr>
    
  </tbody>
</table>
<!-- <button type="button " class="btn btn-primary" v-on:click="update_values()" >update
        </button> -->


</template>


<script>




import axios from 'axios'




export default{
    name: 'SmartStation',
    props:{
      user:String
    },
    data(){
      return {
        temp:0,
        humi:0,
        
      }
    },

    // computed: {
    //   get_value() {
    //     var temp = 1
    //     var humi= 2
        
    //     return {"temp":temp,"humi":humi}
    //   },

      
    // },
    methods :{
      // sent_request () {
      sent_request : function() {
      var config = {
      method: 'get',
      url: 'http://127.0.0.1/api/dht22/user01/',
      headers: {}};
  
      axios(config)
        .then(function (response) {
            // console.log(response.data);
        
            this.temp=response.data['temperature']
            this.humi=response.data['humidity']
           
            
        }.bind(this))
        .catch(function (error) {
          console.log(error);
        });
        
        
          },
      update_values : function(){
        // var re = null
        this.sent_request()
        // console.log(this.temp)
        // console.log()
     
      },
      sleep :  function(ms){
          return new Promise(resolve => setTimeout(resolve, ms));

      },
      auto_update: async function() {
        var T = true
        while (T){
          await this.sleep(3000)
          this.sent_request()
        }
     

      }

    },
    mounted(){
    
      this.update_values()
      this.auto_update()
    }
    

     
}


</script>