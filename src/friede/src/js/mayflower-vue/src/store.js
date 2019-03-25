import Vue from 'vue'
import Vuex from 'vuex'

Vue.use( Vuex )

export default new Vuex.Store({
  state: {
    location: [{ href: '/', title: '/' }]
  },
  mutations: {
    goto( state, location ) {
      if ( typeof location == 'string') {
        location = location.split('/');
      }
      location = location.map( x => (
        (typeof x == 'string' ) ? { href: x, title: x } : x
      ));
      if ( !location.length || location[0].href != '/' ) {
        location.unshift({ href: '/', title: '/' });
      }
      state.location = location;
    }
  },
  actions: {

  }
})
