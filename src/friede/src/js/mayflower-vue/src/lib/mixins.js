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
