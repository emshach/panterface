import Vue from 'vue'
import './plugins/fontawesome'
import App from './App.vue'
import router from './router'
import store from './store'
import UIkit from 'uikit'
import '@/assets/styles/styles.scss'
import Icons from 'uikit/dist/js/uikit-icons'
import axios from 'axios'

UIkit.use(Icons)
window.UIkit = UIkit

Vue.config.productionTip = false
Vue.prototype.$api = function() {
  return axios.get( '/api/' + Array.prototype.join.call( arguments, '/' ))
}

function Mayflower( args ) {
  this.options = {
    router,
    store,
    render: h => h(App)
  };
  if ( args ) {
    Object.assign( this.options, args );
  }
  this.mountpoint = '#app';
  this.vm = null;
  return this;
}
Mayflower.prototype.init = function () {
  if (! this.vm )
    this.vm = new Vue( this.options ).$mount( this.mountpoint );
};

window.Vue = Vue;
window.Mayflower = Mayflower;
window.MayflowerApp = new Mayflower();
