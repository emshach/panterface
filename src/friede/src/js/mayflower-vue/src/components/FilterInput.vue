<template lang="html">
  <div class="filter-input">
    <multiselect
      placeholder="filter"
      track-by="key"
      label="label"
      :options=filters
      :value=value
      :multiple=true
      :taggable=true
      @input=input
      @tag="addFilter"
      />
  </div>
</template>

<script lang="js">
import Multiselect from 'vue-multiselect'
export default {
  name: 'filter-input',
  components: { Multiselect },
  props: {
    value: {
      type: Array,
      default: () => []
    },
    filters: {
      type: Array,
      default: () => []
    }
  },
  mounted() {
    this._value = this.value.slice();
    this._filters = this.filters.slice();
  },
  data() {
    return {
      _value: [],
      _filters: [],
    }
  },
  methods: {
    input( val ) {
      console.log( 'input val', val );
      this.$emit( 'input', val );
    },
    addFilter( tag ) {
      if ( this._filters.find( x => x.key === key ))
        return;
      const filter = {
        key: tag,
        label: tag
      }
      this._filters.push( filter );
      this._value.push( filter );
    },
  },
  computed: {}
}
</script>

<style scoped lang="scss">
.filter-input {
}
</style>
