<template lang="html">
  <span class="json-number">
    <input v-if="editing" type="number" v-model="_value" @input="input"
           @change="input" /> 
    <template v-else>{{ _value }}</template>
  </span>
</template>

<script lang="js">
import { JsonWidgetMixin } from '@/lib/mixins'
export default  {
  name: 'json-number',
  mixins: [ JsonWidgetMixin ],
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
  .json-number {

  }
</style>
