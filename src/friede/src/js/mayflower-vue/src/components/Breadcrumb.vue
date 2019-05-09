<template lang="html">
  <vk-breadcrumb class="breadcrumb">
    <vk-breadcrumb-item
      v-for="( item, index ) in items"
      :key="index"
      :href="item.href"
      :target="item.target">{{ item.title }}</vk-breadcrumb-item>
  </vk-breadcrumb>
</template>

<script lang="js">
import { Breadcrumb as VkBreadcrumb,
         BreadcrumbItem as VkBreadcrumbItem } from 'vuikit/lib/breadcrumb';
export default {
  name: 'Breadcrumb',
  props: {
    items: {
      type: Array,
      default: () => []
    }
  },
  components: { VkBreadcrumb, VkBreadcrumbItem },
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
