<template lang="html">
  <vk-breadcrumb class="breadcrumb">
    <vk-breadcrumb-item
      v-for="( item, index ) in items"
      :key="index"
      :href="item.href"
      :target="item.target">{{ label( item )}}</vk-breadcrumb-item>
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
    return {}
  },
  methods: {
    label( item ) {
      if ( 'label' in item )
        return item.label;
      return item.title
    }
  },
  computed: {
  }
}
</script>

<style scoped lang="scss">
  .breadcrumb {

  }
</style>
