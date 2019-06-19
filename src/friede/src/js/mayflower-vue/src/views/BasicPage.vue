<template lang="html">
  <div :class=classes >
    <slot />
  </div>
</template>

<script lang="js">
import { PageMixin } from '@/lib/mixins'
export default {
  name: 'BasicPage',
  mixins: [ PageMixin ],
  props: [],
  mounted() {
  },
  data() {
    return {
      classes: { 'basic-page': true }
    }
  },
  methods: {},
  computed: {}
}
</script>

<style lang="scss">
.basic-page {
}
</style>
