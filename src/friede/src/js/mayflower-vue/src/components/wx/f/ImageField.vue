<template lang="html">
  <div v-if="readonly" v-html="field.html" :class="fieldClasses" />
  <input v-else-if="editMode" type="file" v-model="field.wip"
         :class="fieldClasses" @blur="commitField" />
  <div v-else v-html="field.html" @click="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { Field } from '@/lib/objects'
import { ModelFieldMixin } from '@/lib/mixins'
export default {
  name: 'ImageField',
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
  .image-field {

  }
</style>
