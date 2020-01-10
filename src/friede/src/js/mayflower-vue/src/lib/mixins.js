import Multiselect from 'vue-multiselect'
import { faPlus, faEdit } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { Field } from '@/lib/objects'
import { JsonInput, FilterInput } from '@/components'
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
import isArray from 'lodash/isArray'

library.add( faPlus, faEdit )

export const ModelWidgetMixin = {
}

export const ModelFieldMixin = {
  components: { FontAwesomeIcon },
  props: {
    field: {
      type: Field,
      required: true
    },
    readonly: {
      type: Boolean,
      default: false
    },
    placeholder: {
      type: String,
      default: 'enter data'
    },
    emptyValue: {
      type: String,
      default: 'not set'
    }
  },
  data() {
    return {
      classes: {},
      editClass: [],
      viewClass: [ 'field-display' ],
      editMode: false,
    }
  },
  methods: {
    editField() {
      if ( this.readonly )
        return;
      this.field.wip = this.field.value;
      this.editMode = true;
      this.$nextTick(() => {
        if ( this.$refs.input )
          this.$refs.input.focus();
        else if ( this.$refs.inputV )
          this.$refs.inputV.$el.focus();
      });
    },
    commitField() {
      this.field.commit();
      this.editMode = false;
    },
    revertField() {
      this.field.revert();
      this.editMode = false;
    }
  },
  computed: {
    fieldClasses() {
      return [
        this.classes,
        this.editMode ? this.editClass : this.viewClass,
        this.isset ? '' : 'no-data',
        this.readonly ? 'readonly' : '',
      ]
    },
    isset() {
      if ( this.field.value === undefined
           || this.field.value === null
           || this.field.value === ''
           || ( typeof this.field.value.length !== 'undefined'
                && !this.field.value.length ))
        return false;
      return true;
    },
    html() {
      if ( !this.isset )
        return this.emptyValue;
      const v = this.field.value;
      return v.label || v.title || v.path || v;
    }
  }
}

export const ModelModelsFieldMixin = {
  components: {
    Multiselect
  },
  data() {
    return {
      loading: false,
      options: [],
      values: []
    }
  },
  methods: {
    editField() {
      if ( this.readonly )
        return;
      this.field.wip = (this.field.value || []).slice();
      this.editMode = true;
      this.$nextTick(() => {
        if ( this.$refs.input )
          this.$refs.input.focus();
        else if ( this.$refs.inputV )
          this.$refs.inputV.$el.focus();
      });
    },
    commitField() {
      if ( this.values.length )
        this.field.wip = ( this.field.wip || []).concat( this.values )
      this.field.commit();
      this.editMode = false;
    },
    async getObjects( query ) {
      const m = this.searchModel;
      const app = m.split('.')[0];
      const model = await this.$store.dispatch( 'getModel', m );
      this.loading = true;
      this.$api( app, model.plural, '?search=' + query ).then( r => {
        this.loading = false;
        this.options = r.data.results.map( x => {
          if ( !x.title )
            x.title = x.path;
          return x;
        });
        // this.options.unshift(
        //   { path: '', title: 'New ' + model.label, ctrl: true },
        //   { path: '_action.cancel', title: 'Cancel', ctrl: true },
        //   { path: '_action.done', title: 'Done', ctrl: true })
        // TODO: put this in maybe
      });
    }
  },
  computed: {
    searchModel() {
      return this.field.meta.related;
    }
  }
};

export const PageMixin = {
  components: {
    VuePerfectScrollbar,
  },
  props: [ 'blocks', 'widgets', 'source', 'model', 'options', 'pageFilters' ],
  data() {
    return {
      classes: {
        'page': true,
        'uk-flex': true,
        'uk-flex-column': true,
      },
      modelObj: null,
      objects: [],
      loading: false,
    }
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      if ( this.loading )
        return new Promise( r => r() );
      this.loading = true;
      if ( !this.model && !this.source )
        return new Promise( r => r() );
      if ( this.source ) {
        const source = isArray( this.source ) ? this.source : [ this.source ];
        return this.$api.get.apply( this, source ).then( r => {
          this.loading = false;
          this.objects = r.data;
        }).catch( err => {
          console.warn( 'error in get from source', err );
          this.loading = false;
        });
      }
      const model = this.model;
      return this.$store.dispatch( 'getModel', this.model ).then( m => {
        this.modelObj = m;
        const objects = this.$store.getters.objects;
        if ( objects && objects.length && !( this.filters && this.filters.length )) {
          this.objects = objects;
        } else if ( m.rest ) {
          this.$api( m.rest, '' ).then( r => { // TODO: paginate, filter?
            if ( model === this.model )
              this.objects = r.data.results || [];
          }).catch( err => {
            console.warn( 'error in get from model', err );
            this.loading = false;
          });
        }
      });
    }
  },
  watch: {
    model() {
      this.$nextTick(() => this.getData());
    },
    source() {
      this.$nextTick(() => this.getData());
    },
  }
};

