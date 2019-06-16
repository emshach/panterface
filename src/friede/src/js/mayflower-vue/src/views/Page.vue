<template lang="html">
  <vue-perfect-scrollbar class="page">
    <component :is=component v-bind=$attrs :model=model :blocks=blocks />
  </vue-perfect-scrollbar>
</template>

<script lang="js">
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
import pages from '@/views'
import { resolve } from '@/lib/util'
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
      return resolve( this.$store.getters.screen )
    },
    component() {
      return this.screen.component || 'HomePage'
    },
    model() {
      return this.screen.model || this.$store.model
    },
    blocks() {
      return this.screen.$blocks || {}
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
