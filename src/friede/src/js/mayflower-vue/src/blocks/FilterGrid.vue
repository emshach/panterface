<template lang="html">
  <div class="filter-grid">
    <filter-input v-model=filters />
    <actions-input :actions=actions :operands=filtered />
    <vk-grid class="content">
      <dashboard-widget v-for="object in objects" :key=object.id >
        <template v-for="( field, slot ) in itemLayout"
                  v-slot:[slot]=o >{{ o[ field ]}}</template>
      </dashboard-widget>
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