export const JsonWidgetMixin = {
  components: { JsonInput },
  props: {
    readonly: {
      type: Boolean,
      default: true
    },
    edit: {
      type: Boolean,
      default: false
    }
  },
  mounted() {
    this.editMode = this.edit;
    this.initVal();
  },
  data() {
    return {
      editMode: false,
      intlVal: null
    }
  },
  methods: {
    initVal() {
      this.intlVal = this.value;
    },
    input( val ) {
      this.intlVal = val;
      this.$emit( 'input', val );
    }
  },
  computed: {
    editing() {
      return !this.readonly && this.editMode;
    }
  },
  watch: {
    edit( val ) {
      this.editMode = val;
    }
  }
}

export const FilteredMixin = {
  components: { FilterInput },
  props: {
    searchFields: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      filters: [],
      presets: [],
      selected: [],
    }
  },
  methods: {
    addOption( filter ) {
      this.presets.push( filter );
    },
    toggleSelect( object ) {
      var index = this.selected.indexOf( object );
      if ( index > -1 )
        this.selected.splice( index, 1 );
      else
        this.selected.push( object );
    },
    isSelected( object ) {
      return this.selected.indexOf( object ) > -1;
    }
  },
  computed: {
    filterFunction() {
      const filters = this.filters.map( f => {
        if (!f) return false;
        var match = f.match || f.key;
        if ( !match ) return false;
        match = new RegExp( match, 'i' );
        var search = f.search || this.searchFields;
        if ( !isArray( search ))
          search = [ search ];
        return search && search.length ? x => {
          return search.find( sf => {
            var field = x[ sf ];
            if ( field === undefined || field === null )
              return false;
            return JSON.stringify( field ).match( match );
          })
        } : x => {
          return Object.values(x).find( field => {
            if ( field === undefined || field === null )
              return false;
            return JSON.stringify( field ).match( match );
          });
        };
      }).filter( f => f );
      return filters.length ? x => filters.find( f => f(x) ) : x => true;
    },
    filtered() {
      return this.objects.filter( this.filterFunction );
    }
  },
  watch: {
    selected() {
      this.$store.commit( 'setSelected', this.selected );
    }
  }
}

export const ActorsMixin = {
  props: {
    mode: {
      type: String,
      default: 'widget',
      // validator: val => !val || /^(widget|modal)$/.test( val )
    },
    action: {
      type: String,
      default: ''
    },
    model: {
      type: Object,
      default: () => ({})
    },
    actions: {
      type: Object,
      default: () => ({})
    },
    operands: {
      type: Array,
      default: () => []
    },
    object: {
      type: Object,
      default: () => ({})
    },
    show: {
      type: Boolean,
      default: false
    },
    actionType: {
      type: String,
      default: 'global'
    },
    now: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      classes: { 'actor-modal': true },
      verify: {},
      permissions: {},
      results: null,
      loading: false,
      next: '',
      autoClose: false,
    }
  },
  created() {
    this.getPerms();
  },
  methods: {
    act( action, object, now ) {
      this.$emit( 'act', action, object, now );
    },
    hideModal() {
      if ( this.loading ) return;
      this.results = null;
      this.next = '';
      this.$emit( 'update:now', false );
      this.$emit( 'update:show', false );
    },
    execute() {
      const action = this.action;
      const data = this.actions[ action ].data;
      const args = {}
      if ( data.args )
        data.args.forEach( a => { args[a] = this[a] });
      this.loading = true;
      return this.$api.post( 'do', action, this.model.fullname,
                             this.applicable.map( x => x.id ).join('+'), args )
         .then( r => {
           const res = r.data[ action ];
           this.loading = false;
           if ( !res || res.error ) {
             this.results = res || r.data;
             return this.results;
           }
           if ( data.next && !Object.values( res ).find( x => x.res && x.res.error ))
             this.next = data.next;
           if ( Object.values( res ).find( x => !x.res || !x.res.error )) {
             this.$emit( 'success', res );
             if ( this.autoClose && this.applicable.length === 1 ) {
               const out = Object.values( res )[0];
               if ( !out.out && !out.err ) {
                 if ( this.next )
                   this.doNext();
                 else
                   this.hideModal();
               } else
                 this.results = res;
             } else
               this.results = res;
           } else
               this.results = res;
           return res;
         }).catch( err => {
           this.loading = false;
           console.warn( 'error performing action', err, err.response );
           this.results = {
             error: err.response.status === 500
                ? err.response.statusText + "\nPlease contact you system administrator"
                : err.response };
         });
    },
    autoExecute() {
      if ( this.now ) {
        this.autoClose = true;
        setTimeout(() => { this.autoClose = false }, 3000 );
        this.execute();
      }
    },
    doNext() {
      this.$emit( 'act', this.next, this.operands, true );
      this.hideModal();
      // setTimeout(() => this.$emit( 'act', this.next, this.operands, true ), 250 );
    },
    getPerms() {
      const model = this.model;
      const actions = Object.keys( this.actions );
      if ( !model || !model.fullname || !actions || !actions.length )
        return;
      this.$canI( actions, model ).then( r => {
        this.permissions = r;
      });
    },
    showApplicable(x) {
      return this.action ? this.verify[ this.action ](x) ? 'uk-active' : [] : []
    },
  },
  computed: {
    arg() {
      return this.operands.length === 1 && this.operands[0];
    },
    applicable() {
      return ( this.action
               ? this.operands.filter( this.verify[ this.action ] || ( x => false ))
               : []);
    },
    can() {
      if ( !this.model ) return {};
      const p = this.permissions;
      const fn = '.' + this.model.fullname
      const min = this.actionType;
      const out = {};
      Object.keys(p).forEach( x => {
        const key = x.replace( fn, '' );
        const perm = p[x];
        out[ key ] = (
          perm === true
             ? true
             : min === 'owner'
             ? ( perm === 'owner' || perm === 'global' ? perm : false )
             : ( min === 'global' && perm === 'global' ) ? 'global' : false);
      });
      return out;
    },
    objects() {
      const out = {};
      this.operands.forEach( x => {
        out[ x.id ] = x;
      });
      return out;
    }
  },
  watch: {
    '$security.permit'( val ) {
      this.getPerms();
    },
    model( val ) {
      this.getPerms();
    },
    actions( val ) {
      this.getPerms();
    }
  }
}

