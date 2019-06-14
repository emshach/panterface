<template lang="html">
  <div :class="classes">
    <vue-perfect-scrollbar>
    </vue-perfect-scrollbar>
  </div>
</template>

<script lang="js">
import DashboardPage from '@/views'
export default {
  name: 'HomeDashboard',
  mixins: [ DashboardPage ],
  props: [],
  mounted() {
    
  },
  data() {
    return {
      classes: [ 'home-dashboard' ]
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style lang="scss">
.home-dashboard {
  
}
</style>
