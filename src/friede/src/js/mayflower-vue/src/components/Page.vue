<script lang="js">
import store from '@/store'
import pages from '@/views'
import { resolve } from '@/lib/util'
export default {
  name: 'Page',
  functional: true,
  render( h, ref ) {
    const screen = resolve( store.getters.screen );
    const model = screen.model || store.model;
    const blocks = screen.$blocks || {};
    const tag = pages[ screen.component ] || pages.HomePage;
    var options = {};
    if ( screen )
      Object.keys( screen ).forEach( x => {
        if ( x[0] != '$' && x !== 'model' )
          options[x] = screen[x];
      });
    Object.assign( ref.props,{ model, blocks, options });
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
