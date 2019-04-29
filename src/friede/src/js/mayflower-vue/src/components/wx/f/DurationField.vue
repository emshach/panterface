<template lang="html">
  <div v-if="readonly" v-html="field.html" :class="fieldClasses" />
  <div v-else-if="editMode" :class="fieldClasses">
    <input type="number" v-model="count" />
    <multiselect v-model="duration"
                 :options="options" @blur="commitField" />
  </div>
  <div v-else v-html="field.html" @click="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { Field } from '@/lib/objects'
import { ModelFieldMixin, DurationOptions } from '@/lib/mixins'
export default {
  name: 'DurationField',
  mixins: [ ModelFieldMixin ],
  props: {},
  components: { Multiselect },
  mounted() {
    
  },
  data() {
    return {
      count: 1,
      duration: '',
      options: DurationOptions
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
  .duration-field {

  }
</style>
