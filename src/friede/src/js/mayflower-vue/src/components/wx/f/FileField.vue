<template lang="html">
  <input v-if="editMode" type="file" v-model="field.wip"
         :class="fieldClasses" @blur="commitField" />
  <a v-else v-html="html" @click.prevent="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { ModelFieldMixin } from '@/lib/mixins'
export default  {
  name: 'FileField',
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
.file-field {
  
}
</style>
