<template lang="html">
  <div class="model-multiple-choice-field" >
    <vk-table v-if="isset" :data="values">
      <vk-table-column v-for="c in columns"
                       :key="c.name" :title="c.name" :name="c.name" />
    </vk-table>
    <div v-else v-html="html" @click="editField" @focus="editField"
         :class="fieldClasses" />
    <multiselect v-if="editMode" v-model="values" ref="inputV"
                 :options="options" :class="fieldClasses"
                 :multiple="true"
                 label="title"
                 track-by="path"
                 open-direction="bottom"
                 @blur="commitField"
                 @search-change="getObjects"
               />
  </div>
</template>

<script lang="js">
import { Table as VkTable, TableColumn as VkTableColumn } from 'vuikit/lib/table'
import { ModelFieldMixin, ModelModelsFieldMixin } from '@/lib/mixins'
export default {
  name: 'ModelMultipleChoiceField',
  mixins: [ ModelFieldMixin, ModelModelsFieldMixin ],
  components: { VkTable, VkTableColumn },
  props: {},
  mounted() {
    
  },
  data() {
    return {
      
    }
  },
  methods: {
  },
  computed: {
    columns() {
      const m = this.field.meta.related;
      const model = this.$store.state.models[m];
      return model.fields
    },
    searchModel() {
      const m = this.field.meta.related;
      let l = this.field.meta.link_field;
      if (l) {
        const model = this.$store.state.models[m];
        var f = model && model.fields.find( x => x.name === l );
        return f && f.related;
      }
      return m;
    }
  }
}
</script>

<style scoped lang="scss">
.model-multiple-choice-field {
  
}
</style>
