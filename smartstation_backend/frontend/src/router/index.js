
const Home = { template: '<div>Home</div>' }
const About = { template: '<div>User01</div>' }

const routes = [
  { path: '/', component: Home },
  { path: '/UserDemo', component: About },
]

const router = VueRouter.createRouter({
  mode:'hash',
  history: VueRouter.createWebHashHistory(),
  routes, 
})


const app = Vue.createApp({})

app.use(router)

app.mount('#app')
