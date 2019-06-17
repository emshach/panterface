<template lang="html">
  <default-action-widget :object="object" />
</template>

<script lang="js">
import DefaultActionWidget from './DefaultActionWidget'
export default  {
  name: 'InlineWidget',
  props: [ 'object' ],
  componeents: { DefaultActionWidget },
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
  .inline-widget {

  }
</style>
