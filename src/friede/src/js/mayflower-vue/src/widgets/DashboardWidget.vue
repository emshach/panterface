<template lang="html">
  <default-action-widget :object=object >
    <template v-for="( _, slot ) in $scopedSlots"
              v-slot:[slot]=scope>
      <slot :name=slot v-bind=scope />
    </template>
  </default-action-widget>
</template>

<script lang="js">
import DefaultActionWidget from './DefaultActionWidget'
import { Model } from '@/lib/objects'

export default {
  name: 'DashboardWidget',
  components: { DefaultActionWidget },
  props: {
    object: {
      type: Object,
      required: true
    },
    model: {
      type: Model,
      default: () => new Model({})
    }
  },
  mounted() {
    
  },
  data() {
    return {
      
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
.dashboard-widget {
  
}
</style>
