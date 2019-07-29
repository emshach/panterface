<template lang="html">
  <div :class=classes >
    <filter-input v-model=filters :filters=presets @add=addOption />
    <vue-perfect-scrollbar class="scroll" @ps-scroll-x="scrollHeader" ref="scroll">
      <vk-table v-if="modelObj" responsive hoverable striped
                :divided=false :data=[]
                class="sticky-header" ref="header" :style=headStyle >
        <vk-column v-for="field in fields" :key=field.name
                   :title=field.name :cell=field.name >
          <template #default={cell} >{{ cell || '' }}</template>
        </vk-column>
      </vk-table>
      <vk-table v-if="modelObj" responsive hoverable striped
                :divided=false
                :data=filtered ref="data" >
        <vk-column v-for="field in fields" :key=field.name
                   :title=field.name :cell=field.name >
          <template #default={cell} >{{ cell || '' }}</template>
        </vk-column>
      </vk-table>
    </vue-perfect-scrollbar>
  </div>
</template>

<script lang="js">
import { PageMixin } from '@/lib/mixins'
import {
  Table as VkTable,
  TableColumn as VkColumn,
  TableColumnSelect as VkColSelect
} from 'vuikit/lib/table'
import { FilteredMixin, ActionsMixin } from '@/lib/mixins'
import { FilterInput, ActionsInput } from '@/components'

export default {
  name: "ListModelPage",
  mixins: [ PageMixin , FilteredMixin ],
  components: {
    VkTable,
    VkColumn,
    VkColSelect,
    FilterInput,
  },
  props: {},
  data() {
    return {
      classes: {
        'list-model-page': true
      },
      headStyle: {
        left: 0
      }
    };
  },
  created() {},
  mounted() {
    if ( this.pageFilters )
      this.filters = this.pageFilters.map( x => ({ key: x, label: x }));
    setInterval(() => this.getColWidths(), 200 );
  },
  methods: {
    getColWidths() {
      if ( !this.$el || !this.$refs || !this.$refs.data || !this.$refs.header
           || !this.$refs.data.$el || !this.$refs.header.$el
           || !this.$refs.data.$el.children || !this.$refs.header.$el.children)
        return;
      let dtr = this.$refs.data.$el.children[0];
      let htr = this.$refs.header.$el.children[0];
      if ( dtr.tagName === 'THEAD' )
        if ( !dtr.children )
          return;
          dtr = dtr.children[0];
      if ( htr.tagName === 'THEAD' )
        if ( !htr.children )
          return;
        htr = htr.children[0];
      Array.prototype.forEach.call( dtr.children, ( th, i ) => {
        htr.children[i].style.width = th.clientWidth + 'px';
      });
      
    },
    scrollHeader() {
      if ( this.$refs && this.$refs.scroll && this.$refs.scroll.$el)
      this.headStyle.left = - this.$refs.scroll.$el.scrollLeft + 'px'
    }
  },
  computed: {
    fields() {
      if ( this.modelObj )
        return this.modelObj.fields.filter( x => !x.related );
      return [];
    }
  },
  watch: {
    pageFilters( val ) {
      this.filters = val.map( x => ({ key: x, label: x }));
    }
  }
}
</script>

<style lang="scss">
.list-model-page {
  padding-left: 1px;
  padding-right: 1px;
  .scroll {
    width: 100%;
  }
  .uk-table {
    margin-top: 0;
    width: 100%;
    font-size: 98%;
    th {
      background: white;
      box-sizing: border-box;
    }
    th, td {
      padding: 8px;
    }
    &.sticky-header {
      position: fixed;
      z-index: 10;
      box-shadow: 0 1px 2px rgba(0,0,0,0.2);
      tr {
        display: flex;
      }
    }
  } 
}
</style>
