import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import one from "../components/one.vue"
import three from "../components/three.vue"
import logging from "../components/Logging.vue"
import two from "../components/two.vue"
import newlog from "../components/newlog.vue"
import logoff from "../components/logoff.vue"
import loginform from "../components/login.vue"
Vue.use(VueRouter)
const routes = [
  { path: '/one', component: one },
  { path: '/two/', component: two },
  { path: '/three', component: three },
  {path: '*',component:one},
  {path: '/logout',component:logoff},
  {path: '/logs/:tid',name:"logview",component:logging},
  {path: '/newlogs/:tid',name:"addlog",component:newlog},
  {path: '/newuser',component:loginform}
  ]

const router = new VueRouter({
  routes
})

export default router
