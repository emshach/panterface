<template lang="html">
  <span class="json-number">
    <input v-if="editing" type="number" :value="value" ref="input"
           @input="input" /> 
    <template v-else>{{ value }}</template>
  </span>
</template>

<script lang="js">
import { JsonWidgetMixin } from '@/lib/mixins'
export default  {
  name: 'json-number',
  mixins: [ JsonWidgetMixin ],
  props: {
    value: {
      type: Number,
      default: 0
    }
  },
  mounted() {
  },
  data() {
    return {
    }
  },
  methods: {
    input() {
      this.$emit( 'input', this.$refs.input.value );
    }
  },
  computed: {
  }
}
</script>

<style scoped lang="scss">
.json-number {
  color: coral;
}
</style>
