<template lang="html">
  <vk-modal class="activator" v-if="mode === 'modal'" :show.sync=show >
    <vk-close @click="show = false" />
  </vk-modal>
  <div v-else class="activator widget">
    <template v-if=object.installed >
      <template v-if=object.required >
        <font-awesome-icon v-if=object.active
                           icon="toggle-on" v-vk-tooltip.bottom="'required'"
                           class="icon activator-enabled" />
        <vk-btn-link v-else v-vk-tooltip.bottom="'activate'"
                     type="text" class="activator-disabled danger"
                     @click.prevent="act( object, 'enable' )" >
          <font-awesome-icon icon="toggle-off" />
        </vk-btn-link>
      </template>
      <vk-btn-link v-else-if=object.active v-vk-tooltip.bottom="'disable'"
                   type="text" class="activator-enabled"
                   @click.prevent="act( object, 'disable' )" >
        <font-awesome-icon icon="toggle-on" />
      </vk-btn-link>
      <vk-btn-link v-else v-vk-tooltip.bottom="'disable'"
                   type="text" class="activator-disabled"
                   @click.prevent="act( object, 'enable' )" >
        <font-awesome-icon icon="toggle-off" />
      </vk-btn-link>
    </template>
  </div>
</template>

<script lang="js">
import { Button as VkBtn, ButtonLink as VkBtnLink } from 'vuikit/lib/button'
import { faToggleOn, faToggleOff } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add( faToggleOn, faToggleOff );
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
.activator {
  &.widget {
    float: left;
    .activator-enabled {
      color: cornflowerblue;
    }
    .activator-disabled {
      color: grey;
      &.danger {
        color: darkred;
      }
    }
    .uk-button, .icon {
      padding: 0 6px;
    }
  }
}
</style>
