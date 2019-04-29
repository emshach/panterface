function chunk( data, size ) {
  var out=[], i, j, tmp, chunk = 10;
  for ( i = 0, j = data.length; i<j; i+=size ) {
    out.push( data.slice( i, i+chunk ))
  }
  return out
}

export { chunk }
