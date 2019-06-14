<template lang="html">
  <div id="app">
    <div id="nav">
      <router-link
        v-for="( link, key ) in menus.nav.$links" :key="key"
        :to="link.location.$href">{{ link.$title || link.location.$title }}
      </router-link>
      <router-link to="/me">
        <font-awesome-icon :icon=" user.anonymous ? 'user-ninja': 'user'"
                           class="nav-icon" /> {{ user.fname }}
      </router-link>
      <user-menu />
    </div>
    <!-- <transition name="fade-fast" mode="out-in"> -->
    <!--   <search-results-page v-if="searching" /> -->
      <router-view />
    <!-- </transition> -->
    <prompt :breadcrumb="context" @update="promptInput" />
  </div>
</template>

<script lang="js">
import { faUserNinja, faUser } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import Prompt from '@/components/Prompt'
import UserMenu from '@/components/UserMenu'

library.add( faUserNinja, faUser )

export default {
  name: 'App',
  components: {
    FontAwesomeIcon,
    Prompt,
    UserMenu,
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
    },
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
  .username {
    font-weight: bold;
    color: steelblue;
  }
  > a {
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
    .nav-icon {
      margin-right: 2px;
    }
  }
}
</style>
