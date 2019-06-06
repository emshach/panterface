<template lang="html">
  <input v-if="editMode" type="number" v-model="field.wip"
         :class="fieldClasses" @blur="commitField" />
  <div v-else v-html="html" @click="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { ModelFieldMixin } from '@/lib/mixins'
export default {
  name: 'DecimalField',
  mixins: [ ModelFieldMixin ],
  props: {},
  mounted() {
    
  },
  data() { 
   return {
      editClass: [ 'uk-input' ]
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
.decimal-field {
  
}
</style>
