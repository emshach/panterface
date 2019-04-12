<template lang="html">
  <vk-card :type="type" :padding="padding" :hover="context.hover"
           class="widget adaptive-widget">
    <close-button @click.prevent="close" v-if="context.closeable" />
    <div #header><slot name="header" /></div>
    <div #badge><slot name="badge" /></div>
    <div #media><slot name="media" /></div>
    <div #media-top><slot name="media-top" /></div>
    <vk-card-title><slot name="title" /></vk-card-title>
    <p class="uk-text-meta uk-margin-remove-top"><slot name="subtitle" /></p>
    <slot name="content" />
    <div #media-bottom><slot name="media-bottom" /></div>
    <div #footer><slot name="footer" /></div>
  </vk-card>
</template>

<script lang="js">
import { Card, CardTitle } from 'vuikit/lib/card'
import CloseButton from '@/src/components/CloseButton.vue'
export default  {
  name: 'adaptive-widget',
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
  components: {
    'vk-card': Card,
    'vk-card-title': CardTitle,
    Closebutton
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
  .adaptive-widget {

  }
</style>
