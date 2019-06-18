<template lang="html">
  <div class="actions-input">
    <a href="#" class="dropdown-trigger">
      <font-awesome-icon :icon="walking" />actions
    </a>
    <vk-dropdown>
      <vk-nav>
        <vk-nav-item v-for"action in actions" :key=action @click="input(action)">
          {{ action }}
        </vk-nav-item>
      </vk-nav>
    </vk-dropdown>
    </select>
  </div>
</template>

<script lang="js">
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

  }
</style>
