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
      const model = this.field.meta.related;
      this.query = query;
      this.loading = true;
      this.$api( model.app, model.plural, '?search='+query ).then( r => {
        this.loading = false;
        this.options = r.data.results;
        this.options.unshift(
          { path: '', title: 'New ' + model.label, ctrl: true },
          { path: '_action.cancel', title: 'Cancel', ctrl: true },
          { path: '_action.done', title: 'Done', ctrl: true })
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
