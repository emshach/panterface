import Vue from 'vue'
import Vuex from 'vuex'

Vue.use( Vuex )

export default new Vuex.Store({
  state: {
    user: null,
    context: [{ href: '', title: '/' }]
  },
  mutations: {
    setUser( state, user ) {
      state.user = user;
    },
    setContext( state, context ) {
      state.context = context;
    },
  },
  actions: {
    setPath({ commit, state }, path ) {
      console.log( 'path', path );
      // Vue.prototype.$api.get( 'path', path ).done( r => {
      //   commit( 'setContext', r.data.context );
      // });
      const ctx = ( path || '' ).split('/');
      commit( 'setContext', ctx.map( x =>({ title: x || '/', href: x })))
    },
  },
  getters: {
    getRoute: state => {
      return state.context.map( x => x.hash || x.href ).join('/');
    }
  }
})
