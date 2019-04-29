<template lang="html">
  <div v-if="readonly" v-html="field.html" :class="fieldClasses" />
  <flat-pickr v-else-if="editMode" v-model="field.wip"
         :class="fieldClasses" @blur="commitField" />
  <div v-else v-html="field.html" @click="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import FlatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import { Field } from '@/lib/objects'
import { ModelFieldMixin } from '@/lib/mixins'
export default {
  name: 'DateField',
  mixins: [ ModelFieldMixin ],
  props: {},
  components: { FlatPickr },
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
  .date-field {

  }
</style>
