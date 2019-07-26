<template lang="html">
  <multiselect v-if="editMode" v-model=field.wip ref="inputV"
               :options="field.meta.options" track-by=key label="label"
               :class=fieldClasses @input=commit @blur=revertField />
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
      return this.meta.options ? this.meta.options[ this.value ]
      : this.value;
    }
  }
}
</script>

<style scoped lang="scss">
.choice-field {
  
}
</style>
