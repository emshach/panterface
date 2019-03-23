<template lang="html">
  <form id="prompt" @submit.prevent="submit" class="mf-prompt uk-flex uk-wrap-around">
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

<style lang="scss">
  .mf-prompt {
    width: 100%;
    .breadcrumb {
      margin: 0;
      padding: 4px;
      color: white;
      text-shadow: 0 0 1px black;
      li {
        font-weight: bold;
        &:before {
          color: lightskyblue !important;
          margin: 0 4px !important;
          display: inline !important;
        }
        a {
          color: white;
          padding: 1px 4px;
          &:hover {
            background: rgba(255,255,255,0.25);
          }
        }
      }
    }
    .cli {
      background: rgba(0,0,0,0.5);
      font-family: monospace;
      padding: 4px 10px;
      height: auto;
      border: 1px solid skyblue;
      border-bottom-width: 0;
      border-right-width: 0;
      border-top-left-radius: 4px;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.25);
      font-size: 14px;
      &:focus {
        background: rgba(0,0,0,0.8);
      }
    }
  }
</style>
