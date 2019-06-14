<template lang="html">
  <vk-dropdown class="user-menu">
    <vk-nav>
      <div class="user-info">
        <form v-if="editUser" class="uk-form-stacked uk-text-left"
              @submit.prevent="submitUser">
          <div class="first-name uk-margin">
            <label>first name</label>
            <div class="uk-form-controls">
              <input class="uk-input" type="text" v-model="user.fname" />
            </div>
          </div>
          <div class="last-name uk-margin">
            <label>last name</label>
            <div class="uk-form-controls">
              <input class="uk-input" type="text" v-model="user.lname" />
            </div>
          </div>
          <vk-btn class="btn-ok"
                  html-type="submit" type="primary" size="small">done</vk-btn>
        </form>
        <div v-else class="username">{{ user.fname}} {{ user.lname }}
          <a href="#" title="change name" @click.prevent="editUser=true">
            <font-awesome-icon icon="user-edit" />
          </a>
        </div>
      </div>
      <vk-divider />
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
  NavItemDivider as VkDivider,
  NavItemParent as VkNavParent,
} from 'vuikit/lib/nav'
export default  {
  name: 'UserMenu',
  components: {
    VkBtn,
    VkBtnLink,
    VkDropdown,
    VkNav,
    VkDivider,
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
      editUser: false
    }
  },
  methods: {
    submitUser() {
      this.editUser = false;
    }
  },
  computed: {
    
  }
}
</script>

<style lang="scss">
.user-menu {
  .username {
    font-weight: bold;
    color: steelblue;
    a {
      padding-left: 10px;
    }
  }
  .user-info {
    margin-top: -4px;
    padding: 12px;
    background: rgba(220,230,255,1);
    .btn-ok {
      width: 100%;
    }
  }
}
</style>
