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
          v-for="m in matches" href :key="m" size="small"
          :class="[ 'match', m === selected ? 'selected' : '' ]"
          @click.prevent="select( m, 'match' )">{{m}}</vk-button-link>
        <vk-button-link
          v-for="l in locations" href :key="l.href" size="small"
          :class="[ 'location', m === selected ? 'selected' : '' ]"
          @click.prevent="select( l, 'location' )">{{ l.href }}</vk-button-link>
        <vk-button-link
          v-for="s in slots" href :key="s.app+'.'+s.model" size="small"
          :class="[ 'slot', m === selected ? 'selected' : '' ]"
          @click.prevent="select( s, 'slot' )">{{ s.label }}</vk-button-link>
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
    },
    slots: {
      type: Array,
      default: () => []
    },
    selected: {
      type: [ String, Object ],
      default: null
    }
  },
  components: { VkGrid, VkButtonLink, Dashboard },
  mounted() {
    this.cr = this.all.indexOf( this.selected );
  },
  data() {
    return {
      cr: -1
    }
  },
  methods: {
    select( match, type ) {
      this.selected = match;
      this.cr = this.all.indexOf( this.selected );
      this.$emit( 'select', match, type );
    },
    selectNext() {
      const all = this.all;
      var type = 'slot';
      if ( this.cr == -1 ) {
        this.cr = 0
      } else {
        this.cr = this.all.indexOf( this.selected ) % this.all.length;
      }
      this.selected = this.all[ this.cr ];
      if ( cr < this.matches.length ) {
        type = 'match';
      } else if ( cr < ( this.matches.length + this.locations.length )) {
        type = 'location';
      }
      this.$emit( 'update', this.selected, type );
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
    all() {
      return this.matches.concat( this.locations ).concat( this.slot );
    },
    columnWidth() {
      return 'uk-child-width-1-' + this.getCompletionColumns()
    },
    widgets() {
      return this.locations.slice( 0, 10 ).forEach( location => {
        var l = location, l2, widget
        do {
          l2 = l;
          if ( !widget ) {
            var w = l._widget_entries
                && l._widget_entries.find( x => x.name === 'card' );
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
