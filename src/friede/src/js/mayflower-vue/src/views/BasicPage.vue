<template lang="html">
  <vue-perfect-scrollbar v-once class="basic-page">
    <component :is="component" />
  </vue-perfect-scrollbar>
</template>

<script lang="js">
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
import Home from '@/views/Home'
const FormPage = () => import(/* webpackChunkName: "pages" */ '@/views/FormPage' )
export default  {
  name: 'BasicPage',
  components: {
    VuePerfectScrollbar,
    Home,
    FormPage
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
    component() {
      return this.$store.getters.screen || 'Home'
    }
  }
}
</script>

<style scoped lang="scss">
.basic-page {
  position: relative;
  height: 100%;
  width: 100%;
  padding: 20px;
}
</style>
