<template lang="html">
  <div class="json-tuple">
    <span class="json-key">
      <input v-if="editing" type="text" v-model="intlVal.key"
             @change="input" @blur="editMode = false" />
      <a v-else href="#" @click.prevent="editMode = true">{{
        intlVal.key.length ? intlVal.key : "''" }}</a>
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
      intlVal: { key: '', value: null },
    }
  },
  methods: {
    input() {
      this.$emit( 'input', this.intlVal );
    }
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
.json-tuple {
  
}
</style>
