// mayflower shell is vue-based
function whenDefined( dict, key, f ) {
  var id = null;
  id = setInterval( () => {
    if ( dict[ key ]) {
      clearInterval( id );
      f();
    }
  }, 500 );
}

whenDefined(
  window, 'MayflowerApp',
  () => { MayflowerApp.init(); }
);
