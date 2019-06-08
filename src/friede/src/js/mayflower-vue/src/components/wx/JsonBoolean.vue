<template lang="html">
  <span class="uk-label" @click.prevent="toggle">{{ this._v ? 'true' : 'false' }}</span>
</template>

<script lang="js">
export default  {
  name: 'JsonBoolean',
  props: [],
  mounted() {
  },
  data() {
    return {
    }
  },
  methods: {
    toggle() {
      this._v = !this._v;
      this.$emit( 'input', this._v );
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
