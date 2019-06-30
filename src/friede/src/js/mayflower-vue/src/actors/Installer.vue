<template lang="html">
  <vk-modal class="installer" v-if="mode === 'modal'" :show.sync=show >
    <vk-close @click="hideModal" />
    <vk-modal-title>{{ op }}
      <template v-if="operands.length == 1"> {{ operands[0].title }}</template>
    </vk-modal-title>
  </vk-modal>
  <div v-else class="installer widget">
    <template v-if=object.installed >
      <vk-btn-link v-if="object.version !== object.available"
                   v-vk-tooltip.bottom="'update'"
                   type="text" @click.prevent="act( 'update', object )" >
        v{{ object.version }} installed
        <font-awesome-icon icon="level-up-alt" />
      </vk-btn-link>
      <span v-else>v{{ object.version }} installed</span>
      <vk-btn-link v-if="!object.required" v-vk-tooltip.bottom="'uninstall'"
                   type="text" @click.prevent="act( 'uninstall', object )" >
        <font-awesome-icon icon="trash" />
      </vk-btn-link>
    </template>
    <vk-btn-link v-else v-vk-tooltip.bottom="'install'"
                 type="text" @click.prevent="act( 'install', object )" >
      <font-awesome-icon icon="download" />
    </vk-btn-link>
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
import { faLevelUpAlt, faDownload, faTrash } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add( faLevelUpAlt, faDownload, faTrash );

export default {
  name: 'Installer',
  mixins: [ ActorsMixin ],
  components: {
    VkBtn,
    VkBtnLink,
    VkModal,
    VkClose,
    VkModaTitle,
    FontAwesomeIcon,
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
  &.widget {
    color: grey;
  }
}
</style>
