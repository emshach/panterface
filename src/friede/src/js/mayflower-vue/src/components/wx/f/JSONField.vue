<template lang="html">
  <json-widget v-if="editMode" v-model="field.wip" :readonly="false"
               :edit="true" :class="fieldClasses"
               @blur="commitField" />
  <a v-else :class="fieldClasses" @click.prevent="editField" @focus="editField">
    <json-widget :value="field.value" />
    <font-awesome-icon v-if="!readonly" :icon="isset ? 'edit': 'plus'"
                       @click="editField" />
  </a>
</template>

<script lang="js">
import Vue from 'vue'
import { ModelFieldMixin } from '@/lib/mixins'
import JsonWidget from '../JsonWidget'

export default {
  name: 'JsonField',
  mixins: [ ModelFieldMixin ],
  components: { JsonWidget },
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
