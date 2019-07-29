<template lang="html">
  <div id="app">
    <div id="nav">
      <router-link
        v-for="( link, key ) in siteLinks" :key="key"
        :to="link.entry.location.href">{{
        link.entry.title || link.entry.location.$title }}
      </router-link>
      <router-link to="/me">
        <font-awesome-icon :icon=" user.anonymous ? 'user-ninja': 'user'"
                           class="nav-icon" /> {{ user.first_name || user.username }}
      </router-link>
      <user-menu :user="user" />
    </div>
    <!-- <transition name="fade-fast" mode="out-in"> -->
    <!--   <search-results-page v-if="searching" /> -->
      <router-view :key="user.username" />
    <!-- </transition> -->
    <prompt :breadcrumb="context" @update="promptInput" />
  </div>
</template>

<script lang="js">
import Vue from 'vue'
import VueToastr from 'vue-toastr'
import { faUserNinja, faUser } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { Prompt, UserMenu } from '@/components'

library.add( faUserNinja, faUser )

let toastcheck;
toastcheck = setInterval(() => {
  if ( !document.body )
    return;
  Vue.use( VueToastr, { defaultPosition: 'toast-bottom-right' });
  clearInterval( toastcheck );
  toastcheck = null;
});

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
  created() {
    this.$store.commit( 'setMenus', Friede.menus );
  },
  methods: {
    async promptInput( route, context ) {
      await this.$store.dispatch( 'setContext', context );
      this.$router.push( route || '/' );
    },
  },
  computed: {
    context() {
      return this.$store.state.context;
    },
    menus() {
      return this.$store.state.menus;
    },
    user() {
      return this.$store.state.user;
    },
    siteLinks() {
      if ( !this.menus || !this.menus.active )
        return
      const links = this.menus.containers.nav.entry.links;
      const out = {};
      Object.keys( links ).forEach( l => {
        if ( links[l].active && links[l].entry.active
             && links[l].entry.location && links[l].entry.location.active
             && links[l].entry.location.href )
          out[l] = links[l];
      });
      return out;
    },
    error() {
      return this.$store.state.error;
    }
  },
  watch: {
    error( err ) {
      this.$toastr.Add({
        type: 'error',
        msg: err,
        timeout: 0
      });
    }
  }
}
</script>

<style scoped lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
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
      border-bottom: 1px solid rgba(255,255,255,0.7);
      box-shadow: inset 0 -1px 3px rgba(0,0,0,0.2);
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
