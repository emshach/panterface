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
  props: [ 'blocks', 'widgets', 'source', 'model', 'options' ],
  data() {
    return {
      classes: {
        'page': true,
        'uk-flex': true,
      }
    }
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
    }
  },
  data() {
    return {
      classes: { 'actor-modal': true },
      verify: {},
      permissions: {}
    }
  },
  created() {
    const model = this.model;
    const actions = Object.keys( this.actions );
    if ( !model || !model.fullname || !actions || !Object.keys( actions ).length )
      return;
    this.$canI( actions, model ).then( r => {
      this.permissions = r;
    });
  },
  methods: {
    act( action, object ) {
      this.$emit( 'act', action, object );
    },
    hideModal() {
      this.$emit( 'update:show', false );
    },
    execute() {
      return this.$api( 'do', this.action, this.model.fullname,
                      this.applicable.map( x => x.id ).join('+'))
    },
    can( action ) {
      const perm = this.permissions[ action ];
      if ( !perm )
        return false;
      const min = this.actionType;
      if ( perm === true )
        return true;
      if ( min === 'owner' ) {
        if ( perm === 'owner' || perm === 'global' ) {
          return perm;
        }
      } else if ( min === 'global' && perm === 'global' ) {
        return 'global';
      }
      return false;
    },
    canUser( action ) {
      return this.can( action ) === 'user'
    }
  },
  computed: {
    arg() {
      return this.operands.length === 1 && this.operands[0];
    },
    applicable() {
      return ( this.action
               ? this.operands.filter( this.verify[ this.action ] || ( x => false ))
               : []);
    }
  }
}

export const ActionsMixin = {}

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
