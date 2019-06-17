import Multiselect from 'vue-multiselect'
import { faPlus, faEdit } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { Field } from '@/lib/objects'
import JsonWidget from '@/components/wx/JsonWidget'
import VuePerfectScrollbar from 'vue-perfect-scrollbar'

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
      classes: [],
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
        else if( this.$refs.inputV )
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
      return this.classes.concat(
        this.editMode ? this.editClass : this.viewClass,
        [
          this.isset ? '' : 'no-data' ,
          this.readonly ? 'readonly' : '',
        ])
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
      if (! this.isset)
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
        else if( this.$refs.inputV )
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
      this.$api( app, model.plural, '?search='+query ).then( r => {
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
};

export const JsonWidgetMixin = {
  components: { JsonWidget },
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

export const DurationOptions = []

export default {
  ModelWidgetMixin,
  ModelFieldMixin,
  ModelModelsFieldMixin,
  JsonWidgetMixin,
  PageMixin,
  DurationOptions,
}
