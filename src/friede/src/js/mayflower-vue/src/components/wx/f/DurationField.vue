<template lang="html">
  <div v-if="editMode" :class="fieldClasses">
    <input type="number" class="uk-input" v-model="days" />days
    <input type="number" class="uk-input" max="23" v-model="hours" />hours
    <input type="number" class="uk-input" max="59" v-model="minutes" />minutes
    <input type="number" class="uk-input" max="59" v-model="seconds" />seconds
  </div>
  <div v-else v-html="html" @click="editField" @focus="editField"
       :class="fieldClasses" />
</template>

<script lang="js">
import { Field } from '@/lib/objects'
import { ModelFieldMixin, DurationOptions } from '@/lib/mixins'
export default {
  name: 'DurationField',
  mixins: [ ModelFieldMixin ],
  props: {},
  mounted() {
    
  },
  data() {
    return {
      days: 1,
      hours: 0,
      minutes: 0,
      seconds: 0,
      duration: '',
      options: DurationOptions
    }
  },
  methods: {
    
  },
  computed: {
    value() {
      return `${this.days} ${this.minutes}:${this.hours}${this.seconds}`;
    }
  },
  watch: {
    value( val ) {
      this.field.wip = val;
    }
  }
}
</script>

<style scoped lang="scss">
  .duration-field {

  }
</style>
