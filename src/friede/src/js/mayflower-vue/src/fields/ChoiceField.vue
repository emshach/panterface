<template lang="html">
  <multiselect v-if="editMode" v-model=field.wip ref="inputV"
               :options="field.meta.options" track-by=key label="label"
               :class=fieldClasses @input=commit @blur=revertField >
    <template slot="clear" slot-scope="props">
      <div class="multiselect__clear" @mousedown.prevent.stop=revertField />
    </template>
  </multiselect>
  <a v-else v-html=html @click.click=editField @focus=editField
       :class=fieldClasses />
</template>

<script lang="js">
import { ModelFieldMixin } from '@/lib/mixins'
import Multiselect from 'vue-multiselect'
export default {
  name: 'ChoiceField',
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
    commit( value ) {
      if ( value )
        this.field.wip = value.key;
      this.commitField();
    }
  },
  computed: {
    html() {
      if ( this.field.meta.options ) {
        let v = this.field.meta.options.find( x => x.key === this.field.value );
        if (v)
          return v.label;
      }
      return this.field.value;
    }
  }
}
</script>

<style scoped lang="scss">
.choice-field {
  
}
</style>
