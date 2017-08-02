import Vue from 'vue'
import App from './App.vue'
import VueProgressBar from 'vue-progressbar'
import 'spectre.css'

const options = {
  color: '#5764c6',
  failedColor: '#e85600'
}

Vue.use(VueProgressBar, options)

new Vue({
  el: '#app',
  render: h => h(App)
})
