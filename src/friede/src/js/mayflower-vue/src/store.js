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
    setContext( state, context, debug ) {
      state.context = context;
    },
  },
  actions: {
    setPath({ commit, state }, path ) {
      var obj = {}
      const ctx = ( path || '' ).split('/').filter( x => {
        if ( !x )
          return false;
        if ( x.indexOf('.') > -1 ) {
          obj[x] = null;
        }
        return true;
      });
      var p = []
      for ( var k in obj ) {
        var d = k.split(':');
        var m = d[0].split('.');
        obj[k] = {
          app: m[0],
          plural: m[1],
          filters: [],
          objects: [],
          idstr: d[1],
          filter: d[2]
        };
        if ( d[1] ) {
          p.push(
            Vue.prototype.$api( m[0], m[1], '?ids='+ d[1].replace( /\+/g, ',' ))
               .then( r => { obj[k].objects = r.data.results }));
        }
        if ( d[2] ) {
          obj[k].filters = d[2].split('+').map( tag => ({
            path: `_filter.${tag}`,
            title: `filter: ${tag}`,
            filter: true,
            tag: tag
          }));
        }
      }
      Promise.all(p).then(() => {
        console.log( 'obj', obj );
        commit( 'setContext', [{ href: '', title: '/' }].concat( ctx.map( x => {
          if ( x in obj ) {
            var o = obj[x];
            var ids = o.objects.map( x => x.id );
            var singular = o.plural; // FIXME: this
            return {
              href: '{' + o.app + '.' + o.plural + '\\*?\\+?}',
              hash: x,
              filter: o.filter,
              filters: o.filters,
              objects: o.objects,
              title: ( o.filter ? ( o.plural + ': ' + o.filter
                            + ( ids ? ' + ' + ids.length : '' ))
                 : o.objects.length === 1
                 ? singular + ': ' + o.objects[0].title
                 : ( o.objects.length ? o.objects.length + ' ' + o.plural : o.plural )),
              slot: 'TBD',
            }
          }
          return { title: x || '/', href: x };
        })), { objects: obj, ctx: ctx });
      })
    },
  },
  getters: {
    route: state => {
      return state.context.map( x => x.hash || x.href ).join('/');
    }
  }
})
