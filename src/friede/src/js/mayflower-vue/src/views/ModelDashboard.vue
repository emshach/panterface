<template lang="html">
<div :class=classes>
  <component :is=tag mode="modal" :key=tag
             v-for="( actor, tag ) in actors"
             :op=op
             :actions=actor.actions
             :operands=actor.operands
             :show.sync=showModals[tag] />
  <component :is=blocks.breakfront.component v-if=blocks.breakfront
             :content=featured />
  <component :is=blocks.main.component v-if=blocks.main
             :objects=objects
             :actions=options.actions
             :item-layout=options.layout
             :search-fields=options.search
             @act=act >
    <template #item-actions={object} >
      <component :is=tag mode="widget" :key=tag
                 v-for="( actor, tag ) in actors"
                 :object=object
                 @act=act />
    </template>
  </component>
</div>
</template>

<script lang="js">
import { PageMixin } from '@/lib/mixins'
import blocks from '@/blocks'
import actors from '@/actors'
import isArray from 'lodash/isArray'
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
    var show = {};
    if ( actions && actions.length ) {
      this.$api( 'friede', 'actions', '?' + this.options.actions.map(
        action => 'path=' + action ).join('&'))
         .then( r => {
           var res = r.data.results;
           if ( res.length )
             res.forEach( a => {
               _actions[ a.name ] = a;
               _operands[ a.data.component ] = [];
               show[ a.data.component ] = false;
             });
           this.actions = _actions;
           this.operands = _operands;
           this.showModals = show;
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
      op: '',
      featured: [],
      objects: [],
      actions: {},
      operands: [],
      showModals: {
      }
    }
  },
  methods: {
    act( action, objects ) {
      const tag = this.actions[ action ].data.component;
      const actor = this.actors[ tag ];
      this.operands[ tag ] = isArray( objects ) ? objects : [ objects ];
      this.op = action;
      this.showModals[ tag ] = true;
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
            actions: {},
          };
        actors[ tag ].actions[ a.name ] = a;
        actors[ tag ].operands = args[ tag ];
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
