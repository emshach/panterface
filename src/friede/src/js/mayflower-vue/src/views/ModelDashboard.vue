<template lang="html">
<div :class=classes>
  <component :is=blocks.breakfront.component v-if=blocks.breakfront
             :content=featured />
  <component :is=blocks.main.component v-if=blocks.main
             :objects=objects
             :actions=options.actions
             :item-layout=options.layout
             :search-fields=options.search />
</div>
</template>

<script lang="js">
import { PageMixin } from '@/lib/mixins'
import blocks from '@/blocks'
export default  {
  name: 'ModelDashboard',
  mixins: [ PageMixin ],
  components: blocks,
  props: [],
  mounted() {
    if ( this.model )
      this.$store.dispatch( 'getModel', this.model ).then( m => {
        if ( m.rest ) {
          this.$api( m.rest, '' ).then( r => { // TODO: paginate, filter?
            this.objects = r.data.results || [];
          });
        }
      });
  },
  data() {
    return {
      classes: {
        'model-dashboard': true,
        'uk-flex-column': true,
      },
      featured: [],
      objects: []
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
.model-dashboard {
  
}
</style>
