<template lang="html">
  <multiselect v-if="editMode" v-model="values" ref="inputV"
               :options="options" :class="fieldClasses"
               label="title"
               track-by="path"
               @blur="commitField"
               @search-change="getObjects"
               />
  <div v-else v-html="html" @click="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { ModelFieldMixin, ModelModelsFieldMixin } from '@/lib/mixins'
export default {
  name: 'ModelChoiceField',
  mixins: [ ModelFieldMixin, ModelModelsFieldMixin ],
  props: [],
  mounted() {
    if ( !this.readonly )
      this.getObjects('');
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
  .model-choice-field {

  }
</style>
