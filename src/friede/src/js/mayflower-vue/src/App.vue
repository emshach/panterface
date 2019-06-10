<template lang="html">
  <div id="app">
    <div id="nav">
      <vk-btn-link><vk-icon-user />{{ user.fname }}</vk-btn-link>
      <vk-dropdown>
        <vk-nav>
          <template v-if="user.uid && !user.anonymous">
            <vk-nav-item href="logout">logout</vk-nav-item>
          </template>
          <template v-else>
            <vk-nav-item href="login">login</vk-nav-item>
            <vk-nav-item href="sign up">login</vk-nav-item>
          </template>
        </vk-nav>
      </vk-dropdown>
      <router-link
        v-for="( link, key ) in menus.nav.$links" :key="key"
        :to="link.location.$href">{{ link.$title || link.location.$title }}</router-link>
    </div>
    <!-- <transition name="fade-fast" mode="out-in"> -->
    <!--   <search-results-page v-if="searching" /> -->
      <router-view />
    <!-- </transition> -->
    <prompt :breadcrumb="context" @update="promptInput" />
  </div>
</template>

<script lang="js">
import { ButtonLink as VkBtnLink } from 'vuikit/lib/button'
import { Dropdown as VkDropdown } from 'vuikit/lib/dropdown'
import { IconUser as VkIconUser } from '@vuikit/icons'
import {
  NavDropdown as VkNav,
  NavItem as VkNavItem,
  NavItemParent as VkNavParent,
} from 'vuikit/lib/nav'
import Prompt from '@/components/Prompt'
export default {
  name: 'App',
  components: {
    VkBtnLink,
    VkDropdown,
    VkNav,
    VkNavItem,
    VkNavParent,
    VkIconUser,
    Prompt,
  },
  data() {
    return {
      searching: false,         // TODO: 
    };
  },
  methods: {
    promptInput( route, context ) {
      this.$store.dispatch( 'setContext', context );
      this.$router.push( route || '/' );
    }
  },
  computed: {
    context() {
      return this.$store.state.context;
    },
    menus: () => Friede.menus,
    user: () => Friede.user,
  }
}
</script>

<style scoped lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}
#nav {
  margin: 0 4px 4px;
  padding: 0;
  position: fixed;
  z-index: 200;
  top: 0;
  right: 0;
  a {
    display: inline-block;
    font-size: 0.9rem;
    color: #2c3e50;
    padding: 2px 8px 4px;
    text-shadow: 0 0 1px black;
    text-decoration: none !important;
    border-radius: 3px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
    text-shadow: 0 0 1px lightskyblue;
    &.router-link-exact-active {
      color: white;
      font-weight: bold;
      background: rgba(0,0,150,0.3);
    }
    &:hover {
      /* background: rgba(255,255,255,0.25); */
      box-shadow: 0 -20px 30px #ffffa3;
    }
  }
}
</style>
