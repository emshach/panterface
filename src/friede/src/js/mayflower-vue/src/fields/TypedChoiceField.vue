<template lang="html">
  <multiselect v-if="editMode" v-model="field.wip" ref="inputV"
               :options="field.meta.options"
               :class="fieldClasses" @input="commitField" @blur="revertField" />
  <a v-else v-html="html" @click.prevent="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
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
