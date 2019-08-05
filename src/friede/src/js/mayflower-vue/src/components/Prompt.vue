<template>
  <form id="prompt" class="mf-prompt uk-flex uk-wrap-around" ref="form"
        autocomplete="off"
        @submit.prevent="submit">
    <switchboard :matches=matches :locations=locations :slots=slots
                 :base-rx=baseRx :focused=completing 
                 v-model=selected @input=update />
    <div class="readline uk-flex uk-wrap-around">
      <breadcrumb class="main" :items=myBreadcrumb />
      <breadcrumb v-if="prospect.length" class="tmp" :items=prospect />
      <div v-if="searching" class="object-search uk-flex uk-wrap-around">
        <span class="object">{{ searching.label }}</span>
        <multiselect
          v-model="objects"
          class="filter uk-input uk-flex-1"
          ref="filter"
          open-direction="above"
          label="title"
          track-by="path"
          placeholder="filter"
          tag-placeholder="add filter"
          tag-position="bottom"
          :options=slotOptions
          :close-on-select=false
          :hide-selected=true
          :show-labels=false
          :internal-search=false
          :loading=loading
          :multiple=searching.multiple
          :taggable=true
          @input=focusSlot
          @search-change=getObjects
          @tag=addFilter
          @select=searchSelect
          @keydown=processSlotKey
          v-shortkey=shortcuts
          @shortkey.native=doSlotShortcut >
          <template #noOptions>All {{ searching.plural }}</template>
        </multiselect>
        <vk-button-link class="btn btn-confirm" @click.prevent="confirmSearch">
          <font-awesome-icon icon="check" />
        </vk-button-link>
        <vk-button-link class="btn btn-cancel" @click.prevent="cancelSearch">
          <font-awesome-icon icon="times" />
        </vk-button-link>
      </div>
      <div v-else-if="creating" class="object-create uk-flex uk-wrap-around">
        <span class="object">new {{ creating.label }}</span>
        <input name="ctrl" class="filter uk-input uk-flex-1" v-model="ctrl"
               ref="ctrl" tabindex="0" />
      </div>
      <template v-else>
        <input name="cli" class="cli uk-input uk-flex-1" v-model="input"
               ref="input" tabindex="0"
               @input=processInput
               @keydown=processKey
               @focus="completing = true"
               @blur="completing = false"
               v-shortkey.focus="['/']"
               v-shortkey.avoid />
        <vk-button-link v-if="canGo" class="btn btn-go">go</vk-button-link>
      </template>
    </div>
  </form>
</template>

<script lang="js">
import Switchboard from './Switchboard'
import Breadcrumb from './Breadcrumb'
import debounce from 'lodash/debounce'
import Multiselect from 'vue-multiselect'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimes, faCheck } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ButtonLink as VkButtonLink } from 'vuikit/lib/button'
import 'vue-multiselect/dist/vue-multiselect.min.css'

