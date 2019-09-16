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
    <vue-perfect-scrollbar class="scroller">
      <component :is=blocks.primary.component v-if=blocks.primary
                 :content=primaryObjects :mode=blocks.secondary.mode />
      <component :is=blocks.secondary.component v-if=blocks.secondary
                 :content=secondaryObjects :mode=blocks.primary.mode />
      <component :is=blocks.body.component v-if=blocks.body
                 :content=bodyObjects :mode=blocks.body.mode />
    </vue-perfect-scrollbar>
  </div>
</template>

<script lang="js">
import { PageMixin, ActionsMixin } from '@/lib/mixins'
import blocks from '@/blocks'
import actors from '@/actors'

export default {
  name: 'SectionalDashboard',
  mixins: [ PageMixin, ActionsMixin ],
  components: { ...blocks, ...actors },
  props: {},
  data() {
    return {
      classes: {
        'sectional-dashboard': true,
        'uk-flex-column': true
      }
    };
  },
  created() {},
  mounted() {},
  methods: {},
  computed: {
    primaryObjects() {
      return this.objects && this.objects.primary || this.objects;
    },
    secondaryObjects() {
      return this.objects && this.objects.secondary || this.objects;
    },
    bodyObjects() {
      return this.objects && this.objects.body || this.objects;
    }
  }
}
</script>

<style lang="scss">
.sectional-dashboard {
  
}
</style>
