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
      return this.content.map( x => {
        const out = Object.assign( {}, x );
        [ 'modified', 'created', 'deteled' ].forEach( y => {
          if ( x[y] ) x[y] = new Date( x[y] );
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
