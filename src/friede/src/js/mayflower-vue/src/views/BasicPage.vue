<template lang="html">
  <div class="basicp-age">
    <component :is="component" />
  </div>
</template>

<script lang="js">
import Home from '@/views/Home'
const FormPage = () => import(/* webpackChunkName: "pages" */ '@/views/FormPage' )
export default  {
  name: 'BasicPage',
  components: {
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

  }
</style>
