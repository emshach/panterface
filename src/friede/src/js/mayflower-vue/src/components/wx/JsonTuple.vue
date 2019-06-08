<template lang="html">
  <div class="json-tuple">
    <span class="json-key">
      <input v-if="editing" type="text" v-model="intlVal.key"
             @change="input" @blur="this.editMode=false" />
      <span v-else @click="this.editMode=true">{{
        intlVal.key.length ? intlVal.key : "''" }}</span>
      :
    </span>
    <json-widget class="json-value" :readonly="readonly" v-model="intlVal.value"/>
  </div>
</template>

<script lang="js">
import { JsonWidgetMixin } from '@/lib/mixins'
export default  {
  name: 'JsonTuple',
  mixins: [ JsonWidgetMixin ],
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
