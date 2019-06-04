<template lang="html">
  <json-editor v-if="editMode" v-model="field.wip"
               :class="fieldClasses" @blur="commitField" />
  <pre v-else v-highlightjs="field.value" @click="editField" @focus="editField"
       :class="fieldClasses" ><code class="json"  /></pre>
</template>

<script lang="js">
import Vue from 'vue'
import VueHighlightJS from 'vue-highlightjs'
import { ModelFieldMixin } from '@/lib/mixins'
import JsonEditor from 'vue-json-edit'

Vue.use( JsonEditor );
Vue.use( VueHighlightJS );
export default {
  name: 'JsonField',
  mixins: [ ModelFieldMixin ],
  components: {},
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
    
  }
}
</script>

<style scoped lang="scss">
  .json-field {

  }
</style>
