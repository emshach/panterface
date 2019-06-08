<template lang="html">
  <span class="json-boolean uk-label" @click.prevent="toggle">{{
    this.intlVal ? 'true' : 'false' }}</span>
</template>

<script lang="js">
import { JsonWidgetMixin } from '@/lib/mixins'
export default  {
  name: 'JsonBoolean',
  mixins: [ JsonWidgetMixin ],
  props: {
    value: {
      type: Boolean,
      default: false,
    }
  },
  mounted() {
  },
  data() {
    return {
    }
  },
  methods: {
    toggle() {
      this.intlVal = !this.intlVal;
      this.$emit( 'input', this.intlVal );
    }
  },
  computed: {
  }
}
</script>

<style lang="scss">
.json-boolean {
  font-weight: bold;
  font-size: 12px;
}
</style>
