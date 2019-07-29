<template lang="html">
  <div :class=classes >
    <vue-perfect-scrollbar class="scroll">
      <vk-table v-if="modelObj" responsive hoverable striped
                :divided=false :data=[]
                class="sticky-header" ref="header"
                :style="{ width: colWidths[ field.name ] + 'px' }">
        <vk-column v-for="field in fields" :key=field.name
                   :title=field.name :cell=field.name >
          <template #default={cell} >{{ cell || '' }}</template>
        </vk-column>
      </vk-table>
      <vk-table v-if="modelObj" responsive hoverable striped
                :divided=false
                :data=objects >
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

export default {
  name: "ListModelPage",
  mixins: [ PageMixin ],
  components: {
    VkTable,
    VkColumn,
    VkColSelect,
  },
  props: {},
  data() {
    return {
      classes: {
        'list-model-page': true,
        colWidths: {}
      }
    };
  },
  created() {},
  mounted() {
    const cw = {};
    this.fields.forEach( f => { ct[f] = 0 });
    this.colWidths = cw;
    this.$nextTick(() => this.getColWidths() );
  },
  updated() {
    this.$nextTick(() => this.getColWidths() );
  },
  methods: {
    getColWidths() {
      if ( !this.$el || !this.$refs || this.$refs.header )
        return;
      let tr = this.$refs.header.children[0];
      if ( tr.tagName === 'THEAD' )
        tr = tr.children[0];
      Array.prottype.forEach.call( tr, ( th, i ) => {
        this.colWidths[ this.fields[i] ] = th.clientWidth;
      });
      
    }
  },
  computed: {
    fields() {
      if ( this.modelObj )
        return this.modelObj.fields.filter( x => !x.related );
      return [];
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
    th {
      background: white;
    }
    th, td {
      padding: 8px;
    }
    &.sticky-header {
      position: fixed;
      z-index: 10;
    }
  } 
}
</style>
