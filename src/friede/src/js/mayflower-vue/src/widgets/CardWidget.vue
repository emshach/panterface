<template lang="html">
  <vk-card :type="type" :padding="padding" :hover="context.hover"
           class="widget">
    <close-button @click.prevent="close" v-if="context.closeable" />
    <slot #header name="header" />
    <slot #badge name="badge" />
    <slot #media name="media" />
    <slot #media-top name="media-top" />
    <vk-card-title><slot name="title" /></vk-card-title>
    <p class="uk-text-meta uk-margin-remove-top"><slot name="subtitle" /></p>
    <slot name="content" />
    <slot #media-bottom name="media-bottom" />
    <slot #footer name="footer" />
  </vk-card>
</template>

<script lang="js">
import { Card as VkCard, CardTitle as VkCardTitle } from 'vuikit/lib/card'
import { CloseButton } from '@/components'
export default  {
  name: 'CardWidget',
  props: {
    cardType: {
      type: Boolean,
      default: 'default'
    },
    context: {
      type: Object,
      default: () => []
    }
  },
  components: { VkCard, VkCardTitle, Closebutton },
  mounted() {
    
  },
  data() {
    return {
      
    }
  },
  methods: {
    
  },
  computed: {
    isInline() {
      return true
    },
    type() {
      return this.isInline() ? 'blank' : this.cardType
    },
    padding() {
      return this.isInline() ? '' : 'small'
    }
  }
}
</script>

<style scoped lang="scss">
  .card-widget {

  }
</style>
