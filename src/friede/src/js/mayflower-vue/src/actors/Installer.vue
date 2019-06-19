<template lang="html">
  <vk-modal class="installer" v-if="mode === 'modal'">
  </vk-modal>
</template>

<script lang="js">
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
