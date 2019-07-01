<template lang="html">
  <vk-modal :class=classes v-if="mode === 'modal'" :show.sync=show >
    <vk-close @click=hideModal />
    <vk-title>{{ op }}<template v-if="arg">: {{ arg.title }}</template>
      <template v-else> {{ model ? model.plural : '' }}</template></vk-title>
    <template v-if="arg">
      <div class="description uk-margin">{{ arg.description }}</div>
      <div class="info"><strong>version: </strong>{{ arg.available }}</div>
      <div v-if="arg.installed" class="info">
        <strong>current: </strong>{{ arg.version }}</div>
    </template>
    <template v-else>
      <vk-table responsive hoverable striped 
                :divided=false
                :data=operands >
        <vk-column :title="model ? model.singular : 'object'" cell="title" />
        <vk-column title="installed" cell="version" />
        <vk-column title="available" cell="available" />
      </vk-table>
    </template>
    <div class="modal-actions">
      <vk-btn class="btn-cancel" type="link" size="small"
              @click.prevent=hideModal >cancel</vk-btn>
      <vk-btn class="btn-ok" type="primary" size="small"
              @clitk.prevent=execute >{{ op }}</vk-btn>
    </div>
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
  ModalTitle as VkTitle
} from 'vuikit/lib/modal'
import {
  Table as VkTable,
  TableColumn as VkColumn,
  TableColumnSelect as VkColSelect
} from 'vuikit/lib/table'
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
    VkTitle,
    VkTable,
    VkColumn,
    VkColSelect,
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
.installer {
  &.widget {
    color: grey;
  }
}
</style>
