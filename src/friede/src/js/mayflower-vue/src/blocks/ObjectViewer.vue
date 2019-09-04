<template lang="html">
  <div class="object-viewer">
    <filter-grid :objects=datedContent :item-layout=layout />
  </div>
</template>

<script lang="js">
import { FilterGrid } from '@/blocks'
export default {
  name: 'ObjectViewer',
  mixins: [],
  components: {},
  props: {
    content: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      layout: {
        title: 'title',
        subtitle: 'path',
        content: 'description'
      }
    };
  },
  created() {},
  mounted() {},
  methods: {},
  computed: {
    datedContent() {
      const out = {}
      Object.keys( this.content ).forEach( k => {
        const x = this.content[k];
        const o = out[k] = {};
        Object.keys(x).forEach( k => {
          const y = Object.assign( {}, x[k] );
          o[k] = y;
          [ 'modified', 'created', 'deteled' ].forEach( k => {
            if ( o[k] ) o[k] = new Date( o[k] );
          });
        });
      });
    }
  }
}
</script>

<style lang="scss">
.object-viewer {
  
}
</style>
