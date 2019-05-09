<template>
  <form id="prompt" class="mf-prompt uk-flex uk-wrap-around" ref="form"
        @submit.prevent="submit">
    <switchboard :matches="matches" :locations="locations" @update="complete" />
    <div class="readline uk-flex uk-wrap-around">
      <breadcrumb class="main" :items="breadcrumb" />
      <breadcrumb v-if="prospect.length" class="tmp" :items="prospect" />
      <div v-if="searching" class="object-search">
        <span class="object">{{ searching }}:</span>
        <input name="filter" class="filter uk-input uk-flex-1" v-model="filter"
               ref="filter" />
      </div>
      <div v-else-if="creating" class="object-create">
        <span class="object">{{ creating }}:</span>
        <input name="ctrl" class="filter uk-input uk-flex-1" v-model="ctrl"
               ref="ctrl" />
      </div>
      <input v-else name="cli" class="cli uk-input uk-flex-1" v-model="input"
             ref="input" @input="processInput" @keydown="processKey( $event )" />
    </div>
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
      this.$refs.input.focus();
      this.getCompletions();
    })
  },
  data() {
    return {
      input: '',
      entered: '',
      state: 'nav',
      filter: '',
      ctrl: '',
      values: {},
      searching: null,
      creating: null,
      prospect:  [],
      pathMatches: [],
      pathSlots: [],
      pathLocations: [],
      enterMeansSubmit: true,
    }
  },
  methods: {
    submit() {
      this.$emit( 'update', this.input );
      // TODO: based on state, push prospect, push breadcrumb
      this.entered = '';
      this.getCompletions();
    },
    getCompletions() {
      this.$api( 'ls', this.input ).then( data => {
        this.pathMatches = data.matches;
        this.pathSlots = data.slots;
        this.pathLocations = data.locations;
      });
    },
    debouncedInput: debounce( function() {
      this.getCompletions();
    }, 250 ),
    processInput() {
      this.entered = this.input;
    },
    complete( match ) {
      this.input = match;
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
    matches() {
      if ( !this.entered )
        return this.pathMatches;
      return this.pathMatches.filter( x => x.indexOf( this.entered ) === 0 )
    },
    slots() {
      if ( !this.entered )
        return this.pathSlots;
      return this.pathSlots.filter(
          x => x.search.filter(
            y => y.indexOf( filter ) > -1 ).length )
    },
    locations() {
      if ( !this.entered )
        return this.pathLocations;
      return this.pathLocations.filter( x => x.name.indexOf( this.entered ) === 0 )
    },
    filters() {
      return this.filter.split(/\s+/)
    }
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
      &.tmp {
        background: rgba(255,255,255,0.3);
        margin-right: -3px;
        border-top-left-radius: 4px;
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
