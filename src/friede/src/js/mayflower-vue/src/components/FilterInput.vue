<template lang="html">
  <div class="filter-input">
    <multiselect
      placeholder="filter"
      :value=value
      :multiple=true
      :taggable=true
      @input=input
      />
  </div>
</template>

<script lang="js">
import Multiselect from 'vue-multiselect'
export default {
  name: 'filter-input',
  props: {
    value: {
      type: Array,
      default: () => []
    }
  },
  mounted() {},
  data() {
    return {}
  },
  methods: {
    input( val ) {
      this.$emit( 'input', val );
    }
  },
  computed: {}
}
</script>

<style scoped lang="scss">
.filter-input {
}
</style>
