import { Field } from '@/lib/objects'
const ModelWidgetMixin = {
}

const ModelFieldMixin = {
  props: {
    field: {
      type: Field,
      required: true
    }
  }
}
const DurationOptions = []

export {
  ModelWidgetMixin,
  ModelFieldMixin,
  DurationOptions }
