<template lang="html">
  <form id="prompt" class="mf-prompt uk-flex uk-wrap-around" ref="form"
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
import Switchboard from '@/components/Switchboard'
import Breadcrumb from '@/components/Breadcrumb'
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
      enterMeansSubmit: true,
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
        this.matches = data.matches;
        this.locations = data.locations;
      });
    },
    debouncedInput: debounce( function() {
      this.getCompletions();
    }, 250 ),
    input() {
      const prev = this.prevCli, cli = this.cli;
      if ( this.matches.length && cli !== prev && cli.indexOf( prev ) === 0 ) {
        // then just filter
        var base = this.base + cli.replace( prev, '' );
        this.base = base;
        var matches = this.matches.filter( x => x.indexOf( base ) === 0 );
        var locations = this.locations.filter(
          x => x.name.indexOf( base ) === 0 );
        if (! matches.length 
            || locations.slice( 0, 10 ).find( x => !x._widget_entries )) {
          this.getCompletions();
        } else {
          this.matches = matches;
          this.locations = locations;
        }
      } else 
        this.debouncedInput();
      this.prevCli = cli;
    },
    complete( match ) {
      this.cli = this.cli.replace( RegExp( this.base + '$' ), match + ' ' );
      this.getCompletions();
      this.$refs.input.focus();
    },
    processKey( $event ) {
      if ( $event.keyCode === 9 )  { // TAB
        $event.preventDefault();
        if ( this.matches.length === 1 )
          this.complete( this.matches[0] + ' ' )
        // TODO: else cycle completions
      } else if( $event.keyCode === 13 && this.multiline && this.enterMeansSubmit) { 
        $event.preventDefault();
        this.$refs.form.submit();
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
