<template lang="html">
  <div class="filter-input">
    <multiselect
      placeholder="filter"
      track-by="key"
      label="label"
      :options=iFilters
      :value=iValue
      :multiple=true
      :taggable=true
      :close-on-select=false
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
    this.iValue = this.value.slice();
    this.ifilters = this.filters.slice();
  },
  data() {
    return {
      iValue: [],
      iFilters: [],
    }
  },
  methods: {
    input( val ) {
      console.log( 'input val', val );
      this.$emit( 'input', val );
    },
    addFilter( tag ) {
      if ( this.iFilters.find( x => x.key === key ))
        return;
      const filter = {
        key: tag,
        label: tag
      }
      this.iFilters.push( filter );
      this.iValue.push( filter );
      this.$emit( 'input', this.iValue );
    },
  },
  computed: {}
}
</script>

<style scoped lang="scss">
.filter-input {
  .multiselect {
    background: transparent;
    border: 0 none;
    &__tags {
      background: transparent;
      border: 0 none;
      padding-top: 0;
      padding-bottom: 0;
      line-height: 39px;
    }
    &__select {
      padding-bottom: 8px;
    }
    &__input {
      background: transparent;
      border: 0 none;
      margin: 0;
      line-height: 40px;
      vertical-align: middle;
    }
    &__placeholder {
      color: darkslateblue;
      margin: 0;
      padding: 0 0 0 5px;
      line-height: 40px;
      font-size: 16px;
    }
  }
}
</style>
