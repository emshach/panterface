<template lang="html">
  <div class="list-model-page">
      <vk-table responsive hoverable striped
                :row-class=showApplicable
                :divided=false
                :data=operands >
      </vk-table>
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
    };
  },
  created() {},
  mounted() {},
  methods: {},
  computed: {}
}
</script>

<style lang="scss">
.list-model-page {
  
}
</style>
