<template lang="html">
  <multiselect v-if="editMode" v-model="values" ref="inputV"
               :options="options" :class="fieldClasses"
               :multiple="true"
               label="title"
               track-by="path"
               open-direction="bottom"
               @blur="commitField"
               @search-change="getObjects"
               />
  <div v-else v-html="html" @click="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { ModelFieldMixin, ModelModelsFieldMixin } from '@/lib/mixins'
export default {
  name: 'ModelMultipleChoiceField',
  mixins: [ ModelFieldMixin, ModelModelsFieldMixin ],
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
    searchModel() {
      const m = this.field.meta.related;
      let l = this.field.meta.link_field;
      if (l) {
        try {
        const model = this.$store.state.models[m];
        console.log( 'model', model);
          m = model && model.fields.find( x => x.name === l );
        } catch (e) {
          console.warn( 'error in eval', e );
        }
      }
      return m;
    }
  }
}
</script>

<style scoped lang="scss">
  .model-multiple-choice-field {

  }
</style>
