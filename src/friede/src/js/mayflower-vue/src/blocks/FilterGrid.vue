<template lang="html">
  <div class="filter-grid">
    <div class="header uk-flex uk-margin">
      <actions-input :actions=actions :operands=filtered />
      <filter-input class="uk-margin-left" v-model=filters
                    :filters=presets />
    </div>
    <vk-grid matched :class=classes >
      <div v-for="object in objects" :key=object.id >
        <dashboard-widget :object=object >
          <template v-for="( field, slot ) in itemLayout"
                    v-slot:[slot]={object} >
            {{ object[ field ]}}
          </template>
        </dashboard-widget>
      </div>
    </vk-grid>
  </div>
</template>

<script lang="js">
import { Grid as VkGrid } from 'vuikit/lib/grid'
import { FilteredMixin, ActionsMixin } from '@/lib/mixins'
import { FilterInput, ActionsInput } from '@/components'
import { DashboardWidget } from '@/widgets'
export default  {
  name: 'FilterGrid',
  mixins: [ FilteredMixin, ActionsMixin ],
  components: {
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
        'uk-child-width-1-3@m',
        'uk-child-width-expand@m'
      ]
    }
  },
  methods: {
    
  },
  computed: {
    filtered() {
      return this.filter( this.objects );
    }
  }
}
</script>

<style scoped lang="scss">
.filter-grid {
  
}
</style>
