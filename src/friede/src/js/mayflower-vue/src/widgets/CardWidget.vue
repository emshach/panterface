<template lang="html">
  <vk-card :type=type :padding=padding :hover=context.hover
           class="widget card-widget">
    <template #header>
      <slot name="header" :object=object >
        <div v-if=object.model class="model-name">{{ object.model }}</div>
      </slot>
    </template>
    <div class="card-bg">
      <slot name="background" :object=object>
        <mf-icon v-if=modelIcon :icon=modelIcon mode="bg" />
      </slot>
    </div>
    <div class="title-actions uk-align-right">
      <slot name="title-actions" :object=object />
      <close-button @click.prevent=close v-if=context.closeable />
    </div>
    <template #badge>
      <slot name="badge" :object=object />
    </template>
    <template #media>
      <slot name="media" :object=object />
    </template>
    <template #media-top>
      <slot name="media-top" :object=object />
    </template>
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
    <div v-if=hasContentActions class="item-actions">
      <slot name="content-actions" :object=object />
    </div>
    <template #media-bottom>
      <slot name="media-bottom" :object=object />
    </template>
    <template #footer>
      <div v-if=hasFooterActions class="item-actions">
        <slot name="footer-actions" :object=object />
      </div>
      <slot name="footer" :object=object />
    </template>
  </vk-card>
</template>

<script lang="js">
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
import { Card as VkCard, CardTitle as VkCardTitle } from 'vuikit/lib/card'
import { CloseButton } from '@/components'
export default {
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
    if ( this.object && this.object.model )
      this.$store.dispatch( 'getModel', this.object.model );
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
    },
    modelObj() {
      if ( this.object && this.object.model )
        return this.$store.state.models[ this.object.model ];
      return null;
    },
    modelIcon() {
      if ( this.modelObj )
        return this.modelObj.icon;
      return '';
    },
    hasContentActions() {
      return !!this.$slots[ 'content-actions' ]
    },
    hasFooterActions() {
      return !!this.$slots[ 'footer-actions' ]
    }
  }
}
</script>

<style lang="scss">
.card-widget {
  position: relative;
  > .uk-card-header {
    padding: 0;
    border-bottom: 0 none;
    + .uk-card-body {
      padding-top: 4px;
    }
  }
  > .uk-card-body {
    /* height: 100%; */
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    border: 1px solid rgba(255,255,255,0.25);
    border-left-color: rgba(255,255,255,0.1);
    border-right-color: rgba(255,255,255,0.15);
    .content {
      flex: 1;
    }
  }
  > .uk-card-footer {
    padding: 0;
    border-top: 0 none;
  }
  .model-name {
    padding: 4px;
    color: cadetblue;
  }
}
</style>
