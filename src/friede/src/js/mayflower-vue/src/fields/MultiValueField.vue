<template lang="html">
  <div v-if="readonly" v-html="field.html" :class="fieldClasses" />
  <div v-else-if="editMode" :class="fieldClasses" @blur="commitField">
    <model-field-widget v-for="f in field.fields" :key="f.name" :field="f" />
  </div>
  <div v-else v-html="field.html" @click="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { Field } from '@/lib/objects'
import { ModelFieldMixin } from '@/lib/mixins'
export default {
  name: 'MultiValueField',
  mixins: [ ModelFieldMixin ],
  props: {},
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
  .multi-value-field {

  }
</style>
