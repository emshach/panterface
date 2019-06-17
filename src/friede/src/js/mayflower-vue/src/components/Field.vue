<template lang="html">
  <div v-if="fieldset" :class="[ 'field', 'uk-fieldset', fieldClass ]">
    <h4>{{ label }}</h4>
    <hr class="titlesep" />
    <component :is="type" :name="name" :field="field" empty-value="None" />
  </div>
  <div v-else :class="[ 'field', fieldClass ]">
    <label class="uk-form-label">{{ label }}</label>
    <div class="uk-form-controls">
      <component :is="type" :name="name" :field="field" />
    </div>
  </div>
</template>

<script lang="js">
import kebabCase from 'lodash/kebabCase'
import { Field } from '@/lib/objects'
import fields from '@/fields'
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
      return this.name.replace( /^_+/, '' ).replace( /_+/g, ' ' );
    },
    fieldClass() {
      return kebabCase( this.type );
    }
  }
}
</script>

<style lang="scss">
.field {
  .field-display {
    > svg.svg-inline--fa, > .btn-edit svg.svg-inline--fa {
      margin-left: 6px;
      font-size: 0.875em;
      vertical-align: 0;
    }
  }
  tr {
    .field-display {
      > svg.svg-inline--fa {
        margin-left: 4px;
        font-size: 10px;
        vertical-align: 0.2em;
      }
    }
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
