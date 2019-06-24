import { API } from './api'
import isArray from 'lodash/isArray'

const permissions = {};

export async function canI( op, arg ) {
  if ( isArray( op )) {
    const ask = [];
    const out = [];
    op.forEach( o => {
      if ( o in permissions ) {
        if ( permissions[o] )
          out.push(o);
      } else
        ask.push(o);
    });
    if ( ask.length ) {
      const res = await API( 'can', '?' + ask.map( o => 'op=' + o ).join('&') )
            .then( r => r.data ).catch( err => {
              console.warn( 'error getting permissions', op, arg, err );
              return {};
            });
      Object.assign( permissions, res );
      return out.concat( Object.keys( res ).filter( k => res[k] ));
    }
    return out
  } else {
    if ( op in permissions && permissions[op] !== null )
      return permissions[ op ];
    const res = await API( 'can', op ).then( r => r.data )
          .catch( err => {
            console.warn( 'error getting permission', op, arg, err );
            return null;
          });
    permissions[ op ] = res;
    return res;
  }
}

window.__DEBUG__permissions = permissions; // TODO: REMOVE SOON

export default {
  canI,
  install( Vue ) {
    Vue.$canI = canI;
    Vue.prototype.$canI = canI;
  }
}
