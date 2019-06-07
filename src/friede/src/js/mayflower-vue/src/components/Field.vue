<template lang="html">
  <div v-if="fieldset" class="uk-fieldset">
    <h4>{{ label }}</h4>
    <hr class="titlesep" />
    <component :is="type" :name="name" :field="field" empty-value="None" />
  </div>
  <div v-else class="field">
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
    },
    fieldset: Boolean
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
      // if ( this.field && this.field.meta) {
      //   if ( this.field.meta.related
      //        && this.$store.state.models[ this.field.meta.related ]) {
      //     return this.$store.state.models[ this.field.meta.related ][
      //       this.type.match( /Multiple|Choices/ ) ? 'plural' : 'singular' ]
      //   }
      // }
      return this.name.replace( /^_/, '' ).replace( /_/g, ' ' );
    }
  }
}
</script>

<style scoped lang="scss">
.field {
  .field-display {
    margin-right: 4px;
  }
}
.uk-fieldset {
  margin: 36px 0 20px;
  h4 {
    margin: 0;
    text-transform: capitalize;
  }
  .titlesep {
    margin: 0 0 12px;
  }
}
</style>
