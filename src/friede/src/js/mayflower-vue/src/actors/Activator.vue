<template lang="html">
  <vk-modal class="activator" v-if="mode === 'modal'">
  </vk-modal>
</template>

<script lang="js">
import {
  Modal as VkModal,
  ModalClose as VkClose,
  ModalTitle as VkModaTitle
} from 'vuikit/lib/modal'
import { ActionsMixin } from '@/lib/mixins'

export default {
  name: 'Activator',
  mixins: [ ActionsMixin ],
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
