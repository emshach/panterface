<template lang="html">
  <div id="app">
    <div id="nav">
      <router-link
        v-for="( link, key ) in menus.nav.$links" :key="key"
        :to="link.location.$href">{{ link.$title || link.location.$title }}</router-link>
    </div>
    <transition name="fade-fast" mode="out-in">
      <search-results-page v-if="searching" />
      <router-view v-else />
    </transition>
    <prompt :breadcrumb="context" @update="promptInput" />
  </div>
</template>

<script lang="js">
import Prompt from '@/components/Prompt'
export default {
  name: 'App',
  components: {
    Prompt
  },
  data() {
    return {
      menus: Friede.menus,
      searching: false,         // TODO: 
    };
  },
  methods: {
    promptInput( route, context ) {
      this.$store.commit( 'setContext', context );
      this.$router.push( route || '/' );
    }
  },
  computed: {
    context() {
      return this.$store.state.context;
    }
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
}
#nav {
  margin: 4px;
  padding: 0;
  position: fixed;
  top: 0;
  right: 0;
  a {
    font-size: 0.9rem;
    color: #2c3e50;
    padding: 4px 8px;
    text-shadow: 0 0 1px black;
    text-decoration: none !important;
    border-radius: 2px;
    text-shadow: 0 0 1px lightskyblue;
    &.router-link-exact-active {
      color: white;
      text-shadow: 0 0 1px black;
    }
    &:hover {
      /* background: rgba(255,255,255,0.25); */
      box-shadow: 0 -20px 30px #ffffa3;
    }
  }
}
</style>
