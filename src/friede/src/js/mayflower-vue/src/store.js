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
    setContext({ commit, state, dispatch }, context ) {
      commit( 'setContext', context );
      dispatch( 'getModel' );
    },
    setPath({ commit, state, dispatch }, path ) {
      Vue.prototype.$api( 'path', path ).then( r => {
        commit( 'setContext', r.data.route );
        dispatch( 'getModel' );
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
        if ( !state.model || state.model.fullname !== model )
          commit( 'setModel', state.models[ model ]);
        return state.models[ model ];
      }
      const have = Object.keys( state.models );
      var models = await getModel( model, have );
      commit( 'addModels', models );
      commit( 'setModel', models[ model ]);
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
