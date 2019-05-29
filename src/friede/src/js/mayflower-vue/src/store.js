import Vue from 'vue'
import Vuex from 'vuex'

Vue.use( Vuex );

export default new Vuex.Store({
  state: {
    user: null,
    context: [{ href: '', title: '/' }],
    location: null,
    lastlocation: null,
  },
  mutations: {
    setUser( state, user ) {
      state.user = user;
    },
    setContext( state, context, debug ) {
      state.context = context;
      state.location = context.length && context[ context.length-1 ].location;
      if ( state.location ){
        state.lastlocation = state.location;
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
      return state.context.map( x => x.hash || x.href ).join('/');
    }
  }
})
