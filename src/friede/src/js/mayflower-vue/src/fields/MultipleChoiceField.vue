<template lang="html">
  <div v-if="readonly" v-html=field.html :class=fieldClasses />
  <multiselect v-else-if="editMode" v-model=field.wip
               :options=[]
               :class=fieldClasses @blur=commitField />
  <a v-else v-html=field.html @click.prevent=editField @focus=editField
     :class=fieldClasses />
</template>

<script lang="js">
import { ModelFieldMixin } from '@/lib/mixins'
import Multiselect from 'vue-multiselect'
export default {
  name: 'MultipleChoiceField',
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
  .multiple-choice-field {

  }
</style>
