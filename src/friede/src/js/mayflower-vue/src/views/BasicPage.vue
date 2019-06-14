<template lang="html">
  <vue-perfect-scrollbar :class="classes">
    <slot />
  </vue-perfect-scrollbar>
</template>

<script lang="js">
import PageMixin from '@/lib/mixins'
export default {
  name: 'BasicPage',
  mixins: [ PageMixin ],
  props: [],
  mounted() {
  },
  data() {
    return {
      classes: [ 'basic-page' ]
    }
  },
  methods: {
  },
  computed: {
  }
}
</script>

<style scoped lang="scss">
.basic-page {
  position: absolute;
  top: 0;
  bottom: 34px;
  left: 0;
  right: 0;
  padding: 40px 20px 10px;
}
</style>
