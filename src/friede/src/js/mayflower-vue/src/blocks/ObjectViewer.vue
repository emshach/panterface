<template lang="html">
  <div class="object-viewer">
    <filter-grid v-if="mode==='normal'" :objects=datedContent :item-layout=layout />
  </div>
</template>

<script lang="js">
import { FilterGrid } from '@/blocks'
export default {
  name: 'ObjectViewer',
  mixins: [],
  components: { FilterGrid },
  props: {
    content: {
      type: Array,
      default: () => []
    },
    mode: {
      type: String,
      default: 'normal'
    }
  },
  data() {
    return {
      layout: {
        title: { key: 'title', default: 'Untitled' },
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
      return this.content.map( x => {
        const out = Object.assign( {}, x );
        [ 'modified', 'created', 'deteled' ].forEach( y => {
          if ( x[y] ) out[y] = new Date( x[y] );
        });
        return out;
      });
    }
  }
}
</script>

<style lang="scss">
.object-viewer {
  
}
</style>
