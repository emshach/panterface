<template lang="html">
  <component :is=component v-bind=$attrs :model=model :blocks=blocks
             :options=options />
</template>

<script lang="js">
import pages from '@/views'
import { resolve } from '@/lib/util'
export default {
  inheritAttrs: false,
  name: 'Page',
  components: {
    VuePerfectScrollbar,
    ...pages
  },
  props: [],
  mounted() {
  },
  data() {
    return {
    }
  },
  methods: {
  },
  computed: {
    screen() {
      return resolve( this.$store.getters.screen )
    },
    component() {
      return this.screen.component || 'HomePage'
    },
    model() {
      return this.screen.model || this.$store.model
    },
    blocks() {
      return this.screen.$blocks || {}
    },
    options() {
      const s = this.screen
      var o = {}
      if ( !s ) return {};
      Object.keys( s ).forEach( x => {
        if ( x[0] != '$' && x !== 'model' )
          o[x] = s[x];
      });
      return o;
    }
  }
}
</script>

<style scoped lang="scss">
.page {
  position: absolute;
  top: 0;
  bottom: 34px;
  left: 0;
  right: 0;
  padding: 40px 20px 10px;
}
</style>
