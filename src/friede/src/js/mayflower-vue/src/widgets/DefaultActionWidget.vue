<template lang="html">
  <card-widget :object=object :inline=inline :context=context
               @click.self=defaultAction >
    <template v-for="( _, slot ) in $scopedSlots"
              v-slot:[slot]=scope >
      <slot :name=slot v-bind=scope />
    </template>
  </card-widget>      
</a>
</template>

<script lang="js">
import CardWidget from './CardWidget'
import { Model } from '@/lib/objects'

export default {
  name: 'DefaultActionWidget',
  components: { CardWidget },
  props: {
    object: {
      type: Object,
      default: () => ({})
    },
    context: {
      type: Object,
      default: () => ({})
    },
    defaultAction: {
      type: Function,
      default: () => {}
    },
    inline: {
      type: Boolean,
      default: false
    },
    model: {
      type: Model,
      default: () => new Model({})
    }
  },
  mounted() {},
  data() {
    return {}
  },
  methods: {},
  computed: {}
}
</script>

<style scoped lang="scss">
  .default-action-widget {

  }
</style>
