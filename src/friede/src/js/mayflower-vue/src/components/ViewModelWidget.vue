<template lang="html">
  <adaptive-widget class="view-model-widget view-widget model-widget">
    <template #content>
      <model-field-widget v-for="field in model.preview_fields" :key="field.name" />
    </template>
  </adaptive-widget>
</template>

<script lang="js">
export default  {
  name: 'view-model-widget',
  props: {
    model: {
      type: Object,
      default: () => {}
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
  .view-model-widget {

  }
</style>
