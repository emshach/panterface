<template lang="html">
  <input v-if="editMode" type="checkbox" v-model="field.wip" ref="input"
         :class="fieldClasses" @change="commitField" @blur="revertField" />
  <a v-else @click.prevent="editField" @focus="editField" :class="fieldClasses">
    <span  v-html="html" />
    <font-awesome-icon v-if="!readonly" :icon="isset ? 'edit': 'plus'"
    @click="editField" />
  </a>
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
    commit( val ) {
      this.field.wip = val;
      this.commitField();
    }
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
