<template lang="html">
  <div :class=classes>
    <vue-perfect-scrollbar>
    </vue-perfect-scrollbar>
  </div>
</template>

<script lang="js">
import { PageMixin } from '@/lib/mixins'
export default {
  name: 'HomeDashboard',
  mixins: [ PageMixin ],
  props: [],
  mounted() {
    
  },
  data() {
    return {
      classes: { 'home-dashboard': true }
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
