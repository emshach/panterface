<template lang="html">
  <span class="json-number">
    <input v-if="editing" type="number" :value="value" ref="input"
           @input="input" @blur="commit" /> 
    <span v-else @click="editMode = true">{{ value }}</span>
  </span>
</template>

<script lang="js">
import { JsonWidgetMixin } from '@/lib/mixins'
export default  {
  name: 'json-number',
  mixins: [ JsonWidgetMixin ],
  props: {
    value: {
      type: Number,
      default: 0
    }
  },
  mounted() {
    this.$nextTick(() => {
      if ( this.editMode )
        this.$refs.input.focus();
    });
  },
  data() {
    return {
    }
  },
  methods: {
    input() {
      this.$emit( 'input', parseInt( this.$refs.input.value || 0 ));
    },
    commit() {
      this.editMode = false;
    }
  },
  computed: {
  }
}
</script>

<style scoped lang="scss">
.json-number {
  color: coral;
}
</style>
