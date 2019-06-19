<template lang="html"></template>

<script lang="js">
import pages from '@/views'
import { resolve } from '@/lib/util'
export default {
  name: 'Page',
  functional: true,
  render( h, ref ) {
    const screen = resolve( this.$store.getters.screen );
    const model = this.screen.model || this.$store.model;
    const blocks = this.screen.$blocks || {};
    const tag = pages[ this.screen.component ] || pages.HomePage;
    console.log( 'page tag', tag );
    var options = {};
    if ( screen )
      Object.keys( screen ).forEach( x => {
        if ( x[0] != '$' && x !== 'model' )
          options[x] = screen[x];
      });
    ref.props.options = {};
    return h( tag, ref );
  }
}
</script>

<style lang="scss">
.page {
  position: absolute;
  top: 0;
  bottom: 34px;
  left: 0;
  right: 0;
  padding: 40px 20px 10px;
}
</style>
