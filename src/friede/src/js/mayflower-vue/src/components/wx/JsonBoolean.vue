<template lang="html">
  <span class="uk-label" @click.prevent="toggle">{{
    this._value ? 'true' : 'false' }}</span>
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
      this._value = !this._value;
      this.$emit( 'input', this._value );
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
