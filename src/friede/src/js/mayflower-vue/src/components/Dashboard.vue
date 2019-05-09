<template lang="html">
  <div class="dashboard">
    <slot name="title" />
    <vk-grid gutter="small" class="uk-margin uk-child-with-1-3">
      <widget-widget v-for="( widget, index ) in displayWidgets" :key="index"
              :data="widget"/> 
    </vk-grid>
  </div>
</template>

<script lang="js">
import { Grid as VkGrid } from 'vuikit/lib/grid'
import Widget from '@/components/wx/WidgetWidget'
export default {
  name: 'Dashboard',
  props: {
    src: {
      type: [ String, Object ],
      default: ''
    },
    widgets: {
      type: Array,
      default: () => []
    }
  },
  components: { VkGrid, Widget },
  data() {
    return {
      results: [],
      elements: [],
    }
  },
  mounted() {
    // TODO: get dashboard elements
  },
  computed: {
    displayWidgets() {
      if ( this.widgets && this.widgets.length )
        return this.widgets;
      else if ( this.src )
        this.getWidgets()
    },
    getWidgets() {
    }
  }
}
</script>

<style scoped lang="scss">
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
