<template lang="html">
  <component :is="type" :name="type" :field="field" />
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
  }
}
</script>

<style scoped lang="scss">
  .field {

  }
</style>
