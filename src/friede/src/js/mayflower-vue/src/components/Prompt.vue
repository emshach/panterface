<template>
  <form id="prompt" class="mf-prompt uk-flex uk-wrap-around" ref="form"
        @submit.prevent="submit">
    <switchboard :matches="matches" :locations="locations" :slots="slots"
                 v-model="selected" @input="update" />
    <div class="readline uk-flex uk-wrap-around">
      <breadcrumb class="main" :items="breadcrumb" />
      <breadcrumb v-if="prospect.length" class="tmp" :items="prospect" />
      <div v-if="searching" class="object-search uk-flex uk-wrap-around">
        <span class="object">{{ searching.label }}:</span>
        <multiselect
          v-model="objects"
          class="filter uk-input uk-flex-1"
          ref="filter"
          open-direction="above"
          label="title"
          track-by="path"
          :options="search"
          :close-on-select="true"
          :show-labels="false"
          :internal-search="false"
          :loading="loading"
          @search-change="getObjects"
          />
      </div>
      <div v-else-if="creating" class="object-create uk-flex uk-wrap-around">
        <span class="object">new {{ creating.label }}:</span>
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
import Multiselect from 'vue-multiselect'
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
  components: { Switchboard, Breadcrumb, Multiselect },
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
      search: [],
      objects: [],
      creating: null,
      prospect:  [],
      pathMatches: [],
      pathSlots: [],
      pathLocations: [],
      enterMeansSubmit: true,
      selected: null,
      loading: false,
    }
  },
  methods: {
    submit() {
      if ( this.selected ) {
        if ( this.selected.href ) { // TODO: go to location
          this.$emit( 'update', this.selected.href );
        } else if ( this.selected.label ) {
          this.searching = this.selected;
        } else {
          this.prospect.push({ href: this.selected, title: this.selected });
        }
        this.input = this.entered = '';
        this.getCompletions();
      }
    },
    getCompletions() {
      this.$api( 'ls', this.input ).then( r => {
        this.pathMatches = r.data.matches;
        this.pathSlots = r.data.slots;
        this.pathLocations = r.data.locations;
      });
    },
    getObjects( query ) {
      const model = this.searching;
      this.loading = true;
      this.$api( model.app, model.plural, '?search='+query ).then( r => {
        this.search = r.data.results;
        this.loading = false;
      });
      
    },
    debouncedInput: debounce( function() {
      this.getCompletions();
    }, 250 ),
    processInput() {
      this.selected = this.entered = this.input;
    },
    select( match ) {
      this.selected = match;
      if ( match.href ) {       // location, about to go
        this.state = 'prelaunch';
        this.input = 'Goto: ' + match.href;
        // TODO: need to extract the part already entered
      } else if ( match.label ) { // slot
        this.state = 'searching';
        this.input = 'Object: ' + match.label
        // TODO: get completions for object
      } else {                  // string match
        this.state = 'nav';
        this.input = match;
      }
    },
    update( match ) {
      this.select( match );
      this.submit()
    },
    processKey( $event ) {
      if ( $event.keyCode === 9 )  { // TAB
        $event.preventDefault();
        if ( this.matches.length ) {
          if ( this.all.length === 1 ) {
            this.update( this.all[0] );
          } else {
            var cr = this.all.indexOf( this.selected );
            if ( $event.shiftKey ) {
              if ( cr != -1 )
                cr--;
            } else {
              cr++;
            }
            this.select( this.all[ cr % this.all.length ]);
          }
        }
        // TODO: else cycle completions
      } else if ( $event.keyCode === 13 ) { 
        $event.preventDefault();
        this.submit();
      } else if ( $event.keyCode === 27 ) {
        if ( this.selected ) {
          this.selected = this.input = this.entered;
        } else if ( this.input ) {
          this.input = this.entered = '';
        } else if ( this.prospect.length ) {
          this.prospect = []
        } else {
          this.$refs.input.blur();
        }
      } else if ( this.selected ) {
        this.selected = this.input = this.entered;
      }
    }
  },
  computed: {
    all() {
      return this.matches.concat( this.locations ).concat( this.slots );
    },
    matches() {
      if ( this.searching || this.creating )
        return [];
      if ( !this.entered )
        return this.pathMatches;
      return this.pathMatches.filter( x => x.indexOf( this.entered ) === 0 )
    },
    slots() {
      if ( this.searching || this.creating )
        return [];
      if ( !this.entered )
        return this.pathSlots;
      return this.pathSlots.filter(
          x => x.search.filter(
            y => y.indexOf( this.entered ) > -1 ).length )
    },
    locations() {
      if ( this.searching || this.creating )
        return [];
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
  .readline {
    width: 100%;
  }
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
  input {
      padding: 4px 10px;
      height: auto;
      font-size: 14px;
    &.cli {
      background: rgba(0,0,0,0.5);
      font-family: monospace;
      border: 1px solid skyblue;
      border-bottom-width: 0;
      border-right-width: 0;
      border-top-left-radius: 4px;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.25);
      &:focus {
        background: rgba(0,0,0,0.8);
      }
    }
  }
  .object-search {
    background: white;
    padding: 0 10px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    span {
      padding: 5px 0 0;
      font-weight: bold;
      color: steelblue;
    }
  }
  textarea.cli {
    line-height: normal;
    padding: 8px 10px;
    }
  }
</style>
