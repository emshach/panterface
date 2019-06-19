<template lang="html"></template>

<script lang="js">
import widgets from '@/widgets'
import { Widget } from '@/lib/objects'
export default  {
  name: 'Widget',
  functional: true,
  render( h, ref ) {
    const object = Widget( ref.props.object || {} );
    const data = object.data || {};
    const tag = widgets[ data.component ] || widgets.Widget;
    ref.props.object = object;
    return h( tag, ref );
  },
}
</script>

<style scoped lang="scss">
  .widget-widget {

  }
</style>
