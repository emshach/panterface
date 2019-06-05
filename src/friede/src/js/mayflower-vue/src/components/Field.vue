<template lang="html">
  <div v-if="fieldset" class="uk-fieldset">
    <h4>{{ label }}</h4>
    <hr class="titlesep" />
    <component :is="type" :name="name" :field="field" />
  </div>
  <div v-else>
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
      if ( this.field && this.field.meta) {
        if ( this.field.meta.related
             && this.$store.state.models[ this.field.meta.related ]) {
          return this.$store.state.models[ this.field.meta.related ][
            this.type.match( /Multiple|Choices/ ) ? 'plural' : 'singular' ]
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
.uk-fieldset {
  margin-top: 30px;
  h4 {
    text-transform: capitalize;
  }
  .titlesep {
    margin-top: 0;
    margin-bottom: 20px;
  }
}
</style>
