<template lang="html">
  <vue-perfect-scrollbar class="basic-page">
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
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 20px;
}
</style>
