<template lang="html">
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
    </div>
    <router-view />
    <Prompt :breadcrumb="breadcrumb" />
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
      breadcrumb: [{ href: '/', title: '/' }]
    };
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
      text-shadow: 0 1 1px black;
    }
    &:hover {
      background: rgba(255,255,255,0.25);
    }
  }
}
</style>
