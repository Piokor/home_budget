import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

const store = new Vuex.Store({
  state () {
    return {
      currentUser: {
        token: localStorage.getItem('token'),
        username: localStorage.getItem('username')
      }      
    }
  },
  mutations: {
    setCurrentUser (state, user) {
      state.currentUser = user;
      localStorage.setItem('token', user.token)
      localStorage.setItem('username', user.username)
    },
    signOff(state) {
      state.currentUser = {
        token: null,
        username: null
      }    
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    }
  }
})

export default store;