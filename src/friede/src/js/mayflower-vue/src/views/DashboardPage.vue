<template lang="html">
  <div :class="classes">
    <slot/>
  </div>
</template>

<script lang="js">
import PageMixin from '@/lib/mixins'
export default {
  name: 'DashboardPage',
  mixins: [ PageMixin ],
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
