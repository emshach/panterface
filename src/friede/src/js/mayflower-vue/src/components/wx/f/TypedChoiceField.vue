<template lang="html">
  <div v-if="readonly" v-html="field.html" :class="fieldClasses" />
  <multiselect v-else-if="editMode" v-model="field.wip"
               :options="[]"
               :class="fieldClasses" @blur="commitField" />
  <div v-else v-html="field.html" @click="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { Field } from '@/lib/objects'
import { ModelFieldMixin } from '@/lib/mixins'
import Multiselect from 'vue-multiselect'
export default {
  name: 'TypedChoiceField',
  mixins: [ ModelFieldMixin ],
  props: {},
  components: { Multiselect },
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
  .typed-choice-field {

  }
</style>
