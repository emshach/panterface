<template lang="html">
  <div>
    <label class="uk-form-label">{{ label }}</label>
    <div class="uk-form-controls">
      <component :is="type" :name="name" :field="field" />
    </div>
  </div>
</template>

<script lang="js">
import { Field } from '@/lib/objects'
import fields from './fields'
export default  {
  name: 'Field',
  components: fields,
  props: {
    type: {
      type: String,
      default: 'CharField'
    },
    name: {
      type: String,
      default: ''
    },
    data: {
      type: Object,
      default: null
    }
  },
  mounted() {
    this.field = Field( this.data || { type: this.type, name: this.name });
  },
  data() {
    return {
      field: Field()
    }
  },
  methods: {
  },
  computed: {
    label() {
      if ( this.field && this.field.meta) {
        if ( this.field.meta.related
             && this.$store.state.models[ this.field.meta.related ]) {
          return this.$store.state.models[ this.field.meta.related ][
            this.type.match(/Multiple|Choices/) ? 'plural' : 'singular' ]
        }
      }
      return this.name;
    }
  }
}
</script>

<style scoped lang="scss">
  .field {

  }
</style>