export const ActionsMixin = {
  mounted() {
    this.initActions();
  },
  data() {
    return {
      action: '',
      actions: {},
      operands: [],
      showModals: {},
      now: {}
    }
  },
  methods: {
    initActions() {
      const actions = this.options.actions;
      var ops = {};
      var operands = {};
      var show = {};
      var now = {};
      if ( !actions || !actions.length ) {
        this.action = '';
        this.actions = {};
        this.operands = [];
        this.showModals = {};
        return;
      }
      var reverse = [];
      this.$api( 'friede', 'actions', '?' + actions.map(
        action => 'path=' + action ).join('&'))
         .then( r => {
           var res = r.data.results;
           if ( res.length )
             res.forEach( a => {
               if ( a.data.reverse )
                 reverse.push( a.data.reverse );
               ops[ a.name ] = a;
               operands[ a.data.component ] = [];
               show[ a.data.component ] = false;
               now[ a.data.component ] = false;
             });
           if ( reverse.length ) {
             this.$api( 'friede', 'actions', '?' + reverse.map(
               action => 'path=' + action ).join('&'))
                .then( r => {
                  var res = r.data.results;
                  if ( res.length )
                    res.forEach( a => {
                      if ( a.data.reverse )
                        ops[ a.name ] = a;
                      operands[ a.data.component ] = [];
                      show[ a.data.component ] = false;
                      now[ a.data.component ] = false;
                    });
                  this.actions = ops;
                  this.operands = operands;
                  this.showModals = show;
                  this.now = now;
                });
           } else {
             this.actions = ops;
             this.operands = operands;
             this.showModals = show;
             this.now = now;
           }
         })
         .catch( err => {
           console.warn( 'couldnt get actions', actions, err );
         });
    },
    act( action, objects, now ) {
      const tag = this.actions[ action ].data.component;
      this.operands[ tag ] = isArray( objects ) ? objects : [ objects ];
      this.action = action;
      this.showModals[ tag ] = true;
      this.now[ tag ] = now || false;
    },
    success( results ) {
      this.getData();
      if ( this.model === 'friede.app' )
        this.$store.dispatch( 'refresh' );
    }
  },
  computed: {
    allActions() {
      return Object.keys( this.actions );
    },
    actors() {
      const actions = this.actions;
      const args = this.operands;
      var actors = {};
      Object.values( actions ).forEach( a => {
        const tag = a.data.component;
        if ( !actors[ tag ])
          actors[ tag ] = {
            actions: {},
          };
        actors[ tag ].actions[ a.name ] = a;
        actors[ tag ].operands = args[ tag ];
      });
      return actors;
    }
  },
  watch: {
    options( to, fr ) {
      setTimeout(() => this.initActions(), 250 );
    }
  }
}

export const DurationOptions = []

export default {
  ModelWidgetMixin,
  ModelFieldMixin,
  ModelModelsFieldMixin,
  JsonWidgetMixin,
  PageMixin,
  FilteredMixin,
  ActorsMixin,
  ActionsMixin,
  DurationOptions,
}
