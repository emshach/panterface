export function chunk( data, size ) {
  var out = [], i, j, chunk = 10;
  for ( i = 0, j = data.length; i < j; i += size ) {
    out.push( data.slice( i, i + chunk ))
  }
  return out
}

export function resolve( obj, defaults ) {
  var objects = [ defaults || {}, {} ];
  while ( obj ) {
    var o = Object.assign( {}, obj.entry ? obj.entry.data : null, obj.data );
    obj = obj.entry || obj;
    Object.keys( obj ).forEach( k => {
      if ( k.match( /_entries/ )) {
        var k0 = '$' + k.substr(1, k.length - 9 ) + 's';
        o[ k0 ] = {};
        Object.keys( obj[k] ).forEach( k1 => {
          o[ k0 ][ obj[k][ k1 ].name ] = resolve( obj[k][ k1 ] );
        });
      }
    });
    objects.unshift( o );
    obj = obj.extends;
  }
  objects.unshift({});
  return Object.assign.apply( null, objects );
}

window.resolve = resolve;
