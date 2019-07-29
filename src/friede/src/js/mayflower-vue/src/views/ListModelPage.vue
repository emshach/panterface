<template lang="html">
  <div :class=classes >
    <vue-perfect-scrollbar>
      <vk-table v-if="modelObj" responsive hoverable striped
                :divided=false
                :data=objects >
        <vk-column v-for="field in fields" :key=field.name
                   :title=field.name :cell=field.name />
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
        'list-model-page': true
      }
    };
  },
  created() {},
  mounted() {},
  methods: {},
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
  .uk-table {
    margin-top: 0;
    th {
      background: white;
    }
    th, td {
      padding: 8px;
    }
  }
}
</style>
