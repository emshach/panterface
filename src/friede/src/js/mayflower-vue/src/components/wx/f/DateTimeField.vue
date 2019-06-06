<template lang="html">
  <flat-pickr v-if="editMode" v-model="field.wip" ref="inputV"
              :config="config" :class="fieldClasses"
              @on-change="commitField"
              @on-close="revertField" />
  <div v-else v-html="html" @click="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import FlatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import { ModelFieldMixin } from '@/lib/mixins'
export default {
  name: 'DateTimeField',
  mixins: [ ModelFieldMixin ],
  props: {},
  components: { FlatPickr },
  mounted() {
    
  },
  data() {
    return {
      config: {
        dateFormat: 'Y-m-d'
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
.date-time-field {
  
}
</style>
