<template lang="html">
  <input v-if="editMode" type="checkbox" v-model="field.wip" ref="input"
         :class="fieldClasses" @input="commitField" @blur="revertField" />
  <div v-else v-html="html" @click="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { Field } from '@/lib/objects'
import { ModelFieldMixin } from '@/lib/mixins'
export default {
  name: 'BooleanField',
  mixins: [ ModelFieldMixin ],
  props: {},
  mounted() {
    
  },
  data() {
    return {
      editClass: [ 'uk-checkbox' ]
    }
  },
  methods: {
    
  },
  computed: {
    html() {
      if ( this.isset ) {
        if ( this.field.value )
          return 'Yes';
        return 'No';
      }
      return this.emptyValue;
    }
  }
}
</script>

<style scoped lang="scss">
  .boolean-field {

  }
</style>
