<template lang="html">
  <input v-if="editMode" type="text" v-model="field.wip" ref="input"
         :class="[ 'uk-input', fieldClasses ]" @blur="commitField" />
  <div v-else v-html="html" @click="editField" @focus="editField"
       :class="fieldClasses" />
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
