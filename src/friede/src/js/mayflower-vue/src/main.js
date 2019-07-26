import Vue from 'vue'
import './plugins/fontawesome'
import App from './App'
import router from './router'
import store from './store'
import UIkit from 'uikit'
import 'uikit/dist/css/uikit.min.css'
import '@/assets/styles/styles.scss'
import Icons from 'uikit/dist/js/uikit-icons'
import API from '@/lib/api'
import security from '@/lib/security'
import Tooltip from 'vuikit/lib/tooltip'
import 'vue-toastr/src/vue-toastr.scss'

UIkit.use( Icons );
Vue.directive( 'vk-tooltip', Tooltip );
Vue.use( API );
Vue.use( security );
Vue.config.productionTip = false;

class Mayflower{
  constructor ( args ) {
    this.options = {
      router,
      store,
      render: h => h( App )
    };
    if ( args ) {
      Object.assign( this.options, args );
    }
    this.mountpoint = '#app';
    this.vm = null;
    return this;
  }
  init() {
    if ( !this.vm )
      this.vm = new Vue( this.options ).$mount( this.mountpoint );
  }
  findComponent( tag ) {
    if ( !this.vm ) return null;
    const stack = this.vm.$children.slice();
    const out = [];
    while ( stack.length ) {
      const comp = stack.shift();
      if ( comp.$options.name === tag )
        out.push( comp );
      stack.unshift.apply( stack, comp.$children );
    }
    return out;
  }
}
window.Vue = Vue;
window.UIkit = UIkit;
window.Mayflower = Mayflower;
window.MayflowerApp = new Mayflower();
