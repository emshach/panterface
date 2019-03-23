<template lang="html">
  <form id="prompt" @submit.prevent="submit" class="prompt uk-flex uk-wrap-around">
    <Breadcrumb class="breadcrumb" :items="breadcrumb" />
    <input name="cli" class="cli uk-input uk-flex-1"
           v-model="cli" @input="input" />
  </form>
</template>

<script lang="js">
import Breadcrumb from '@/components/Breadcrumb.vue'
export default {
  name: 'Prompt',
  props: {
    breadcrumb: {
      type: Array,
      default: () => []
    }
  },
  components: { Breadcrumb },
  mounted() {

  },
  data() {
    return {
      cli: ''
    }
  },
  methods: {
    submit() {
    },
    input() {
    }
  },
  computed: {

  }
}
</script>

<style scoped lang="scss">
  .prompt {
    width: 100%;
    .breadcrumb {
      margin: 0;
      padding: 4px;
      font-weigt: bold;
      color: white;
      text-shadow: 0 0 1px black;
      a {
        color: white;
      }
    }
    .cli {
      background: black;
      font-family: monospace;
      padding: 4px;
      height: auto;
    }
  }
</style>
