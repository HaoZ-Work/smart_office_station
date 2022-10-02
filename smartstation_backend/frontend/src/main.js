import { createApp } from 'vue'
import App from './App.vue'

import 'bootstrap/dist/css/bootstrap.min.css'
import "bootstrap"


import axios from 'axios'
// import Vue from 'vue'

// Vue.prototype.$axios = axios
axios.defaults.baseURL = '/api'

createApp(App).mount('#app')