library.add( faTimes, faCheck )

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
  components: {
    Switchboard,
    Breadcrumb,
    Multiselect,
    FontAwesomeIcon,
    VkButtonLink,
  },
  mounted() {
    this.myBreadcrumb = this.breadcrumb.slice();
    this.$nextTick(() => {
      this.$refs.input.focus();
      this.getCompletions();
    })
  },
  data() {
    return {
      base: '',
      input: '',
      entered: '',
      state: 'nav',
      filters: [],
      ctrl: '',
      values: {},
      searching: null,
      search: [],
      query: '',
      objects: [],
      creating: null,
      prospect:  [],
      pathMatches: [],
      pathSlots: [],
      pathLocations: [],
      enterMeansSubmit: true,
      selected: null,
      loading: false,
      myBreadcrumb: [],
      endpoint: false,
      completing: false,
      exactMatch: false,
      showSwitchboard: true,
      shortcuts: { enter: ['enter'], esc: ['esc'], bkspc: ['backspace'] }
    }
  },
  methods: {
    submit() {
      if ( this.selected ) {
        if ( this.selected.href ) { // TODO: go to location
          let hash = this.selected.href.replace( this.baseRx, '' );
          this.prospect.push({
            href: this.selected.href,
            title: hash,
            hash,
            location: this.selected
          });
          this.selected = null;
          this.$nextTick(() => {
            this.submit();
          });
        } else if ( this.selected.label ) {
          this.searching = this.selected;
          this.focusSlot();
        } else {
          this.prospect.push({ href: this.selected, title: this.selected });
          this.$nextTick(() => {
            this.$refs.input.focus();
          });
        }
        this.input = this.entered = '';
        this.selected = null;
        this.getCompletions();
      } else {
        this.$emit( 'update', this.route, this.myBreadcrumb.concat( this.prospect ));
        // this.myBreadcrumb = this.myBreadcrumb.concat( this.prospect );
        this.prospect = [];
      }
    },
    getCompletions() {
      const path = this.path;
      return this.$api( 'ls', this.path ).then( r => {
        if ( this.path !== path ) return;
        this.base = r.data.base;
        this.endpoint = r.data.endpoint;
        this.pathMatches = r.data.matches;
        this.pathSlots = r.data.slots;
        this.pathLocations = r.data.locations;
        if ( this.endpoint && this.prospect.length ) {
          this.prospect[ this.prospect.length-1 ].location = this.endpoint;
        }
      });
    },
    addFilter( tag ) {
      if ( this.filters.find( x => x.tag === tag ))
        return;
      const filter = {
        path: `_filter.${tag}`,
        title: `filter: ${tag}`,
        filter: true,
        tag: tag
      }
      this.filters.push( filter );
      this.objects.push( filter );
    },
    getObjects( query ) {
      this.query = query;
      const model = this.searching;
      this.loading = true;
      this.$api( model.app, model.plural, '?search='+query ).then( r => {
        this.loading = false;
        this.search = r.data.results;
        if ( model.create ) {
          this.search.unshift({ path: '', title: 'New ' + model.label, ctrl: true })
        }
        this.search.unshift({ path: '_action.cancel', title: 'Cancel', ctrl: true })
        this.search.unshift({ path: '_action.done', title: 'Done', ctrl: true })
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
      this.exactMatch = false;
      this.select( match );
      this.submit()
    },
    processKey( $event ) {
      if ( $event.key === '/' ) {
        $event.preventDefault();
        if ( this.selected && this.all.find( x => x === this.selected )) {
          this.submit();
          return;
        }
        if ( !this.input && !this.prospect.length ) {
          this.myBreadcrumb = [ this.myBreadcrumb[0] ];
          this.getCompletions();
          return;
        }
        let l = this.all.filter( x => x.path && /^locations./.test( x.path ));
        if ( l.length === 1 ) {
          this.update( l[0] );
          return;
        } else {
          let l = this.all.filter( x =>  typeof x === 'string' );
          if ( l.length === 1 ) {
            this.update( l[0] );
            return;
          }
        }
        this.exactMatch = !this.exactMatch;
        this.$nextTick(() => {
          if ( this.all.length === 1 )
            this.update( this.all[0] );
        });
      } else if ( $event.key === 'Tab' )  {
        $event.preventDefault();
        let l = this.all.length;
        if ( l ) {
          if ( l === 1 ) {
            this.update( this.all[0] );
          } else {
            var cr = this.all.indexOf( this.selected );
            if ( $event.shiftKey ) {
              if ( cr != -1 ) 
                cr--;
            } else {
              cr++;
            }
            this.select( this.all[( cr + l ) % l ]);
          }
        }
        // TODO: else cycle completions
      } else if ( $event.key === 'Enter' ) {
        $event.preventDefault();
        this.submit();
      } else if ( $event.key === 'Escape' ) {
        if ( this.selected ) {
          this.selected = this.input = this.entered;
        } else if ( this.input ) {
          this.input = this.entered = '';
        } else if ( this.prospect.length ) {
          this.prospect = []
        } else if ( this.partial ) {
          this.myBreadcrumb = this.breadcrumb.slice();
        } else {
          this.$refs.input.blur();
        }
        this.getCompletions();
      } else if ( $event.key === 'ArrowLeft' ) {
        $event.preventDefault();
        let l = this.all.length;
        if ( l < 2 )
          return;
        let cr = this.all.indexOf( this.selected );
        if ( cr != -1 ) 
          cr--;
        this.select( this.all[( cr + l ) % l ]);
      } else if ( $event.key === 'ArrowRight' ) {
        $event.preventDefault();
        let l = this.all.length;
        if ( l < 2 )
          return;
        let cr = this.all.indexOf( this.selected ) + 1;
        this.select( this.all[( cr + l ) % l ]);
      } else if ( $event.key === 'Backspace' ) {
        if ( this.state === 'searching' ) {
          this.selected = this.input = this.entered;
        }
        if ( !this.entered ) {
          if ( this.prospect.length ) {
            $event.preventDefault();
            this.prospect.pop();
            this.getCompletions();
          } else if ( this.myBreadcrumb.length > 1 ) {
            $event.preventDefault();
            this.myBreadcrumb.pop();
            this.getCompletions();
          }
        }
      } else if ( !( $event.key === 'Shift' || $event.key === 'Control'
                    || $event.key === 'Meta'  || $event.key === 'Command')
                  && this.selected ) {
        this.selected = this.input = this.entered;
      }
    },
    processSlotKey( $event ) {
      console.log( 'processSlotKey', $event );
      if ( $event.key === 'Enter' ) {
        if ( !this.query ) {
          $event.preventDefault();
          this.confirmSearch();
        }
      } else if ( $event.key === 'Escape' ) {
        $event.preventDefault();
        this.cancelSearch();
      }
    },
    doSlotShortcut( $event ) {
      switch( $event.srcKey ) {
      case 'enter':
        this.confirmSearch();
      case 'esc':
      case 'bkspc':
        this.cancelSearch();
      }
    },
    focusSlot() {
      this.$nextTick(() => {
        if ( this.$refs.filter )
          this.$refs.filter.$el.focus();
      });
    },
    searchSelect( value ) {
      if ( value.path === '_action.done' ) {
        this.confirmSearch();
        return false;
      } else if ( value.path === '_action.cancel' ) {
        this.cancelSearch();
        return false;
      }
    },
    confirmSearch() {
      const s = this.searching;
      const o = this.objects;
      var filters = o.filter( x => x.filter ).map( x => ( x.tag ))
      var filter = filters.join('+');
      var objects = o.filter( x => x.id );
      var ids = objects.map( x => x.id );
      this.prospect.push({
        href: '{' + s.app + '.' + s.model + '\\*?\\+?}',
        hash: '-' + s.app + '-' + s.plural
           + ( ids.length ? '-' + ids.join('-') : filter ? '+' : '' )
           + ( filter ? '+' + filter : '' ),
        objects: objects,
        filters: filters,
        filter: filter,
        title: ( filter ? ( s.plural + ': ' + filter
                            + ( ids ? ' + ' + ids.length : '' ))
                 : objects.length === 1
                 ? s.singular + ': ' + o[0].title
                 : ( o.length ? o.length + ' ' + s.plural : s.plural )),
        slot: s });
      this.cancelSearch();      // lol
      this.getCompletions();
    },
    cancelSearch() {
      this.searching = null;
      this.filters = [];
      this.search = [];
      this.objects = [];
      this.input = this.entered = '';
      this.$nextTick(() => {
        this.$refs.input.focus();
      });
    },
    serializeNode( node ) {
      return node.hash || node.href;
    }
  },
  computed: {
    all() {
      return this.matches.concat( this.locations ).concat( this.slots );
    },
    baseRx() {
      return new RegExp( this.base, 'i' );
    },
    matches() {
      if ( this.searching || this.creating )
        return [];
      const l = this.locationHrefs;
      if ( !this.entered )
        return this.pathMatches.filter( x => !l.find( y => x === y ));
      return this.pathMatches.filter(
        x => x.indexOf( this.entered ) === 0 && !l.find( y => x === y ));
    },
    slots() {
      if ( this.searching || this.creating )
        return [];
      if ( !this.entered )
        return this.pathSlots;
      const rx = new RegExp( this.entered, 'i' );
      return this.pathSlots.filter( x => x.search.filter( y => y.match( rx )).length )
    },
    locations() {
      if ( this.searching || this.creating )
        return [];
      if ( !this.entered )
        return this.pathLocations.filter( x => x.href.replace( this.baseRx, '' ));
      return this.pathLocations.filter(
        x => x.name.indexOf( this.entered ) === 0 && x.href.replace( this.baseRx, '' ));
    },
    locationHrefs() {
      return this.locations.map( x => x.href.replace( this.baseRx, '' ));
    },
    path() {
      return this.myBreadcrumb.map( x => escape( x.href )).concat(
        this.prospect.map( x => escape( x.href ))).join('/');
    },
    route() {
      return this.myBreadcrumb.map( this.serializeNode ).concat(
        this.prospect.map( this.serializeNode )).join('/');
    },
    partial() {
      return ( this.route != this.$store.getters.route );
    },
    canGo() {
      return this.endpoint && this.partial;
    },
    slotOptions() {
      return this.filters.concat( this.search );
    }
  },
  watch: {
    breadcrumb( val ) {
      this.myBreadcrumb = val.slice();
      this.prospect = [];
    },
    path( val ) {
      this.$nextTick(() => this.$refs.input.focus());
      this.getCompletions();
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
    /* text-shadow: 0 0 1px black; */
    li {
      /* font-weight: bold; */
      &:before {
        /* color: lightskyblue !important; */
        color: #3a3a92;
        margin: 0 !important;
        display: inline !important;
        font-size: 0.875rem !important;
        font-weight: bold !important;
      }
      a {
        color: #3a3a92;
        padding: 1px 2px;
        &:hover {
          background: rgba(255,255,255,0.25);
        }
      }
    }
    &.tmp {
      background: rgba(255,255,255,0.3);
      margin-right: -3px;
      border-top-left-radius: 4px;
      padding-right: 6px;
      li {
        a{
          color: #3f3f98;
        }
      }
    }
  }
  input {
    &.cli {
      padding: 4px 10px;
      height: auto;
      font-size: 14px;
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
    > span {
      padding: 5px 0 0;
      color: steelblue;
    }
    >.multiselect {
      padding-right: 0;
      background: transparent;
      height: 32px;
      min-height: 32px;
      .multiselect__tags {
        padding-top: 4px;
        padding-left: 4px;
        height: 32px;
        min-height: 32px;
      }
      .multiselect__select {
        height: 32px;
      }
      .multiselect__placeholder {
        padding-top: 0;
        height: 24px;
        min-height: 24px;
        line-height: 24px;
        vertical-align: top;
      }
    }
    .btn {
      padding: 0 7px;
      height: 30px;
      line-height: 33px;
      &.btn-confirm {
        color: limegreen;
        &:hover {
          color: forestgreen;
        }
      }
      &.btn-cancel {
        color: red;
        &:hover {
          color: darkred;
        }
      }
    }
  }
  .btn-go {
    background: limegreen;
    color: white;
    height: 32px;
    border: 1px solid lightgreen;
    border-radius: 4px 0 0 0;
    border-bottom-width: 0;
    border-right-width: 0;
    line-height: 30px;
  }
  textarea.cli {
    line-height: normal;
    padding: 8px 10px;
    }
  }
</style>
