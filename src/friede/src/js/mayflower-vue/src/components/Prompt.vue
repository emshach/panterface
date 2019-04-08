<template lang="html">
  <form id="prompt" class="mf-prompt uk-flex uk-wrap-around"
        @submit.prevent="submit">
    <switchboard />
    <breadcrumb class="breadcrumb" :items="breadcrumb" />
    <textarea v-if="multiline" name="cli" class="cli uk-input uk-flex-1"
              rows="1"  v-model="cli" @input="input" />
    <input v-else name="cli" class="cli uk-input uk-flex-1" v-model="cli"
           @input="input" />
  </form>
</template>

<script lang="js">
import Switchboard from '@/components/Switchboard.vue'
import Breadcrumb from '@/components/Breadcrumb.vue'
import _ from 'lodash'
export default {
  name: 'Prompt',
  props: {
    breadcrumb: {
      type: Array,
      default: () => []
    },
    multiline: {
      type: Boolean,
      default: true
    },
    matches: {
      type: Array,
      default: () => []
    },
    locations: {
      type: Array,
      default: () => []
    }
  },
  components: { Switchboard, Breadcrumb },
  mounted() {
  },
  data() {
    return {
      cli: ''
    }
  },
  methods: {
    submit() {
      this.$emit( 'update', this.cli );
      this.cli = '';
    },
    input() {
      _.debounce(() => {
        this.$api( 'complete/' + this.cli ).then( data => {
          this.matches = data.matches;
          this.locations = data.locations;
        })
      }, 500 );
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
    textarea.cli {
      line-height: normal;
      padding: 8px 10px;
    }
  }
</style>
