import Vue from 'vue'
import Vuex from 'vuex'

Vue.use( Vuex );

async function getModel( model, have ) {
  return Vue.prototype.$api(
    'models', model,
    have ? '?'+ have.map( x => 'have='+x ).join('&') : '' ).then( r => {
    return r.data.models;
  })
}

export default new Vuex.Store({
  state: {
    user: null,
    context: [],
    location: null,
    lastLocation: null,
    screen: null,
    models: {},
    modelsRequested: {},
    model: null,
    modelData: null,
  },
  mutations: {
    setUser( state, user ) {
      state.user = user;
    },
    setContext( state, context, debug ) {
      state.context = context;
      state.location = context.length && context[ context.length-1 ].location;
      if ( state.location ) {
        state.lastLocation = state.location;
      }
    },
    addModels( state, models ) {
      state.models = Object.assign( {}, state.models, models );
    },
    setModel( state, model ) {
      state.model = model;
    }
  },
  actions: {
    async setContext({ commit, state, dispatch }, context ) {
      commit( 'setContext', context );
      var model = await dispatch( 'getModel' );
      commit( 'setModel', model );
    },
    async setPath({ commit, state, dispatch }, path ) {
      Vue.prototype.$api( 'path', path ).then( async r => {
        commit( 'setContext', r.data.route );
        var model = await dispatch( 'getModel' );
        commit( 'setModel', model );
      }).catch( x => {
        // TODO: handle
      });
    },
    async getModel({ commit, state }, model ) {
      if ( !model ) {
        model = state.lastLocation && state.lastLocation.data.model;
        if ( !model ) 
          return null;
      }
      if ( model in state.models ) {
        return state.models[ model ];
      }
      const have = Object.keys( state.models );
      var models = await getModel( model, have );
      commit( 'addModels', models );
      return models[ model ];
    }
  },
  getters: {
    route: state => {
      if ( !state.context.length )
        return null;
      return state.context.map( x => x.hash || x.href ).join('/');
    },
    screen: state => {
      return state.lastLocation
         && state.lastLocation.screens
         && state.lastLocation.screens.default
         && state.lastLocation.screens.default.data.component
    },
  }
})
