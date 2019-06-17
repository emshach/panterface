<template lang="html">
  <adaptive-widget class="view-model-widget view-widget model-widget">
    <template #content>
      <model-field-widget v-for="f in model.preview_fields"
                          :key="model._fields[f].name"
                          :field="model._fields[f]"  />
    </template>
  </adaptive-widget>
</template>

<script lang="js">
import ModelFieldWidget from './ModelFieldWidget'
import { ModelWidgetMixin } from '@/lib/mixins'
export default  {
  name: 'ViewModelWidget',
  mixins: [ ModelWidgetMixin ],
  props: {},
  components: { ModelFieldWidget },
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
