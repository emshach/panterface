<template lang="html">
  <vue-perfect-scrollbar class="page">
    <component :is="component" v-bind="$attrs" />
  </vue-perfect-scrollbar>
</template>

<script lang="js">
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
import pages from '@/views'
export default {
  inheritAttrs: false,
  name: 'Page',
  components: {
    VuePerfectScrollbar,
    ...pages
  },
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
    screen() {
      return this.$store.getters.screen

    },
    component() {
      var screen = this.screen;
      while ( screen && !screen.data.component
              && screen.extends )
        screen = screen.extends;
      return screen && screen.data.component || 'HomePage'
    }
  }
}
</script>

<style scoped lang="scss">
.page {
  position: absolute;
  top: 0;
  bottom: 34px;
  left: 0;
  right: 0;
  padding: 40px 20px 10px;
}
</style>
