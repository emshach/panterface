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
    }
  },
  data() {
    return {
      editMode: false
    }
  },
  methods: {
    editField() {
      this.editMode = true;
      this.$nextTick(() => {
        if ( this.$refs.input )
          this.$refs.input.focus();
        else if( this.$refs.inputV )
          this.$refs.inputV.$el.focus();
      });
    },
    commitField() {
      this.field.html = this.field.wip;
      this.editMode = false;
    }
  },
  computed: {
    fieldClasses() {
      return []
    }
  }
}
const DurationOptions = []

export {
  ModelWidgetMixin,
  ModelFieldMixin,
  DurationOptions }
