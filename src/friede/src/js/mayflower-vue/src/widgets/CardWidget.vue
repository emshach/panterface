<template lang="html">
  <vk-card :type=type :padding=padding :hover=context.hover
           class="widget card-widget">
      <div class="title-actions uk-align-right">
        <slot name="title-actions" :object=object />
        <close-button @click.prevent=close v-if=context.closeable />
      </div>
    <slot #header name="header" :object=object />
    <slot #badge name="badge" :object=object />
    <slot #media name="media" :object=object />
    <slot #media-top name="media-top" :object=object />
    <vk-card-title>
      <slot name="title" :object=object />
    </vk-card-title>
    <p class="uk-text-meta card-subtitle">
      <slot name="subtitle" :object=object />
    </p>
    <div class="content">
      <vue-perfect-scrollbar>
        <slot name="content" :object=object />
      </vue-perfect-scrollbar>
    </div>
    <div class="item-actions">
      <slot name="content-actions" :object=object />
    </div>
    <slot #media-bottom name="media-bottom" :object=object />
    <slot #footer name="footer" :object=object />
  </vk-card>
</template>

<script lang="js">
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
import { Card as VkCard, CardTitle as VkCardTitle } from 'vuikit/lib/card'
import { CloseButton } from '@/components'
export default  {
  name: 'CardWidget',
  components: {
    VuePerfectScrollbar,
    VkCard,
    VkCardTitle,
    CloseButton
  },
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

<style lang="scss">
.card-widget {
  position: relative;
  .uk-card-body {
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    .content {
      flex: 1;
    }
  }
}
</style>
