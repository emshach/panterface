<template lang="html">
  <vk-dropdown class="user-menu" animation="slide-top-small"
               :delay-hide=3000 :offset=0 >
    <vk-nav>
      <div class="user-info">
        <form v-if="editUser || loginUser || registerUser"
              class="uk-form-stacked uk-text-left"
              @submit.prevent=submitUser @reset.prevent=resetUser >
          <div v-if="error" class="uk-text-danger uk-text-small" v-html=error />
          <template v-if="!loginUser">
            <div class="first-name field">
              <label>first name (or last name required)</label>
              <div class="uk-form-controls">
                <input class="uk-input" type="text" v-model=fname />
              </div>
            </div>
            <div class="last-name field">
              <label>last name</label>
              <div class="uk-form-controls">
                <input class="uk-input" type="text" v-model=lname />
              </div>
            </div>
          </template>
          <div class="username field">
            <label>username (or email required)</label>
            <div class="uk-form-controls">
              <input class="uk-input" type="text" v-model=username />
            </div>
          </div>
          <div class="email field">
            <label>email address (recommended)</label>
            <div class="uk-form-controls">
              <input class="uk-input" type="text" v-model=email />
            </div>
          </div>
          <div class="phone field">
            <label>phone number</label>
            <div class="uk-form-controls">
              <input class="uk-input" type="text" v-model=phone />
            </div>
          </div>
          <vk-btn v-if="editUser" type="link" class="change-password">
            change password</vk-btn>
          <div v-else class="password field">
            <label>password</label>
            <div class="uk-form-controls">
              <input class="uk-input" type="password" v-model=password />
            </div>
          </div>
          <vk-btn class="btn-cancel"
                  html-type="reset" type="link" size="small">cancel</vk-btn>
          <vk-btn class="btn-ok"
                  html-type="submit" type="primary" size="small">{{
              loginUser ? 'login' : registerUser ? 'sign up' : 'done'
            }}</vk-btn>
        </form>
        <template v-else>
          <div class="user-title">{{ user.first_name}} {{ user.last_name }}
            <a href="#" title="edit info"
               @click.prevent="editUser = true">
              <font-awesome-icon icon="user-edit" />
            </a>
          </div>
          <div class="user-subtitle">
            <div>@{{ user.username }}</div>
            <div>{{ user.email }}</div>
          </div>
        </template>
      </div>
      <template v-if="user.id && !user.anonymous">
        <vk-nav-item>
          <router-link
            v-for="( link, key ) in userLinks" :key=key
            :to=link.entry.location.href >{{
              link.entry.title || link.entry.location.title
            }}</router-link>
        </vk-nav-item>
        <vk-nav-item href="logout" title="logout" @click.prevent="logout" />
      </template>
      <template v-else>
        <vk-nav-item href="login" title="login"
                     @click.prevent="loginUser = true" />
        <vk-nav-item href="sign up" title="sign up"
                     @click.prevent="registerUser = true" />
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
      loginUser: false,
      registerUser: false,
      changePassword: false,
      username: '',
      fname: '',
      lname: '',
      email: '',
      phone: '',
      password: '',
      error: ''
    }
  },
  methods: {
    submitUser() {
      if ( this.loginUser ) {
        this.$api.post( 'login', {
          username: this.username,
          email: this.email,
          phone: this.phone,
          password: this.password
        }).then( r => {
          this.$store.commit( 'setUser', r.data.user );
          this.resetUser();
        }).catch( e => {
          if ( e.response )
            this.error = e.response.data.error;
        });
      } else if ( this.registerUser ) {
        this.$api.post( 'register', {
          username: this.username,
          email: this.email,
          phone: this.phone,
          password: this.password,
          fname: this.fname,
          lname: this.lname,
        }).then( r => {
          this.$store.commit( 'setUser', r.data.user );
          this.resetUser();
        }).catch( e => {
          if ( e.response )
            this.error = e.response.data.error;
        });
      } else {
        this.$api.post( 'aries', 'users', this.user.id, {
          username: this.username,
          fname: this.fname,
          lname: this.lname,
          email: this.email,
          phone: this.phone,
        }).then( r => {
          this.$store.commit( 'setUser', r.data.user );
          this.resetUser();
        }).catch( e => {
          if ( e.response )
            this.error = e.response.data.error;
        });
      }
    },
    resetUser() {
      this.username = this.user.username;
      this.fname = this.user.first_name;
      this.lname = this.user.last_name;
      this.email = this.user.email;
      this.phone = this.user.phone;
      this.editUser = false;
      this.loginUser = false;   // 
      this.registerUser = false;
      this.error = '';
      this.$security.refresh();
    },
    logout() {
      this.$api( 'logout' ).then( r => {
        this.$store.commit( 'setUser', r.data.user );
        this.resetUser();
      }).catch( e => {
        if ( e.response )
          this.error = e.response.data.error;
      });
    }
  },
  computed: {
    userLinks() {
      if ( !this.menus || !this.menus.active )
        return
      const links = this.menus.containers.user_shortcuts.entry.links;
      const out = {};
      Object.keys( links ).forEach( l => {
        if ( links[l].active && links[l].entry.active
             && links[l].entry.location && links[l].entry.location.active
             && links[l].entry.location.href )
          out[l] = links[l];
      });
      return out;
    },
  }
}
</script>

<style lang="scss">
.user-menu {
  min-width: 256px;
  .user-title {
    font-weight: bold;
    font-size: 1.2em;
    a {
      padding-left: 10px;
    }
  }
  .user-subtitle {
    font-size: 0.9em;
  }
  .note {
    margin-top: 2px;
  }
  .user-info {
    margin-top: -4px;
    padding: 12px;
    background: rgba(220,230,255,1);
    border-bottom: 1px solid rgba(0,0,0,0.05);
    color: steelblue;
    .change-password {
      display: block;
      margin: 8px 0;
    }
    .btn-ok, .btn-cancel {
      display: inline-block;
      width: 40%;
    }
    .btn-ok {
      width: 60%;
    }
    .field {
      margin-bottom: 8px;
    }
  }
}
</style>
