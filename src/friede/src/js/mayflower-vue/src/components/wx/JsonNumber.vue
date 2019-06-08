<template lang="html">
  <span class="json-number">
    <input v-if="editing" type="number" v-model="_v" @input="input" @change="input" />
    <template v-else>{{ _v }}</template>
  </span>
</template>

<script lang="js">
export default  {
  name: 'json-number',
  props: [],
  mounted() {
  },
  data() {
    return {
    }
  },
  methods: {
  },
  computed: {
  }
}
</script>

<style scoped lang="scss">
  .json-number {

  }
</style>
