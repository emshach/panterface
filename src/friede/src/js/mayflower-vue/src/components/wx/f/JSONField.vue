<template lang="html">
  <json-editor v-if="editMode" v-model="field.wip" :objData="field.wip"
               :class="fieldClasses" @blur="commitField" :options="options" />
  <a v-else :class="fieldClasses" @click.prevent="editField" @focus="editField">
    <span v-html="html" />
    <font-awesome-icon v-if="!readonly" :icon="isset ? 'edit': 'plus'"
    @click="editField" />
  </a>
</template>

<script lang="js">
import Vue from 'vue'
import { ModelFieldMixin } from '@/lib/mixins'
import JsonEditor from 'vue-json-edit'

Vue.use( JsonEditor );
export default {
  name: 'JsonField',
  mixins: [ ModelFieldMixin ],
  components: {},
  props: {},
  mounted() {
    
  },
  data() {
    return {
      options: {
        confirmText: 'confirm',
        cancelText: 'cancel'
      }
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
  .json-field {

  }
</style>
