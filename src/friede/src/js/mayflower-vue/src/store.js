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
        if ( x[0] === '-' ) {
          obj[x] = null;
        }
        return true;
      });
      var p = []
      for ( var k in obj ) {
        var top = k.split('+');
        var pre = top[0].split('-');
        var app = pre[1];
        var mod = pre[2];
        var ids = pre.slice(3).join(',')
        var filters = top.slice(1)
        var m = Friede.models[ app ][ mod ]
        obj[k] = {
          app: app,
          model: m.model,
          singular: m.singular,
          plural: m.plural,
          filters: [],
          objects: [],
          idstr: ids,
          filter: filters
        };
        if ( ids ) {
          p.push(
            Vue.prototype.$api( app, mod, '?ids='+ ids )
               .then( r => { obj[k].objects = r.data.results }));
        }
        if ( filters.length ) {
          obj[k].filters = filters.map( tag => ({
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
            return {
              href: '{' + o.app + '.' + o.model + '\\*?\\+?}',
              hash: x,
              filter: o.filter,
              filters: o.filters,
              objects: o.objects,
              title: ( o.filter ? ( o.plural + ': ' + o.filter
                            + ( ids ? ' + ' + ids.length : '' ))
                 : o.objects.length === 1
                 ? o.singular + ': ' + o.objects[0].title
                 : ( o.objects.length ? o.objects.length + ' ' + o.plural : o.plural )),
              slot: null,
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
