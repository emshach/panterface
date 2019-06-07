<template lang="html">
  <textarea v-if="editMode" v-model="field.wip" ref="input"
         :class="fieldClasses" @blur="commitField" />
  <a v-else v-html="html" @click.prevent="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { ModelFieldMixin } from '@/lib/mixins'
export default {
  name: 'TextField',
  mixins: [ ModelFieldMixin ],
  props: {},
  mounted() {
    
  },
  data() {
    return {
      editClass: [ 'uk-textarea' ]
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
.text-field {
  
}
</style>
