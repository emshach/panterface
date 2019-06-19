<template lang="html">
  <vk-modal class="activator" v-if="mode === 'modal'" :show-sync=show >
    <vk-close @click="show = false"></vk-close>
  </vk-modal>
  <div v-else></div>
</template>

<script lang="js">
import {
  Modal as VkModal,
  ModalClose as VkClose,
  ModalTitle as VkModaTitle
} from 'vuikit/lib/modal'
import { ActorsMixin } from '@/lib/mixins'

export default {
  name: 'Activator',
  mixins: [ ActorsMixin ],
  components: {
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
.activator {
  
}
</style>
