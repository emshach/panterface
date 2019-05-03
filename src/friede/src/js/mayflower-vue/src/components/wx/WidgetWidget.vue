<template lang="html"></template>

<script lang="js">
import widgets from '@/lib/widgets'
import { Widget } from '@/lib/objects'
export default  {
  name: 'WidgetWidget',
  functional: true,
  render( h, ref ) {
    var props = ref.props;
    var object = Widget( props.object || {} );
    props.object = object;
    var data = object.data || {};
    var tag = widgets[ data.component ] || widgets.Widget;
    return h( tag, ref );
  },
}
</script>

<style scoped lang="scss">
  .widget-widget {

  }
</style>
