<template lang="html">
  <vk-modal :class=classes v-if="mode === 'modal'" :show.sync=show >
    <vk-close @click=hideModal />
    <action-result v-if="results" :action="actions[ action ]"
                   :objects=objects :results=results />
    <div class="modal-actions">
      <vk-btn class="btn-cancel" type="link" size="small"
              @click.prevent=hideModal >cancel</vk-btn>
      <vk-btn class="btn-ok" type="primary" size="small"
              @click.prevent=execute >{{ action }}</vk-btn>
    </div>
  </vk-modal>
  <div v-else class="activator widget">
    <template v-if=object.installed >
      <template v-if=object.required >
        <font-awesome-icon v-if=object.active
                           icon="toggle-on" v-vk-tooltip.bottom="'required'"
                           class="icon activator-enabled" />
        <vk-btn-link v-else-if="can.activate"
                     v-vk-tooltip.bottom="'activate'"
                     type="text" class="activator-disabled danger"
                     @click.prevent="act( 'activate', object )" >
          <font-awesome-icon icon="toggle-off" />
        </vk-btn-link>
        <font-awesome-icon v-else
                           icon="toggle-off" v-vk-tooltip.bottom="'required'"
                           class="icon activator-disabled danger" />
      </template>
      <template v-else-if="can.activate">
        <vk-btn-link v-if=object.active v-vk-tooltip.bottom="'disable'"
                     type="text" class="activator-enabled"
                     @click.prevent="act( 'deactivate', object )" >
          <font-awesome-icon icon="toggle-on" />
        </vk-btn-link>
        <vk-btn-link v-else v-vk-tooltip.bottom="'activate'"
                     type="text" class="activator-disabled"
                     @click.prevent="act( 'activate', object )" >
          <font-awesome-icon icon="toggle-off" />
        </vk-btn-link>
      </template>
      <template v-else>
        <font-awesome-icon v-if=object.active
                           icon="toggle-on" v-vk-tooltip.bottom="'active'"
                           class="icon activator-enabled" />
        <font-awesome-icon v-else
                           icon="toggle-off" v-vk-tooltip.bottom="'disabled'"
                           class="icon activator-disabled" />
      </template>
    </template>
  </div>
</template>

<script lang="js">
import { Button as VkBtn, ButtonLink as VkBtnLink } from 'vuikit/lib/button'
import { faToggleOn, faToggleOff } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  Modal as VkModal,
  ModalClose as VkClose,
  ModalTitle as VkModaTitle
} from 'vuikit/lib/modal'
import { ActorsMixin } from '@/lib/mixins'

library.add( faToggleOn, faToggleOff );

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
    return {
      classes: { installer: true }
    }
  },
  methods: {},
  computed: {}
}
</script>

<style lang="scss">
.activator {
  &.widget {
    .activator-enabled {
      color: cornflowerblue;
    }
    .activator-disabled {
      color: grey;
      &.danger {
        color: darkred;
      }
    }
  }
}
</style>
