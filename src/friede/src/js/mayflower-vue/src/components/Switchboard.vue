<template lang="html">
  <div class="switchboard">
    <transition mode="in-out">
      <dashboard :widgets="widgets" />
    </transition>
    <transition mode="in-out">
      <vk-grid
        v-if="focused && ( matches.length || locations.length || slots.length )"
        gutter="collapse" :class="[ 'completions', 'uk-margin', columnWidth ]"
        :style="{ minWidth: 92 * ( completionColumns / 6 ) + '%' }">
        <vk-button-link
          v-for="m in filteredMatches" href :key="m" size="small"
          :class="[ 'match', m === value ? 'selected' : '' ]"
          @click.prevent="select(m)">{{m}}</vk-button-link>
        <vk-button-link
          v-for="l in locations" href :key="l.href" size="small"
          :class="[ 'location', l === value ? 'selected' : '' ]"
          @click.prevent="select(l)">{{ l.href.replace( baseRx, '' )}}</vk-button-link>
        <vk-button-link
          v-for="s in slots" href :key="s.app+'.'+s.model" size="small"
          :class="[ 'slot', s === value ? 'selected' : '' ]"
          @click.prevent="select(s)">{{ s.label }}</vk-button-link>
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
    value: {
      type: [ String, Object ],
      default: null
    },
    base: {
      type: String,
      default: ''
    },
    focused: {
      type: Boolean,
      default: false
    }
  },
  components: { VkGrid, VkButtonLink, Dashboard },
  mounted() {
  },
  data() {
    return {}
  },
  methods: {
    select( match, type ) {
      this.$emit( 'input', match );
    },
  },
  computed: {
    completionColumns() {
      const length = this.filteredMatches.length + this.locations.length
            + this.slots.length;
      switch ( length ) {
      case 0:
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
        return length;
      }
      return 6;
    },
    columnWidth() {
      return 'uk-child-width-1-' + this.completionColumns;
    },
    baseRx() {
      return new RegExp( this.base, 'i' );
    },
    locationHrefs() {
      return this.locations.map( x => x.href.replace( this.baseRx, '' ));
    },
    filteredMatches() {
      const l = this.locationHrefs;
      return this.matches.filter( x => !l.find( y => x === y ));
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
    background: rgba(0,0,0,0.5);
    color: white;
    border-radius: 4px;
    padding: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    text-align: left;
    .uk-button {
      padding: 0px 8px;
      text-align: left;
      text-transform: none;
      color: lightskyblue;
      &.uk-button-default {
        background: transparent;
        border: 0 none;
        &.selected {
          background: rgba(255,255,255,0.2);
        }
        &:hover {
          background: rgba(255,255,255,0.3);
        }
      }
      &.location {
        color: lime;
      }
      &.slot {
        color: white;
        font-weight: bold;
      }
    }
  }
}
</style>
