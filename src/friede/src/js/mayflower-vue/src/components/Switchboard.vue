<template lang="html">
  <div class="switchboard">
    <transition mode="in-out">
      <dashboard :widgets="widgets" />
    </transition>
    <transition mode="in-out">
      <vk-grid v-if="matches.length || locations.length"
               gutter="collapse" :class="[ 'completions', 'uk-margin', columnWidth ]"
               :style="{ minWidth: 92 * ( getCompletionColumns() / 6 ) + '%' }">
        <vk-button-link
          v-for="match in matches" href :key="match" size="small"
          @click.prevent="select( match )">{{ match }}</vk-button-link>
      </vk-grid>
    </transition>
  </div>
</template>

<script lang="js">
import { Grid as VkGrid } from 'vuikit/lib/grid'
import { ButtonLink as VkButtonLink } from 'vuikit/lib/button'
import Dashboard from '@/components/Dashboard'
import { Widget } from '@/lib/objects'
export default {
  name: 'Switchboard',
  props: {
    matches: {
      type: Array,
      default: () => []
    },
    locations: {
      type: Array,
      default: () => []
    }
  },
  components: { VkGrid, VkButtonLink, Dashboard },
  mounted() {
  },
  data() {
    return {}
  },
  methods: {
    select( match ) {
      this.$emit( 'update', match )
    },
    getCompletionColumns() {
      const matches = this.matches.length;
      switch ( matches ) {
      case 0:
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
        return matches;
      }
      return 6;
    }
  },
  computed: {
    columnWidth() {
      return 'uk-child-width-1-' + this.getCompletionColumns()
    },
    widgets() {
      return this.locations.slice( 0, 10 ).forEach( location => {
        var l = location, l2, widget
        do {
          l2 = l;
          if ( !widget ) {
            var w = l._widget_entries.find( x => x.name === 'card' );
            if (w)
              widget = Widget( w.entry );
          }
          l = l.redirect_to
        } while (l);
        if ( widget )
          widget.data.location = l2;
        return widget;
      });
    }
  }
}
</script>

<style scoped lang="scss">
.switchboard {
  .dashboard {
  }
  .completions{
    transition: 0.3s;
    position: fixed;
    bottom: 18px;
    right: 6px;
    max-width: 92%;
    background: rgba(0,0,0,0.75);
    color: white;
    border-radius: 4px;
    padding: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    text-align: left;
    .uk-button {
      padding: 0px 8px;
      text-align: left;
      text-transform: none;
      color: white;
      &.uk-button-default {
        background: transparent;
        border: 0 none;
        &:hover {
          background: rgba(255,255,255,0.1);
        }
      }
    }
  }
}
</style>
