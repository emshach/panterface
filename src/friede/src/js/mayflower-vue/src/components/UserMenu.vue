<template lang="html">
  <vk-dropdown>
    <vk-nav>
      <form v-if="editUsername" class="uk-form-stacked uk-text-left"
            @submit.prevent="submitUsername">
        <div class="first-name">
          <label class="uk-form-label">first name</label>
          <div class="uk-form-controls">
            <input class="uk-input" type="text" />
          </div>
        </div>
        <div class="last-name">
          <label class="uk-form-label">last name</label>
          <div class="uk-form-controls">
            <input class="uk-input" type="text" />
          </div>
        </div>
        <vk-btn html-type="submit">done</vk-btn>
      </form>
      <div v-else class="username">{{ user.fname}} {{ user.lname }}
        <a href="#" @click.prevent="editUsername=true">
          <font-awesome-icon icon="user-edit" />
        </a>
      </div>
      <template v-if="user.uid && !user.anonymous">
        <vk-nav-item href="logout" title="logout" />
      </template>
      <template v-else>
        <vk-nav-item href="login" title="login" />
        <vk-nav-item href="sign up" title="sign up" />
      </template>
    </vk-nav>
  </vk-dropdown>
</template>

<script lang="js">
import { Button as VkBtn, ButtonLink as VkBtnLink } from 'vuikit/lib/button'
import { Dropdown as VkDropdown } from 'vuikit/lib/dropdown'
import {
  NavDropdown as VkNav,
  NavItem as VkNavItem,
  NavItemParent as VkNavParent,
} from 'vuikit/lib/nav'
export default  {
  name: 'UserMenu',
  components: {
    VkBtn,
    VkBtnLink,
    VkDropdown,
    VkNav,
    VkNavItem,
    VkNavParent,
  },
  props: {
    user: {
      type: Object,
      default: () => ({})
    }
  },
  mounted() {
    
  },
  data() {
    return {
      editUsername: false
    }
  },
  methods: {
    submitUsername() {
      this.editUsername = false;
    }
  },
  computed: {
    
  }
}
</script>

<style lang="scss">
.user-menu {
  .username {
  }
}
</style>
