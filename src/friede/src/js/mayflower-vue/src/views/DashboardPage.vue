<template lang="html">
  <div :class="classes">
    <slot/>
  </div>
</template>

<script lang="js">
import BasicPage from '@/views'
export default {
  name: 'DashboardPage',
  mixins: [ BasicPage ],
  props: [],
  mounted() {
    
  },
  data() {
    return {
      classes: [ 'dashboard-page' ]
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
.dashboard-page {
  
}
</style>
