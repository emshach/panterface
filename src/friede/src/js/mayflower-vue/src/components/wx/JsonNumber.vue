<template lang="html">
  <span class="json-number">
    <input v-if="editing" type="number" v-model="intlVal" @input="input"
           @change="input" /> 
    <template v-else>{{ intlVal }}</template>
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
  color: coral;
}
</style>
