import { Field } from '@/lib/objects'
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
      editMode: false
    }
  },
  methods: {
    editField() {
      if ( this.readonly )
        return;
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
        this.field.value === undefined
           || this.field.value === null
           || this.field.value === '' ? 'no-data' : '' ,
        this.readonly ? 'readonly' : '',
      ]
    },
    html() {
      return this.field.value;
    }
  }
}
const DurationOptions = []

export {
  ModelWidgetMixin,
  ModelFieldMixin,
  DurationOptions }
