<template lang="html">
  <multiselect v-if="editMode" v-model="values" ref="inputV"
               :options="options" :class="fieldClasses"
               label="title"
               track-by="path"
               @input="commit"
               @blur="revertField"
               @search-change="getObjects"
               />
  <a v-else @click.prevent="editField" @focus="editField" :class="fieldClasses">
    <span v-html="html" />
    <font-awesome-icon :icon="isset ? 'edit': 'plus'" @click="editField" />
  </a>
</template>

<script lang="js">
import { ModelFieldMixin, ModelModelsFieldMixin } from '@/lib/mixins'
export default {
  name: 'ModelChoiceField',
  mixins: [ ModelFieldMixin, ModelModelsFieldMixin ],
  props: [],
  mounted() {
  },
  data() {
    return {
      
    }
  },
  methods: {
    editField: ModelFieldMixin.methods.editField,
    commit( val ) {
      this.field.wip = val;
      this.commitField();
    }
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
.model-choice-field {
  
}
</style>
