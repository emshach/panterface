<template lang="html">
  <vk-dropdown class="user-menu">
    <vk-nav>
      <div class="user-info">
        <form v-if="editUser" class="uk-form-stacked uk-text-left"
              @submit.prevent="submitUser" @reset.prevent="resetUser">
          <div class="first-name field">
            <label>first name</label>
            <div class="uk-form-controls">
              <input class="uk-input" type="text" v-model="fname" />
            </div>
          </div>
          <div class="last-name field">
            <label>last name</label>
            <div class="uk-form-controls">
              <input class="uk-input" type="text" v-model="lname" />
            </div>
          </div>
          <div class="username field">
            <label>username</label>
            <div class="uk-form-controls">
              <input class="uk-input" type="text" v-model="username" />
            </div>
          </div>
          <div class="email field">
            <label>email addres</label>
            <div class="uk-form-controls">
              <input class="uk-input" type="text" v-model="email" />
            </div>
          </div>
          <vk-btn class="btn-ok"
                  html-type="submit" type="primary" size="small">done</vk-btn>
          <vk-btn class="btn-cancel"
                  html-type="reset" type="link" size="small">cancel</vk-btn>
        </form>
        <template v-else>
          <div class="user-title">{{ user.fname}} {{ user.lname }}
            <a href="#" title="change name" @click.prevent="editUser=true">
              <font-awesome-icon icon="user-edit" />
            </a>
          </div>
          <div class="user-subtitle">
            <div>@{{ user.username }}</div>
            <div>{{ user.email }}</div>
          </div>
        </template>
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
    this.resetUser();
  },
  data() {
    return {
      editUser: false,
      fname: '',
      lname: '',
      username: '',
      email: '',
    }
  },
  methods: {
    submitUser() {
      this.user.fname = this.fname;
      this.user.lname = this.lname;
      this.user.username = this.username;
      this.user.email = this.email;
      this.editUser = false;
    },
    resetUser() {
      this.fname = this.user.fname;
      this.lname = this.user.lname;
      this.username = this.user.username;
      this.email = this.user.email;
      this.editUser = false;
    }
  },
  computed: {
    
  }
}
</script>

<style lang="scss">
.user-menu {
  .user-title {
    font-weight: bold;
    a {
      padding-left: 10px;
    }
  }
  .user-info {
    margin-top: -4px;
    padding: 12px;
    background: rgba(220,230,255,1);
    border-bottom: 1px solid rgba(0,0,0,0.05);
    color: steelblue;
    .btn-ok, .btn-cancel {
      display: block;
      width: 100%;
      margin-bottom: 4px;
    }
    .field {
      margin-bottom: 8px;
    }
  }
}
</style>
