import Vue from 'vue'
import Vuex from 'vuex'

const Friede = window.Friede;

Vue.use( Vuex );

async function getModel( model, have ) {
  return Vue.prototype.$api(
    'models', model, have ? '?' + have.map( x => 'have=' + x ).join('&') : '' )
     .then( r => r.data.models );
}

export default new Vuex.Store({
  state: {
    user: Friede.user,
    context: [],
    location: null,
    lastLocation: null,
    screen: null,
    models: {},
    modelsRequested: {},
    model: null,
    modelData: null,
    error: ''
  },
  mutations: {
    setUser( state, user ) {
      state.user = user;
    },
    setContext( state, context, debug ) {
      state.context = context;
      state.location = context.length && context[ context.length - 1 ].location;
      if ( state.location ) {
        state.lastLocation = state.location;
      }
    },
    addModels( state, models ) {
      state.models = Object.assign( {}, state.models, models );
    },
    setModel( state, model ) {
      state.model = model;
    },
    setError( state, err ) {
      state.error = err;
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
      }).catch( err => {
        console.warn( `error getting '${path}'`, err, err.response );
        commit( 'setError', `Error getting '${path}'<br/>/` + err + '<br/>'
                + err.response );
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
      var models = await getModel( model, have ).catch( err => {
        console.warn( `error getting model '${model}'`, err, err.response );
        commit( 'setError', `Error getting model '${model}'<br/>` + err + '<br/>'
                + ( err.response && err.response.msg ? err.response.msg
                    : err.response && err.response.message ? err.response.message
                    : err.response && err.response.error ? err.response.error
                    : err.response ));
      });
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
    },
  }
})
