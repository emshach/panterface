import Vue from 'vue'
import { API } from './api'
import isArray from 'lodash/isArray'

const permissions = {};

export async function canI( op, arg ) {
  var ops;
  if ( arg ) {
    if ( isArray( arg )) {
      arg = arg.map( a => a.fullname || a );
      if (! isArray( op ))
        op = [ op ];
      ops = [];
      op.forEach( o => {
        arg.forEach( a => {
          ops.push( o + '.' + a );
        });
      })
    } else if ( arg.fullname ) {
      arg = arg.fullname;
      if ( isArray( op )) {
        ops = op.map( o => o + '.' + arg );
      } else {
        ops = op + '.' + arg;
      }
    }
  } else {
    ops = op;
  }
  
  if ( isArray( ops )) {
    const ask = [];
    const out = {};
    ops.forEach( o => {
      if ( o in permissions ) {
        if ( permissions[o] )
          out[o] = true;
      } else
        ask.push(o);
    });
    if ( ask.length ) {
      const res = await API( 'can', '?' + ask.map( o => 'op=' + o ).join('&') )
            .then( r => r.data ).catch( err => {
              console.warn( 'error getting permissions', op, arg, ops, err );
              return {};
            });
      Object.assign( permissions, res );
      return Object.assign( out, res );
    }
    return out
  } else {
    if ( ops in permissions && permissions[ ops ] !== null )
      return permissions[ ops ];
    const res = await API( 'can', ops ).then( r => r.data )
          .catch( err => {
            console.warn( 'error getting permission', op, arg, ops, err );
            return null;
          });
    permissions[ ops ] = res;
    return res;
  }
}
export const security = new Vue({
  data: {
    permit: 0
  },
  methods: {
    refresh() {
      const perms = Object.keys( permissions ).map( x => {
        delete permissions[x];
        return x;
      });
      canI( perms ).then(() => { this.permit++ });
      // TODO: catch
    }
  }
});

window.__DEBUG__permissions = permissions; // TODO: REMOVE SOON

export default {
  canI,
  install( Vue ) {
    Vue.$canI = canI;
    Vue.$security = security;
    Vue.prototype.$canI = canI;
    Vue.prototype.$security = security;
  }
}
