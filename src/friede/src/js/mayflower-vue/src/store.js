import Vue from 'vue'
import Vuex from 'vuex'

Vue.use( Vuex );

export default new Vuex.Store({
  state: {
    user: null,
    context: [],
    location: null,
    lastLocation: null,
    screen: null,
  },
  mutations: {
    setUser( state, user ) {
      state.user = user;
    },
    setContext( state, context, debug ) {
      state.context = context;
      state.location = context.length && context[ context.length-1 ].location;
      if ( state.location ){
        state.lastLocation = state.location;
      }
    },
  },
  actions: {
    setPath({ commit, state }, path ) {
      Vue.prototype.$api( 'path', path ).then( r => {
        commit( 'setContext', r.data.route );
      }).catch( x => {
        // TODO: handle
      });
    },
  },
  getters: {
    route: state => {
      if ( !state.context.length )
        return null;
      return state.context.map( x => x.hash || x.href ).join('/');
    },
    screen: state => {
      return state.lastLocation && state.lastLocation.screens
         && state.lastLocation.screens.default
         && state.lastLocation.screens.default.data
         && state.lastLocation.screens.default.data.model
    }
  }
})
