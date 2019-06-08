<template lang="html">
  <div class="json-object">
    <span class="json-delim">[</span>
    <vk-btn class="json-collapse" type="light" @click.prevent="collapse=!collapse">
      <font-awesome-icon :icon="collapse ? 'plus' : 'minus' " />
    </vk-btn>
    <span v-if="collapse" class="json-object-content">...</span>
    <div v-else class="json-object-content">
      <template v-for"( v, i ) in _value" :key="i">
        <json-widget :readonly="readonly" v-model="v" @input="input" />
        <span class="json-sep">,</span>
      </template>
    </div>
    <span class="json-delim">]</span>
  </div>
</template>

<script lang="js">
import { Button as VkBtn } from 'vuikit/lib/button'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add( faPlus, faMinus )
export default  {
  name: 'JsonArray',
  components: { VkBtn },
  props: [],
  mounted() {
    
  },
  data() {
    return {
      
    }
  },
  methods: {
    input() {
      this.$emit( 'input', this._value );
      this.$emit( 'change', this._value );
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
