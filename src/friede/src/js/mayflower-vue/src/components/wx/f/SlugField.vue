<template lang="html">
  <input v-if="editMode" type="text" v-model="field.wip" ref="input"
         :class="fieldClasses" @blur="commitField" />
  <a v-else @click.prevent="editField" @focus="editField"
     :class="fieldClasses" >
    <div v-html="html" />
    <font-awesome-icon :icon="isset ? 'edit': 'plus'" @click="editField" />
  </a>
</template>

<script lang="js">
import { ModelFieldMixin } from '@/lib/mixins'
export default {
  name: 'SlugField',
  mixins: [ ModelFieldMixin ],
  props: {},
  mounted() {
  },
  data() {
    return {
      editClass: [ 'uk-input' ]
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
