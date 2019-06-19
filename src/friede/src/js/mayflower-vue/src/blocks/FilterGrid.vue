<template lang="html">
  <div class="filter-grid uk-flex uk-flex-column uk-flex-1">
    <div class="header uk-flex">
      <actions-input :actions=actions
                     :operands=filtered
                     :count=selected.length
                     :count-v=visibleSelected
                     :visible=filtered.length
                     :total=objects.length
                     @input=doAction />
      <filter-input v-model=filters :filters=presets @add=addOption />
    </div>
    <vue-perfect-scrollbar class="scroller uk-flex-1">
      <vk-grid matched :class=classes >
        <div v-for="object in filtered" :key=object.id >
          <dashboard-widget :object=object
                            :class=" isSelected( object ) ? 'selected' : ''" >
            <template v-for="( field, slot ) in itemLayout"
                      v-slot:[slot]={object} >
              {{ object[ field ]}}
            </template>
            <template #title-actions={object} >
              <vk-btn type="light" @click.prevent="toggleSelect( object )">
                <font-awesome-icon :icon="isSelected( object ) ? 'check' : 'plus'"
                                   class="selector" />
              </vk-btn>
            </template>
            <template #content-actions={object} >
              <slot name=item-actions :object=object />
            </template>
          </dashboard-widget>
        </div>
    </vk-grid>
    </vue-perfect-scrollbar>
  </div>
</template>

<script lang="js">
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
import { ButtonLink as VkBtn } from 'vuikit/lib/button'
import { Grid as VkGrid } from 'vuikit/lib/grid'
import { FilteredMixin, ActionsMixin } from '@/lib/mixins'
import { FilterInput, ActionsInput } from '@/components'
import { DashboardWidget } from '@/widgets'
import { faPlus, faCheck } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add( faPlus, faCheck );
VkBtn.props.type.validator = val =>
   !val || /^(light|primary|secondary|danger|text|link)$/.test( val );

export default  {
  name: 'FilterGrid',
  mixins: [ FilteredMixin, ActionsMixin ],
  components: {
    VuePerfectScrollbar,
    VkBtn,
    VkGrid,
    DashboardWidget,
    FilterInput,
    ActionsInput,
  },
  props: {
    objects: {
      type: Array,
      default: () => []
    },
    actions: {
      type: Array,
      default: () => []
    },
    itemLayout: {
      type: Object,
      default: () => ({})
    }
  },
  mounted() {
    
  },
  data() {
    return {
      classes: [
        'content',
        'uk-child-width-1-1@s',
        'uk-child-width-1-2@m',
        'uk-child-width-1-3@l',
        'uk-child-width-1-5@xl',
        'uk-grid-match',
      ]
    }
  },
  methods: {
    addOption( filter ) {
      this.presets.push( filter );
    },
    doAction( action, arg ) {
      if ( action === 'select' ) {
        switch ( arg ) {
        case 'all':
          this.selected = this.objects.slice();
          break;
        case 'filtered':
          this.selected = this.selected.concat(
            this.filtered.filter( x => !this.isSelected(x) ));
          break;
        case 'none':
          this.selected = [];
          break;
        }
        return;
      }
    }
  },
  computed: {
    visibleSelected() {
      return this.filtered.filter( x => this.isSelected(x) ).length
    }
  }
}
</script>

<style scoped lang="scss">
.filter-grid {
  width: 100%;
  .header {
    margin-bottom: 4px;
  }
  .filter-input {
    margin-left: 8px;
  }
  >.scroller {
    padding: 3px;
  }
}
</style>
