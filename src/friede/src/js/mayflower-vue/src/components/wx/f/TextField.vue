<template lang="html">
  <textarea v-if="editMode" v-model="field.wip" ref="input"
         :class="fieldClasses" @blur="commitField" />
  <a v-else @click.prevent="editField" @focus="editField" :class="fieldClasses">
    <span v-html="html" />
    <font-awesome-icon :icon="isset ? 'edit': 'plus'" @click="editField" />
  </a>
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
