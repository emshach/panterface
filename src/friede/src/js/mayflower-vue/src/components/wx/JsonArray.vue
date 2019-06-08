<template lang="html">
  <div class="json-object">
    <span class="json-delim">[</span>
    <vk-btn class="json-collapse" type="light" @click.prevent="collapse=!collapse">
      <font-awesome-icon :icon="collapse ? 'plus' : 'minus' " />
    </vk-btn>
    <span v-if="collapse" class="json-object-content">...</span>
    <div v-else class="json-object-content">
      <template v-for="( v, i ) in _value">
        <json-widget :readonly="readonly" :key="i" v-model="v.data" @input="input" />
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
    this._value = this.value.map( x => ({ data: x }))
  },
  data() {
    return {
      
    }
  },
  methods: {
    input() {
      this.$emit( 'input', this._value.map( x => x.data ));
      this.$emit( 'change', this._value.map( x => x.data ));
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
