import Vue from 'vue'
import Vuex from 'vuex'
import { API } from '@/lib/api'

const Friede = window.Friede;

Vue.use( Vuex );

async function getModel( model, have ) {
  return API(
    'models', model, have ? '?' + have.map( x => 'have=' + x ).join('&') : '' )
     .then( r => r.data.models );
}

export default new Vuex.Store({
  state: {
    menus: Friede.menu,
    user: Friede.user,
    context: [],
    location: null,
    lastLocation: null,
    screen: null,
    models: {},
    modelsRequested: {},
    model: null,
    modelData: null,
    error: '',
    selected: [],
    caret: null,
  },
  mutations: {
    setUser( state, user ) {
      state.user = user;
    },
    setContext( state, context, querystring, debug ) {
      state.context = context;
      state.location = context.length && context[ context.length - 1 ].location;
      state.querystring = querystring;
      if ( state.location ) {
        state.lastLocation = state.location;
        document.title = state.location.title + ', apps @ sandbox0'
      }
    },
    setQuery( qs ) {
      this.querystring = qs;
    },
    setLocation( state, location ) {
      const ctx = state.context;
      state.location = ctx.length && ctx[ ctx.length - 1 ].location;
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
    },
    setMenus( state, menus ) {
      state.menus = menus;
    },
    setSelected( state, selected ) {
      state.selected = selected;
    },
    addToSelected( state, selected ) {
      state.selected = state.selected.concat( selected );
    },
    clearSelected( state ) {
      state.selected = []
    },
    setCaret( state, object ) {
      state.caret = object;
    },
    clearCaret( state ) {
      state.caret = null;
    }
  },
  actions: {
    refresh({ commit, state, dispatch }) {
      dispatch( 'getMenus' );
    },
    getMenus({ commit, state }) {
      API( 'menus' ).then( r => {
        commit( 'setMenus', r.data );
      }).catch( err => {
        console.warn( `error getting menus`, err, err.response );
        commit( 'setError', `Error getting menus<br/>/` + err + '<br/>'
                + err.response );
      })
    },
    async setContext({ commit, state, dispatch }, context ) {
      commit( 'setContext', context );
      if ( context && context.length && context[ context.length - 1 ].location ) {
        const location = await API( 'ls', context[ context.length - 1 ].location.id )
              .then( r => r.data.location )
              .catch( err => {
                console.warn( `error getting location`, err, err.response );
                commit( 'setError', `Error getting location<br/>/` + err + '<br/>'
                        + err.response );
              });
        if ( location ) {
          context[ context.length - 1 ].location = location;
          commit( 'setLocation', location );
        }
      }
      var model = await dispatch( 'getModel' );
      commit( 'setModel', model );
    },
    async setPath({ commit, state, dispatch }, path ) {
      API( 'path', path ).then( async r => {
        commit( 'setContext', r.data.route, path.replace(/.*?\?/, '?' ));
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
      if ( model && model.fullname )
        return model;
      if ( state.models[ model ]) {
        return state.models[ model ];
      }
      const have = Object.keys( state.models );
      var models = await getModel( model, have ).catch( err => {
        console.warn( `error getting model '${model}'`, err, err.response );
        commit( 'setError', `Error getting model '${model}'<br/>` + err + '<br/>'
                + ( err.response
                    ? ( err.response.data.msg ? err.response.data.msg
                        : err.response.data.message ? err.response.data.message
                        : err.response.data.error ? err.response.data.error
                        : err.response.data )
                    : '' ));
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
         && state.lastLocation.screens.default;
    },
    objects: state => {
      return state.context
         && state.context.length
         && state.context[ state.context.length - 1 ].objects;
    },
    filters: state => {
      return state.context
         && state.context.length
         && state.context[ state.context.length - 1 ].filters;
    }
  }
})
