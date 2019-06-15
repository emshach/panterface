export function chunk( data, size ) {
  var out=[], i, j, tmp, chunk = 10;
  for ( i = 0, j = data.length; i<j; i+=size ) {
    out.push( data.slice( i, i+chunk ))
  }
  return out
}

export function resolve( obj ) {
  var objects = [];
  while ( obj ) {
    var o = Object.assign( {}, obj.data );
    Object.keys( obj ).forEach( k => {
      if ( k.match( /_entries/ )) {
        var k0 = k['$' + k.substr(1, k.length - 9 ) + 's' ];
        o[ k0 ] = {};
        Object.keys( o[k] ).forEach( k1 => {
          o[ k0 ][ k1 ] = resolve( obj[k][ k1 ])
        });
      }
    });
    objects.unshift( o );
    obj = obj.extends;
  }
  return Object.assign.apply( {}, objects );
}
