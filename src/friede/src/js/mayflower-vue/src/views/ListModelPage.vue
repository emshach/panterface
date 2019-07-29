<template lang="html">
  <div class="list-model-page">
    <vk-table v-if="modelObj" responsive hoverable striped
              :divided=false
              :data=objects >
      <vk-column v-for="field in modelObj.fields" :key=field.name
                 :title=field.name :cell=field.name />
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
