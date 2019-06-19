<template lang="html">
  <vue-perfect-scrollbar :class="classes">
    <slot />
  </vue-perfect-scrollbar>
</template>

<script lang="js">
import { PageMixin } from '@/lib/mixins'
export default {
  name: 'ScrollPage',
  mixins: [ PageMixin ],
  props: [],
  mounted() {
  },
  data() {
    return {
      classes: { 'scroll-page': true }
    }
  },
  methods: {
  },
  computed: {
  }
}
</script>

<style lang="scss">
.scroll-page {
}
</style>
