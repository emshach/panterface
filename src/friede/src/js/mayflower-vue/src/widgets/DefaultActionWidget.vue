<template lang="html">
  <a :href="defaultAction">
    <card-widget :object=object >
      <template v-for="( _, slot ) in $scopedSlots"
                v-slot:[slot]=scope >
        <slot :name=slot v-bind=scope />
      </template>
    </card-widget>      
  </a>
</template>

<script lang="js">
import CardWidget from './CardWidget'
export default {
  name: 'DefaultActionWidget',
  components: { CardWidget },
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
