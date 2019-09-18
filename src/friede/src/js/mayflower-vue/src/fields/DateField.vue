<template lang="html">
  <flat-pickr v-if="editMode" :value="field.wip" ref="inputV"
              :config="config" :class="fieldClasses"
              @on-change="setDate" />
  <a v-else v-html="html" @click.prevent="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import FlatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
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
      config: {
        dateFormat: 'Y-m-d'
      }
    }
  },
  methods: {
    setDate( date, str ) {
      this.fieeld.wip = str;
      this.commitField();
    }
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
.date-field {
  
}
</style>
