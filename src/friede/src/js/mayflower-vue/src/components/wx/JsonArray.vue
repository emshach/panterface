<template lang="html">
  <div class="json-object">
    <span class="json-delim">[</span>
    <vk-btn v-if="value.length > 1" class="json-collapse" type="light"
            @click.prevent="collapse=!collapse">
      <font-awesome-icon :icon="collapse ? 'plus' : 'minus' " />
    </vk-btn>
    <span v-if="collapse" class="json-object-content">...</span>
    <span v-else class="json-object-content">
      <template v-for="( v, i ) in intlVal">
        <json-widget :readonly="readonly" :key="i" v-model="v.data" @input="input" />
      </template>
      <vk-btn v-if="editing" class="json-add" type="light" @click.prevent="addElem">
        <font-awesome-icon icon="plus" />
      </vk-btn>
    </span>
    <span class="json-delim">]</span>
  </div>
</template>

<script lang="js">
import { Button as VkBtn } from 'vuikit/lib/button'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { JsonWidgetMixin } from '@/lib/mixins'

library.add( faPlus, faMinus )

export default  {
  name: 'JsonArray',
  mixins: [ JsonWidgetMixin ],
  components: { VkBtn },
  props: {
    value: {
      type: Array,
      default: () => []
    }
  },
  created() {
    this.intlVal = this.value.map( x => ({ data: x }))
  },
  data() {
    return {
      collapse: false,
    }
  },
  methods: {
    input() {
      this.$emit( 'input', this.intlVal.map( x => x.data ));
      this.$emit( 'change', this.intlVal.map( x => x.data ));
    },
    addElem() {
      this.intlVal.push({ data: null });
    }
  },
  computed: {
    
  }
}
</script>

<style lang="scss">
  .json-array {

  }
</style>
