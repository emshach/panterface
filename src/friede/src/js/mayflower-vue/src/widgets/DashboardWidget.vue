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
export default {
  name: 'DashboardWidget',
  components: { DefaultActionWidget },
  props: [],
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
