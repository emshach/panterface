<template lang="html">
  <multiselect v-if="editMode" v-model=values ref="inputV"
               :options=options :class=fieldClasses
               label="title" track-by="path"
               @input=commit
               @blur=revertField
               @search-change=fieldGetObjects >
    <template slot="clear" slot-scope="props">
      <div class="multiselect__clear" @mousedown.prevent.stop=revertField />
    </template>
  </multiselect>
  <a v-else @click.prevent="editField" @focus="editField" :class="fieldClasses">
    <span v-html="html" />
    <font-awesome-icon v-if="!readonly" :icon="isset ? 'edit': 'plus'"
    @click="editField" />
  </a>
</template>

<script lang="js">
import { ModelFieldMixin, ModelModelsFieldMixin } from '@/lib/mixins'
export default {
  name: 'ModelChoiceField',
  mixins: [ ModelFieldMixin, ModelModelsFieldMixin ],
  props: [],
  mounted() {
    setTimeout(() => {
      if ( !this.hasInput )
        this.getObjects('');
    }, 2000 );
  },
  data() {
    return {
      hasInput: false
    }
  },
  methods: {
    editField: ModelFieldMixin.methods.editField,
    commit( val ) {
      this.field.wip = val;
      this.commitField();
    },
    fieldGetObject( query ) {
      this.hasInput = true;
      this.getObjects( query );
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
