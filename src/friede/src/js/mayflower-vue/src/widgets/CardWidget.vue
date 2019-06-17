<template lang="html">
  <vk-card :type=type :padding=padding :hover=context.hover
           class="widget">
    <close-button @click.prevent=close v-if=context.closeable />
    <slot #header name="header" :object=object />
    <slot #badge name="badge" :object=object />
    <slot #media name="media" :object=object />
    <slot #media-top name="media-top" :object=object />
    <vk-card-title><slot name="title" :object=object /></vk-card-title>
    <p class="uk-text-meta uk-margin-remove-top">
      <slot name="subtitle" :object=object />
    </p>
    <slot name="content" :object=object />
    <slot #media-bottom name="media-bottom" :object=object />
    <slot #footer name="footer" :object=object />
  </vk-card>
</template>

<script lang="js">
import { Card as VkCard, CardTitle as VkCardTitle } from 'vuikit/lib/card'
import { CloseButton } from '@/components'
export default  {
  name: 'CardWidget',
  components: { VkCard, VkCardTitle, CloseButton },
  props: {
    object: {
      type: Object,
      required: true
    },
    cardType: {
      type: String,
      default: 'default'
    },
    context: {
      type: Object,
      default: () => ({})
    },
    layout: {
      type: Object,
      default: () => ({})
    },
    inline: {
      type: Boolean,
      default: true
    }
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
    type() {
      return this.inline ? 'blank' : this.cardType
    },
    padding() {
      return this.inline ? '' : 'small'
    }
  }
}
</script>

<style scoped lang="scss">
  .card-widget {

  }
</style>
