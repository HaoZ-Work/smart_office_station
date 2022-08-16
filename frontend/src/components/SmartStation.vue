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
      <td>{{get_value["humi"]}}</td>

    </tr>
    
  </tbody>
</table>

</template>


<script>

// import { getValues } from '../api'

export default{
    name: 'SmartStation',
    props:['id'],
    data(){
      return {
        temp:1,
        humi:0
      }
    },
    computed: {
      get_value() {
        var temp = 1
        var humi= 2
        
        return {"temp":temp,"humi":humi}
      },

      
    },
    // test_func() 
    // {
    //   return getValues()
      
    // }

    
}

// export default Vue.component('SmartStation',
// {
//   name: 'SmartStation',
//     props:['id']
// }


// )
</script>