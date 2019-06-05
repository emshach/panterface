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
      if ( this.field.meta.link_field ) {
        const model = this.$store.state.models[m];
        m = model.fields.find( x => x.name === this.field.meta.link_field );
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
