<template lang="html">
  <vk-modal :class=classes v-if="mode === 'modal'" :show=show @shown=autoExecute >
    <vk-close @click=hideModal />
    <vk-title>{{ action }}<template v-if="arg">: {{ arg.title }}</template>
      <template v-else> {{ model ? model.plural : '' }}</template>
    </vk-title>
    <label v-if="action === 'install' || action === 'reinstall'">
      <input class="uk-checkbox" type="checkbox" v-model=install_userdata >
      Install user-data
    </label>
    <template v-if="arg">
      <div class="description uk-margin">{{ arg.description }}</div>
      <div class="info"><strong>version: </strong>{{ arg.available }}</div>
      <div v-if="arg.installed" class="info">
        <strong>current: </strong>{{ arg.version }}</div>
    </template>
    <template v-else>
      <vk-table responsive hoverable striped
                :row-class=showApplicable
                :divided=false
                :data=operands >
        <vk-column :title="model ? model.singular : 'object'" cell="title" />
        <vk-column title="installed" cell="version" >
          <template #default="{ cell, row }">
            {{ row.installed ? cell : 'no' }}
          </template>
        </vk-column>
        <vk-column title="available" cell="available" />
      </vk-table>
    </template>
    <action-result v-if="results" :action="actions[ action ]"
                   :objects=objects :results=results />
    <div :class="[ 'loading', loading ? 'active' : '' ]">
      <div class="label">{{ action.replace( /e$/,'' ) + 'ing' }}</div>
      <bar-loader :width=100 widthUnit="%" :height=1 :size=50 sizeUnit="%"
                  :loading=loading color="#39f" class="spinner" />
    </div>
    <div class="modal-actions">
      <vk-btn v-if="!results || next" class="btn-cancel" type="link"
              size="small" :disabled=loading
              @click.prevent=hideModal >cancel</vk-btn>
      <template v-if="results">
        <vk-btn v-if="next" class="btn-ok" type="primary" size="small"
                :disabled=loading @click.prevent=doNext >{{ next }}</vk-btn>
        <vk-btn v-else class="btn-ok" type="primary" size="small"
                :disabled=loading @click.prevent=hideModal >Done</vk-btn>
      </template>
      <vk-btn v-else class="btn-ok" type="primary" size="small"
              :disabled=loading @click.prevent=execute >{{ action }}</vk-btn>
    </div>
  </vk-modal>
  <div v-else-if="mode === 'widget'" class="installer widget">
    <template v-if=object.installed >
      <vk-btn-link v-if="object.version !== object.available && can.update"
                   v-vk-tooltip.bottom="'update'"
                   type="text" @click.prevent="act( 'update', object )" >
        v{{ object.version }} installed
        <font-awesome-icon icon="level-up-alt" />
      </vk-btn-link>
      <span v-else>v{{ object.version }} installed</span>
      <vk-btn-link v-if="can.uninstall && !object.required"
                   v-vk-tooltip.bottom="'uninstall'"
                   type="text" @click.prevent="act( 'uninstall', object )" >
        <font-awesome-icon icon="trash" />
      </vk-btn-link>
    </template>
    <vk-btn-link v-else-if="can.install"
                 v-vk-tooltip.bottom="'install'"
                 type="text" @click.prevent="act( 'install', object )" >
      <font-awesome-icon icon="download" />
    </vk-btn-link>
  </div>
  <div v-else />
</template>

<script lang="js">
import { Button as VkBtn, ButtonLink as VkBtnLink } from 'vuikit/lib/button'
import { faLevelUpAlt, faDownload, faTrash } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { BarLoader } from '@saeris/vue-spinners'
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
import { ActionResult } from '@/components'

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
    ActionResult,
    BarLoader,
  },
  data() {
    return {
      classes: { installer: true },
      verify: {
        install:   x => !x.installed,
        reinstall: x => x.installed,
        uninstall: x => x.installed && !x.required,
        update:    x => x.installed && x.version !== x.available
      },
      install_userdata: true
    }
  },
}
</script>

<style lang="scss">
.installer {
  &.widget {
    color: grey;
  }
}
</style>
