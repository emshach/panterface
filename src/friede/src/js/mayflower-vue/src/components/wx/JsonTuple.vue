<template lang="html">
  <div class="json-tuple">
    <span class="json-key">
      <input v-if="editing" type="text" :value="value.key" @blur="commit"
             ref="key" />
      <a v-else href="#" @click.prevent="editKey">{{
        value.key.length ? value.key : "''" }}</a>
      :
    </span>
    <json-widget class="json-value" :readonly="readonly" :value="value.value"
                 @input="updateVal" :edit="!readonly"/>
  </div>
</template>

<script lang="js">
import { JsonWidgetMixin } from '@/lib/mixins'
export default  {
  name: 'JsonTuple',
  mixins: [ JsonWidgetMixin ],
  props: {
    value: {
      type: Object,
      default: () => ({ key: '', value: null })
    },
  },
  mounted() {
    this.$nextTick(() => {
      if ( this.editMode )
        this.$refs.key.focus();
    });
  },
  data() {
    return {
      intlVal: { key: '', value: null },
    }
  },
  methods: {
    commit() {
      this.input();
      this.editMode = false;
    },
    input() {
      this.$emit( 'input', { key: this.$refs.key.value, value: this.value.value })
    },
    updateVal( val ) {
      this.$emit( 'input', { key: this.value.key, value: val })
    },
    editKey() {
      this.editMode = true;
      this.$nextTick(() => {
        this.$refs.key.focus();
      });
    }
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
.json-tuple {
  margin-left: 1em;
}
</style>
