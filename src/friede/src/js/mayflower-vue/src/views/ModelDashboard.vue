<template lang="html">
<div :class=classes>
  <component :is=blocks.breakfront.component v-if=blocks.breakfront
             :content=content />
  <component :is=blocks.main.component v-if=blocks.main :model=model
             :actions=options.actions />
</div>
</template>

<script lang="js">
import { PageMixin } from '@/lib/mixins'
import blocks from '@/blocks'
export default  {
  name: 'ModelDashboard',
  mixins: [ PageMixin ],
  components: blocks,
  props: [],
  mounted() {
    
  },
  data() {
    return {
      classes: [ 'model-dashboard' ],
      content: [],
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
