<template lang="html">
  <multiselect v-if="editMode" v-model=values ref="inputV"
               :options=options :class=fieldClasses
               label="title" track-by="path"
               @input=commit
               @blur=revertField
               @search-change=fieldGetObjects >
    <template #clear >
      <div class="multiselect__clear" @mousedown.prevent.stop=revertField />
    </template>
  </multiselect>
  <a v-else @click.prevent=edit @focus=edit :class=fieldClasses >
    <span v-html="html" />
    <font-awesome-icon v-if="!readonly" :icon="isset ? 'edit': 'plus'" @click=edit />
  </a>
</template>

<script lang="js">
import { ModelFieldMixin, ModelModelsFieldMixin } from '@/lib/mixins'
export default {
  name: 'ModelChoiceField',
  mixins: [ ModelFieldMixin, ModelModelsFieldMixin ],
  props: [],
  mounted() {},
  data() {
    return {
      hasInput: false
    }
  },
  methods: {
    edit() {
      setTimeout(() => {
        if ( !this.hasInput )
          this.getObjects('');
      }, 2000 );
      this.editField();
    },
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
