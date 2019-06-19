<template lang="html">
<div :class=classes>
  <component :is=tag mode="modal" :key=tag
             v-for="( actor, tag ) in actors"
             :actions=actor.actions
             :operands=actor.operands
             :show.sync=actor.show />
  <component :is=blocks.breakfront.component v-if=blocks.breakfront
             :content=featured />
  <component :is=blocks.main.component v-if=blocks.main
             :objects=objects
             :actions=options.actions
             :item-layout=options.layout
             :search-fields=options.search>
    <template #item-actions={object} >
      <component :is=tag mode="widget" :key=tag
                 v-for="( actor, tag ) in actors"
                 :object=object
                 @act="act( $event, actor, object, actions )" />
    </template>
  </component>
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
    var _actions = {};
    var _operands = {};
    if ( actions && actions.length ) {
      this.$api( 'friede', 'actions', '?' + this.options.actions.map(
        action => 'path=' + action ).join('&'))
         .then( r => {
           var res = r.data.results;
           if ( res.length )
             res.forEach( a => {
               _actions[ a.name ] = a;
               _operands[ a.name ] = [];
             });
           this.actions = _actions;
           this.operands = _operands;
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
      operands: {},
    }
  },
  methods: {
    act( actor, object, actions ) {
      console.log( arguments );
      Object.keys( actor.actions ).forEach( k => {
        this.operands[k] = [ object ];
      });
      actor.show = true;
    }
  },
  computed: {
    actors() {
      const actions = this.actions;
      const args = this.operands;
      var actors = {};
      Object.values( actions ).forEach( a => {
        const tag = a.data.component;
        if ( !actors[ tag ])
          actors[ tag ] = {
            show: false,
            actions: {},
            operands: {},
          };
        actors[ tag ].actions[ a.name ] = a;
        actors[ tag ].operands[ a.name ] = args[ a.name ];
      });
      return actors;
    }
  }
}
</script>

<style scoped lang="scss">
.model-dashboard {
  
}
</style>
