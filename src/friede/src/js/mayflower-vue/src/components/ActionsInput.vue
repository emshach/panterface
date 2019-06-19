<template lang="html">
  <div class="actions-input">
    <vk-btn type="light" href="#" class="dropdown-trigger">
      <font-awesome-icon icon="walking" class="btn-icon" />actions
      {{ count ? '(' + count + ' object' + ( count == 1 ? '' : 's' ) + ')' : '' }}
    </vk-btn>
    <vk-dropdown>
      <vk-nav>
        <vk-nav-item v-for="action in actions" :key=action :title=action
                     @click.prevent="input( action )" />
        <vk-divider v-if=total />
        <vk-nav-item v-if="countV < visible"
          title="select all visible" @click.prevent="input( 'select', 'filtered' )" />
        <vk-nav-item v-if="count < total"
          title="select all" @click.prevent="input( 'select', 'all' )" />
        <vk-nav-item v-if=count
          title="clear selected" @click.prevent="input( 'select', 'none' )" />
      </vk-nav>
    </vk-dropdown>
    </select>
  </div>
</template>

<script lang="js">
import { ButtonLink as VkBtn } from 'vuikit/lib/button'
import { Dropdown as VkDropdown } from 'vuikit/lib/dropdown'
import {
  NavDropdown as VkNav,
  NavItemDivider as VkDivider,
  NavItem as VkNavItem,
} from 'vuikit/lib/nav'
import { faWalking } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add( faWalking );
VkBtn.props.type.validator = val =>
   !val || /^(light|primary|secondary|danger|text|link)$/.test( val );

export default {
  name: 'ActionsInput',
  components: {
    VkBtn,
    VkDropdown,
    VkNav,
    VkDivider,
    VkNavItem,
    FontAwesomeIcon,
  },
  props: {
    actions: {
      type: Array,
      default: () => []
      // TODO: get fride action objects
    },
    operands: {
      type: Array,
      default: () => []
    },
    count: {
      type: Number,
      default: 0
    },
    countV: {
      type: Number,
      default: 0
    },
    visible: {
      type: Number,
      default: 0
    },
    total: {
      type: Number,
      default: 0
    }
  },
  mounted() {
  },
  data() {
    return {
    }
  },
  methods: {
    input( action ) {
      this.$emit( 'input', action );
    }
  },
  computed: {}
}
</script>

<style scoped lang="scss">
.actions-input {
  flex-wrap: nowrap;
  flex-shrink: 0;
  height: 40px;
  .dropdown-trigger {
    padding: 0;
  }
}
</style>
