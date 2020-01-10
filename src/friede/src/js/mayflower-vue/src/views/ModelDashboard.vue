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
    <component :is=blocks.header.component v-if=blocks.header >
      <template #actions="data" >
        <component :is=tag mode="header" :key=tag
                   v-for="( actor, tag ) in actors"
                   :actions=actor.actions
                   :model=modelObj
                   @act=act />
      </template>
    </component>
    <component :is=blocks.left_sidebar.component v-if=blocks.left_sidebar >
      <template #actions="data" >
        <component :is=tag mode="left-sidebar" :key=tag
                   v-for="( actor, tag ) in actors"
                   :actions=actor.actions
                   :model=modelObj
                   @act=act />
      </template>
    </component>
    <component :is=blocks.right_sidebar.component v-if=blocks.right_sidebar >
      <template #actions="data" >
        <component :is=tag mode="right-sidebar" :key=tag
                   v-for="( actor, tag ) in actors"
                   :actions=actor.actions
                   :model=modelObj
                   @act=act />
      </template>
    </component>
    <component :is=blocks.breakfront.component v-if=blocks.breakfront
               :content=featured :model=modelObj />
    <component :is=blocks.main.component v-if=blocks.main
               :objects=objects
               :actions=allActions
               :item-layout=options.layout
               :search-fields=options.search
               :model=modelObj
               @act=act >
      <template #header-actions="data" >
        <component :is=tag mode="content-header" :key=tag
                   v-for="( actor, tag ) in actors"
                   :actions=actor.actions
                   :model=modelObj
                   @act=act />
      </template>
      <template #item-actions="{ object }" >
        <component :is=tag mode="widget" :key=tag
                   v-for="( actor, tag ) in actors"
                   :object=object
                   :actions=actor.actions
                   :model=modelObj
                   @act=act />
      </template>
      <template #footer-actions="data" >
        <component :is=tag mode="content-footer" :key=tag
                   v-for="( actor, tag ) in actors"
                   :actions=actor.actions
                   :model=modelObj
                   @act=act />
      </template>
    </component>
    <component :is=blocks.footer.component v-if=blocks.footer >
      <template #actions="data" >
        <component :is=tag mode="footer" :key=tag
                   v-for="( actor, tag ) in actors"
                   :actions=actor.actions
                   :model=modelObj
                   @act=act />
      </template>
    </component>
  </div>
</template>

<script lang="js">
import { PageMixin, ActionsMixin } from '@/lib/mixins'
import blocks from '@/blocks'
import actors from '@/actors'
import isArray from 'lodash/isArray'
export default  {
  name: 'ModelDashboard',
  mixins: [ PageMixin, ActionsMixin ],
  components: { ...blocks, ...actors },
  props: [],
  mounted() {},
  data() {
    return {
      classes: {
        'model-dashboard': true,
        'uk-flex-column': true,
      },
      featured: [],
    }
  },
  methods: {},
  computed: {}
}
</script>

<style lang="scss">
.model-dashboard {
  
}
</style>
