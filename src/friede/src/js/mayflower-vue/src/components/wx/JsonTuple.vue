<template lang="html">
  <div class="json-tuple">
    <span class="json-key">
      <input v-if="editing" type="text" v-model="_v.key" @change="input" />
      <template v-else>{{ _v.key }}</template>
      :
    </span>
    <json-widget class="json-value" :readonly="readonly" v-model="_v.value"/>
  </div>
</template>

<script lang="js">
import { JsonWidgetMixn } from '@/lib/mixins'
export default  {
  name: 'JsonTuple',
  props: {
    value: {
      type: Object,
      default: () => ({ key: '', value: null })
    },
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
.json-tuple {
  
}
</style>
