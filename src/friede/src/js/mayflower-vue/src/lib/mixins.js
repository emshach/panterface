import { Field } from '@/lib/objects'
import Multiselect from 'vue-multiselect'
const ModelWidgetMixin = {
}

const ModelFieldMixin = {
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
    }
  },
  computed: {
    fieldClasses() {
      return [
        this.isset ? '' : 'no-data' ,
        this.readonly ? 'readonly' : '',
      ]
    },
    isset() {
      if ( this.field.value === undefined
           || this.field.value === null
           || this.field.value === '' )
        return false;
      return true;
    },
    html() {
      return this.isset ? this.field.value : this.emptyValue;
    }
  }
}

const ModelModelsFieldMixin = {
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
    getObjects( query ) {
      const m = this.field.meta.related;
      const app = m.split('.')[0];
      const model = this.$store.state.models[m];
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
  }
};

const DurationOptions = []

export {
  ModelWidgetMixin,
  ModelFieldMixin,
  ModelModelsFieldMixin,
  DurationOptions }
