import Vue from 'vue'
import Vuex from 'vuex'
import createPersisterState from "vuex-persistedstate"
Vue.use(Vuex)

const store= new Vuex.Store({
  state: {
    currenttracker:{}
  },
  getters: {

  },
  mutations: {
    settracker(state,obj){
      state.currenttracker=obj
    }
  },
  actions: {
  },
  modules: {
  },
  plugins:[createPersisterState()]
})
export default store