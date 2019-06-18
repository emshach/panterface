<template lang="html">
  <div class="actions-input">
    <vk-btn type="light" href="#" class="dropdown-trigger">
      <font-awesome-icon icon="walking" class="btn-icon" />actions
    </vk-btn>
    <vk-dropdown>
      <vk-nav>
        <vk-nav-item v-for="action in actions" :key=action :title=action
                     @click="input(action)" />
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
  NavItem as VkNavItem,
} from 'vuikit/lib/nav'
import { faWalking } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add( faWalking )

export default {
  name: 'ActionsInput',
  components: {
    VkBtn,
    VkDropdown,
    VkNav,
    VkNavItem,
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
