<template>


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
<button type="button " class="btn btn-primary" v-on:click="update_values()" >update
        </button>


</template>


<script>

// import { getValues } from '../api'

import axios from 'axios'



export default{
    name: 'SmartStation',
    props:['id'],
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
      url: '/dht22_data/get_last/',
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
      }

    }
    

     
}


</script>