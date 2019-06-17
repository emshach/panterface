<template lang="html">
  <vk-grid class="filter-grid">
    <div>app 1</div>
    <div>app 2</div>
  </vk-grid>
</template>

<script lang="js">
import { Grid as VkGrid } from 'vuikit/lib/grid'
import { Card as VkCard, CardTitle as VkCardTitle } from 'vuikit/lib/card'
export default  {
  name: 'filter-grid',
  components: {
    VkGrid,
    VkCard,
    VkCardTitle,
  },
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
.filter-grid {
  
}
</style>
