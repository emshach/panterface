<template lang="html">
  <div class="dashboard">
    <thing v-for="( thing, index ) in things" :key="index" :is="thing"/>
  </div>
</template>

<script lang="js">
export default {
  name: 'Dashboard',
  props: {
    src: {
      type: [ String, Object ],
      default: ''
    },
    elements: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      results: []
    }
  },
  mounted() {
    // TODO: get dashboard elements
  },
  computed: {
    things() {
      if ( this.results && this.results.length ) {
        return this.results;
      } else if ( this.elements && this.elements.length ) {
        return this.elements;
      } else {
        return []
      }
    }
  }
}
</script>

<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
