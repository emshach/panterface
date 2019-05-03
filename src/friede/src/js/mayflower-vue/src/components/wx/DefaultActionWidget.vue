<template lang="html">
  <a href="defaultAction">
    <card-widget :object="object" />
  </a>
</template>

<script lang="js">
import CardWidget from '@/components/CardWidget'
export default  {
  name: 'DefaultActionWidget',
  props: {
    object: {
      type: Object,
      required: true
    },
    context: {
      type: Object,
      default: {}
    }
  },
  components: { CardWidget },
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
  .default-action-widget {

  }
</style>
