<template lang="html">
  <div class="filter-input uk-flex">
    <div v-if=value.length class="label">:</div>
    <multiselect
      placeholder="filter"
      track-by="key"
      label="label"
      :options=filters
      :value=value
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
  },
  data() {
    return {
    }
  },
  methods: {
    input( val ) {
      console.log( 'input val', val );
      this.$emit( 'input', val );
    },
    addFilter( tag ) {
      if ( this.filters.find( x => x.key === tag ))
        return;
      const filter = {
        key: tag,
        label: tag
      }
      this.$emit( 'input', this.value.concat([ filter ]));
      this.$emit( 'add', filter );
    },
  },
  computed: {}
}
</script>

<style lang="scss">
.filter-input {
  >.label {
    line-height: 39px;
    font-weight: bold;
    color: cornflowerblue;
  }
  .multiselect {
    background: transparent;
    border: 0 none;
    &__tags {
      display: inline;
      background: transparent;
      border: 0 none;
      padding-top: 0;
      padding-bottom: 0;
      padding-left: 0;
      line-height: 39px;
      &-wrap {
        flex: 1;
        flex-basis: 100%;
      }
    }
    &__tag {
      margin-top: 8px;
      margin-bottom: -3px;
      margin-right: 4px;
      background: transparent;
      color: #266d4d;
      &-icon:after {
        font-size: 14px;
        vertical-align: -1px;
      }
    }
    &__select {
      padding-bottom: 8px;
    }
    &__input {
      max-width: 6em;
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
