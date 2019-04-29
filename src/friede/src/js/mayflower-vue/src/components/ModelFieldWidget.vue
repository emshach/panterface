<template lang="html"></template>

<script lang="js">
import fields from '@/lib/fields'
import { Field } from '@/lib/objects'
export default  {
  name: 'ModelFieldWidget',
  functional: true,
  props: {
    object: {
      type: Field,
      default: () => {},
      required: true
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },
  render( h, ref ) {
    var props = ref.props
    var tag = fields[ props.field.type ];
    if ( !tag ) {
      tag = fields.CharField;
      props.readonly = true
    }
    return h( tag, Object.assign({}, ref.data, {
      props: Object.assign( {}, props, {
      })
    }));
  }
}
</script>

<style scoped lang="scss">
.model-field-widget {

  }
</style>
