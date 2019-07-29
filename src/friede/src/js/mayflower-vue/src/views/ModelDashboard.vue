<template lang="html">
<div :class=classes>
  <component :is=tag mode="modal" :key=tag
             v-for="( actor, tag ) in actors"
             :action=action
             :model=modelObj
             :actions=actor.actions
             :operands=actor.operands
             :show.sync=showModals[tag]
             :now.sync=now[tag]
             @act=act
             @success=success() />
  <component :is=blocks.breakfront.component v-if=blocks.breakfront
             :content=featured />
  <component :is=blocks.main.component v-if=blocks.main
             :objects=objects
             :actions=allActions
             :item-layout=options.layout
             :search-fields=options.search
             @act=act >
    <template #item-actions={object} >
      <component :is=tag mode="widget" :key=tag
                 v-for="( actor, tag ) in actors"
                 :object=object
                 :actions=actor.actions
                 :model=modelObj
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
    var ops = {};
    var operands = {};
    var show = {};
    var now = {};
    if ( actions && actions.length ) {
      var reverse = [];
      this.$api( 'friede', 'actions', '?' + actions.map(
        action => 'path=' + action ).join('&'))
         .then( r => {
           var res = r.data.results;
           if ( res.length )
             res.forEach( a => {
               if ( a.data.reverse )
                 reverse.push( a.data.reverse );
               ops[ a.name ] = a;
               operands[ a.data.component ] = [];
               show[ a.data.component ] = false;
               now[ a.data.component ] = false;
             });
           if ( reverse.length ) {
             this.$api( 'friede', 'actions', '?' + reverse.map(
               action => 'path=' + action ).join('&'))
                .then( r => {
                  var res = r.data.results;
                  if ( res.length )
                    res.forEach( a => {
                      if ( a.data.reverse )
                        ops[ a.name ] = a;
                      operands[ a.data.component ] = [];
                      show[ a.data.component ] = false;
                      now[ a.data.component ] = false;
                    });
                  this.actions = ops;
                  this.operands = operands;
                  this.showModals = show;
                  this.now = now;
                });
           }
           else {
             this.actions = ops;
             this.operands = operands;
             this.showModals = show;
             this.now = now;
           }
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
      action: '',
      actions: {},
      operands: [],
      showModals: {},
      now: {}
    }
  },
  methods: {
    act( action, objects, now ) {
      const tag = this.actions[ action ].data.component;
      const actor = this.actors[ tag ];
      this.operands[ tag ] = isArray( objects ) ? objects : [ objects ];
      this.action = action;
      this.showModals[ tag ] = true;
      this.now[ tag ] = now || false;
    },
    success( results ) {
      this.getData();
      if ( this.model === 'friede.app' )
        this.$store.dispatch( 'refresh' );
    }
  },
  computed: {
    allActions() {
      return Object.keys( this.actions );
    },
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
