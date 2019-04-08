<template lang="html">
  <form id="prompt" class="mf-prompt uk-flex uk-wrap-around"
        @submit.prevent="submit">
    <switchboard :matches="matches" :locations="locations" @update="complete" />
    <breadcrumb class="breadcrumb" :items="breadcrumb" />
    <textarea v-if="multiline" name="cli" class="cli uk-input uk-flex-1"
              rows="1"  v-model="cli" @input="input" ref="input"
              @keydown="processKey( $event )" />
    <input v-else name="cli" class="cli uk-input uk-flex-1" v-model="cli"
           ref="input" @input="input" @keydown="processKey( $event )" />
  </form>
</template>

<script lang="js">
import Switchboard from '@/components/Switchboard.vue'
import Breadcrumb from '@/components/Breadcrumb.vue'
import debounce from 'lodash/debounce'
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
    }
  },
  components: { Switchboard, Breadcrumb },
  mounted() {
    this.$nextTick(() => {
      this.$refs.input.focus()
    })
  },
  data() {
    return {
      cli: '',
      prevCli: '',
      base: '',
      matches: [],
      locations: [],
    }
  },
  methods: {
    submit() {
      this.$emit( 'update', this.cli );
      this.cli = '';
    },
    getCompletions() {
      this.$api( 'complete/' + this.cli ).then( data => {
        this.base = data.base;
        this.matches = data.matches.sort();
        this.locations = data.locations.sort();
      });
    },
    debouncedInput: debounce( function() {
      this.getCompletions();
    }, 250 ),
    input() {
      if ( this.matches.length &&
           this.cli !== this.prevCli && this.cli.indexOf( this.prevCli ) === 0 ) {
        // then just filter
        var base = this.base + this.cli.replace( this.prevCli, '' );
        this.base = base;
        this.matches = this.matches.filter( x => x.indexOf( base ) === 0 );
        this.locations = this.locations.filter(
          x => x.name.indexOf( base ) === 0 );
        if (! this.matches.length )
          this.getCompletions();
      } else 
        this.debouncedInput();
      this.prevCli = this.cli;
    },
    complete( match ) {
      this.cli = this.cli.replace( RegExp( this.base + '$' ), match );
      this.getCompletions();
      this.$refs.input.focus();
    },
    processKey( $event ) {
      if ( $event.keyCode === 9 )  { // TAB
        $event.preventDefault();
        if ( this.matches.length === 1 )
          this.complete( this.matches[0] + ' ' )
        // TODO: else cycle completions
      }
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
