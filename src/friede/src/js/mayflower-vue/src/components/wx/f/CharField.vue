<template lang="html">
  <input v-if="editMode" type="text" v-model="field.wip" ref="input"
         :class="fieldClasses" @blur="commitField" />
  <a v-else v-html="html" @click.prevent="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { ModelFieldMixin } from '@/lib/mixins'
export default {
  name: 'CharField',
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
  .char-field {

  }
</style>
