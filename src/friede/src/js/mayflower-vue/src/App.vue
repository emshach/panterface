<template lang="html">
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
    </div>
    <transition name="fade-fast" mode="out-in">
      <search-results-page v-if="searching" />
      <router-view v-else />
    </transition>
    <prompt :breadcrumb="breadcrumb" @update="promptInput" />
  </div>
</template>

<script lang="js">
import Prompt from '@/components/Prompt.vue'
export default {
  name: 'App',
  components: {
    Prompt
  },
  data() {
    return {
      searching: false,         // TODO: 
      breadcrumb: [{ href: '/', title: '/' }]
    };
  },
  methods: {
    promptInput( value ) {
      if ( !value ) {
        return;
      }
      this.breadcrumb = value.split( /\s+/ )
         .map( x => ({ href: x, title: x }));
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
    font-weight: bold;
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
