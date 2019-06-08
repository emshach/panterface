<template lang="html">
  <div class="json-object">
    <span class="json-delim">{</span>
    <vk-btn class="json-collapse" type="light" @click.prevent="collapse=!collapse">
      <font-awesome-icon :icon="collapse ? 'plus' : 'minus' " />
    </vk-btn>
    <span v-if="collapse" class="json-object-content">...</span>
    <div v-else class="json-object-content">
      <template v-for="v in _value">
        <json-tuple :readonly="readonly" :key="v.data.key" v-model="v.data"
                    @input="input" />
        <span class="json-sep">,</span>
      </template>
      <vk-btn v-if="editing" class="json-add" type="light" @click.prevent="addTuple">
        <font-awesome-icon icon="plus" />
      </vk-btn>
    </div>
    <span class="json-delim">}</span>
  </div>
</template>

<script lang="js">
import { ButtonLink as VkBtn } from 'vuikit/lib/button'
import { JsonTuple } from './json'
import { JsonWidgetMixin } from '@/lib/mixins'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add( faPlus, faMinus )

export default  {
  name: 'json-object',
  mixins: [ JsonWidgetMixin ],
  components: { VkBtn, JsonTuple },
  props: {
    value: {
      type: Object,
      default: () => ({})
    },
  },
  created() {
    this._value = Object.keys( this.value ).map( x => ({
      data: {
        key: x,
        value: this.value[x]
      }
    }))
  },
  data() {
    return {
      collapse: false,
    }
  },
  methods: {
    input() {
      this.$emit( 'input', this.objectVal );
      this.$emit( 'change', this.objectVal );
    },
    addTuple() {
      this._value.push( { data: { key: '', value: null }});
    }
  },
  computed: {
    objectVal() {
      var o = {}
      this._value.forEach( x => {
        o[v.key] = o.value
      });
      return o
    }
  }
}
</script>

<style lang="scss">
.json-object {
  
}
</style>
