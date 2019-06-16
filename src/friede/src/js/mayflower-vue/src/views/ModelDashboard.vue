<template lang="html">
<div class="model-dashboard">
  <component :is=blocks.breakfront.component v-if=blocks.breakfront />
  <component :is=blocks.main.component v-if=blocks.main />
</div>
</template>

<script lang="js">
import { PageMixin } from '@/lib/mixins'
export default  {
  name: 'ModelDashboard',
  mixins: [ PageMixin ],
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
.model-dashboard {
  
}
</style>
