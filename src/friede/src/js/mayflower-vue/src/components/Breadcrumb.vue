<template lang="html">
  <vk-breadcrumb>
    <vk-breadcrumb-item
      v-for="( item, index ) in breadcrumb"
      :key="index"
      :href="item.href"
      :target="item.target" />
  </vk-breadcrumb>
</template>

<script lang="js">
import { Breadcrumb, BreadcrumbItem } from 'vuikit/lib/breadcrumb';
export default {
  name: 'Breadcrumb',
  props: [],
  components: {
    'vk-breadcrumb': Breadcrumb,
    'vk-breadcrumb-item': BreadcrumbItem
  },
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
  .breadcrumb {

  }
</style>
