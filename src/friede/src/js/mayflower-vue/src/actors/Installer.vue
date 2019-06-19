<template lang="html">
  <vk-modal class="installer" v-if="mode === 'modal'" :show-sync=show >
    <vk-modal-close @click="show = false"></vk-modal-close>
  </vk-modal>
  <div v-else>
    <vk-button-link v-if=object.installed @click.prevent="act( object )">
      v{{ object.version }} installed
    </vk-button-link>
  </div>
</template>

<script lang="js">
import { Button as VkBtn, ButtonLink as VkBtnLink } from 'vuikit/lib/button'
import {
  Modal as VkModal,
  ModalClose as VkClose,
  ModalTitle as VkModaTitle
} from 'vuikit/lib/modal'
import { ActorsMixin } from '@/lib/mixins'

export default {
  name: 'Installer',
  mixins: [ ActorsMixin ],
  components: {
    VkButton,
    VkButtonLink,
    VkTooltip,
    VkModal,
    VkClose,
    VkModaTitle
  },
  props: [],
  mounted() {},
  data() {
    return {}
  },
  methods: {},
  computed: {}
}
</script>

<style lang="scss">
.installer {
  
}
</style>
