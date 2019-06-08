<template lang="html">
  <span class="json-boolean uk-label" @click.prevent="toggle">{{
    this.value ? 'true' : 'false' }}</span>
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
      if ( this.readonly )
        return;
      this.$emit( 'input', !this.value );
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
