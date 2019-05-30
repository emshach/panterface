<template lang="html">
  <div v-if="readonly" v-html="field.html" :class="fieldClasses" />
  <input v-else-if="editMode" type="text" v-model="field.wip"
         :class="[ 'uk-input', fieldClasses ]" @blur="commitField" ref="input" />
  <div v-else-if="field.html" v-html="field.html" @click="editField" @focus="editField"
       :class="fieldClasses" />
  <div v-else @click="editField" @focus="editField"
       :class="[ fieldClasses, 'no-data' ]">{{ placeholder }}</div>
</template>

<script lang="js">
import { ModelFieldMixin } from '@/lib/mixins'
export default  {
  name: 'SlugField',
  mixins: [ ModelFieldMixin ],
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
  .slug-field {

  }
</style>
