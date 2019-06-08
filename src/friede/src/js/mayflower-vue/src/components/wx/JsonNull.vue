<template lang="html">
  <span class="json-null uk-label uk-label-success" @click.prevent="toggle">null</span>
</template>

<script lang="js">
export default  {
  name: 'JsonNull',
  props: [],
  mounted() {},
  data() {
    return {}
  },
  methods: {},
  computed: {}
}
</script>

<style scoped lang="scss">
.json-null {
  font-weight: bold;
  font-size: 12px;
}
</style>
