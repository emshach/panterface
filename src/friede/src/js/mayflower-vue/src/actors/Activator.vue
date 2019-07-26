<template lang="html">
  <vk-modal :class=classes v-if="mode === 'modal'" :show=show @shown=autoExecute >
    <vk-close @click=hideModal />
    <vk-title>{{ action }}<template v-if="arg">: {{ arg.title }}</template>
      <template v-else> {{ model ? model.plural : '' }}</template>
    </vk-title>
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
        <vk-column title="version" cell="version" />
        <vk-column title="active" cell="active" >
          <template #default="{ cell, row }">
            {{ cell ? 'yes' : 'no' }}
          </template>
        </vk-column>
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
import { BarLoader } from '@saeris/vue-spinners'
import {
  Modal as VkModal,
  ModalClose as VkClose,
  ModalTitle as VkModaTitle
} from 'vuikit/lib/modal'
import {
  Table as VkTable,
  TableColumn as VkColumn,
  TableColumnSelect as VkColSelect
} from 'vuikit/lib/table'
import { ActionResult } from '@/components'
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
    VkTable,
    VkColumn,
    VkColSelect,
    FontAwesomeIcon,
    ActionResult,
    BarLoader,
  },
  data() {
    return {
      classes: { activator: true },
      verify: {
        activate:   x => !x.active,
        deactivate: x => x.active,
      }
    }
  },
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
