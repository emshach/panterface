<template lang="html">
<div :class=classes>
  <component :is=action.data.component mode="modal" :args=operands[action.name]
             :key=action.name
             v-for="( action ) in actions" />
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
import actors from '@/actors'
export default  {
  name: 'ModelDashboard',
  mixins: [ PageMixin ],
  components: { ...blocks, ...actors },
  props: [],
  mounted() {
    const actions = this.options.actions;
    if ( this.model )
      this.$store.dispatch( 'getModel', this.model ).then( m => {
        if ( m.rest ) {
          this.$api( m.rest, '' ).then( r => { // TODO: paginate, filter?
            this.objects = r.data.results || [];
          });
        }
      });
    if ( actions && actions.length ) {
      this.$api( 'friede', 'actions', '?' + this.options.actions.map(
        action => 'path=' + action ).join('&'))
         .then( r => {
           var res = r.data.results;
           if ( res.length )
             res.forEach( a => {
               this.actions[ a.name ] = a;
             });
         })
         .catch ( err => {
           console.warn( 'couldnt get actions', actions, err );
         });
    }
  },
  data() {
    return {
      classes: {
        'model-dashboard': true,
        'uk-flex-column': true,
      },
      featured: [],
      objects: [],
      actions: {},
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
