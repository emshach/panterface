<template lang="html"></template>

<script lang="js">
import DashboardWidget from '@/components/wx/DashboardWidget'
import InlineWidget from '@/components/wx/InlineWidget'
import { Widget } from '@/lib/objects'
export default  {
  name: 'AdaptiveWidget',
  functional: true,
  props: {
    object: {
      type: Widget,             // TODO: or Object and cast to Widget
      default: 'default'
    },
    context: {
      type: Object,
      default: () => []
    }
  },
  render( h, ref ) {
    function isInline() {
      return true;
    }
    var tag = isInline() ? InlineWidget : DashboardWidget;
    var props = ref.props
    return h( tag, Object.assign({}, ref.data, {
      props: Object.assign( {}, props, {
      })
    }));
  }
}
</script>

<style scoped lang="scss">
  .adaptive-widget {

  }
</style>
