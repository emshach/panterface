<template lang="html">
  <span class="uk-label" @click.prevent="toggle">{{
    this.intlVal ? 'true' : 'false' }}</span>
</template>

<script lang="js">
import { JsonWidgetMixin } from '@/lib/mixins'
export default  {
  name: 'JsonBoolean',
  mixins: [ JsonWidgetMixin ],
  props: [],
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
  
}
</style>
